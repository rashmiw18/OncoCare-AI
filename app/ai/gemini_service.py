import os
import json

from google import genai

from app.ai.prompt_templates import (
    SYSTEM_PROMPT,
    HEALTH_ANALYSIS_PROMPT
)


class GeminiService:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing from the .env file."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        # Use a model available in your API key
        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.5-flash"
        )


    def generate_health_insight(self, analysis_data):

        health_data = analysis_data.get(
            "health_data",
            {}
        )

        risk_level = analysis_data.get(
            "risk_level",
            "Unknown"
        )

        risk_factors = analysis_data.get(
            "risk_factors",
            []
        )


        prompt = f"""
{SYSTEM_PROMPT}

{HEALTH_ANALYSIS_PROMPT}

PATIENT HEALTH DATA:
{json.dumps(health_data, indent=2, default=str)}

CURRENT RISK LEVEL:
{risk_level}

DETECTED RISK FACTORS:
{json.dumps(risk_factors, indent=2)}

IMPORTANT:
Return the health analysis using exactly these sections:

SUMMARY:
Write a short and clear 2-3 sentence summary.

KEY OBSERVATIONS:
- Write observation 1
- Write observation 2
- Write observation 3

RISK FACTORS:
- Write risk factor 1
- Write risk factor 2
- Write risk factor 3

RECOMMENDATIONS:
- Write recommendation 1
- Write recommendation 2
- Write recommendation 3

CONFIDENCE:
High

STRICT RULES:
1. Keep every section separate.
2. Do not combine all content into one paragraph.
3. Do not use Markdown headings like ##.
4. Do not write SUMMARY, OBSERVATIONS, RISKS, and RECOMMENDATION on the same line.
5. Use simple language.
6. Do not diagnose diseases.
7. Do not prescribe medicines.
8. Do not recommend changing medicines or treatment.
9. For severe abnormal values, advise contacting a healthcare professional.
"""


        try:

            response = self.client.models.generate_content(

                model=self.model,

                contents=prompt

            )


            if not response or not response.text:

                return self._fallback_response(

                    risk_level,

                    risk_factors

                )


            return response.text.strip()


        except Exception as error:

            print(

                "Gemini API Error:",

                error

            )


            return self._fallback_response(

                risk_level,

                risk_factors

            )


    def _fallback_response(

        self,

        risk_level,

        risk_factors

    ):

        """

        Fallback response if Gemini API
        is temporarily unavailable.

        """

        factors_text = "\n".join(

            [

                f"- {factor}"

                for factor in risk_factors

            ]

        )


        return f"""

SUMMARY:

The health monitoring data indicates a {risk_level.lower()}-risk
health pattern based on the available vital signs and reported
symptoms. The results should be reviewed alongside professional
medical guidance.


KEY OBSERVATIONS:

- Abnormal health patterns were detected in the available monitoring data.
- The current risk level has been classified as {risk_level}.
- Further monitoring of health trends is recommended.


RISK FACTORS:

{factors_text if factors_text else "- No specific risk factors were identified."}


RECOMMENDATIONS:

- Continue recording health data regularly.
- Monitor any worsening or unusual symptoms.
- Contact a qualified healthcare professional for medical evaluation
  when symptoms are severe or concerning.


CONFIDENCE:

Medium

"""