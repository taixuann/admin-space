#!/usr/bin/env python3
"""Refresh a dated model catalog, verify a selection, and update OpenCode's default."""
import argparse
import fcntl
import json
import math
import os
import re
import subprocess
import tempfile
import urllib.error
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

LOCAL = ZoneInfo('Asia/Ho_Chi_Minh')
ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / 'model-list.json'
CONFIG = Path.home() / '.config/opencode/opencode.jsonc'
SELECTION_CONFIG = ROOT / 'selection.json'
MODEL_ID = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._:-]*$')
PROVIDER_ID = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]*$')
HF = 'https://datasets-server.huggingface.co/rows?dataset=lmarena-ai/leaderboard-dataset&split=latest'
QUALITY_CACHE = ROOT / '.quality-cache'


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.' + path.name, dir=path.parent)
    try:
        with os.fdopen(fd, 'w') as stream:
            json.dump(value, stream, indent=2)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def is_fresh(state, now=None):
    now = now or datetime.now(LOCAL)
    try:
        updated = datetime.fromisoformat(state['dateUpdated'])
        return (state.get('refreshStatus') != 'failed' and updated.tzinfo is not None and updated <= now
                and updated.astimezone(LOCAL).date() == now.astimezone(LOCAL).date()
                and state['selected']['status'] == 'ready'
                and valid_selection(state['selected']['id']))
    except (KeyError, TypeError, ValueError):
        return False


def valid_selection(model):
    if not isinstance(model, str) or model.count('/') != 1:
        return False
    provider, name = model.split('/')
    return bool(PROVIDER_ID.fullmatch(provider) and MODEL_ID.fullmatch(name))


def free_candidates(catalog):
    if not isinstance(catalog, dict) or not isinstance(catalog.get('data'), list):
        raise ValueError('Invalid provider catalog')
    return sorted({item['id'] for item in catalog['data']
                   if isinstance(item, dict) and isinstance(item.get('id'), str)
                   and MODEL_ID.fullmatch(item['id'])
                   and item['id'].endswith(('-free', ':free'))})


def tokens(name):
    name = name.lower().split('/')[-1]
    name = re.sub(r'[-_]free$', '', name)
    name = re.sub(r'(\d)-(\d{1,2})(?![\d.a-z])', r'\1.\2', name)
    name = re.sub(r'([a-z]{2,})(\d)', r'\1 \2', name)
    name = re.sub(r'\bv(\d)', r'\1', name)
    ignored = {'max', 'high', 'medium', 'low', 'xhigh', 'thinking', 'preview', 'latest', 'free', 'exp', 'instruct', 'chat'}
    return [t for t in re.split(r'[\s_\-/]+', re.sub(r'\(([^)]*)\)', r' \1 ', name))
            if t and t not in ignored and not re.fullmatch(r'\d{4}|\d{8}', t)]


def match_quality(model, rows):
    candidate = set(tokens(model))
    best = None
    qualifiers = {'small', 'mini', 'nano', 'lite', 'flash', 'pro', 'ultra', 'super', 'plus', 'turbo', 'air', 'omni', 'code', 'coder', 'vl', 'lightning'}
    for row in rows:
        board = set(tokens(row['name']))
        if not candidate or not candidate.issubset(board):
            continue
        if (candidate ^ board) & qualifiers:
            continue
        extra = len(board - candidate)
        if best is None or extra < best[0] or (extra == best[0] and row['value'] > best[1]['value']):
            best = (extra, row)
    return best[1] if best else None


