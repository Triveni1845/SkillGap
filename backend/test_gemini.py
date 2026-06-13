import google.generativeai as genai

genai.configure(api_key="your_api_key_here")

model = genai.GenerativeModel("gemini-2.5-flash")

response = model.generate_content(
    "List the skills required for a Python Developer. Return only skill names."
)

print(response.text)