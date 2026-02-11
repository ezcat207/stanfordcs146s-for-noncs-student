import unittest
from unittest.mock import patch, MagicMock
from week2.app.services.extract import extract_action_items_llm

class TestExtractLLM(unittest.TestCase):

    @patch('week2.app.services.extract.chat')
    def test_extract_action_items_llm_success(self, mock_chat):
        # Mock the Ollama response
        mock_response = {
            'message': {
                'content': '{"items": ["buy milk", "walk dog"]}'
            }
        }
        mock_chat.return_value = mock_response

        text = "I need to buy milk and walk the dog."
        items = extract_action_items_llm(text)

        self.assertEqual(items, ["buy milk", "walk dog"])
        # Verify prompt contained specific instructions
        args, kwargs = mock_chat.call_args
        self.assertIn('json', str(kwargs).lower()) # Simple check for structured output intent

    @patch('week2.app.services.extract.chat')
    def test_extract_action_items_llm_empty(self, mock_chat):
        mock_response = {
            'message': {
                'content': '{"items": []}'
            }
        }
        mock_chat.return_value = mock_response

        text = "Just some random notes."
        items = extract_action_items_llm(text)

        self.assertEqual(items, [])
    
    @patch('week2.app.services.extract.chat')
    def test_extract_action_items_llm_error(self, mock_chat):
        # Simulate an error (e.g. JSON parse error or network error)
        mock_chat.side_effect = Exception("Ollama error")

        items = extract_action_items_llm("foo")
        self.assertEqual(items, []) # Should gracefully handle error and return empty list

if __name__ == '__main__':
    unittest.main()
