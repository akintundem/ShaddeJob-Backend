import logging
import docx
import PyPDF2
import google.generativeai as genai

class ResumeProcessor:
    def __init__(self, api_key, system_instructions):
        genai.configure(api_key=api_key)
        self.system_instructions = system_instructions

    @staticmethod
    def convert_resume_to_text(file_path):
        logging.info(file_path)
        file_ext = file_path.split(".")[1].lower()

        if file_ext == 'pdf':
            return ResumeProcessor._convert_pdf_to_text(file_path)
        elif file_ext == 'docx':
            return ResumeProcessor._convert_docx_to_text(file_path)
        else:
            logging.error("Unsupported file format")
            return None

    @staticmethod
    def _convert_pdf_to_text(file_path):
        try:
            with open(file_path, 'rb') as pdf_file:
                total_text = ""
                reader = PyPDF2.PdfReader(pdf_file)
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text = page.extract_text()
                    total_text += text
                return total_text
        except Exception as e:
            logging.error(f"Error reading PDF: {e}")
            return None

    @staticmethod
    def _convert_docx_to_text(file_path):
        try:
            doc = docx.Document(file_path)
            text = "".join([para.text + "\n" for para in doc.paragraphs])
            return text
        except Exception as e:
            logging.error(f"Error reading DOCX: {e}")
            return None

    def generate_response(self, instruction_key, prompt):
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
            system_instruction=self.system_instructions[instruction_key],
        )

        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(prompt)

        return response
