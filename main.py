import streamlit as st
import json
import sys
import os
import inspect
from collections import Counter

# Добавляем путь к project/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Импортируем функции и сущности
from core.domain import Candidate, Resume, Job
from core.transforms import parse_resume, filter_by_skill, avg_exp, normalize_text

# Загружаем данные
with open("project/data/seed.json", encoding="utf-8") as f:
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

# Overview
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
