import redis
import json
from flask import Flask, jsonify, request
from model.job import Language, JobStatus, to_request, to_job, BashJob

app = Flask(__name__)

jobs = []
redis_client = redis.Redis()

@app.route("/")
def ping():
    return "I am alive!"

@app.route("/jobs", methods=['POST'])
def submit_command():
    new_job = to_request(job_details=request.get_json())
    jobs.append(new_job)
    redis_client.set(f"{new_job.id}", json.dumps(new_job.to_dict()))
    return f'created: {new_job.id}', 200

@app.route("/job/<job_id>", methods=['GET'])
def get_job(job_id):
    key = job_id
    job_raw_data = redis_client.get(key)
    job_data = json.loads(job_raw_data)
    return jsonify(job_data), 200

@app.route("/execute/<job_id>", methods=['GET'])
def execute_job(job_id):
    return_code = 404
    key = job_id
    job_raw_data = redis_client.get(key)
    job_data = json.loads(job_raw_data)
    dummy, return_code = to_job(job_data)
    return 200
    

@app.route("/jobs")
def get_command_list():
    job_id_list = []
    for job in jobs:
        job_id_list.append(job.id)
    return f'{job_id_list}', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)