import requests
import base64
import time
import os
from dotenv import load_dotenv


load_dotenv()


def yandex_lite_request(prompt):
    prompt = {
        "modelUri": "gpt://b1g7pshk305408d7kssj/yandexgpt",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "100",
            "reasoningOptions": {
                "mode": "DISABLED"
            }
        },
        "messages": [
            {
            "role": "system",
            "text": "Сгенерируй по описанию короткое рекламное объявление"
            },
            {
            "role": "user",
            "text": prompt
            }
    ]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-key {os.getenv('YANDEX_LITE_API_KEY')}"
    }

    response = requests.post('https://llm.api.cloud.yandex.net/foundationModels/v1/completion', headers=headers, json=prompt)
    response.encoding = 'utf-8'

    return response.json()["result"]["alternatives"][0]["message"]["text"]

def yandex_art_request(prompt, seed):
    request_body = {
        "modelUri": "art://b1g7pshk305408d7kssj/yandex-art/latest",
        "generationOptions": {
            "seed": seed,
            "aspectRatio": {
                "widthRatio": "1",
                "heightRatio": "1"
            }
        },
        "messages": [
            {
                "weight": "1",
                "text": "Сгенерируй рекламный баннер для размещения на сайте: " + prompt
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-key {os.getenv('YANDEX_ART_API_KEY')}"
    }

    create_request = requests.post(
        'https://llm.api.cloud.yandex.net/foundationModels/v1/imageGenerationAsync',
        headers=headers,
        json=request_body
    )

    operation_id = create_request.json()["id"]

    while True:
        time.sleep(5)
        done_request = requests.get(
            f'https://llm.api.cloud.yandex.net/operations/{operation_id}',
            headers=headers
        )

        if done_request.json().get('done'):
            image_data = done_request.json()['response']['image']
            file_name = f'{operation_id}.jpeg'

            with open(f'images/{file_name}', 'wb') as file:
                file.write(base64.b64decode(image_data))

            return {"filename": operation_id}  # <-- Возвращаем как словарь
