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
    return 'created', 200

@app.route("/jobs")
def get_command_list():
    job_id_list = []
    for job in jobs:
        job_id_list.append(job.id)
    return f'{job_id_list}', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)