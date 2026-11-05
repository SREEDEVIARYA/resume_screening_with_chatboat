import fitz

class ResumeParserAgent:

    def run(self, pdf_path):

        doc = fitz.open(pdf_path)

        resume_text = ""

        for page in doc:

            resume_text += page.get_text()

        doc.close()

        return resume_text