import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from base64 import b64encode
from datetime import datetime

def get_latest_screenshot():
    # Get the screenshots directory relative to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    screenshots_dir = os.path.join(script_dir, "screenshots")
    
    if not os.path.exists(screenshots_dir):
        raise FileNotFoundError(f"Screenshots directory not found at: {screenshots_dir}")
    
    latest_screenshot = None
    latest_time = 0
    
    for file in os.listdir(screenshots_dir):
        file_path = os.path.join(screenshots_dir, file)
        # Check if it's a file and has a screenshot-like extension
        if os.path.isfile(file_path) and file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_time = os.path.getmtime(file_path)
            if file_time > latest_time:
                latest_time = file_time
                latest_screenshot = file_path
    
    if latest_screenshot is None:
        raise FileNotFoundError(f"No screenshots found in {screenshots_dir}")
        
    return latest_screenshot

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return b64encode(image_file.read()).decode('utf-8')

def parse_screenshot(image_path):
    # Load environment variables
    load_dotenv()
    
    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Encode the image
    base64_image = encode_image(image_path)
    
    # Prepare the messages for the API
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "This is a Robinhood screenshot. Please extract the total balance from the top left. On the right, there is a list of stocks. Extract the stock symbol and total value for each one. Return ONLY a valid JSON object with this format: {\"total_balance\": \"$X,XXX.XX\", \"stocks\": {\"symbol\": \"$XX.XX\", \"symbol\": \"$XX.XX\"}}"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ]
    
    # Make the API call
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=1000
    )
    
    # Parse the response
    try:
        content = response.choices[0].message.content
        # Remove any markdown formatting if present
        if content.startswith("```") and content.endswith("```"):
            content = content.split("```")[1]
            if content.startswith("json\n"):
                content = content[5:]
        # Try to parse the JSON
        result = json.loads(content)
    except json.JSONDecodeError:
        # If not valid JSON, return the raw response
        result = {"error": "Could not parse response", "raw_response": response.choices[0].message.content}
    
    return result

def main():
    try:
        # Get the most recent screenshot
        image_path = get_latest_screenshot()
        print(f"Using most recent screenshot: {image_path}")
        
        result = parse_screenshot(image_path)
        print("\nParsed Data:")
        print(json.dumps(result, indent=2))
    except FileNotFoundError as e:
        print(f"\nError: {str(e)}")
        print("Please make sure to:")
        print("1. Create a 'screenshots' folder in the same directory as this script")
        print("2. Place your Robinhood screenshots in that folder")
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main() 