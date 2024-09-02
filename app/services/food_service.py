import requests
import re
import json
from ..config import Config


def detect_food_and_calories(base64_image):

    """
        Detects food items, estimates calories, and lists nutrients from a base64-encoded image.

        This function sends a request to the Google AI API to identify food items in the provided image,
        estimate their calories, and list all present nutrients. The response is expected to be in JSON format.

        Parameters:
        base64_image (str): The base64-encoded image string containing the image data in the format "data:image/{type};base64,{data}".

        Returns:
        dict: A dictionary containing detected items, total calories, nutrients, and success status.
            Format: {'items': list, 'calories': int, 'nutrients': dict, 'success': bool}

        Raises:
        ValueError: If the image data format is invalid.
        requests.exceptions.RequestException: If the API request fails.
    """

    mime_type, base64_data = extract_base64_data(base64_image)
    
    request_body = {
        "contents": [
            {
                "parts": [
                    {"text": 'Identify the food in this picture, estimate the calories, and list all nutrients present. Please make sure to return the content in this structure as JSON. {"items": ["ice", "apple"], "total_calories": xx, "nutrients": {"carbohydrates": xx, "proteins": xx, "fats": xx, ...}} Just return JSON, do not include other content.'},
                    {"inline_data": {"mime_type": mime_type, "data": base64_data}}
                ]
            }
        ]
    }
    
    api_url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={Config.GOOGLE_AI_API_KEY}'
    
    response = requests.post(api_url, json=request_body, headers={'Content-Type': 'application/json'})
    response.raise_for_status()
    
    print("Raw response:", response.text)
    
    data = response.json()
    text = data['candidates'][0]['content']['parts'][0]['text']
    
    try:
        items, calories, nutrients = parse_response(text)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return {'success': False, 'error': str(e)}
    
    return {'items': items, 'calories': calories, 'nutrients': nutrients, 'success': True}





def extract_base64_data(base64_image):
    """
        Extracts MIME type and base64 data from a base64-encoded image string.

        Parameters:
        base64_image (str): The base64-encoded image string in the format "data:image/{type};base64,{data}".

        Returns:
        tuple: A tuple containing the MIME type (str) and the base64 data (str).

        Raises:
        ValueError: If the image data format is invalid.
    """
    match = re.match(r'^data:(image/\w+);base64,(.*)$', base64_image)
    if not match:
        raise ValueError('Invalid image data format.')
    return match.group(1), match.group(2)





def parse_response(text):

    """
        Parses the JSON response text to extract food items, total calories, and nutrients.

        This function searches for the JSON structure within the response text, ensures it is correctly formatted,
        and extracts the relevant data.

        Parameters:
        text (str): The response text containing JSON data.

        Returns:
        tuple: A tuple containing a list of items (list), total calories (int), and nutrients (dict).

        Raises:
        ValueError: If no valid JSON is found in the response.
        json.JSONDecodeError: If the JSON structure is malformed and cannot be parsed.
    """

    json_match = re.search(r'\{.*?\}', text, re.DOTALL)
    if not json_match:
        raise ValueError('No valid JSON found in the response.')
    
    json_str = json_match.group(0)

    # Attempt to fix JSON if it's missing a closing brace
    if json_str.count('{') > json_str.count('}'):
        json_str += '}'

    try:
        parsed_data = json.loads(json_str)
    except json.JSONDecodeError as e:
        print("Problematic JSON string:", json_str)
        raise e

    items = parsed_data.get('items', [])
    calories = parsed_data.get('total_calories', 0)
    nutrients = parsed_data.get('nutrients', {})
    return items, calories, nutrients