def validate_selection(selection):
    if not isinstance(selection, dict) or not isinstance(selection.get('quality'), dict) or not isinstance(selection.get('groups'), list):
        raise ValueError('Invalid model selection configuration')
    quality = selection['quality']
    max_age = quality.get('maxAgeHours')
    if isinstance(max_age, bool) or not isinstance(max_age, (int, float)) or not math.isfinite(max_age) or not 0 < max_age <= 720:
        raise ValueError('Invalid quality ranking age limit')
    if not isinstance(quality.get('attribution'), str) or len(quality['attribution']) > 500:
        raise ValueError('Invalid benchmark attribution')
    if selection.get('googleAuthProvider') != 'google':
        raise ValueError('Invalid Google authentication provider')
    allowed = {'arena_agent': ('agent', 'score'), 'arena_webdev': ('webdev', 'rating'), 'arena_text': ('text', 'rating')}
    sources = quality.get('sources')
    if not isinstance(sources, dict) or not sources:
        raise ValueError('No benchmark sources configured')
    for source, entry in sources.items():
        if source not in allowed or not isinstance(entry, dict) or (entry.get('config'), entry.get('field')) != allowed[source]:
            raise ValueError('Invalid benchmark source configuration')
        if isinstance(entry.get('weight'), bool) or not isinstance(entry.get('weight'), (int, float)) or not math.isfinite(entry['weight']) or entry['weight'] <= 0:
            raise ValueError('Invalid benchmark source weight')
    required = quality.get('requiredSources', ['arena_agent', 'arena_webdev'])
    if not isinstance(required, list) or not required or any(not isinstance(source, str) or source not in sources for source in required):
        raise ValueError('Invalid required benchmark sources')
    seen = set()
    for group in selection['groups']:
        if (not isinstance(group, dict) or not isinstance(group.get('id'), str) or group.get('id') in seen
                or not isinstance(group.get('label'), str) or not group['label']
                or group.get('strategy') not in {'quality', 'fixed'}):
            raise ValueError('Invalid provider group configuration')
        seen.add(group['id'])
        provider = group.get('provider')
        if not isinstance(provider, str) or not PROVIDER_ID.fullmatch(provider):
            raise ValueError('Invalid model provider')
        names = group.get('models', [])
        if not isinstance(names, list) or any(not isinstance(name, str) or not valid_selection(provider + '/' + name) for name in names):
            raise ValueError('Invalid configured model ID')
        catalog = group.get('catalog')
        if (catalog not in {None, 'zen', 'go'} or group.get('authProvider') not in {None, 'google'}
                or (catalog == 'zen' and provider != 'opencode')
                or (catalog == 'go' and provider != 'opencode-go')):
            raise ValueError('Invalid provider catalog')


def ordered_candidates(catalogs, selection, boards, fetched_at, now):
    validate_selection(selection)
    quality_config = selection['quality']
    if fetched_at > now or now - fetched_at > timedelta(hours=quality_config['maxAgeHours']):
        raise ValueError('Quality benchmark data is stale')
    sources = quality_config['sources']
    values = {source: sorted(row['value'] for row in boards.get(source, []) if row.get('value') is not None)
              for source in sources}
    result = []
    for group in selection['groups']:
        if group.get('catalog') in ('zen', 'go'):
            models = catalogs.get(group['catalog'], [])
        elif group.get('authProvider'):
            models = group.get('models', []) if catalogs.get(group['authProvider']) else []
        else:
            models = group.get('models', [])
        if group['strategy'] == 'fixed':
            result.extend({'group': group['id'], 'provider': group['provider'], 'id': group['provider'] + '/' + model,
                           'status': 'not_probed'} for model in models)
            continue
        ranked = []
        unranked = []
        for name in models:
            if not isinstance(name, str) or not valid_selection(group['provider'] + '/' + name):
                raise ValueError('Invalid model ID in provider catalog')
            ident = group['provider'] + '/' + name
            hits = {}
            for source, definition in sources.items():
                match = match_quality(ident, boards.get(source, []))
                source_values = values[source]
                if match is None or len(source_values) < 2:
                    continue
                pct = sum(value < match['value'] for value in source_values) / (len(source_values) - 1)
                hits[source] = {'name': match['name'], 'value': match['value'], 'percentile': round(pct, 4)}
            denominator = sum(sources[source]['weight'] for source in hits)
            if denominator and set(quality_config.get('requiredSources', ['arena_agent', 'arena_webdev'])).issubset(hits):
                score = sum(sources[source]['weight'] * hit['percentile'] for source, hit in hits.items()) / denominator
                ranked.append({'group': group['id'], 'provider': group['provider'], 'id': ident,
                               'status': 'not_probed', 'quality': {'score': round(score, 4), 'sources': hits}})
            else:
                unranked.append({'group': group['id'], 'provider': group['provider'], 'id': ident, 'status': 'unranked'})
        result.extend(sorted(ranked, key=lambda row: (-row['quality']['score'], row['id'])) + unranked)
    return result


def apply_model(path, model):
    if not valid_selection(model):
        raise ValueError('Invalid selected model')
    before = path.read_bytes() if path.exists() else b'{}'
    data = json.loads(before)
    if not isinstance(data, dict):
        raise ValueError('OpenCode configuration must be an object')
    if data.get('model') == model:
        return
    data['model'] = model
    # Refuse to rewrite JSONC comments rather than silently stripping them.
    path.parent.mkdir(parents=True, exist_ok=True)
    backup = path.with_name(path.name + '.admin-backup-' + datetime.now(LOCAL).strftime('%Y%m%dT%H%M%S%f'))
    with backup.open('xb') as out:
        os.chmod(backup, 0o600)
        out.write(before)
    if path.exists() and path.read_bytes() != before:
        raise RuntimeError('OpenCode configuration changed during update')
    atomic_json(path, data)


