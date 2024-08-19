import google.generativeai as genai

class GeminiService:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)

    def generate_response(self,system_instructions, history, prompt):
        generation_config = {
            "temperature": 0,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction=self.system_instructions
        )
        
        # TO DO: fix the history = []
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(prompt)

        return response
