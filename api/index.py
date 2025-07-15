from flask import Flask, jsonify, request

app = Flask(__name__)

jobs = [
    {   'id': "1",
        'command': 'ls',
        'status': 'queued'
    }
]

@app.route("/")
def ping():
    return "I am alive!"

@app.route("/jobs", methods=['POST'])
def submit_command():
    jobs.append(request.get_json())
    return '', 200

@app.route("/jobs")
def get_command_list():
    return f'{jobs}', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)