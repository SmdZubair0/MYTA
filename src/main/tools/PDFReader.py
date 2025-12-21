from pypdf import PdfReader

from src.main.core.config import settings

class PDFReader:
    def __init__(self):
        self.pdf_text = {}

    def read_resume_pdf(self, pdf_path: str) -> str:
        if pdf_path not in self.pdf_text.keys():
            reader = PdfReader(settings.resumesPath / pdf_path)
            text = []
            for page in reader.pages:
                text.append(page.extract_text() or "")
            self.pdf_text[pdf_path] = "\n".join(text)
        return self.pdf_text.get(pdf_path, "")
    
if __name__ == "__main__":
    resumeReader = PDFReader()
    print(resumeReader.read_resume_pdf(settings.resumesPath / "Zubair_resume.pdf"))
