# -*- coding: utf-8 -*-

import requests
import time
import json

# Укажите ваш API-ключ и ссылку на аудиофайл в Object Storage.
key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# или загрузите его из yaml файла
with open('api-key.yaml', 'r') as apif:
    key = load(apif)['secret']

filelink = 'https://storage.yandexcloud.net/speech-test-bucket/lection01.opus'

POST = "https://transcribe.api.cloud.yandex.net/speech/stt/v2/longRunningRecognize"

body ={
    "config": {
        "specification": {
            "languageCode": "ru-RU"
        }
    },
    "audio": {
        "uri": filelink
    }
}

# Если вы хотите использовать IAM-токен для аутентификации, замените Api-Key на Bearer.

header = {'Authorization': 'Api-Key {}'.format(key)}
# header = {'Authorization': 'Bearer {}'.format(key)}

# Отправить запрос на распознавание.
req = requests.post(POST, headers=header, json=body)
data = req.json()
print(data)

jid = data.get('id')
# jid = data.get('details')[0].get('requestId')

# Запрашивать на сервере статус операции, пока распознавание не будет завершено.
while True:

    time.sleep(1)

    GET = "https://operation.api.cloud.yandex.net/operations/{id}"
    request = requests.get(GET.format(id=jid), headers=header)
    response = request.json()
    print(response)
    if response['done']: break
    print("Not ready")

# Показать полный ответ сервера в формате JSON.
print("Response:")
print(json.dumps(response, ensure_ascii=False, indent=2))

# Показать только текст из результатов распознавания.
print("Text chunks:")
for chunk in response['response']['chunks']:
    print(chunk['alternatives'][0]['text'])

# Сохранить распознанный текст из резу льтатов распознавания.
print("Text file")
i = 0
with open('lection01_for_say.txt', 'w+') as f:
    for chunk in response['response']['chunks']:
        if i % 2:
            f.write(chunk['alternatives'][0]['text'])
            f.write('.')
            f.write(' ')
            f.write('\n')
        i += 1
