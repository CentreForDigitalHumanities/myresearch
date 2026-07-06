import json
import os
import tempfile
from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase


class TestCreateFormFixture(TestCase):
    """Smokescreen tests for the create_form_fixture management command."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.output_path = os.path.join(self.temp_dir, "test_fixture.json")

    def tearDown(self):
        """Clean up temporary files."""
        if os.path.exists(self.output_path):
            os.remove(self.output_path)
        os.rmdir(self.temp_dir)

    @patch("form.management.commands.create_form_fixture.call_command")
    def test_command_creates_output_file(self, mock_call_command):
        """Test that the command creates an output file."""
        # Mock the dumpdata call to create a basic fixture
        mock_call_command.side_effect = self._create_mock_fixture

        out = StringIO()
        call_command("create_form_fixture", output=self.output_path, stdout=out)

        assert os.path.exists(self.output_path)
        assert "Successfully dumped fixture" in out.getvalue()

    @patch("form.management.commands.create_form_fixture.call_command")
    def test_basequestion_sorted_by_step_then_order(self, mock_call_command):
        """Test that basequestions are sorted by step first, then _order."""
        mock_call_command.side_effect = self._create_mock_fixture

        call_command("create_form_fixture", output=self.output_path)

        with open(self.output_path, "r") as f:
            data = json.load(f)

        questions = [item for item in data if item["model"] == "form.basequestion"]

        # Verify sorted by step, then _order
        for i in range(len(questions) - 1):
            curr_step = questions[i]["fields"]["step"]
            curr_order = questions[i]["fields"]["_order"]
            next_step = questions[i + 1]["fields"]["step"]
            next_order = questions[i + 1]["fields"]["_order"]

            if curr_step == next_step:
                assert (
                    curr_order <= next_order
                ), f"Same step {curr_step}: order {curr_order} should be <= {next_order}"
            else:
                assert (
                    curr_step < next_step
                ), f"Step should be ascending: {curr_step} >= {next_step}"

    @patch("form.management.commands.create_form_fixture.call_command")
    def test_selectoption_sorted_by_question_then_order(self, mock_call_command):
        """Test that selectoptions are sorted by question first, then _order."""
        mock_call_command.side_effect = self._create_mock_fixture

        call_command("create_form_fixture", output=self.output_path)

        with open(self.output_path, "r") as f:
            data = json.load(f)

        options = [item for item in data if item["model"] == "form.selectoption"]

        # Verify sorted by question, then _order
        for i in range(len(options) - 1):
            curr_question = options[i]["fields"]["question"]
            curr_order = options[i]["fields"]["_order"]
            next_question = options[i + 1]["fields"]["question"]
            next_order = options[i + 1]["fields"]["_order"]

            if curr_question == next_question:
                assert (
                    curr_order <= next_order
                ), f"Same question {curr_question}: order {curr_order} should be <= {next_order}"
            else:
                assert (
                    curr_question < next_question
                ), f"Question should be ascending: {curr_question} >= {next_question}"

    @patch("form.management.commands.create_form_fixture.call_command")
    def test_step_sorted_by_form_then_parent_then_order(self, mock_call_command):
        """Test that steps are sorted by form, parent, then _order."""
        mock_call_command.side_effect = self._create_mock_fixture

        call_command("create_form_fixture", output=self.output_path)

        with open(self.output_path, "r") as f:
            data = json.load(f)

        steps = [item for item in data if item["model"] == "form.step"]

        # Verify sorted by form, parent, _order
        for i in range(len(steps) - 1):
            curr_form = steps[i]["fields"]["form"]
            curr_parent = steps[i]["fields"].get("parent")
            curr_order = steps[i]["fields"]["_order"]
            next_form = steps[i + 1]["fields"]["form"]
            next_parent = steps[i + 1]["fields"].get("parent")
            next_order = steps[i + 1]["fields"]["_order"]

            if curr_form == next_form:
                if curr_parent == next_parent:
                    assert (
                        curr_order <= next_order
                    ), f"Same form {curr_form}, parent {curr_parent}: order {curr_order} should be <= {next_order}"
                else:
                    # None values become float("-inf") and sort first
                    curr_parent_val = (
                        curr_parent if curr_parent is not None else float("-inf")
                    )
                    next_parent_val = (
                        next_parent if next_parent is not None else float("-inf")
                    )
                    assert (
                        curr_parent_val < next_parent_val
                    ), f"Parent should be ascending in same form {curr_form}"
            else:
                assert (
                    curr_form < next_form
                ), f"Form should be ascending: {curr_form} >= {next_form}"

    @patch("form.management.commands.create_form_fixture.call_command")
    def test_none_values_handled_gracefully(self, mock_call_command):
        """Test that None values in sort fields are handled gracefully."""

        def create_fixture_with_none(*args, **kwargs):
            output_path = kwargs.get("output")
            data = [
                {
                    "model": "form.step",
                    "pk": 1,
                    "fields": {"form": 1, "parent": None, "_order": 0},
                },
                {
                    "model": "form.step",
                    "pk": 2,
                    "fields": {"form": 1, "parent": 1, "_order": 0},
                },
            ]
            with open(output_path, "w") as f:
                json.dump(data, f)

        mock_call_command.side_effect = create_fixture_with_none

        call_command("create_form_fixture", output=self.output_path)

        with open(self.output_path, "r") as f:
            data = json.load(f)

        # Verify it handles None parent without crashing
        assert len(data) == 2
        assert data[0]["fields"]["parent"] is None
        assert data[1]["fields"]["parent"] == 1

    @patch("form.management.commands.create_form_fixture.call_command")
    def test_output_is_valid_json(self, mock_call_command):
        """Test that output is valid JSON."""
        mock_call_command.side_effect = self._create_mock_fixture

        call_command("create_form_fixture", output=self.output_path)

        # Should not raise exception
        with open(self.output_path, "r") as f:
            data = json.load(f)

        assert isinstance(data, list)
        assert len(data) > 0

    def _create_mock_fixture(self, *args, **kwargs):
        """Helper to create a mock fixture file for testing."""
        output_path = kwargs.get("output")

        fixture_data = [
            {
                "model": "form.basequestion",
                "pk": 1,
                "fields": {"step": 1, "_order": 0, "text": "Q1"},
            },
            {
                "model": "form.basequestion",
                "pk": 2,
                "fields": {"step": 1, "_order": 1, "text": "Q2"},
            },
            {
                "model": "form.basequestion",
                "pk": 3,
                "fields": {"step": 2, "_order": 0, "text": "Q3"},
            },
            {
                "model": "form.selectoption",
                "pk": 1,
                "fields": {"question": 1, "_order": 0, "label": "Option A"},
            },
            {
                "model": "form.selectoption",
                "pk": 2,
                "fields": {"question": 1, "_order": 1, "label": "Option B"},
            },
            {
                "model": "form.selectoption",
                "pk": 3,
                "fields": {"question": 2, "_order": 0, "label": "Option C"},
            },
            {
                "model": "form.step",
                "pk": 1,
                "fields": {"form": 1, "parent": None, "_order": 0, "name": "Step 1"},
            },
            {
                "model": "form.step",
                "pk": 2,
                "fields": {"form": 1, "parent": 1, "_order": 0, "name": "Step 1.1"},
            },
            {
                "model": "form.step",
                "pk": 3,
                "fields": {"form": 1, "parent": None, "_order": 1, "name": "Step 2"},
            },
        ]

        with open(output_path, "w") as f:
            json.dump(fixture_data, f, indent=4)
