import os

from google import genai


class ChatbotService:

    def __init__(self):

        chatbot_api_key = os.getenv(
            "CHATBOT_GEMINI_API_KEY"
        )

        if not chatbot_api_key:

            raise ValueError(
                "CHATBOT_GEMINI_API_KEY is missing."
            )

        self.client = genai.Client(

            api_key=chatbot_api_key

        )

        self.model = "gemini-3.5-flash"


    def generate_response(

        self,

        user_message,

        health_context=""

    ):

        system_prompt = """

You are OncoCare AI Health Assistant.

You are a helpful and responsible health-information assistant.

Your role is to:

- Explain health information clearly.
- Help users understand their recorded health data.
- Explain AI-generated health insights.
- Identify trends in provided health data.
- Suggest questions the user may discuss with a qualified healthcare professional.

Important safety rules:

- Do not diagnose diseases.
- Do not prescribe medicines.
- Do not recommend changing prescribed medication.
- Do not claim to replace a doctor.
- If the user describes a serious or urgent health concern, advise them to seek professional medical care promptly.
- Use simple, supportive, and easy-to-understand language.

Always answer based on the available health data when relevant.

Use organized responses with:

- Short headings
- Bullet points
- Clear explanations

"""


        prompt = f"""

{system_prompt}


PATIENT HEALTH CONTEXT:

{health_context}


USER QUESTION:

{user_message}


Give a clear and helpful response.

"""


        try:

            response = (

                self.client.models.generate_content(

                    model=self.model,

                    contents=prompt

                )

            )

            return response.text


        except Exception as error:

            print(

                "CHATBOT ERROR:",

                error

            )

            raise