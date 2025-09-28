from dataclasses import dataclass
from typing import Tuple, Dict

@dataclass(frozen=True)
class Candidate:
    id: str
    name: str
    skills: Tuple[str, ...]
    exp_years: int
    location: str
    edu: str

@dataclass(frozen=True)
class Resume:
    id: str
    cand_id: str
    text: str
    parsed: Dict

@dataclass(frozen=True)
class Job:
    id: str
    title: str
    skills_req: Tuple[str, ...]
    exp_req: int
    location: str
