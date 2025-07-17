import uuid
import datetime
import json
from enum import Enum
from abc import ABC, abstractmethod

class JobStatus(Enum):
    QUEUED = 1
    IN_PROGRESS = 2
    COMPLETE = 3
    ERROR = 4
    TIMEOUT = 5

class Language(Enum):
    PYTHON = 1
    BASH = 2

def to_request(job_details):
        job_language = str(job_details["language"])
        job_script = job_details["script"]
        job_retries = job_details["retries"]
        uppercase_job_language = job_language.upper()
        if uppercase_job_language == Language.BASH.name:
            return BashJob(job_language, job_script, job_retries)

def to_job(job_details):
    job_id = job_details['id']
    job_language = job_details['language'].upper()
    job_script = job_details['script']
    job_retries = job_details['retries']
    try:
        job_status = JobStatus[job_details['status']]
    except k as KeyError:
        return None, 500
    date_time_format = "%Y-%m-%d %H:%M:%S.%f"
    job_creation_time = datetime.datetime.strptime(job_details['created_at'], date_time_format)
    print()
    return None, 200      

class Job(ABC):
    def __init__(self, language, script, retries):
        self.language = language
        self.script = script
        self.retries = retries

        self.id = uuid.uuid4().hex
        self.status = JobStatus.QUEUED
        self.created_at = datetime.datetime.now()
        self.started_at = None
        self.finished_at = None
        self.exit_code = 1
        self.stdout = ""
        self.stderr = ""
        self.timeout = 60 

    @abstractmethod
    def run(self):
        pass
    
    def to_dict(self):
        dictionary_to_return = {
            "id": str(self.id),
            "language": self.language,
            "script": self.script,
            "retries": self.retries,
            "status": self.status.name,
            "created_at": str(self.created_at),
            "started_at": str(self.started_at),
            "finished_at": str(self.finished_at),
            "exit_code": self.exit_code,
            "stdout": self.stdout,
            "stderr": self.stderr
        }

        return dictionary_to_return
    
class BashJob(Job):
    def __init__(self, language, script, retries):
        super().__init__(language, script, retries)

    def run(self):
        self.status = JobStatus.IN_PROGRESS
        self.started_at = datetime.datetime.now()

        with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as temp:
            temp.write(self.script)
            temp.flush()
            filename = temp.name
        
        try:
            result = subprocess.run(
                ["bash", filename],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=self.timeout
            )
            self.stdout = result.stdout.decode()
            self.stderr = result.stderr.decode()
            self.exit_code = result.returncode
            if result.returncode == 0:
                self.status = JobStatus.COMPLETE
            else:
                self.status = JobStatus.ERROR
        except subprocess.TimeoutExpired as timeout_expired:
            self.stderr = str(timeout_expired)
            self.status = JobStatus.TIMEOUT
            self.exit_code = -1
        finally:
            self.finished_at = datetime.datetime.now()
            os.remove(filename)