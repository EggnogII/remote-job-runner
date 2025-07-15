from flask import Flask, jsonify, request

app = Flask(__name__)

commands = [
    { 'command': 'ls'}
]

@app.route("/")
def ping():
    return "I am alive!"

@app.route("/submit", methods=['POST'])
def submit_command():
    commands.append(request.get_json())
    return '', 200

@app.route("/command_list")
def get_command_list():
    return f'{commands}', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)