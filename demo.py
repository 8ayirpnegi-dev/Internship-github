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








