from openai import OpenAI
import google.generativeai as genai

class AIAssistant:
    def __init__(self, provider, api_key):
        self.provider = provider.lower()
        self.api_key = api_key

        if self.provider == "openai":
            if OpenAI is None:
                raise ImportError("openai is not installed.")
            self.client = OpenAI(api_key=api_key)

        elif self.provider == "gemini":
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel("gemini-2.5-flash")

        else:
            raise ValueError("Unsupported Provider")

    def generate_summary(self, insights):
        prompt = self._build_prompt(insights)
        
        if self.provider == 'openai':
            try:
                return self._openai_response(prompt)
            except Exception as e:
                return f"AI Error: {str(e)}"
        
        elif self.provider == 'gemini':
            try:
                return self._gemini_response(prompt)
            except Exception as e:
                return f"AI Error: {str(e)}"


    def _openai_response(self,prompt):
        response = self.client.chat.completions.create(
            model = 'gpt-4o-mini',
            messages = [
                {"role": "system", "content": "You are a Data Analyst"},
                {"role": "user", "content": prompt}
            ],
            temperature = 0.3
        )
        return response.choices[0].message.content
    

    def _gemini_response(self, prompt):
        response = self.model.generate_content(prompt)
        return self._trim_response(response.text)
    

    def _trim_response(self,text,max_lines = 20):
        lines = text.split("\n")
        return "\n".join(lines[:max_lines])
    


    def _build_prompt(self, insights):
        text = "You are a senior data analyst.\n"
        text += "Analyze the dataset insights and respond VERY CONCISELY.\n\n"

        for category, items in insights.items():
            text += f"{category.upper()}:\n"
            for item in items[:3]:
                text += f"- {item}\n"

        text += """
    STRICT RULES:
    - Max 200 words total
    - Use bullet points only
    - No paragraphs
    - No explanations longer than 1 line
    - Focus only on important issues

    FORMAT:

    KEY INSIGHTS:
    - ...

    ISSUES:
    - ...

    RECOMMENDATIONS:
    - ...
    """

        return text