def match_resume_to_job(resume_data, job_description):
    skills = resume_data.get("resume_intelligence", {}).get("skills", [])

    jd = job_description.lower()

    matched = []
    missing = []

    for skill in skills:
        if skill.lower() in jd:
            matched.append(skill)
        else:
            missing.append(skill)

    score = int((len(matched) / len(skills)) * 100) if skills else 0

    return {
        "match_score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "suggestion": "Improve missing skills to increase match score."
    }