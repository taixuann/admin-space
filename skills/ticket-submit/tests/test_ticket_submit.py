import json
import os
import subprocess
import unittest
from unittest.mock import MagicMock, patch

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))

import ticket_submit


class TestTicketSubmit(unittest.TestCase):
    def setUp(self):
        self.datasource_id = "test-datasource-123"
        self.database_id = "test-database-456"

    @patch("ticket_submit.run_ntn_command")
    def test_query_open_ticket_found(self, mock_ntn):
        mock_response = {
            "results": [
                {
                    "id": "page-open-789",
                    "properties": {
                        "Ticket": {"title": [{"plain_text": "Error in automation"}]}
                    }
                }
            ]
        }
        mock_ntn.return_value = (0, json.dumps(mock_response), "")

        page_id = ticket_submit.query_open_ticket("Error in automation", data_source_id=self.datasource_id)
        self.assertEqual(page_id, "page-open-789")
        mock_ntn.assert_called_once()
        args = mock_ntn.call_args[0]
        self.assertIn("v1/data_sources/test-datasource-123/query", args[0])

    @patch("ticket_submit.run_ntn_command")
    def test_query_open_ticket_not_found(self, mock_ntn):
        mock_response = {"results": []}
        mock_ntn.return_value = (0, json.dumps(mock_response), "")

        page_id = ticket_submit.query_open_ticket("Unknown error", data_source_id=self.datasource_id)
        self.assertIsNone(page_id)

    @patch("ticket_submit.run_ntn_command")
    def test_append_ticket_comment(self, mock_ntn):
        mock_ntn.return_value = (0, json.dumps({"id": "comment-1"}), "")
        success = ticket_submit.append_ticket_comment("page-123", "Recurring error log")
        self.assertTrue(success)
        mock_ntn.assert_called_once()
        args = mock_ntn.call_args[0]
        self.assertIn("v1/comments", args[0])

    @patch("ticket_submit.run_ntn_command")
    def test_create_ticket(self, mock_ntn):
        mock_ntn.return_value = (0, json.dumps({"id": "new-page-999"}), "")
        result = ticket_submit.create_ticket(
            title="[Auto-Sync] Error in skill update",
            target_space="Development",
            system_component="Automations & Runtime",
            request_type="Fix",
            status="Blocked",
            current_step="Daily maintenance failure",
            body="Stack trace details here",
            database_id=self.database_id,
        )
        self.assertEqual(result, "new-page-999")
        mock_ntn.assert_called_once()
        args = mock_ntn.call_args[0]
        self.assertIn("v1/pages", args[0])

    @patch("ticket_submit.create_ticket")
    @patch("ticket_submit.append_ticket_comment")
    @patch("ticket_submit.query_open_ticket")
    def test_submit_or_update_ticket_dedup_branch(self, mock_query, mock_comment, mock_create):
        mock_query.return_value = "existing-page-111"
        mock_comment.return_value = True

        res = ticket_submit.submit_or_update_ticket(
            title="[Auto-Sync] Error in skill update",
            target_space="Development",
            system_component="Automations & Runtime",
            request_type="Fix",
            status="Blocked",
            body="New run error log",
            data_source_id=self.datasource_id,
            database_id=self.database_id,
        )
        self.assertTrue(res["success"])
        self.assertEqual(res["action"], "commented")
        self.assertEqual(res["page_id"], "existing-page-111")
        mock_create.assert_not_called()
        mock_comment.assert_called_once()

    @patch("ticket_submit.create_ticket")
    @patch("ticket_submit.append_ticket_comment")
    @patch("ticket_submit.query_open_ticket")
    def test_submit_or_update_ticket_create_branch(self, mock_query, mock_comment, mock_create):
        mock_query.return_value = None
        mock_create.return_value = "brand-new-page-222"

        res = ticket_submit.submit_or_update_ticket(
            title="[Auto-Sync] Error in skill update",
            target_space="Development",
            system_component="Automations & Runtime",
            request_type="Fix",
            status="Blocked",
            body="New run error log",
            data_source_id=self.datasource_id,
            database_id=self.database_id,
        )
        self.assertTrue(res["success"])
        self.assertEqual(res["action"], "created")
        self.assertEqual(res["page_id"], "brand-new-page-222")
        mock_comment.assert_not_called()
        mock_create.assert_called_once()

    @patch("ticket_submit.query_open_ticket")
    def test_submit_or_update_ticket_soft_failure(self, mock_query):
        mock_query.side_effect = RuntimeError("ntn executable missing")
        res = ticket_submit.submit_or_update_ticket(
            title="[Auto-Sync] Error",
            target_space="Development",
            system_component="Automations & Runtime",
            body="Log",
            data_source_id=self.datasource_id,
            database_id=self.database_id,
        )
        self.assertFalse(res["success"])
        self.assertEqual(res["action"], "failed")
        self.assertIn("ntn executable missing", res["error"])


if __name__ == "__main__":
    unittest.main()
