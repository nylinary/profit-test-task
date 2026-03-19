from dataclasses import dataclass
from typing import Optional


@dataclass
class JobState:
    job_id: str
    product: str
    status: str
    progress: Optional[int]
    updated_at: str


class JobStorage:
    def __init__(self):
        self._storage: dict[str, JobState] = {}

    def save(self, state: JobState) -> None:
        self._storage[state.job_id] = state

    def get(self, job_id: str) -> Optional[JobState]:
        return self._storage.get(job_id)
