from openai import OpenAI 
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)
text = "в чем смысл жизни"
def process_with_openrouter(text):
    """Отправляет текст в OpenRouter API и возвращает ответ."""
    if not text.strip():
        print("Ошибка: текст для обработки пустой.")
        return "Текст для обработки пустой."
    try:
        print("Отправка запроса в OpenRouter API...")
        completion = client.chat.completions.create(
            #
            extra_body={},
            model="deepseek/deepseek-v3-base:free",
            messages=[
                {
                    "role": "user",
                    "content": str(text)
                }
            ]
        )
        print("Запрос успешно выполнен.")
        print("Полный ответ от API:", completion)
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Ошибка при обращении к OpenRouter API: {e}")
        return "Ошибка при обработке текста нейросетью."
    
    
if text.strip():
        response = process_with_openrouter(text)
        print("Ответ от нейросети:")
        print(response)
else:
        print("Текст не распознан.")