import uuid
import datetime
import json
import tempfile
import os
import subprocess
from enum import Enum
from abc import ABC, abstractmethod


# Some other stuff, we gotta incorporate multiple files for distinction in the module.

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
        elif uppercase_job_language == Language.PYTHON.name:
            return PythonJob(job_language, job_script, job_retries)

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
    if job_details['started_at'] == 'None':
        job_started_at = None
    else:
        job_started_at = datetime.datetime.strptime(job_details['started_at'], date_time_format)
    if job_details['finished_at'] == 'None':
        job_finished_at = None
    else:
        job_finished_at = datetime.datetime.strptime(job_details['finished_at'], date_time_format)
    job_exit_code = job_details['exit_code']
    job_stdout = job_details['stdout']
    job_stderr = job_details['stderr']
    return_job = None
    if job_language == Language.BASH.name:
        bash_job = BashJob.from_data(job_id, job_language, job_script, job_retries, job_status, job_creation_time, job_started_at, job_finished_at, job_exit_code, job_stdout, job_stderr)
        return_job = bash_job
    elif job_language == Language.PYTHON.name:
        return_job = PythonJob.from_data(job_id, job_language, job_script, job_retries, job_status, job_creation_time, job_started_at, job_finished_at, job_exit_code, job_stdout, job_stderr)

    return return_job, 200      

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
    
    @classmethod
    def from_data(cls, job_id, job_language, job_script, job_retries, job_status, job_creation_time, job_start_time, job_end_time, job_exit_code, job_stdout, job_stderr):
        job_data = cls(
            language=job_language,
            script=job_script,
            retries=job_retries,
        )
        job_data.id = job_id
        job_data.status = job_status
        job_data.created_at = job_creation_time
        job_data.started_at = job_start_time
        job_data.finished_at = job_end_time
        job_data.exit_code = job_exit_code
        job_data.stdout = job_stdout
        job_data.stderr = job_stderr

        return job_data

    @classmethod
    def from_dict(cls, job_dict):
        job_data = cls(
            language=job_dict["language"],
            script=job_dict["script"],
            retries=job_dict["retries"]
        )
        job_data.id = job_dict["id"]
        eval_status = job_dict["status"].upper()
        
        if eval_status == JobStatus.QUEUED.name:
            job_data.status = JobStatus.QUEUED
        elif eval_status == JobStatus.IN_PROGRESS.name:
            job_data.status = JobStatus.IN_PROGRESS
        elif eval_status == JobStatus.ERROR.name:
            job_data.status = JobStatus.ERROR
        elif eval_status == JobStatus.COMPLETE.name:
            job_data.status = JobStatus.COMPLETE
        elif eval_status == JobStatus.TIMEOUT.name:
            job_data.status = JobStatus.TIMEOUT
        else:
            job_data.status = None
        
        if job_data.status == None:
            raise KeyError(f"Nonvalid Job Status {eval_status}")

        date_time_format = "%Y-%m-%d %H:%M:%S.%f"
        job_data.created_at = datetime.datetime.strptime(job_dict["created_at"], date_time_format)

        if job_dict["started_at"] == "None":
            job_data.started_at = None
        else:
            job_data.started_at = datetime.datetime.strptime(job_dict["started_at"], date_time_format)

        if job_dict["finished_at"] == "None":
            job_data.finished_at = None
        else:
            job_data.finished_at = datetime.datetime.strptime(job_dict["finished_at"], date_time_format)

        job_data.exit_code = job_dict["exit_code"]
        job_data.stdout = job_dict["stdout"]
        job_data.stderr = job_dict["stderr"]

        return job_data

        

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
class PythonJob(Job):
    def __init__(self, language, script, retries):
        super().__init__(language, script, retries)
    
    @classmethod
    def from_data(cls, id, language, script, retries, status, creation_time, start_time, end_time, exit_code, stdout, stderr):
        job = super().from_data(id, language, script, retries, status, creation_time, start_time, end_time, exit_code, stdout, stderr)
        return job
        
    def run(self):
        if is_complete(self.status):
            return self.status
        self.status = JobStatus.IN_PROGRESS
        self.started_at = datetime.datetime.now()

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp:
            temp.write(self.script)
            temp.flush()
            filename = temp.name
        
        try:
            result = subprocess.run(
                ["python3", filename],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=self.timeout
            )
        except subprocess.TimeoutExpired as timeout_expired:
            self.stderr = str(timeout_expired)
            self.status = JobStatus.TIMEOUT
            self.exit_code = -1
        finally:
            self.finished_at = datetime.datetime.now()
            os.remove(filename)
        return self.status

def is_complete(status: JobStatus):
    if status == JobStatus.COMPLETE:
        return True
    else:
        return False

class BashJob(Job):
    def __init__(self, language, script, retries):
        super().__init__(language, script, retries)

    @classmethod
    def from_data(cls, id, language, script, retries, status, creation_time, start_time, end_time, exit_code, stdout, stderr):
        job = super().from_data(id, language, script, retries, status, creation_time, start_time, end_time, exit_code, stdout, stderr)
        return job

    @classmethod
    def from_dict(cls, job_dict):
        return super().from_dict(job_dict)

    def run(self):
        if is_complete(self.status):
            return self.status
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
        return self.status
