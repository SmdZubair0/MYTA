from pathlib import Path

from src.main.core.config import settings

PROMPT_PATHS = {
    "resume reader" : Path("ResumeExtractionPrompt.txt"),
    "education summary" : Path("EducationSummarizerPrompt.txt"),
    "experience summary" : Path("ExperienceSummarizerPrompt.txt")
}

class PromptReader:
    def __init__(self):
        self.prompts = {}

    def read(self, type : str) -> str:
        if type not in self.prompts.keys():
            path = settings.careerStatePromptsPath / PROMPT_PATHS[type.lower().strip()]
            with open(path, "r") as f:
                self.prompts[type] = f.read()
        
        return self.prompts.get(type, "")
    
if __name__ == "__main__":
    promptReader = PromptReader()
    print(promptReader.read("resume reader"))