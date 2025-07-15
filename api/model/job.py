import uuid
import datetime
import json
from enum import Enum

class JobStatus(Enum):
    QUEUED = 1
    IN_PROGRESS = 2
    COMPLETE = 3
    ERROR = 4
    TIMEOUT = 5

class Language(Enum):
    PYTHON = 1
    BASH = 2

class Job(object):
    def __init__(self, language, script, retries):
        self.language = language
        self.script = script
        self.retries = retries

        self.id = uuid.uuid4()
        self.status = JobStatus.QUEUED
        self.created_at = datetime.datetime.now()
        self.started_at = None
        self.finished_at = None
        self.exit_code = 1
        self.stdout = ""
        self.stderr = ""
        self.timeout = 60 

    def run(self):
        raise NotImplementedError()
    
    def to_dict(self, job_details):
        job_language = job_details["language"]
        job_script = job_details["script"]
        job_retries = job_details["retries"]
        return Job(job_language, job_script, job_retries)
    
