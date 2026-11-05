from agents.resume_parser_agent import ResumeParserAgent
from agents.candidate_profile_agent import CandidateProfileAgent
from agents.skill_extraction_agent import SkillExtractionAgent
from agents.job_analyzer_agent import JobAnalyzerAgent
from agents.semantic_matching_agent import SemanticMatchingAgent
from agents.scoring_agent import ScoringAgent
from agents.ranking_agent import RankingAgent
from agents.recommendation_agent import RecommendationAgent


class RecruitmentOrchestrator:

    def __init__(self):

        self.parser = ResumeParserAgent()

        self.profile = CandidateProfileAgent()

        self.skill_agent = SkillExtractionAgent()

        self.job_agent = JobAnalyzerAgent()

        self.semantic_agent = SemanticMatchingAgent()

        self.scoring_agent = ScoringAgent()

        self.ranking_agent = RankingAgent()

        self.recommendation_agent = RecommendationAgent()

    def run(self, resume_files, job_description):

        print("Starting recruitment workflow...")

        # Step 1: Analyze job description
        job_data = self.job_agent.run(job_description)

        required_skills = job_data["required_skills"]

        candidates = []

        # Step 2: Process each resume
        for pdf_path in resume_files:

            print("Processing:", pdf_path)

            # Resume Parser Agent
            resume_text = self.parser.run(pdf_path)

            # Candidate Profile Agent
            profile_data = self.profile.run(resume_text)

            # Skill Extraction Agent
            candidate_skills = self.skill_agent.run(
                resume_text
            )

            # Semantic Matching Agent
            semantic_score = self.semantic_agent.run(
                resume_text,
                job_description
            )

            # Scoring Agent
            scores = self.scoring_agent.run(
                candidate_skills,
                required_skills,
                semantic_score
            )

            candidate = {
                **profile_data,
                "filename": pdf_path,
                "skills": candidate_skills,
                **scores
            }

            candidates.append(candidate)

        # Step 3: Rank candidates
        ranked_candidates = self.ranking_agent.run(
            candidates
        )

        # Step 4: Generate recommendations
        for candidate in ranked_candidates:

            recommendation = self.recommendation_agent.run(
                candidate
            )

            candidate.update(recommendation)

        print("Recruitment workflow completed.")

        return ranked_candidates