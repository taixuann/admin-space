"""Probe approved provider routes with synthetic data. Never print credentials."""
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def env_file(path):
    values = {}
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        key, sep, value = line.removeprefix('export ').partition('=')
        if sep:
            values[key.strip()] = value.strip().strip('\"\'')
    return values


def request(url, headers, payload=None):
    req = urllib.request.Request(url, headers=headers, data=None if payload is None else json.dumps(payload).encode())
    start = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            return response.status, json.load(response), round(time.monotonic() - start, 2)
    except urllib.error.HTTPError as error:
        # Preserve status only. Provider bodies can echo credentials or request details.
        return error.code, {}, round(time.monotonic() - start, 2)
    except (urllib.error.URLError, TimeoutError, OSError):
        return 0, {}, round(time.monotonic() - start, 2)


def main():
    secrets = env_file(Path.home() / '.hermes/.env')
    profile = env_file(Path.home() / '.hindsight/profiles/coding-agent.env')
    go_key = secrets.get('OPENCODE_GO_API_KEY', '')
    google_key = profile.get('GEMINI_API_KEY', '')
    report = {'timestamp_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'prompt': 'Reply with exactly OK.', 'catalogs': [], 'routes': []}
    for provider, base, key in [('zen', 'https://opencode.ai/zen/v1', secrets.get('OPENCODE_ZEN_API_KEY', go_key)), ('go', 'https://opencode.ai/zen/go/v1', go_key)]:
        headers = {'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json', 'User-Agent': 'opencode-cli/1.0', 'x-opencode-session': 'admin-route-verification'}
        status, catalog, seconds = request(base + '/models', headers)
        ids = [x['id'] for x in catalog.get('data', []) if isinstance(x, dict) and isinstance(x.get('id'), str)]
        free_ids = sorted(x for x in ids if x.endswith('-free') or x.endswith(':free'))
        report['catalogs'].append({'provider': provider, 'status': status, 'model_ids': ids, 'seconds': seconds})
        models = free_ids + (['muse-spark-1.3-contributor'] if provider == 'go' else [])
        if not models:
            report['routes'].append({'provider': provider, 'model': None, 'status': 'no_verified_catalog_candidates', 'ok': False})
        for model in models:
            payload = {'model': model, 'messages': [{'role': 'user', 'content': report['prompt']}], 'max_tokens': 16}
            status, data, seconds = request(base + '/chat/completions', headers, payload)
            content = str(data.get('choices', [{}])[0].get('message', {}).get('content') or '').strip()
            report['routes'].append({'provider': provider, 'model': model, 'http_status': status, 'ok': status == 200 and content == 'OK', 'nonempty_response': bool(content), 'seconds': seconds})
    headers = {'x-goog-api-key': google_key, 'Content-Type': 'application/json'}
    status, catalog, seconds = request('https://generativelanguage.googleapis.com/v1beta/models', headers)
    report['catalogs'].append({'provider': 'google', 'status': status, 'model_ids': [x.get('name') for x in catalog.get('models', [])], 'seconds': seconds})
    model = 'gemini-3.8-flash'
    status, data, seconds = request(f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent', headers, {'contents': [{'parts': [{'text': report['prompt']}]}], 'generationConfig': {'maxOutputTokens': 32}})
    text = ''.join(p.get('text', '') for c in data.get('candidates', []) for p in c.get('content', {}).get('parts', []))
    report['routes'].append({'provider': 'google', 'model': model, 'http_status': status, 'ok': status == 200 and text.strip() == 'OK', 'nonempty_response': bool(text.strip()), 'seconds': seconds})
    destination = ROOT / 'docs/verification.json'
    destination.write_text(json.dumps(report, indent=2) + '\n')
    for row in report['routes']:
        print(json.dumps(row))
    print('Report:', destination)
    return 0 if report['routes'] and all(x['ok'] for x in report['routes']) else 1


if __name__ == '__main__':
    raise SystemExit(main())
