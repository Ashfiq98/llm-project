

from django.core.management.base import BaseCommand
from llm_app.models import Hotel
from llm_app.helper import generate_title_and_description, generate_summary_and_review
from django.db import connection

class Command(BaseCommand):
    help = 'Generate titles, descriptions, summaries, and reviews for hotels'

    def handle(self, *args, **kwargs):
        # Fetch hotels using raw SQL
        hotels = self.fetch_hotels_raw_sql()

        if not hotels:
            self.stdout.write(self.style.WARNING('No hotels found in the database.'))
            return

        for hotel in hotels:
            # Extract data from each hotel row
            id, title, price, rating, location, room_type, latitude, longitude, image_url = hotel
            # Create a hotel object-like structure to pass to the generate functions
            hotel_obj = Hotel(
                hotel_id=id,
                title=title,
                # city_name=city_name,
                price=price,
                rating=rating,
                room_type=room_type,
                location=location,
                latitude=latitude,
                longitude=longitude,
                image=image_url
            )

            self.stdout.write(f"Generating content for hotel {id}...")

            # Generate and store title and description
            generate_title_and_description(hotel_obj)

            # Generate and store summary, rating, and review
            generate_summary_and_review(hotel_obj)

        self.stdout.write(self.style.SUCCESS('Successfully generated content for all hotels'))

    def fetch_hotels_raw_sql(self):
        # Function to fetch hotels from database using raw SQL
        with connection.cursor() as cursor:
            cursor.execute("SELECT id,hotel_title,rating,price,location,room_type, latitude, longitude, image_url FROM hotels;")
            hotels = cursor.fetchall()
        return hotels


















# from django.core.management.base import BaseCommand
# from django.db import connection

# class Command(BaseCommand):
#     help = 'Fetch hotels data from the database using raw SQL'

#     def fetch_hotels_raw_sql(self):
#         # Function to fetch hotels from the database using raw SQL
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT id,hotel_title,rating,location,latitude, longitude, image_url FROM hotels;")
#             hotels = cursor.fetchall()
#             print("-----------------------------------------")
#             print(hotels)
#             print("-----------------------------------------")
#         return hotels

#     def handle(self, *args, **kwargs):
#         # Call the fetch function and print the result
#         hotels = self.fetch_hotels_raw_sql()
#         for hotel in hotels:
#             self.stdout.write(self.style.SUCCESS(f"Hotel ID: {hotel[0]}, Title: {hotel[1]}, City: {hotel[2]}, Price: {hotel[3]}"))
