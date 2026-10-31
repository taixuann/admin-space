import json
import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import ticket_submit


class TestTicketSubmit(unittest.TestCase):
    def setUp(self):
        self.datasource_id = "test-datasource-123"
        self.database_id = "test-database-456"

    @patch("ticket_submit.run_ntn_command")
    def test_create_payload_no_current_step(self, mock_ntn):
        mock_ntn.return_value = (0, json.dumps({"id": "new-page-999"}), "")
        ticket_submit.create_ticket(
            title="Test ticket",
            target_space="Development",
            system_component="Automations & Runtime",
            request_type="Fix",
            body="Stack trace details here",
            current_step="Daily maintenance failure",
            database_id=self.database_id,
        )
        # The CLI/function keeps `step`/`current_step`? Inspect payload passed to ntn.
        self.assertTrue(mock_ntn.called)
        args = mock_ntn.call_args[0][0]
        # find the -d payload
        payload_str = None
        for i, a in enumerate(args):
            if a == "-d" and i + 1 < len(args):
                payload_str = args[i + 1]
        self.assertIsNotNone(payload_str)
        payload = json.loads(payload_str)
        self.assertNotIn("Current Step", payload.get("properties", {}))
        # Status defaults to Captured when not provided
        # (covered in separate test)

    @patch("ticket_submit.run_ntn_command")
    def test_status_defaults_to_captured(self, mock_ntn):
        mock_ntn.return_value = (0, json.dumps({"id": "new-page-999"}), "")
        ticket_submit.create_ticket(
            title="Test ticket",
            database_id=self.database_id,
        )
        args = mock_ntn.call_args[0][0]
        payload_str = None
        for i, a in enumerate(args):
            if a == "-d" and i + 1 < len(args):
                payload_str = args[i + 1]
        payload = json.loads(payload_str)
        self.assertEqual(payload["properties"]["Status"]["status"]["name"], "Captured")

    @patch("ticket_submit.run_ntn_command")
    def test_step_text_as_children_paragraph(self, mock_ntn):
        mock_ntn.return_value = (0, json.dumps({"id": "new-page-999"}), "")
        step_text = "Daily maintenance failure"
        ticket_submit.create_ticket(
            title="Test ticket",
            current_step=step_text,
            database_id=self.database_id,
        )
        args = mock_ntn.call_args[0][0]
        payload_str = None
        for i, a in enumerate(args):
            if a == "-d" and i + 1 < len(args):
                payload_str = args[i + 1]
        payload = json.loads(payload_str)
        children = payload.get("children", [])
        self.assertTrue(any(
            c.get("type") == "paragraph"
            and any(rt.get("text", {}).get("content") == step_text for rt in c.get("paragraph", {}).get("rich_text", []))
            for c in children
        ), "step text not found as paragraph block")


if __name__ == "__main__":
    unittest.main()
