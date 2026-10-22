"""Verify Zen candidates through the native CLI, with bounded synthetic prompts."""
import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    report = json.loads((ROOT / 'docs/verification.json').read_text())
    models = next(c['model_ids'] for c in report['catalogs'] if c['provider'] == 'zen')
    results = []
    for model in sorted(m for m in models if m.endswith('-free') or m.endswith(':free')):
        started = time.monotonic()
        try:
            run = subprocess.run(['/opt/homebrew/bin/opencode', 'run', '--standalone', '-m', 'opencode/' + model, '--format', 'json', 'Reply with exactly OK.'], cwd='/private/tmp', capture_output=True, text=True, timeout=40)
            texts = []
            errors = []
            for line in run.stdout.splitlines():
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if event.get('type') == 'text':
                    texts.append(event.get('part', {}).get('text', ''))
                if event.get('type') == 'error':
                    errors.append('native_cli_error')
            answer = ''.join(texts).strip().rstrip('.').strip()
            result = {'model': model, 'transport': 'native OpenCode CLI', 'exit_code': run.returncode, 'ok': run.returncode == 0 and answer == 'OK', 'error_count': len(errors), 'nonempty_response': bool(answer)}
        except subprocess.TimeoutExpired:
            result = {'model': model, 'transport': 'native OpenCode CLI', 'ok': False, 'error': 'timeout_40s'}
        result['seconds'] = round(time.monotonic() - started, 2)
        results.append(result)
        (ROOT / 'docs/zen-cli-verification.json').write_text(json.dumps({'results': results, 'complete': len(results) == len([m for m in models if m.endswith('-free') or m.endswith(':free')])}, indent=2) + '\n')
        print(json.dumps(result), flush=True)
    return 0 if results and all(r['ok'] for r in results) else 1


if __name__ == '__main__':
    raise SystemExit(main())