def refresh(state_path, config_path, catalogs, probe, force=False, now=None, selection=None, boards=None, fetched_at=None):
    now = now or datetime.now(LOCAL)
    old = json.loads(state_path.read_text()) if state_path.exists() else {}
    if not force and is_fresh(old, now):
        apply_model(config_path, old['selected']['id'])
        return old
    stamp = now.isoformat()
    cooldowns = old.get('cooldowns', {})
    selection = selection or json.loads(SELECTION_CONFIG.read_text())
    rows = ordered_candidates(catalogs, selection, boards or {}, fetched_at or now, now)
    if not any(row.get('quality') for row in rows):
        rows = [row for row in rows if row['status'] == 'unranked']
    selected = None
    for row in rows:
        if row['status'] == 'unranked':
            continue
        until = cooldowns.get(row['id'], {}).get('until')
        if until and datetime.fromisoformat(until) > now:
            row['status'] = 'cooldown'
            continue
        result = probe(row['id'])
        row.update(result)
        row['checkedAt'] = stamp
        if row['status'] == 'ready':
            selected = dict(row)
            cooldowns.pop(row['id'], None)
            break
        retry = result.get('retryAfterSeconds')
        # shortcut: providers without a reset time use a bounded retry interval; use quota APIs when available.
        seconds = retry or (21600 if row['status'] == 'quota_exhausted' else 1800)
        cooldowns[row['id']] = {'until': (now + timedelta(seconds=seconds)).isoformat(), 'reason': row['status']}
    attempt = {'attemptedAt': stamp, 'models': rows, 'modelGroups': [
        {'id': group['id'], 'label': group['label'], 'order': index + 1,
         'models': [row for row in rows if row['group'] == group['id']]}
        for index, group in enumerate(selection['groups'])],
        'modelsByProvider': {group: names for group, names in catalogs.items() if group in {'zen', 'go'}},
        'selected': selected, 'timezone': str(LOCAL), 'cooldowns': cooldowns,
        'qualitySource': selection['quality']['attribution'], 'qualityFetchedAt': fetched_at.isoformat() if fetched_at else stamp}
    if selected is None:
        atomic_json(state_path, dict(old, lastAttempt=attempt, cooldowns=cooldowns, refreshStatus='failed'))
        raise RuntimeError('No model passed verification; previous OpenCode model and successful date are preserved')
    # Write configuration first. A failed apply must not mark the catalog fresh.
    apply_model(config_path, selected['id'])
    result = dict(attempt, dateUpdated=stamp, status='ready')
    atomic_json(state_path, result)
    return result


def catalog(provider):
    base = 'https://opencode.ai/zen/' + ('go/' if provider == 'go' else '') + 'v1/models'
    req = urllib.request.Request(base, headers={'User-Agent': 'admin-model-catalog/1.0'})
    with urllib.request.urlopen(req, timeout=20) as response:
        return free_candidates(json.load(response))


def quality_source(config, field):
    allowed = {'agent': 'score', 'webdev': 'rating', 'text': 'rating'}
    if allowed.get(config) != field:
        raise ValueError('Unsupported benchmark source')
    rows = []
    for offset in range(0, 5000, 100):
        url = f'{HF}&config={config}&offset={offset}&length=100'
        req = urllib.request.Request(url, headers={'User-Agent': 'admin-model-catalog/1.0'})
        with urllib.request.urlopen(req, timeout=20) as response:
            data = json.load(response)
        if not isinstance(data, dict):
            raise ValueError('Invalid benchmark response')
        page = data.get('rows')
        if not isinstance(page, list):
            raise ValueError('Invalid benchmark response')
        for item in page:
            row = item.get('row') if isinstance(item, dict) else None
            if not isinstance(row, dict) or row.get('category') != 'overall':
                continue
            name, value = row.get('model_name'), row.get(field)
            if (isinstance(name, str) and len(name) <= 200 and isinstance(value, (int, float))
                    and not isinstance(value, bool) and math.isfinite(value)):
                rows.append({'name': name, 'value': float(value)})
        total = data.get('num_rows_total', 0)
        if not isinstance(total, int) or offset + 100 >= total:
            break
    return rows


