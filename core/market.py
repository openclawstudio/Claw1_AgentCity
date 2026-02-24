from typing import List, Dict
from .models import Job

class Marketplace:
    def __init__(self):
        self.job_board: List[Job] = []
        self.resource_prices: Dict[str, float] = {"food": 10.0, "energy": 5.0}

    def post_job(self, job: Job):
        self.job_board.append(job)

    def get_available_jobs(self) -> List[Job]:
        return self.job_board

    def remove_job(self, job_id: str):
        self.job_board = [j for j in self.job_board if j.job_id != job_id]