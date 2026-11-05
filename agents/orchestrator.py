
class RecruitmentOrchestrator:

    def __init__(self):

        # Lightweight initialization only
        self._parser = None
        self._profile = None
        self._skill_agent = None
        self._job_agent = None
        self._semantic_agent = None
        self._scoring_agent = None
        self._ranking_agent = None
        self._recommendation_agent = None

    @property
    def parser(self):
        if self._parser is None:
            from agents.resume_parser_agent import ResumeParserAgent
            self._parser = ResumeParserAgent()
        return self._parser

    @property
    def profile(self):
        if self._profile is None:
            from agents.candidate_profile_agent import CandidateProfileAgent
            self._profile = CandidateProfileAgent()
        return self._profile

    @property
    def skill_agent(self):
        if self._skill_agent is None:
            from agents.skill_extraction_agent import SkillExtractionAgent
            self._skill_agent = SkillExtractionAgent()
        return self._skill_agent

    @property
    def job_agent(self):
        if self._job_agent is None:
            from agents.job_analyzer_agent import JobAnalyzerAgent
            self._job_agent = JobAnalyzerAgent()
        return self._job_agent

    @property
    def semantic_agent(self):
        if self._semantic_agent is None:
            from agents.semantic_matching_agent import SemanticMatchingAgent
            self._semantic_agent = SemanticMatchingAgent()
        return self._semantic_agent

    @property
    def scoring_agent(self):
        if self._scoring_agent is None:
            from agents.scoring_agent import ScoringAgent
            self._scoring_agent = ScoringAgent()
        return self._scoring_agent

    @property
    def ranking_agent(self):
        if self._ranking_agent is None:
            from agents.ranking_agent import RankingAgent
            self._ranking_agent = RankingAgent()
        return self._ranking_agent

    @property
    def recommendation_agent(self):
        if self._recommendation_agent is None:
            from agents.recommendation_agent import RecommendationAgent
            self._recommendation_agent = RecommendationAgent()
        return self._recommendation_agent

    def run(self, resume_files, job_description):

        print("Starting recruitment workflow...")

        # Step 1: Analyze job description
        job_data = self.job_agent.run(job_description)

        required_skills = job_data["required_skills"]

        candidates = []

        # Step 2: Process each resume
        for pdf_path in resume_files:

            print("Processing:", pdf_path)

            resume_text = self.parser.run(pdf_path)

            profile_data = self.profile.run(resume_text)

            candidate_skills = self.skill_agent.run(
                resume_text
            )

            semantic_score = self.semantic_agent.run(
                resume_text,
                job_description
            )

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
