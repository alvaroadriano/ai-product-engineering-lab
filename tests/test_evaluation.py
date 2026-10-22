import unittest

from app.schema import EvidenceBrief, FeedbackDataset, Theme
from evals.evaluate import evaluate


class EvaluationTests(unittest.TestCase):
    def test_flags_invalid_citations_and_nonverbatim_quotes(self):
        dataset = FeedbackDataset.model_validate({
            "project": "fictional",
            "feedback": [{"id": "F-1", "text": "Stock was unavailable at checkout."}],
        })
        reference = {
            "dataset_version": "test",
            "themes": {"Inventory visibility": ["F-1"]},
        }
        brief = EvidenceBrief.model_validate({
            "project": "fictional",
            "themes": [Theme(
                name="Inventory visibility",
                summary="Most users cannot find stock.",
                source_ids=["F-404"],
                representative_quotes=["Stock was not available."],
                confidence="low",
            )],
            "claims_to_validate": [],
            "research_questions": [],
            "limitations": [],
        })

        result = evaluate(brief, dataset, reference)

        self.assertEqual(result["citation_validity"], 0.0)
        self.assertEqual(result["exact_quote_rate"], 0.0)
        self.assertEqual(result["reference_pair_recall"], 0.0)
        self.assertTrue(result["unsupported_claims_flagged_by_heuristic"])


if __name__ == "__main__":
    unittest.main()
