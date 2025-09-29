from core.filters import by_location, by_exp_range, by_skill
from core.recursion import expand_resume_fields
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.domain import Candidate, Resume
from core.transforms import normalize_text, parse_resume, filter_by_skill, avg_exp


def test_normalize_text():
    assert normalize_text("Python, SQL!") == "python sql"


def test_parse_resume():
    r = Resume(
        id="1",
        cand_id="1",
        text="Python developer with 3 years in Almaty. Bachelor degree.",
        parsed={},
    )
    parsed = parse_resume(r)
    assert parsed["exp"] == 3
    assert "python" in parsed["skills"]
    assert parsed["edu"] == "bachelor"
    assert parsed["loc"] == "almaty"


def test_filter_by_skill():
    c1 = Candidate(
        id="1",
        name="A",
        skills=("python",),
        exp_years=2,
        location="almaty",
        edu="bachelor",
    )
    c2 = Candidate(
        id="2", name="B", skills=("java",), exp_years=3, location="astana", edu="master"
    )
    result = filter_by_skill((c1, c2), "python")
    assert len(result) == 1
    assert result[0].name == "A"


def test_avg_exp():
    c1 = Candidate(id="1", name="A", skills=(), exp_years=2, location="", edu="")
    c2 = Candidate(id="2", name="B", skills=(), exp_years=4, location="", edu="")
    assert avg_exp((c1, c2)) == 3.0


def test_normalize_text_empty():
    assert normalize_text("") == ""


def test_filter_by_skill_not_found():
    c1 = Candidate(
        id="1",
        name="A",
        skills=("python",),
        exp_years=2,
        location="almaty",
        edu="bachelor",
    )
    c2 = Candidate(
        id="2", name="B", skills=("java",), exp_years=3, location="astana", edu="master"
    )
    result = filter_by_skill((c1, c2), "docker")
    assert result == ()


def test_by_location():
    c = Candidate(1, "A", ("Python",), 3, "Almaty", "BSU")
    assert by_location("Almaty")(c)


def test_by_exp_range():
    c = Candidate(1, "A", ("Python",), 3, "Almaty", "BSU")
    assert by_exp_range(2, 5)(c)


def test_by_skill():
    c = Candidate(1, "A", ("Python", "SQL"), 3, "Almaty", "BSU")
    assert by_skill("sql")(c)


def test_expand_resume_fields():
    r = Resume(1, 1, "text", {"skills": "Python", "exp": "3"})
    assert expand_resume_fields(r, ("skills", "exp")) == ("Python", "3")
