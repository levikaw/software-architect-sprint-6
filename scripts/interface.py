from flask import Flask, request, jsonify
from rag import get_response

app = Flask(__name__)

@app.route('/messages', methods=['POST'])
def send_message():
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "query key are required"}), 400

    enable_thinking = False
    search_deep = 10

    if 'enable_thinking' in data:
        try:
            enable_thinking = bool(data['enable_thinking'])
        except:
            pass

    if 'search_deep' in data:
        try:
            search_deep = int(data['search_deep'])
        except:
            pass

    message = get_response(query=data['query'], enable_thinking=enable_thinking, search_deep=search_deep)

    return jsonify(message), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
