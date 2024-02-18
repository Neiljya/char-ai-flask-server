import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from characterai import PyCAI

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*", "allow_headers": ["Content-Type"]}})

token = os.getenv('CHARACTER_AI_TOKEN')
char_id = os.getenv('CHARACTER_AI_ID')

client = PyCAI(token)


@app.route('/chat', methods=['POST'])
def chat():
    message = request.json.get('message')
    if not message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        chat = client.chat.get_chat(char_id)
        participants = chat['participants']
        target = participants[0]['user']['username'] if not participants[0]['is_human'] else participants[1]['user'][
            'username']

        data = client.chat.send_message(chat['external_id'], target, message)
        name = data['src_char']['participant']['name']
        text = data['replies'][0]['text']

        return jsonify({'name': name, 'reply': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