def cached_quality(source, now, max_age_hours):
    paths = [QUALITY_CACHE / (source + '.json'), Path.home() / '.config/opencode/free-router/cache' / (source + '.json')]
    for path in paths:
        try:
            cached = json.loads(path.read_text())
            fetched = cached.get('fetchedAt')
            fetched_at = (datetime.fromtimestamp(fetched / 1000, LOCAL) if isinstance(fetched, (int, float))
                          else datetime.fromisoformat(fetched))
            rows = cached.get('data')
            if (fetched_at.tzinfo is None or fetched_at > now or now - fetched_at > timedelta(hours=max_age_hours)
                    or not isinstance(rows, list) or not rows):
                continue
            valid = [row for row in rows if isinstance(row, dict) and isinstance(row.get('name'), str)
                     and isinstance(row.get('value'), (int, float)) and not isinstance(row.get('value'), bool)
                     and math.isfinite(row['value'])]
            if valid:
                return valid, fetched_at
        except (OSError, ValueError, TypeError, KeyError):
            continue
    raise ValueError('No recent cached benchmark data')


def selection_data():
    return json.loads(SELECTION_CONFIG.read_text())


def load_quality_boards(selection):
    now = datetime.now(LOCAL)
    boards, stamps = {}, []
    for source, definition in selection['quality']['sources'].items():
        try:
            rows = quality_source(definition['config'], definition['field'])
            fetched_at = datetime.now(LOCAL)
            atomic_json(QUALITY_CACHE / (source + '.json'), {'fetchedAt': fetched_at.isoformat(), 'data': rows})
        except urllib.error.URLError:
            rows, fetched_at = cached_quality(source, now, selection['quality']['maxAgeHours'])
        boards[source] = rows
        stamps.append(fetched_at)
    return boards, min(stamps)


def probe_native(model):
    try:
        run = subprocess.run(['/opt/homebrew/bin/opencode', 'run', '--standalone', '-m', model,
                              '--format', 'json', 'Reply with exactly OK.'],
                             cwd='/private/tmp', capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        return {'status': 'timeout'}
    texts = []
    errors = []
    for line in run.stdout.splitlines():
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if item.get('type') == 'text':
            texts.append(item.get('part', {}).get('text', ''))
        elif item.get('type') == 'error':
            errors.append(json.dumps(item))
    if run.returncode == 0 and ''.join(texts).strip().rstrip('.').strip() == 'OK':
        return {'status': 'ready'}
    error = ' '.join(errors) + run.stderr
    status = 'quota_exhausted' if re.search(r'quota|usage limit|credits|exhausted', error, re.I) else 'failed'
    if status == 'failed' and re.search(r'429|rate.?limit', error, re.I):
        status = 'rate_limited'
    # Raw provider errors and subprocess output stay out of the public catalog.
    return {'status': status, 'exitCode': run.returncode}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--force', action='store_true', help='Refresh even after a successful update today')
    parser.add_argument('--status', action='store_true', help='Read current state without network or writes')
    args = parser.parse_args()
    if args.status:
        state = json.loads(STATE.read_text()) if STATE.exists() else {}
        print(json.dumps({'freshToday': is_fresh(state), **state}, indent=2))
        return 0
    with (ROOT / '.model-sync.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        old = json.loads(STATE.read_text()) if STATE.exists() else {}
        if not args.force and is_fresh(old):
            catalogs, boards = {}, {}
            selection, fetched_at = selection_data(), datetime.now(LOCAL)
        else:
            catalogs = {name: catalog(name) for name in ['zen', 'go']}
            # Native OpenCode credentials, not the Hindsight key, determine availability here.
            auth = Path.home() / '.local/share/opencode/auth.json'
            credentials = json.loads(auth.read_text()) if auth.exists() else {}
            selection = selection_data()
            catalogs['google'] = selection['googleAuthProvider'] if credentials.get(selection['googleAuthProvider']) else False
            boards, fetched_at = load_quality_boards(selection)
        result = refresh(STATE, CONFIG, catalogs, probe_native, args.force, selection=selection, boards=boards, fetched_at=fetched_at)
        print(json.dumps({'dateUpdated': result['dateUpdated'], 'selected': result['selected']['id'], 'freshToday': True}))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, KeyError) as error:
        # aqg: top-level boundary. Avoid credential-bearing provider bodies in logs.
        print('model-sync failed: ' + type(error).__name__, file=__import__('sys').stderr)
        raise SystemExit(1)
