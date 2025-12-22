import json
from dotenv import load_dotenv

from src.main.agents import LLMClient
from src.main.tools.PDFReader import PDFReader
from src.main.utils.textHelpers import extract_json
from src.main.utils.PromptReader import PromptReader
from src.main.schemas.UserCareerProfile import Education, Experience, Skills, Project
from src.main.schemas.ResumeExtraction import ResumeExtractionInput, ResumeExtractedData


promptReader = PromptReader()
RESUME_EXTRACTION_PROMPT = promptReader.read("resume reader")

def resumeExtractionNode(state : ResumeExtractionInput) -> ResumeExtractedData:

    resume_path = state.file_name

    if resume_path is None:
        return ResumeExtractedData()
    
    if state.text is None:
        pdfReader = PDFReader()
        state.text = pdfReader.read_resume_pdf(state.file_name)

    if state.text is None:
        return ResumeExtractedData()
    
    llm_response = LLMClient.generate(
        prompt=RESUME_EXTRACTION_PROMPT.replace("{{resume_text}}", state.text)
    )

    try:
        structured_data = extract_json(llm_response)
    except json.JSONDecodeError:
        return ResumeExtractedData()

    return ResumeExtractedData(
        education=[Education(**e) for e in structured_data.get("education", [])],
        experience=[Experience(**e) for e in structured_data.get("experience", [])],
        skills=Skills(**structured_data.get("skills", {})),
        projects=[Project(**p) for p in structured_data.get("projects", [])]
    )


if __name__ == "__main__":
    load_dotenv()
    resume = ResumeExtractionInput(
        file_name="Zubair_resume.pdf"
    )
    print(resumeExtractionNode(resume))