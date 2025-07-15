import sys
from flask import Flask, jsonify, request
from api.model.job import Job, Language, JobStatus
app = Flask(__name__)

jobs = []

@app.route("/")
def ping():
    return "I am alive!"

@app.route("/jobs", methods=['POST'])
def submit_command():
    new_job = Job.to_dict(None,job_details=request.get_json())
    jobs.append(new_job)
    return '', 200

@app.route("/jobs")
def get_command_list():
    return f'{jobs}', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)