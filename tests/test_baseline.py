import json
import unittest
from pathlib import Path

from app.analysis import baseline_analysis
from app.schema import FeedbackDataset


def fixture_dataset():
    path = Path(__file__).resolve().parents[1] / "fixtures" / "feedback.json"
    return FeedbackDataset.model_validate(json.loads(path.read_text(encoding="utf-8")))


class BaselineTests(unittest.TestCase):
    def test_groups_expected_fixture_items_and_preserves_quotes(self):
        dataset = fixture_dataset()
        brief = baseline_analysis(dataset)
        by_name = {theme.name: theme for theme in brief.themes}

        self.assertEqual(set(by_name), {
            "Inventory visibility",
            "Checkout reliability",
            "Order status clarity",
        })
        self.assertEqual(by_name["Inventory visibility"].source_ids, ["F-001", "F-004", "F-006"])
        self.assertEqual(by_name["Checkout reliability"].source_ids, ["F-002"])
        self.assertEqual(by_name["Order status clarity"].source_ids, ["F-003", "F-005"])
        self.assertEqual(by_name["Checkout reliability"].representative_quotes, [dataset.feedback[1].text])

    def test_labels_limitations_and_keeps_claims_cautious(self):
        brief = baseline_analysis(fixture_dataset())

        self.assertTrue(all(theme.confidence == "low" for theme in brief.themes))
        self.assertTrue(any("synthetic" in item for item in brief.limitations))
        self.assertTrue(all("revenue" not in claim.lower() for claim in brief.claims_to_validate))


if __name__ == "__main__":
    unittest.main()
