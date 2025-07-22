from model.job import Job,PythonJob, BashJob, Language
import redis
import json

def run_job(job_id):
    redis_client = redis.Redis()
    job_raw_data = redis_client.get(job_id)
    if not job_raw_data:
        return {"Results": "Not Found"}
    
    job_data = json.loads(job_raw_data)
    lang = job_data["language"].upper()

    if lang == Language.BASH.name:
        new_job = BashJob.from_dict(job_data)
    elif lang == Language.PYTHON.name:
        new_job = PythonJob.from_dict(job_data)
    else:
        new_job = None
    
    if not new_job:
        raise KeyError("Unsupported Job Type")
    
    new_job.run()

    redis_client.set(job_id, json.dumps(new_job.to_dict()))
    return {"job_id": job_id, "status": new_job.status}
