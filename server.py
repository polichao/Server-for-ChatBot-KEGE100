from flask import Flask, request, jsonify
from flask_cors import CORS
import redis
import json

app = Flask(__name__)

# Настройка CORS: разрешаем запросы со всех доменов
CORS(app)

redis_url = 'redis://red-cl0jd2c8s0fs73csl1e0:6379'
redis_client = redis.Redis.from_url(redis_url, decode_responses=True)
@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        key = request.args.get('key')
        if key:
            # Retrieve the JSON string from Redis
            value_json = redis_client.get(key)

            if value_json:
                # Decode the JSON string to a dictionary
                value_dict = json.loads(value_json)
                return jsonify(value_dict)
            else:
                return jsonify({'error': 'Key not found'}), 404
        else:
            return jsonify({'error': 'Missing key parameter'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/set_data', methods=['POST'])
def set_data():
    try:
        data = request.get_json()
        key = data.get('key')
        value = data.get('value')

        if key and value:
            # Serialize the value (nested dictionary) to a JSON string
            json_value = json.dumps(value)

            # Store the JSON string in Redis
            redis_client.set(key, json_value)

            return jsonify({'success': True}), 200
        else:
            return jsonify({'error': 'Missing key or value parameters'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
