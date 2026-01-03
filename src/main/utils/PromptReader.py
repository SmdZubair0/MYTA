from pathlib import Path

from src.main.core.config import settings

PROMPT_PATHS = {
    "resume reader" : Path("CareerStatePrompts/ResumeExtractionPrompt.txt"),
    "education summary" : Path("CareerStatePrompts/EducationSummarizerPrompt.txt"),
    "experience summary" : Path("CareerStatePrompts/ExperienceSummarizerPrompt.txt"),
    "project summary": Path("CareerStatePrompts/ProjectSummarizerPrompt.txt"),
    "skills summary": Path("CareerStatePrompts/SkillsSummarizerPrompt.txt"),
    "target roles" : Path("CareerStatePrompts/TargetRolesPrompt.txt"),
    "strengths" : Path("CareerStatePrompts/StrengthsPrompt.txt"),
    "skills gap" : Path("CareerStatePrompts/SkillsGapPrompt.txt"),
    "job intent" : Path("JobSeekerPrompts/JobSearchIntentPrompt.txt"),
    "job fit score" : Path("JobSeekerPrompts/FitScorePrompt.txt")
}

class PromptReader:
    def __init__(self):
        self.prompts = {}

    def read(self, type : str) -> str:
        if type not in self.prompts.keys():
            path = settings.promptsPath / PROMPT_PATHS[type.lower().strip()]
            with open(path, "r") as f:
                self.prompts[type] = f.read()
        
        return self.prompts.get(type, "")
    
if __name__ == "__main__":
    promptReader = PromptReader()
    print(promptReader.read("resume reader"))