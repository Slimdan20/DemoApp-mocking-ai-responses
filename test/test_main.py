from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from main import app, get_groq
import json

client = TestClient(app)

def test_labor_signs():
    def fake_get_groq():
        fake = MagicMock()
        fake.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(
                message=MagicMock(
                    content=json.dumps({
                        "true_labor_signs": "cervical dilation, regular contractions, and water breaking.",
                        "false_labor_signs": "braxton hicks contractions, irregular contractions, and no cervical changes.",
                        "early_signs": "light spotting, backache, and pelvic pressure.",
                        "disclaimer": "This is for informational purposes only. Always consult a qualified healthcare provider."
                    })
                )
            )]
        )
        return fake

    app.dependency_overrides[get_groq] = fake_get_groq
    
    response = client.get("/v1/labor-signs")
    assert response.status_code == 200
    data = response.json()
    assert data["true_labor_signs"] == "cervical dilation, regular contractions, and water breaking."
    assert data["false_labor_signs"] == "braxton hicks contractions, irregular contractions, and no cervical changes."
    assert data["early_signs"] == "light spotting, backache, and pelvic pressure."