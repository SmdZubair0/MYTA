from src.main.schemas import CareerState
from src.main.schemas.JobSearchState import JobSearchTarget
from datetime import datetime


career = CareerState(
    name= "dummy",
    current_location= "Hyderabad",
    target_roles= ['AI Engineer', 'Machine Learning Engineer', 'Junior Data Scientist', 'Automation Specialist - AI', 'ML Developer'],
    job_type_preference= ["Full-time", "Hybrid"],
    preferred_locations= ["Bangalore", "Hyderabad", "Remote"],

    current_ctc = 8.5,
    expected_ctc = 18.5,

    education_summary = 'B.Tech in Computer Science from XYZ Institute of Technology (2023) and B.Tech in Mechanical from G.Pullaiah College of Engineering and Technology (2025), with prior education including Intermediate (M.P.C) from Narayana Junior College, Kurnool (2021) and 10th (SSC) from KVR English Medium High School, Kurnool (2019).',
    experience_summaries =  ['Associate Software Engineer at ABC Tech Solutions, building and maintaining automation frameworks and AI workflows.', 'Interned in Full Stack Development, designing and developing responsive UI components using MERN stack.'],

    skills_summary = ['JavaScript', 'HTML', 'CSS', 'Python', 'Java', 'Git', 'Docker', 'MySQL', 'React JS', 'Machine Learning', 'Deep Learning', 'Automation', 'FastAPI'],

    project_summaries = ['Developed an LLM-based system to analyze resumes and recommend career paths with code available on GitHub', 'Built a fully responsive and user-friendly Netflix clone using HTML and CSS', 'Created an interactive Rock, Paper and Scissor game using HTML, CSS, and JavaScript'],

    online_presence_urls = [],

    career_stage = 'junior',  # junior / mid / senior
    strengths= ['Automation framework development', 'AI workflow maintenance', 'Full stack development', 'Responsive UI component design', 'Machine learning model implementation', 'Cloud-based system deployment with Docker'],
    skill_gaps=  ['Node.js', 'Cloud Computing', 'NoSQL Databases', 'Data Preprocessing'],

    last_updated = datetime.now()
)


queries = ['Junior AI Engineer jobs in Bangalore', 'Machine Learning Engineer entry level jobs Hyderabad', 'Junior Data Scientist full-time jobs Remote', 'Automation Specialist AI ML jobs in Bangalore', 'ML Developer junior jobs Hybrid', 'Junior AI ML jobs in Hyderabad']

job_search_targets = [
    JobSearchTarget(source='linkedin', search_url='https://www.linkedin.com/jobs/search/?keywords=Junior+AI+Engineer+jobs+in+Bangalore', query='Junior AI Engineer jobs in Bangalore'),
    JobSearchTarget(source='indeed', search_url='https://www.indeed.com/jobs?q=Junior+AI+Engineer+jobs+in+Bangalore', query='Junior AI Engineer jobs in Bangalore'),
    JobSearchTarget(source='naukri', search_url='https://www.naukri.com/Junior+AI+Engineer+jobs+in+Bangalore-jobs', query='Junior AI Engineer jobs in Bangalore'),
    JobSearchTarget(source='linkedin', search_url='https://www.linkedin.com/jobs/search/?keywords=Machine+Learning+Engineer+entry+level+jobs+Hyderabad', query='Machine Learning Engineer entry level jobs Hyderabad'),
    JobSearchTarget(source='indeed', search_url='https://www.indeed.com/jobs?q=Machine+Learning+Engineer+entry+level+jobs+Hyderabad', query='Machine Learning Engineer entry level jobs Hyderabad'),
    JobSearchTarget(source='naukri', search_url='https://www.naukri.com/Machine+Learning+Engineer+entry+level+jobs+Hyderabad-jobs', query='Machine Learning Engineer entry level jobs Hyderabad'),
    JobSearchTarget(source='linkedin', search_url='https://www.linkedin.com/jobs/search/?keywords=Junior+Data+Scientist+full-time+jobs+Remote', query='Junior Data Scientist full-time jobs Remote'),
    JobSearchTarget(source='indeed', search_url='https://www.indeed.com/jobs?q=Junior+Data+Scientist+full-time+jobs+Remote', query='Junior Data Scientist full-time jobs Remote'),
    JobSearchTarget(source='naukri', search_url='https://www.naukri.com/Junior+Data+Scientist+full-time+jobs+Remote-jobs', query='Junior Data Scientist full-time jobs Remote'),
    JobSearchTarget(source='linkedin', search_url='https://www.linkedin.com/jobs/search/?keywords=Automation+Specialist+AI+ML+jobs+in+Bangalore', query='Automation Specialist AI ML jobs in Bangalore'),
    JobSearchTarget(source='indeed', search_url='https://www.indeed.com/jobs?q=Automation+Specialist+AI+ML+jobs+in+Bangalore', query='Automation Specialist AI ML jobs in Bangalore'),
    JobSearchTarget(source='naukri', search_url='https://www.naukri.com/Automation+Specialist+AI+ML+jobs+in+Bangalore-jobs', query='Automation Specialist AI ML jobs in Bangalore'),
    JobSearchTarget(source='linkedin', search_url='https://www.linkedin.com/jobs/search/?keywords=ML+Developer+junior+jobs+Hybrid', query='ML Developer junior jobs Hybrid'),
    JobSearchTarget(source='indeed', search_url='https://www.indeed.com/jobs?q=ML+Developer+junior+jobs+Hybrid', query='ML Developer junior jobs Hybrid'),
    JobSearchTarget(source='naukri', search_url='https://www.naukri.com/ML+Developer+junior+jobs+Hybrid-jobs', query='ML Developer junior jobs Hybrid'),
    JobSearchTarget(source='linkedin', search_url='https://www.linkedin.com/jobs/search/?keywords=Junior+AI+ML+jobs+in+Hyderabad', query='Junior AI ML jobs in Hyderabad'),
    JobSearchTarget(source='indeed', search_url='https://www.indeed.com/jobs?q=Junior+AI+ML+jobs+in+Hyderabad', query='Junior AI ML jobs in Hyderabad'),
    JobSearchTarget(source='naukri', search_url='https://www.naukri.com/Junior+AI+ML+jobs+in+Hyderabad-jobs', query='Junior AI ML jobs in Hyderabad')]