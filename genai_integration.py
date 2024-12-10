import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Retrieve API key from environment variables (for security)
#API_KEY = os.getenv("gemini_api_key")  # Make sure you set the environment variable for API_KEY
API_KEY = os.getenv("gemini_api_key")
if not API_KEY:
    raise ValueError("API key not found. Please set the GENAI_API_KEY environment variable.")

# Configure the Generative AI model
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(model_name='gemini-1.5-flash')


def response_of_gemini(query):
    try:
        # Generate the response from the Gemini model
        response = model.generate_content(query)
        return response.text
    except Exception as e:
        print(f"Error getting Gemini model response: {e}")
        return "I'm sorry, I couldn't process that request."
