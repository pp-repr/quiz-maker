from g4f.client import Client

async def create_quiz(text):
    client = Client()
    quiz = client.chat.completions.create(
                                model="gpt-3.5-turbo",
                                messages=[{"role": "user", "content": text}])
    return quiz.choices[0].message.content