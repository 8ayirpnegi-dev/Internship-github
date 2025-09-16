"""# internship_recommendation_app.py

import streamlit as st

# Sample internship data
internships = [
    {"title": "Data Analyst Intern", "company": "ABC Pvt Ltd", "skills": ["Excel", "SQL", "PowerBI"]},
    {"title": "ML Intern", "company": "XYZ Tech", "skills": ["Python", "Machine Learning", "NLP"]},
    {"title": "Web Developer Intern", "company": "WebWorks", "skills": ["HTML", "CSS", "JavaScript", "React"]},
    {"title": "UI/UX Intern", "company": "DesignPro", "skills": ["Figma", "Adobe XD", "Creativity"]},
]

st.title("🎯 Internship Recommendation System")
st.write("Enter your skills below (comma separated) to get personalized recommendations.")

user_input = st.text_input("Your Skills", placeholder="e.g. Python, SQL, Machine Learning")

if st.button("Get Recommendations"):
    if not user_input.strip():
        st.warning("Please enter at least one skill!")
    else:
        user_skills = [s.strip().lower() for s in user_input.split(",") if s.strip()]
        recommendations = []

        for internship in internships:
            internship_skills = [s.lower() for s in internship["skills"]]
            match_count = len(set(user_skills) & set(internship_skills))
            score = match_count / len(internship_skills)
            recommendations.append({**internship, "score": score})

        recommendations.sort(key=lambda x: x["score"], reverse=True)

        st.subheader("🔍 Recommended Internships")
        for rec in recommendations:
            st.write(f"**{rec['title']}** at *{rec['company']}*")
            st.write(f"Required Skills: {', '.join(rec['skills'])}")
            st.progress(rec["score"])
            st.write(f"Match: **{int(rec['score']*100)}%**")
            st.divider()"""

