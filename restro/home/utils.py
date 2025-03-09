import google.generativeai as genai

# Configure the Gemini API with your API key
GEMINI_API_KEY="AIzaSyBXqExUkHEfcTICjqGMW9wag57qe_bG-Fc"   # Replace with your API key
genai.configure(api_key=GEMINI_API_KEY)

def generate_gemini_response(prompt):
    try:
        # Use Gemini 1.5 Flash model (or another model like gemini-pro)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"