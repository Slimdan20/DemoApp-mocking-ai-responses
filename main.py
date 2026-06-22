from fastapi import FastAPI, Depends
from dotenv import load_dotenv
from groq import Groq
import os
import json

app = FastAPI(
    title="Materna API",
    description="Materna is an AI-powered maternal health API that provides risk assessment, weekly pregnancy guidance, drug safety checks, antenatal scheduling, and delivery preparation — built for developers creating maternal health applications across Africa and beyond.",
    version="1.0.0"
)

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_groq():
    return client

@app.get("/v1/labor-signs")
def labor_signs(groq_client=Depends(get_groq)):
    prompt = """
      You are a clinical maternal health assistant. Provide comprehensive information on the signs of labor, including early signs, active labor signs, and when to seek medical attention.
      
      Keep all field values concise — maximum 1-2 sentences per field.

      Respond ONLY with a JSON object in this exact format, no extra text, no markdown:
      {
        "true_labor_signs": "signs that indicate true labor",
        "false_labor_signs": "signs that may mimic labor but are not true labor (Braxton Hicks contractions, etc.)",
        "early_signs": "common early signs of labor",
        "active_labor_signs": "signs that indicate active labor",
        "when_to_seek_care": "specific signs or situations that should prompt immediate medical attention",
        "disclaimer": "This is for informational purposes only. Always consult a qualified healthcare provider."
      }
      """

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    result = json.loads(response.choices[0].message.content)
    return result
