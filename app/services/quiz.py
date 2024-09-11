import re
import json
import google.generativeai as genai
from app.config.settings import get_settings


settings = get_settings()
genai.configure(api_key=settings.GOOGLE_KEY)


def create_output(text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt1 = "Wygeneruj test sprawdzające wiedze z podanego tekstu: "
    prompt2 = 'Umieść test 5 pytań, odpowiedzi i poprawną odpowiedz w nastepujący sposób [{"pytanie":..., "a":..., "b":..., "c":..., "d":..., "poprawna_odpowiedz":...}, {"pytanie":.... etc}... etc]'
    response = model.generate_content(prompt1+text+prompt2)
    return response.text


def parse_quiz(quiz_text):
    text = quiz_text.replace("\n", "")
    pattern = r'\[(.*?)\]'
    match = re.search(pattern, text, re.DOTALL)
    quiz = json.loads(match.group(0))
    questions, correct_answers = split_json(quiz)
    return questions, correct_answers


def split_json(json_data):
    json_answers = {}
    for i, question in enumerate(json_data, start=1):
        json_answers[f"{i}"] = question.pop("poprawna_odpowiedz")
    return json_data, json_answers