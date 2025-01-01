import requests
import random
from .models import GeneratedTitleDesc, SummaryTable
import re

# API Key and Endpoint for Gemini Flash 2.0
API_KEY = 'AIzaSyDvNJyX6-EaREyte97TO8vxCkr65lktaMM'
API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=' + API_KEY

def parse_generated_text(text):
    """ Helper function to parse the text and extract titles and descriptions """
    options = []
    
    # Split by '**Option' (use regex to capture each option correctly)
    option_pattern = r"\*\*Option.*?Title:\s*(.*?)\s*\*\*Description:\s*(.*?)\s*(?=\*\*Option|$)"
    matches = re.findall(option_pattern, text, re.DOTALL)
    
    # Add matched titles and descriptions to the options list
    for match in matches:
        title, description = match
        # Remove unwanted '**' and '*' characters from both title and description
        title = re.sub(r"[\*\*]", "", title).strip()
        description = re.sub(r"[\*\*]", "", description).strip()
        description = re.sub(r"\*", "", description).strip()  # Removing '*' as well
        options.append((title, description))
    
    return options



def generate_title_and_description(hotel):
    title = hotel.title
    # city_name = hotel.city_name
    room_type = hotel.room_type
    location = hotel.location
    prompt = f"generate a unique title for this '{title}', generate a description for this: title: '{title}', room_type: '{room_type}', location: '{location}' "

    # Send request to Gemini API to generate content
    response = requests.post(API_URL, json={
        "contents": [{"parts": [{"text": prompt}]}]
    })

    if response.status_code == 200:
        data = response.json()
        print(data)

        # Extract generated title and description
        generated_title = ""
        description = ""

        if "candidates" in data and len(data["candidates"]) > 0:
            content = data["candidates"][0].get("content", {})
            if "parts" in content and len(content["parts"]) > 0:
                text = content["parts"][0].get("text", "")
                if text:
                    # Parse the generated text using the helper function
                    options = parse_generated_text(text)
                    
                    if options:
                        # Use the first option or select a suitable one
                        generated_title, description = options[0]  # Get the first valid option

        # Log the generated title and description for debugging
        print(f"Generated Title: {generated_title}")
        print(f"Description: {description}")

        # Save the generated title and description to the database
        if generated_title and description:
            generated_record = GeneratedTitleDesc(
                hotel_id=hotel.hotel_id,
                title=title,
                generated_title=generated_title,
                description=description
            )
            generated_record.save()
    else:
        print(f"Failed to generate title and description for hotel {hotel.hotel_id}: {response.status_code}")


def generate_summary_and_review(hotel):
    # Generating a summary based on title, city_name, price, rating, room_type
    title = hotel.title
    # city_name = hotel.city_name
    price = hotel.price
    rating = hotel.rating
    room_type = hotel.room_type
    location = hotel.location

    summary_prompt = f"Generate a summary for a hotel which is named {title} and offers {room_type} rooms. The price is {price} with rating {rating}, and the location is {location}."

    # Send the request to Gemini API for summary
    response = requests.post(API_URL, json={
        "contents": [{"parts": [{"text": summary_prompt}]}]
    })

    if response.status_code == 200:
        data = response.json()
        print('--------------------------------')
        print(data)  # Debug print to check the API response
        print('--------------------------------')
        
        # Extract and clean summary from the response
        summary = data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', "").strip()

        # Generate a random rating between 1 and 5
        rating_value = random.randint(1, 5)

        # Generate a review based on price, rating, and room type
        review_prompt = f"Generate a review for a hotel based on its price ({price}), rating ({rating_value}), and room type ({room_type})."
        review_response = requests.post(API_URL, json={
            "contents": [{"parts": [{"text": review_prompt}]}]
        })

        if review_response.status_code == 200:
            review_data = review_response.json()
            print(f"API Response for {hotel.hotel_id} Review: {review_data}")  # Debug print to check review response
            
            # Extract and clean review from the response
            review = review_data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', "").strip()

            # Check if summary and review are not empty before saving
            if summary and review:
                # Print the hotel_id, summary, rating, and review before saving
                print(f"Hotel ID: {hotel.hotel_id}")
                print(f"Summary: {summary}")
                print(f"Rating: {rating_value}")
                print(f"Review: {review}")
                
                # Save the summary, rating, and review in the database
                summary_record = SummaryTable(
                    hotel_id=hotel.hotel_id,  # Use hotel_id instead of hotel
                    summary=summary,
                    rating=rating_value,
                    review=review
                )
                summary_record.save()  # Saving the record
                
            else:
                print(f"Empty summary or review for hotel {hotel.hotel_id}. Not saving.")
        else:
            print(f"Failed to generate review for hotel {hotel.hotel_id}: {review_response.status_code}")
    else:
        print(f"Failed to generate summary for hotel {hotel.hotel_id}: {response.status_code}")