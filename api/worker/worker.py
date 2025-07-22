from api.model.job import PythonJob, BashJob, Language
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
        print()
    elif lang == Language.PYTHON.name:
        print()
    else:
        print()
