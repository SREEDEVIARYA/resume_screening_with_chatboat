from agents.skill_extraction_agent import SkillExtractionAgent


class JobAnalyzerAgent:

    def __init__(self):

        self.skill_agent = SkillExtractionAgent()

    def run(self, job_description):

        required_skills = self.skill_agent.run(
            job_description
        )

        return {
            "job_description": job_description,
            "required_skills": required_skills,
            "total_required_skills": len(required_skills)
        }