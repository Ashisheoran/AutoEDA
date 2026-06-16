from openai import OpenAI
import google.generativeai as genai


class AIAssistant:

    def __init__(self, provider, api_key):
        self.provider = provider.lower()
        self.api_key = api_key

        if self.provider == "openai":
            self.client = OpenAI(api_key=api_key)

        elif self.provider == "gemini":
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel("gemini-2.5-flash")

        else:
            raise ValueError("Unsupported Provider")

    def generate_summary(
        self,
        insights,
        dataset_info=None,
        ml_results=None,
        custom_prompt=None
    ):

        prompt = self._build_prompt(
            insights,
            dataset_info,
            ml_results,
            custom_prompt
        )

        try:

            if self.provider == "openai":
                return self._openai_response(prompt)

            elif self.provider == "gemini":
                return self._gemini_response(prompt)

        except Exception as e:
            return f"AI Error: {str(e)}"

    def _openai_response(self, prompt):

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a senior data analyst. "
                        "Provide concise and actionable insights."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.3,
        )

        return response.choices[0].message.content

    def _gemini_response(self, prompt):

        response = self.model.generate_content(prompt)

        return self._trim_response(response.text)

    def _trim_response(self, text, max_lines=30):

        lines = text.split("\n")

        return "\n".join(lines[:max_lines])

    def _build_prompt(
        self,
        insights,
        dataset_info=None,
        ml_results=None,
        custom_prompt=None
    ):

        text = """
You are a senior data analyst.

Analyze the dataset and provide:

1. Key Findings
2. Data Quality Issues
3. Business Insights
4. Recommendations

Keep the response concise and professional.

"""

        if dataset_info:

            text += "\nDATASET INFORMATION:\n"

            for key, value in dataset_info.items():
                text += f"- {key}: {value}\n"

        text += "\nDATA INSIGHTS:\n"

        for category, items in insights.items():

            text += f"\n{category.upper()}:\n"

            for item in items[:5]:
                text += f"- {item}\n"

        if ml_results:

            text += "\nML RESULTS:\n"

            text += (
                f"- Problem Type: "
                f"{ml_results.get('type', 'Unknown')}\n"
            )

            text += (
                f"- Best Model: "
                f"{ml_results.get('best_model', 'N/A')}\n"
            )

            text += (
                f"- Best Score: "
                f"{ml_results.get('best_score', 'N/A')}\n"
            )

        if custom_prompt:

            text += "\nUSER REQUEST:\n"

            text += f"""
            {custom_prompt}

            IMPORTANT:
            Focus ONLY on the requested analysis type.
            Do not provide generic dataset summaries.
            Do not repeat the dataset information.
            """