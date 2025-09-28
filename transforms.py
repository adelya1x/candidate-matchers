from core.domain import Resume, Candidate
from typing import Tuple
from functools import reduce
import re

def normalize_text(text: str) -> str:
    return re.sub(r'\W+', ' ', text.lower()).strip()

def parse_resume(r: Resume) -> dict:
    text = normalize_text(r.text)
    skills = tuple(re.findall(r'\b(python|java|sql|docker|react|node|c\+\+|git|linux)\b', text))
    exp = int(re.search(r'(\d+)\s+years', text).group(1)) if re.search(r'(\d+)\s+years', text) else 0
    edu = 'bachelor' if 'bachelor' in text else 'master' if 'master' in text else 'unknown'
    loc = re.search(r'\b(almaty|astana|moscow|spb)\b', text)
    return {'skills': skills, 'exp': exp, 'edu': edu, 'loc': loc.group(0) if loc else 'unknown'}

def filter_by_skill(cands: Tuple[Candidate, ...], skill: str) -> Tuple[Candidate, ...]:
    return tuple(c for c in cands if skill in c.skills)

def avg_exp(cands: Tuple[Candidate, ...]) -> float:
    total = reduce(lambda acc, c: acc + c.exp_years, cands, 0)
    return round(total / len(cands), 2) if cands else 0.0
