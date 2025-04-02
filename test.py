import requests
import json

# Ваш API-ключ OpenRouter
OPENROUTER_API_KEY = "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"

def process_with_openrouter(text):
    """Отправляет текст в OpenRouter API и возвращает ответ."""
    if not text.strip():
        print("Ошибка: текст для обработки пустой.")
        return "Текст для обработки пустой."
    
    try:
        print("Отправка запроса в OpenRouter API...")
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENROUTER_API_KEY}"
        }
        data = {
            "model": "deepseek/deepseek-v3-base:free",
            "messages": [
                {
                    "role": "user",
                    "content": text
                }
            ]
        }
        
        # Отправляем POST-запрос
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Проверяем наличие ошибок HTTP
        
        # Обрабатываем ответ
        result = response.json()
        print("Полный ответ от API:", result)
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при обращении к OpenRouter API: {e}")
        return "Ошибка при обработке текста нейросетью."

# Пример использования
if __name__ == "__main__":
    text = "в чем смысл жизни"
    response = process_with_openrouter(text)
    print("Ответ от нейросети:")
    print(response)