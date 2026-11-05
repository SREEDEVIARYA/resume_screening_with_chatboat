from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticMatchingAgent:

    def __init__(self):

        print("Loading Hugging Face model...")

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    def run(self, resume_text, job_description):

        resume_embedding = self.model.encode(
            [resume_text]
        )

        job_embedding = self.model.encode(
            [job_description]
        )

        similarity = cosine_similarity(
            resume_embedding,
            job_embedding
        )[0][0]

        score = max(0, min(100, float(similarity) * 100))

        return round(score, 2)