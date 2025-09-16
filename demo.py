import React, { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";

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
    <div className="min-h-screen bg-gray-50 flex flex-col items-center p-8">
      <motion.h1
        className="text-3xl font-bold mb-4 text-center"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        Internship Recommendation Demo
      </motion.h1>

      <div className="w-full max-w-lg bg-white shadow-lg rounded-2xl p-6">
        <Input
          placeholder="Enter your skills (e.g. Python, SQL, React)"
          value={inputSkills}
          onChange={(e) => setInputSkills(e.target.value)}
          className="mb-4"
        />
        <Button onClick={handleRecommend} className="w-full">
          Get Recommendations
        </Button>
      </div>

      <div className="w-full max-w-lg mt-6">
        {results.length > 0 && results.map((r, idx) => (
          <motion.div
            key={idx}
            className="mb-4"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <Card>
              <CardContent className="p-4">
                <h2 className="text-xl font-semibold">{r.title}</h2>
                <p className="text-gray-600">Company: {r.company}</p>
                <p className="text-sm mt-1">Required Skills: {r.skills.join(", ")}</p>
                <div className="mt-2 h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div className="bg-green-500 h-2" style={{ width: `${r.score * 100}%` }}></div>
                </div>
                <p className="text-sm mt-1 font-medium">Match: {(r.score * 100).toFixed(0)}%</p>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>
    </div>
  );
}