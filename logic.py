import pyautogui  # Для работы с координатами мыши и экраном
from PIL import ImageGrab  # Для создания снимков экрана
import pytesseract  # Для распознавания текста
import os  # Для работы с файловой системой
import time  # Для работы с временными метками
import tkinter as tk  # Для создания графического интерфейса
from openai import OpenAI  # Для работы с OpenRouter API
import json  # Для работы с JSON

# Укажите путь к исполняемому файлу Tesseract, если он не добавлен в PATH
pytesseract.pytesseract.tesseract_cmd = r"C:\\program Files\\Tesseract-OCR\\tesseract.exe"

# Папка для сохранения изображений
output_folder = "screenshots"
os.makedirs(output_folder, exist_ok=True)

# Ваш API-ключ OpenRouter
OPENROUTER_API_KEY = "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"

# Создаем клиент OpenAI для работы с OpenRouter API
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

def capture_area():
    # Функция для выделения области с помощью графического интерфейса
    def on_mouse_press(event):
        nonlocal start_x, start_y
        start_x, start_y = event.x, event.y

    def on_mouse_drag(event):
        canvas.coords(rect, start_x, start_y, event.x, event.y)

    def on_mouse_release(event):
        nonlocal left, top, right, bottom
        left = min(start_x, event.x)
        top = min(start_y, event.y)
        right = max(start_x, event.x)
        bottom = max(start_y, event.y)
        root.destroy()

    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-alpha", 0.3)
    root.configure(background="black")

    canvas = tk.Canvas(root, cursor="cross", bg="black", highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    start_x = start_y = left = top = right = bottom = 0
    rect = canvas.create_rectangle(0, 0, 0, 0, outline="white", width=4)

    canvas.bind("<ButtonPress-1>", on_mouse_press)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_release)

    root.mainloop()

    if left == right or top == bottom:
        print("Ошибка: выделенная область имеет нулевую ширину или высоту. Повторите выделение.")
        return

    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(output_folder, f"screenshot_{timestamp}.png")
    screenshot.save(file_path, "PNG")
    print(f"Изображение сохранено: {file_path}")

    # Распознаем текст с изображения
    text = extract_text(file_path)

    # Отправляем текст в OpenRouter API и получаем ответ
    if text.strip():
        response = process_with_openrouter(text)
        print("Ответ от нейросети:")
        print(response)
    else:
        print("Текст не распознан.")

def extract_text(image_path):
    """Распознает текст с изображения."""
    try:
        # Указываем несколько языков для распознавания (русский и английский)
        text = pytesseract.image_to_string(image_path, lang="rus+eng")
        print("Распознанный текст:")
        print(text)
        return text
    except Exception as e:
        print(f"Ошибка при распознавании текста: {e}")
        return ""

def process_with_openrouter(text):
    """Отправляет текст в OpenRouter API и возвращает ответ."""
    if not text.strip():
        print("Ошибка: текст для обработки пустой.")
        return "Текст для обработки пустой."
    
    try:
        print("Отправка запроса в OpenRouter API...")
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://example.com",  # Optional. Site URL for rankings on openrouter.ai.
                "X-Title": "Image Analysis App",  # Optional. Site title for rankings on openrouter.ai.
            },
            extra_body={},
            model="qwen/qwen2.5-vl-3b-instruct:free",
            messages=[
                {
                    "role": "user",
                    "content": [{"type": "text", "text": text}]
                }
            ],
        )
        print("Запрос успешно выполнен.")
        print()
        #print("Полный ответ от API:", completion)
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Ошибка при обращении к OpenRouter API: {e}")
        return "Ошибка при обработке текста нейросетью."

def main():
    root = tk.Tk()
    root.title("Скриншотер")

    start_button = tk.Button(root, text="Начать выделение", command=capture_area, width=20, height=2)
    start_button.pack(pady=10)

    exit_button = tk.Button(root, text="Выход", command=root.destroy, width=20, height=2)
    exit_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()