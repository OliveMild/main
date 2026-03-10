import unittest
import feedback


class TestFeedback(unittest.TestCase):
    def setUp(self):
        feedback.reset_feedback()

    def test_submit_and_average(self):
        feedback.submit_feedback(4, comment="Works well")
        feedback.submit_feedback(5)
        self.assertEqual(feedback.get_average_rating(), 4.5)

    def test_average_with_no_feedback(self):
        self.assertIsNone(feedback.get_average_rating())

    def test_single_feedback(self):
        feedback.submit_feedback(3)
        self.assertEqual(feedback.get_average_rating(), 3.0)

    def test_feedback_with_comment(self):
        feedback.submit_feedback(5, comment="Great application!")
        feedback.submit_feedback(3)
        self.assertEqual(feedback.get_average_rating(), 4.0)

    def test_invalid_rating_type(self):
        with self.assertRaises(TypeError):
            feedback.submit_feedback("five")

    def test_invalid_rating_out_of_range(self):
        with self.assertRaises(ValueError):
            feedback.submit_feedback(6)
        with self.assertRaises(ValueError):
            feedback.submit_feedback(0)


if __name__ == "__main__":
    unittest.main()
