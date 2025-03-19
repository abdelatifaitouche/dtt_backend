import google.generativeai as genai





class Chatbot : 
    def __init__(self, API_KEY : str):
        self.API_KEY = API_KEY
        self.MODEL = "gemini-1.5-flash"
        genai.configure(api_key=API_KEY)
        self.model = genai.GenerativeModel(self.MODEL)

    def generate(self , query : str):
        response = self.model.generate_content(query)
        return response.text

