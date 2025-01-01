import unittest
from unittest.mock import patch, MagicMock, call
from django.test import TestCase
from django.core.management import call_command
from django.db import connection
from io import StringIO
from llm_app.models import Hotel, GeneratedTitleDesc, SummaryTable
from llm_app.management.commands.generate import Command
from llm_app.helper import generate_title_and_description, generate_summary_and_review

class TestGenerateCommand(TestCase):
    def setUp(self):
        # Sample hotel data for testing
        self.sample_hotels = [
            (1, "Test Hotel", "100", "4.5", "Test Location", "Single", "12.34", "56.78", "test.jpg"),
            (2, "Another Hotel", "200", "4.0", "Another Location", "Double", "23.45", "67.89", "another.jpg")
        ]
        
    @patch('django.db.connection.cursor')
    def test_fetch_hotels_raw_sql(self, mock_cursor):
        # Setup mock cursor
        mock_cursor_cm = MagicMock()
        mock_cursor_cm.fetchall.return_value = self.sample_hotels
        mock_cursor.return_value.__enter__.return_value = mock_cursor_cm

        # Create command instance and test fetch_hotels_raw_sql
        command = Command()
        result = command.fetch_hotels_raw_sql()

        # Assertions
        self.assertEqual(result, self.sample_hotels)
        mock_cursor_cm.execute.assert_called_once_with(
            "SELECT id,hotel_title,rating,price,location,room_type, latitude, longitude, image_url FROM hotels;"
        )

    @patch('llm_app.helper.generate_title_and_description')
    @patch('llm_app.helper.generate_summary_and_review')
    @patch('llm_app.management.commands.generate.Command.fetch_hotels_raw_sql')
    def test_handle_with_hotels(self, mock_fetch, mock_gen_summary, mock_gen_title):
        # Setup
        mock_fetch.return_value = self.sample_hotels
        out = StringIO()

        # Execute command
        call_command('generate', stdout=out)

        # Verify calls to generate functions
        self.assertEqual(mock_gen_title.call_count, 2)
        self.assertEqual(mock_gen_summary.call_count, 2)
        
        # Verify output messages
        output = out.getvalue()
        self.assertIn('Generating content for hotel 1', output)
        self.assertIn('Successfully generated content for all hotels', output)

    @patch('llm_app.management.commands.generate.Command.fetch_hotels_raw_sql')
    def test_handle_no_hotels(self, mock_fetch):
        # Setup
        mock_fetch.return_value = []
        out = StringIO()

        # Execute command
        call_command('generate', stdout=out)

        # Verify output message
        self.assertIn('No hotels found in the database.', out.getvalue())


class TestHelperFunctions(TestCase):
    def setUp(self):
        # Create a sample hotel object for testing
        self.hotel = Hotel(
            hotel_id=1,
            title="Test Hotel",
            price="100",
            rating="4.5",
            location="Test Location",
            room_type="Single",
            latitude="12.34",
            longitude="56.78",
            image="test.jpg"
        )

    @patch('requests.post')
    def test_generate_title_and_description(self, mock_post):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "candidates": [{
                "content": {
                    "parts": [{
                        "text": "**Option 1**Title: Luxurious Test Hotel**Description: A wonderful stay"
                    }]
                }
            }]
        }
        mock_post.return_value = mock_response

        # Call function
        generate_title_and_description(self.hotel)

        # Verify API call
        mock_post.assert_called_once()
        
        # Verify database record
        generated = GeneratedTitleDesc.objects.first()
        self.assertIsNotNone(generated)
        self.assertEqual(generated.hotel_id, 1)
        self.assertEqual(generated.title, "Test Hotel")

    @patch('requests.post')
    def test_generate_summary_and_review(self, mock_post):
        # Setup mock responses for both API calls
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "candidates": [{
                "content": {
                    "parts": [{
                        "text": "This is a test summary"
                    }]
                }
            }]
        }
        mock_post.return_value = mock_response

        # Call function
        generate_summary_and_review(self.hotel)

        # Verify API calls
        self.assertEqual(mock_post.call_count, 2)
        
        # Verify database record
        summary = SummaryTable.objects.first()
        self.assertIsNotNone(summary)
        self.assertEqual(summary.hotel_id, 1)
        self.assertIsNotNone(summary.summary)
        self.assertIsNotNone(summary.review)

    @patch('requests.post')
    def test_generate_summary_and_review_api_failure(self, mock_post):
        # Setup mock response with failure
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        # Call function
        generate_summary_and_review(self.hotel)

        # Verify no database record was created
        self.assertEqual(SummaryTable.objects.count(), 0)


if __name__ == '__main__':
    unittest.main()