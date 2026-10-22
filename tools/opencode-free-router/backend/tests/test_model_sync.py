import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

path = Path(__file__).resolve().parents[1] / 'model_sync.py'
spec = importlib.util.spec_from_file_location('model_sync', path)
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class ModelSyncTests(unittest.TestCase):
    def test_candidates_follow_quality_score_within_configured_groups(self):
        selection = {
            'googleAuthProvider': 'google',
            'groups': [
                {'id': 'zen', 'label': 'Zen free', 'provider': 'opencode', 'catalog': 'zen', 'strategy': 'quality'},
                {'id': 'go', 'label': 'Go free', 'provider': 'opencode-go', 'catalog': 'go', 'strategy': 'quality'},
            ],
            'quality': {'maxAgeHours': 168, 'attribution': 'LMArena', 'sources': {
                'arena_agent': {'weight': 1, 'config': 'agent', 'field': 'score'},
                'arena_webdev': {'weight': 1, 'config': 'webdev', 'field': 'rating'},
            }},
        }
        boards = {
            'arena_agent': [{'name': 'GLM-5.3-Flash', 'value': 80}, {'name': 'DeepSeek-V4.1-Flash-20261017 (Max)', 'value': 90}],
            'arena_webdev': [{'name': 'GLM-5.3-Flash', 'value': 1500}, {'name': 'DeepSeek-V4.1-Flash (Max)', 'value': 1600}],
        }
        candidates = sync.ordered_candidates(
            {'zen': ['glm-5.3-flash-free', 'deepseek-v4.1-flash-free'], 'go': ['glm-5.3-flash-free']},
            selection, boards, datetime(2026, 10, 22, tzinfo=sync.LOCAL), datetime(2026, 10, 22, tzinfo=sync.LOCAL),
        )
        self.assertEqual([row['id'] for row in candidates], [
            'opencode/deepseek-v4.1-flash-free', 'opencode/glm-5.3-flash-free', 'opencode-go/glm-5.3-flash-free',
        ])
        self.assertGreater(candidates[0]['quality']['score'], candidates[1]['quality']['score'])
        self.assertEqual(candidates[0]['group'], 'zen')

    def test_missing_quality_evidence_fails_closed(self):
        candidates = sync.ordered_candidates(
            {'zen': ['beam-free', 'flint-40b-free'], 'go': []},
            {'googleAuthProvider': 'google', 'groups': [{'id': 'zen', 'label': 'Zen free', 'provider': 'opencode', 'catalog': 'zen', 'strategy': 'quality'}], 'quality': {'maxAgeHours': 24, 'attribution': 'LMArena', 'sources': {
                'arena_agent': {'weight': 1, 'config': 'agent', 'field': 'score'},
                'arena_webdev': {'weight': 1, 'config': 'webdev', 'field': 'rating'},
            }}},
            {'arena_agent': [{'name': 'Beam 1.0 501B A23B', 'value': 0.5}], 'arena_webdev': []},
            datetime(2026, 10, 22, tzinfo=sync.LOCAL), datetime(2026, 10, 22, tzinfo=sync.LOCAL),
        )
        self.assertEqual([row['status'] for row in candidates], ['unranked', 'unranked'])

    def test_refresh_tries_best_quality_first_then_falls_back_after_quota(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state, config = root / 'model-list.json', root / 'opencode.jsonc'
            config.write_text('{}')
            now = datetime(2026, 10, 22, tzinfo=sync.LOCAL)
            selection = {'googleAuthProvider': 'google', 'groups': [{'id': 'zen', 'label': 'Zen free', 'provider': 'opencode', 'catalog': 'zen', 'strategy': 'quality'}], 'quality': {'maxAgeHours': 24, 'requiredSources': ['arena_agent'], 'attribution': 'LMArena', 'sources': {
                'arena_agent': {'weight': 1, 'config': 'agent', 'field': 'score'},
            }}}
            boards = {'arena_agent': [{'name': 'GLM-5.3-Flash', 'value': 80}, {'name': 'DeepSeek-V4.1-Flash', 'value': 90}]}
            checked = []
            def probe(model):
                checked.append(model)
                return {'status': 'quota_exhausted'} if len(checked) == 1 else {'status': 'ready'}
            result = sync.refresh(state, config, {'zen': ['glm-5.3-flash-free', 'deepseek-v4.1-flash-free']}, probe,
                                  force=True, now=now, selection=selection, boards=boards, fetched_at=now)
            self.assertEqual(checked, ['opencode/deepseek-v4.1-flash-free', 'opencode/glm-5.3-flash-free'])
            self.assertEqual(result['selected']['id'], 'opencode/glm-5.3-flash-free')
            self.assertEqual(json.loads(config.read_text())['model'], 'opencode/glm-5.3-flash-free')

    def test_unranked_candidates_do_not_change_default_or_reach_subscription_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state, config = root / 'model-list.json', root / 'opencode.jsonc'
            config.write_text('{"model":"opencode/previous-free"}')
            now = datetime(2026, 10, 22, tzinfo=sync.LOCAL)
            selection = {'googleAuthProvider': 'google', 'groups': [
                {'id': 'zen', 'label': 'Zen free', 'provider': 'opencode', 'catalog': 'zen', 'strategy': 'quality'},
                {'id': 'fallback', 'label': 'Muse fallback', 'provider': 'opencode-go', 'models': ['muse-spark-1.3-contributor'], 'strategy': 'fixed'},
            ], 'quality': {'maxAgeHours': 24, 'requiredSources': ['arena_agent'], 'attribution': 'LMArena', 'sources': {
                'arena_agent': {'weight': 1, 'config': 'agent', 'field': 'score'},
            }}}
            checked = []
            with self.assertRaisesRegex(RuntimeError, 'No model passed verification'):
                sync.refresh(state, config, {'zen': ['beam-free']}, lambda model: checked.append(model), force=True,
                             now=now, selection=selection, boards={'arena_agent': []}, fetched_at=now)
            self.assertEqual(checked, [])
            self.assertEqual(json.loads(config.read_text())['model'], 'opencode/previous-free')
            self.assertFalse(sync.is_fresh(json.loads(state.read_text())))

    def test_vietnam_day_and_future_cache(self):
        now = datetime(2026, 10, 22, 17, 1, tzinfo=timezone.utc)
        self.assertFalse(sync.is_fresh({'dateUpdated': '2026-10-22T23:59:00+07:00', 'selected': {'id': 'opencode/beam-free', 'status': 'ready'}}, now))
        self.assertTrue(sync.is_fresh({'dateUpdated': '2026-10-23T00:00:00+07:00', 'selected': {'id': 'opencode/beam-free', 'status': 'ready'}}, now))
        self.assertFalse(sync.is_fresh({'dateUpdated': '2026-10-23T02:00:00+07:00', 'selected': {'id': 'opencode/beam-free', 'status': 'ready'}}, now))

    def test_free_catalog_cannot_select_paid_models(self):
        models = sync.free_candidates({'data': [{'id': 'beam-free'}, {'id': 'muse-spark-1.3-contributor'}, {'id': '../bad-free'}, {'id': 'beam-free'}]})
        self.assertEqual(models, ['beam-free'])

    def test_new_fixed_provider_group_uses_configured_position(self):
        now = datetime(2026, 10, 22, tzinfo=sync.LOCAL)
        selection = {'googleAuthProvider': 'google', 'groups': [
            {'id': 'custom-free', 'label': 'Custom provider free', 'provider': 'custom-provider', 'models': ['model-free'], 'strategy': 'fixed'},
        ], 'quality': {'maxAgeHours': 24, 'requiredSources': ['arena_agent'], 'attribution': 'LMArena', 'sources': {
            'arena_agent': {'weight': 1, 'config': 'agent', 'field': 'score'},
        }}}
        candidates = sync.ordered_candidates({}, selection, {'arena_agent': []}, now, now)
        self.assertEqual(candidates[0]['id'], 'custom-provider/model-free')
        self.assertEqual(candidates[0]['group'], 'custom-free')

    def test_quality_cache_is_reused_only_within_configured_age(self):
        with tempfile.TemporaryDirectory() as tmp:
            old = sync.QUALITY_CACHE
            sync.QUALITY_CACHE = Path(tmp)
            try:
                now = datetime(2026, 10, 22, tzinfo=sync.LOCAL)
                cache = Path(tmp) / 'arena_agent.json'
                cache.write_text(json.dumps({'fetchedAt': '2026-10-20T00:00:00+07:00', 'data': [{'name': 'model', 'value': 1.0}]}))
                rows, fetched = sync.cached_quality('arena_agent', now, 168)
                self.assertEqual(rows[0]['name'], 'model')
                self.assertEqual(fetched.isoformat(), '2026-10-20T00:00:00+07:00')
                with self.assertRaisesRegex(ValueError, 'No recent cached benchmark data'):
                    sync.cached_quality('arena_agent', now, 24)
            finally:
                sync.QUALITY_CACHE = old

    def test_apply_preserves_other_configuration_and_backup(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / 'opencode.jsonc'
            original = {'plugins': ['existing'], 'permission': {'edit': 'ask'}}
            config.write_text(json.dumps(original))
            sync.apply_model(config, 'opencode/beam-free')
            actual = json.loads(config.read_text())
            self.assertEqual(actual, dict(original, model='opencode/beam-free'))
            self.assertTrue(list(config.parent.glob('*.admin-backup-*')))

    def test_failed_refresh_preserves_last_success_and_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / 'model-list.json'
            config = root / 'opencode.jsonc'
            config.write_text('{"model":"opencode/previous"}')
            previous = {'dateUpdated': '2026-10-21T00:00:00+07:00', 'selected': {'id': 'opencode/previous', 'status': 'ready'}}
            state.write_text(json.dumps(previous))
            with self.assertRaises(RuntimeError):
                sync.refresh(state, config, {'zen': ['beam-free'], 'go': []}, lambda mid: {'status': 'failed'}, force=True)
            self.assertEqual(json.loads(state.read_text())['dateUpdated'], previous['dateUpdated'])
            self.assertEqual(json.loads(config.read_text())['model'], 'opencode/previous')

    def test_failed_forced_refresh_invalidates_same_day_cache(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / 'model-list.json'
            config = root / 'opencode.jsonc'
            config.write_text('{}')
            state.write_text(json.dumps({'dateUpdated': datetime.now(sync.LOCAL).isoformat(), 'selected': {'id': 'opencode/beam-free', 'status': 'ready'}}))
            with self.assertRaises(RuntimeError):
                sync.refresh(state, config, {'zen': [], 'go': []}, lambda mid: {'status': 'failed'}, force=True)
            self.assertFalse(sync.is_fresh(json.loads(state.read_text())))

    def test_same_day_skips_probing_and_reapplies_cached_selection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            state = root / 'model-list.json'
            config = root / 'opencode.jsonc'
            config.write_text('{}')
            state.write_text(json.dumps({'dateUpdated': datetime.now(sync.LOCAL).isoformat(), 'selected': {'id': 'opencode/beam-free', 'status': 'ready'}}))
            def unexpected(_):
                self.fail('fresh cache must not trigger a live probe')
            result = sync.refresh(state, config, {}, unexpected)
            self.assertEqual(result['selected']['id'], 'opencode/beam-free')
            self.assertEqual(json.loads(config.read_text())['model'], 'opencode/beam-free')


if __name__ == '__main__':
    unittest.main()
