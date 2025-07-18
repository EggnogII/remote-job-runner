import redis
import json
from flask import Flask, jsonify, request
from model.job import Language, JobStatus, to_request, to_job, BashJob, PythonJob

app = Flask(__name__)

jobs = []
redis_client = redis.Redis()

@app.route("/")
def ping():
    return "I am alive!"

@app.route("/jobs", methods=['POST'])
def add_job():
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
    job_obj, return_code = to_job(job_data)
    state = job_obj.run()
    if state == JobStatus.COMPLETE:
        return f'completed: {job_obj.id}', 200
    elif state == JobStatus.IN_PROGRESS:
        return f'started: {job_obj.id}', 200
    else:
        return f'{state.name}, ID: {job_obj.id}', 200
    
# More context would be nice but w/e
@app.route("/jobs")
def get_jobs():
    keys = redis_client.keys()
    return_dict = {}
    for key in keys:
        job_raw_data = redis_client.get(key)
        job_data = json.loads(job_raw_data)
        job_obj, return_code = to_job(job_data)
        return_dict[job_obj.id] = job_obj.script
    
    return f'{return_dict}', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)