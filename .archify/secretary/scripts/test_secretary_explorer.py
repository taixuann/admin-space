#!/usr/bin/env python3
"""Contract tests for one unified graph and fail-closed authored mappings."""
import copy
import sys
import tempfile
import unittest
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import secretary_explorer as se
import profile_capabilities as pc

class UnifiedTests(unittest.TestCase):
    def test_legacy_output_stays_in_hidden_archive(self):
        self.assertEqual(
            se.output_path(se.REPO_ROOT),
            se.REPO_ROOT / '.archify/secretary/native/profile-legacy.html',
        )

    def setUp(self):
        self.data = pc.load_yaml_text(se.yaml_path(se.REPO_ROOT).read_text())
        self.mapping = se.load_mapping(se.mapping_path(se.REPO_ROOT))

    def test_one_native_document_not_frames(self):
        text = se.output_path(se.REPO_ROOT).read_text()
        for forbidden in ('<iframe', 'srcdoc=', '<object', '<embed'):
            self.assertNotIn(forbidden, text.lower())
        self.assertEqual(text.count('id="secretary-primary-graph"'), 1)
        self.assertEqual(text.lower().count('<!doctype html'), 1)
        self.assertEqual(text.lower().count('<html lang'), 1)

    def test_model_connects_every_capability_to_authored_stages(self):
        model = se.make_model(self.data, self.mapping)
        edges = {(x['from'], x['to']) for x in model['connections']}
        for cid, node_id in se.capability_nodes(self.data).items():
            for stage in self.mapping['stages']:
                if cid in stage['capability_ids']:
                    self.assertIn((node_id, stage['id']), edges)
        self.assertIn(('identity', 'inspect'), edges)
        self.assertIn(('permissions', 'delegate'), edges)
        self.assertIn(('inspect', 'memory_context'), edges)

    def test_opencode_is_only_delegate_dependency(self):
        self.assertEqual([s['id'] for s in self.mapping['stages'] if 'opencode' in s['capability_ids']], ['delegate'])
        self.assertEqual(self.data['external_tools'], [])
        self.assertEqual(self.data['mcps'], [])

    def test_invalid_mapping_shapes_fail_closed(self):
        invalid = [None, {}, {'stages': []}, {'stages': 'bad'},
                   {'stages': [{'id': '../bad', 'label': 'x', 'capability_ids': []}]},
                   {'stages': [{'id': 'x', 'label': 'x', 'capability_ids': ['unknown']}]},
                   {'stages': [{'id': 'x', 'label': 'x', 'capability_ids': [], 'surprise': 1}]}]
        for m in invalid:
            with self.subTest(mapping=m), self.assertRaises(se.MappingError):
                se.validate_mapping(m, se.capability_ids_from_yaml(self.data))

    def test_duplicate_stages_and_dependencies_rejected(self):
        for duplicate in ('stages', 'capability_ids'):
            m = copy.deepcopy(self.mapping)
            if duplicate == 'stages': m['stages'].append(m['stages'][0])
            else: m['stages'][1]['capability_ids'] *= 2
            with self.assertRaises(se.MappingError):
                se.validate_mapping(m, se.capability_ids_from_yaml(self.data))

    def test_duplicate_yaml_rejected(self):
        with tempfile.TemporaryDirectory(dir=Path.home()/'.hermes/cache/scratch') as tmp:
            path = Path(tmp)/'mapping.yaml'
            path.write_text('stages: []\nstages: []\n')
            with self.assertRaises(se.MappingError): se.load_mapping(path)

    def test_unknown_graph_stage_rejected(self):
        m = copy.deepcopy(self.mapping)
        m['stages'][0]['id'] = 'unmapped_graph_stage'
        with self.assertRaises(se.MappingError): se.make_model(self.data, m)

    def test_malicious_labels_are_text(self):
        m = copy.deepcopy(self.mapping)
        m['stages'][0]['label'] = '</script><img src=x onerror=alert(1)>'
        baseline = '<html><head></head><body><svg ' + ' '.join([]) + '></svg></body></html>'
        # The controls use escaped HTML and script-safe JSON, never raw labels.
        controls = se.controls_html(self.data, m)
        self.assertNotIn('<img', controls)
        self.assertIn('&lt;img', controls)

    def test_unmapped_capability_says_not_assessed(self):
        data = copy.deepcopy(self.data)
        data['skills'].append('unmapped <capability>')
        self.assertIn('Not assessed: no authored stage dependency', se.controls_html(data, self.mapping))

if __name__ == '__main__': unittest.main()
