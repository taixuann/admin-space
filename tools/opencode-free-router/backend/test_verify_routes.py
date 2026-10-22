import importlib.util
import io
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('verify_routes', Path(__file__).with_name('verify_routes.py'))
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


class ProbeTests(unittest.TestCase):
    def test_env_ignores_comments_and_reads_quoted_key(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'private.env'
            path.write_text('# TOKEN=old\nexport TOKEN="synthetic"\n')
            self.assertEqual(probe.env_file(path), {'TOKEN': 'synthetic'})

    def test_http_error_body_is_not_returned(self):
        error = urllib.error.HTTPError('https://example.invalid', 429, 'quota', {}, io.BytesIO(b'sensitive echoed credential'))
        with patch.object(probe.urllib.request, 'urlopen', side_effect=error):
            status, data, seconds = probe.request('https://example.invalid', {})
        self.assertEqual((status, data), (429, {}))
        self.assertGreaterEqual(seconds, 0)

    def test_network_failure_is_explicit(self):
        with patch.object(probe.urllib.request, 'urlopen', side_effect=urllib.error.URLError('offline')):
            status, data, _ = probe.request('https://example.invalid', {})
        self.assertEqual((status, data), (0, {}))


if __name__ == '__main__':
    unittest.main()
