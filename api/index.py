import redis
import json
from flask import Flask, jsonify, request
from model.job import Language, JobStatus, to_request, to_job, BashJob, PythonJob

app = Flask(__name__)

jobs = []
redis_client = redis.Redis()

# Make sure you don't forget, this needs to work with a worker agent, and needs logging functionality

@app.route("/")
def ping():
    return 'I am alive', 200

# More context would be nice but w/e
# Remember to add return code
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

# Remember to add return code
@app.route("/job/<job_id>", methods=['GET'])
def get_job(job_id):
    key = job_id
    job_raw_data = redis_client.get(key)
    job_data = json.loads(job_raw_data)
    return jsonify(job_data), 200

# Remember to add return code
@app.route("/jobs", methods=['POST'])
def add_job():
    new_job = to_request(job_details=request.get_json())
    jobs.append(new_job)
    redis_client.set(f"{new_job.id}", json.dumps(new_job.to_dict()))
    return f'created: {new_job.id}', 200

# Add handling for if you don't find the job, e.g. 404
# Remember to add return code
@app.route("/execute/<job_id>", methods=['GET'])
def execute_job(job_id):
    return_code = 404
    key = job_id
    job_raw_data = redis_client.get(key)
    job_data = json.loads(job_raw_data)
    job_obj, exit_code = to_job(job_data)
    state = job_obj.run()
    if state == JobStatus.COMPLETE:
        return_code = 200
        return f'completed: {job_obj.id}', return_code
    elif state == JobStatus.IN_PROGRESS:
        return_code = 200
        return f'started: {job_obj.id}', return_code
    else:
        return_code = 200
        return f'{state.name}, ID: {job_obj.id}', return_code

@app.route("/status/<job_id>", methods=['GET'])
def get_job_status(job_id):
    job_raw_data = redis_client.get(job_id)
    if not job_raw_data:
        return f'not found: {job_id}', 404

    job_data = json.loads(job_raw_data)
    status = job_data.get('status')
    return f'{status}', 200


# Delete a job from redis
@app.route("/job/<job_id>", methods=['DELETE'])
def delete_job(job_id):
    """Remove the job with the given ID from the data store."""
    deleted = redis_client.delete(job_id)
    if deleted:
        return f'deleted: {job_id}', 200
    return f'not found: {job_id}', 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)