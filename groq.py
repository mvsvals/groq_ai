import datetime
from groq import Groq
import requests

client = Groq(
    api_key='YOUR-API-KEY-HERE',
)

headers = {
    "Authorization": f"Bearer {client.api_key}",
    "Content-Type": "application/json"
}

current_model = None
response = requests.get("https://api.groq.com/openai/v1/models", headers=headers)
available_models = response.json()
model_ids = [item['id'] for item in available_models['data']]

while not current_model:
    print('\n'.join(model_ids))
    current_model = input('Please input one of the models above:')
    if current_model not in model_ids:
        if current_model.lower() in ['exit', 'quit']:
            print('Goodbye! 👋')
            exit()
        else:
            print('Incorrect input! Make sure you type the name of model correctly.')
            current_model = None
    else:
        print(f'You\'ve selected {current_model}. Proceeding...')


def get_ai_response(user_input):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {'role': 'user', 'content': user_input}
            ],
            model=current_model,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f'Error: {e}'


with open('log.txt', 'a') as log_file:
    while True:
        user_input = input('You: ')
        if user_input.lower() in ['exit', 'quit']:
            print('Goodbye! 👋')
            break
        response = get_ai_response(user_input)
        print("AI: " + response)
        current_time = datetime.datetime.now().strftime('%c')
        log_file.write(f'[{current_time}] User: ' + user_input + '\n' + 'Response: ' + response + '\n')