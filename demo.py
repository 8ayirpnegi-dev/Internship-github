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

"""import streamlit as st
import pandas as pd
import math
from io import StringIO
from datetime import datetime

st.set_page_config(page_title="Internship Recommendation Engine", layout="wide")

# ----------------------- Sample dataset -----------------------
SAMPLE_DATA = [
    {
        "id": 1,
        "title": "Data Analyst Intern",
        "company": "ABC Pvt Ltd",
        "location": "Remote",
        "description": "Work on cleaning datasets, creating dashboards and exploratory analysis.",
        "skills": "Excel, SQL, PowerBI, Data Visualization, Python"
    },
    {
        "id": 2,
        "title": "Machine Learning Intern",
        "company": "XYZ Tech",
        "location": "Bengaluru, India",
        "description": "Model prototyping, feature engineering, and experimentation.",
        "skills": "Python, Pandas, Scikit-Learn, TensorFlow, ML"
    },
    {
        "id": 3,
        "title": "Frontend Intern",
        "company": "DesignHub",
        "location": "Hyderabad, India",
        "description": "Build responsive UI components and help with accessibility.",
        "skills": "HTML, CSS, JavaScript, React, Tailwind"
    },
    {
        "id": 4,
        "title": "Backend Intern",
        "company": "CloudWorks",
        "location": "Remote",
        "description": "Work on REST APIs, databases and deployment pipelines.",
        "skills": "Python, Django, REST, PostgreSQL, Docker"
    },
    {
        "id": 5,
        "title": "Product Management Intern",
        "company": "FinServe",
        "location": "Mumbai, India",
        "description": "Assist PMs with requirement gathering and stakeholder communication.",
        "skills": "Communication, Excel, SQL, Wireframing"
    },
]

# ----------------------- Utility functions -----------------------

def normalize_skill_text(text: str):
    """Lowercase, split by comma/semicolon/newline/space and strip."""
    if not isinstance(text, str):
        return []
    tokens = []
    for part in text.replace(';', ',').replace('\n', ',').split(','):
        s = part.strip().lower()
        if s:
            tokens.append(s)
    return tokens


def compute_score(candidate_skills, internship_skills, description_text, user_keywords=[]):
    """Simple scoring: intersection over union for skills + small boost for keyword matches in title/description.
    Returns float score between 0 and 1.
    """
    c_set = set([s for s in candidate_skills])
    i_set = set([s for s in internship_skills])
    if not i_set:
        skill_score = 0.0
    else:
        inter = c_set.intersection(i_set)
        union = c_set.union(i_set)
        # if user provided no skills, fallback to description similarity via keywords
        if not c_set:
            skill_score = 0.0
        else:
            skill_score = len(inter) / len(union)

    keyword_boost = 0.0
    desc = (description_text or '').lower()
    for kw in user_keywords:
        if not kw:
            continue
        if kw.lower() in desc:
            keyword_boost += 0.06

    # clamp
    score = min(1.0, skill_score + keyword_boost)
    return round(score, 4)


# ----------------------- App layout -----------------------

st.title("🚀 Internship Recommendation Engine")
st.write("Enter your skills and optional filters to get recommended internships ranked by relevance.")

col1, col2 = st.columns([2, 1])

with col1:
    skills_input = st.text_area("Your skills (comma-separated)", placeholder="e.g. Python, SQL, React, Excel")
    keywords_input = st.text_input("Optional keywords (boost matches if present in description/title)", placeholder="e.g. dashboard, computer vision")
    uploaded = st.file_uploader("Upload internships CSV (optional). Columns expected: title,company,location,description,skills", type=["csv"])
    sample_button = st.button("Load sample internships")

with col2:
    role_filter = st.text_input("Role/title filter (optional)")
    location_filter = st.text_input("Location filter (optional)")
    company_filter = st.text_input("Company filter (optional)")
    top_k = st.slider("Show top K results", min_value=3, max_value=50, value=10)

# Load dataset
if uploaded is not None:
    try:
        df_uploaded = pd.read_csv(uploaded)
        # ensure required columns
        needed = {"title", "company", "location", "description", "skills"}
        if not needed.issubset(set(df_uploaded.columns.str.lower())):
            # try to normalize header case
            df_uploaded.columns = [c.lower() for c in df_uploaded.columns]
            if not needed.issubset(set(df_uploaded.columns)):
                st.error("CSV missing one of required columns: title,company,location,description,skills")
                st.stop()
        df = df_uploaded.rename(columns={c: c.lower() for c in df_uploaded.columns})
        df = df.reset_index(drop=True)
    except Exception as e:
        st.error(f"Failed to parse CSV: {e}")
        st.stop()
else:
    df = pd.DataFrame(SAMPLE_DATA)

# Preprocess dataset
if 'skills' not in df.columns:
    st.error('Dataset has no skills column.')
    st.stop()

df['skills_list'] = df['skills'].apply(normalize_skill_text)

# Parse user skills and keywords
user_skills = normalize_skill_text(skills_input)
user_keywords = [k.strip().lower() for k in keywords_input.split(',') if k.strip()] if keywords_input else []

# Filter by title/location/company if provided
if role_filter:
    df = df[df['title'].str.lower().str.contains(role_filter.lower(), na=False)]
if location_filter:
    df = df[df['location'].str.lower().str.contains(location_filter.lower(), na=False)]
if company_filter:
    df = df[df['company'].str.lower().str.contains(company_filter.lower(), na=False)]

# Compute scores
results = []
for idx, row in df.iterrows():
    score = compute_score(user_skills, row['skills_list'], f"{row.get('title','')} {row.get('description','')}", user_keywords)
    results.append({
        'id': row.get('id', idx),
        'title': row.get('title',''),
        'company': row.get('company',''),
        'location': row.get('location',''),
        'description': row.get('description',''),
        'skills': row.get('skills',''),
        'score': score
    })

res_df = pd.DataFrame(results).sort_values('score', ascending=False)

st.markdown("---")

left, right = st.columns([3, 1])

with left:
    st.subheader(f"Top {min(top_k, len(res_df))} matches")
    if res_df.empty:
        st.info("No internships found with the current filters. Try removing filters or load sample data.")
    else:
        for _, r in res_df.head(top_k).iterrows():
            st.markdown(f"**{r['title']}** — {r['company']} \| {r['location']}")
            st.write(r['description'])
            st.write(f"**Required skills:** {r['skills']}")
            st.progress(r['score'])
            st.write(f"Match score: {r['score']}")
            st.markdown("---")

with right:
    st.subheader("Controls & Export")
    if st.button("Export top results as CSV"):
        out = res_df.head(top_k).to_csv(index=False)
        st.download_button("Download CSV", data=out, file_name=f"internship_matches_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", mime='text/csv')

    st.write("\n")
    st.write("**Tips to improve matches:**")
    st.write("- Add more specific skills (e.g., 'react' instead of 'javascript')")
    st.write("- Use keywords to boost matching on descriptions (e.g., 'dashboard', 'nlp')")
    st.write("- Upload a CSV with a 'skills' column containing comma-separated skills")

st.markdown("---")
st.caption("Prototype built with Streamlit. If you want a React + Flask deployment, or automatic scraping of live internship posts (LinkedIn/Internshala/GitHub Jobs), I can provide that next — note scraping job sites may require respecting their terms of service.")
"""
# ----------------------- End -----------------------
import React, { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { Briefcase, Star } from "lucide-react";

const internships = [
  { title: "Data Analyst Intern", company: "ABC Pvt Ltd", skills: ["Excel", "SQL", "PowerBI"] },
  { title: "ML Intern", company: "XYZ Tech", skills: ["Python", "Machine Learning", "NLP"] },
  { title: "Web Developer Intern", company: "WebWorks", skills: ["HTML", "CSS", "JavaScript", "React"] },
  { title: "UI/UX Intern", company: "DesignPro", skills: ["Figma", "Adobe XD", "Creativity"] },
];

export default function DemoPrototype() {
  const [inputSkills, setInputSkills] = useState("");
  const [results, setResults] = useState([]);

  const handleRecommend = () => {
    const userSkills = inputSkills.split(",").map((s) => s.trim().toLowerCase()).filter(Boolean);
    const recommendations = internships.map((internship) => {
      const internshipSkills = internship.skills.map((s) => s.toLowerCase());
      const matchCount = userSkills.filter((skill) => internshipSkills.includes(skill)).length;
      const score = matchCount / internshipSkills.length;
      return { ...internship, score };
    });

    recommendations.sort((a, b) => b.score - a.score);
    setResults(recommendations);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-100 flex flex-col items-center p-8">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.6 }}
        className="flex flex-col items-center mb-6"
      >
        <Briefcase className="w-12 h-12 text-purple-600 mb-2" />
        <h1 className="text-4xl font-extrabold text-purple-700 text-center">
          Internship Recommendation Demo
        </h1>
        <p className="text-gray-700 text-center mt-2 max-w-md">
          Get personalized internship suggestions based on your skills. Enter your skills and explore!
        </p>
      </motion.div>

      <motion.div
        className="w-full max-w-lg bg-white shadow-2xl rounded-3xl p-6 border border-purple-200"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <Input
          placeholder="Enter your skills (e.g. Python, SQL, React)"
          value={inputSkills}
          onChange={(e) => setInputSkills(e.target.value)}
          className="mb-4"
        />
        <Button onClick={handleRecommend} className="w-full bg-purple-600 hover:bg-purple-700 text-white">
          Get Recommendations
        </Button>
      </motion.div>

      <div className="w-full max-w-lg mt-6 space-y-4">
        {results.length > 0 && results.map((r, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
          >
            <Card className="hover:shadow-xl transition duration-300">
              <CardContent className="p-5">
                <div className="flex justify-between items-center">
                  <h2 className="text-xl font-bold text-purple-700 flex items-center gap-2">
                    <Star className="w-5 h-5 text-yellow-500" /> {r.title}
                  </h2>
                  <span className="text-sm font-medium bg-purple-100 text-purple-800 px-3 py-1 rounded-full">
                    {(r.score * 100).toFixed(0)}% Match
                  </span>
                </div>
                <p className="text-gray-600 mt-1">Company: {r.company}</p>
                <p className="text-sm mt-1 text-gray-700">Required Skills: {r.skills.join(", ")}</p>
                <div className="mt-3 h-3 bg-gray-200 rounded-full overflow-hidden">
                  <motion.div
                    className="bg-gradient-to-r from-green-400 to-green-600 h-3"
                    initial={{ width: 0 }}
                    animate={{ width: `${r.score * 100}%` }}
                    transition={{ duration: 0.5 }}
                  ></motion.div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>
    </div>
  );
}




