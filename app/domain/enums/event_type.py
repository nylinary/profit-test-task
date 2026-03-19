from enum import Enum


class EventType(str, Enum):
    JOB_STARTED = "job.started"
    JOB_PROGRESS = "job.progress"
    JOB_FINISHED = "job.finished"
