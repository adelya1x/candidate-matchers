from collections import Counter
from core.filters import by_location, by_exp_range, by_skill

import sys
import os

sys.path.append(os.path.dirname(__file__))
import streamlit as st
import json
import inspect

# Добавляем путь к project/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.domain import Candidate, Resume, Job
from core.transforms import normalize_text, parse_resume, filter_by_skill, avg_exp

# Загружаем данные
with open("data/seed.json", encoding="utf-8") as f:
    data = json.load(f)

candidates = tuple(Candidate(**c) for c in data["candidates"])
resumes = tuple(Resume(**r) for r in data["resumes"])
jobs = tuple(Job(**j) for j in data["jobs"])

# Парсим резюме
parsed_resumes = tuple(parse_resume(r) for r in resumes)

# Топ-10 навыков
all_skills = [s for r in parsed_resumes for s in r["skills"]]
top_skills = Counter(all_skills).most_common(10)

# Меню
menu = st.sidebar.radio("Меню", ["Overview", "Data", "Functional Core"])


# Собираем все навыки
all_skills = [skill for c in candidates for skill in c.skills]
top_skills = Counter(all_skills).most_common(10)

# Отображаем
st.subheader("Топ-10 навыков среди кандидатов")
for skill, count in top_skills:
    st.write(f"🔹 {skill}: {count}")

if menu == "Overview":
    st.title("📊 Overview")
    st.metric("Total Candidates", len(candidates))
    st.metric("Total Jobs", len(jobs))
    st.metric("Average Experience", avg_exp(candidates))

    st.subheader("Top 10 Skills")
    for skill, count in top_skills:
        st.write(f"{skill}: {count}")

# Data
elif menu == "Data":
    st.title("📁 Data")
    st.subheader("📋 Candidates Preview")
    st.dataframe([c.__dict__ for c in candidates])

    st.subheader("📋 Jobs Preview")
    st.dataframe([j.__dict__ for j in jobs])

    st.subheader("📋 Parsed Resumes")
    st.dataframe(parsed_resumes)

# Functional Core
elif menu == "Functional Core":
    st.title("🧠 Functional Core")
    st.subheader("normalize_text")
    st.code(inspect.getsource(normalize_text))

    st.subheader("parse_resume")
    st.code(inspect.getsource(parse_resume))

    st.subheader("filter_by_skill")
    st.code(inspect.getsource(filter_by_skill))

    st.subheader("avg_exp")
    st.code(inspect.getsource(avg_exp))

# Фильтры
st.sidebar.header("Фильтрация")
city = st.sidebar.text_input("Город")
exp_lo = st.sidebar.slider("Опыт от", 0, 20, 1)
exp_hi = st.sidebar.slider("Опыт до", 0, 20, 10)
skill = st.sidebar.text_input("Навык")

filtered = candidates
if city:
    filtered = list(filter(by_location(city), filtered))
if skill:
    filtered = list(filter(by_skill(skill), filtered))
filtered = list(filter(by_exp_range(exp_lo, exp_hi), filtered))

st.subheader("Результаты фильтрации")
st.dataframe(filtered)
