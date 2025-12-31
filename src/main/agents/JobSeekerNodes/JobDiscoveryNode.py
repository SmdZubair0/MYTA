import certifi
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from sympy import false

from src.main.schemas.JobSearchState import JobSearchTarget, JobSearchState, RawJobPosting

from src.resources.mockData.careerState import career, job_search_targets

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; MYTA/1.0)"
}
def discover_from_linkedin(target: JobSearchTarget) -> list[RawJobPosting]:
    response = requests.get(target.search_url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    for link in soup.select("a[href*='/jobs/view/']"):
        jobs.append(
            RawJobPosting(
                title=None,              # masked
                company=None,
                location=None,
                description=None,
                url=link["href"],
                source="linkedin"
            )
        )

    return jobs

def discover_from_indeed(target: JobSearchTarget) -> list[RawJobPosting]:
    try:
        response = requests.get(
            target.search_url,
            headers=HEADERS,
            timeout=10,
            # verify=certifi.where()
            verify=false
        )
    except:
        return []
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    for card in soup.select(".job_seen_beacon"):
        title = card.select_one("h2 span")
        company = card.select_one(".companyName")
        location = card.select_one(".companyLocation")
        desc = card.select_one(".job-snippet")

        link = card.select_one("a")

        if link:
            jobs.append(
                RawJobPosting(
                    title=title.text.strip() if title else None,
                    company=company.text.strip() if company else None,
                    location=location.text.strip() if location else None,
                    description=desc.text.strip() if desc else None,
                    url="https://www.indeed.com" + link["href"],
                    source="indeed"
                )
            )

    return jobs

def discover_from_naukri(target: JobSearchTarget) -> list[RawJobPosting]:
    try:
        response = requests.get(
            target.search_url,
            headers=HEADERS,
            timeout=10,
            # verify=certifi.where()
            verify=false
        )
    except:
        return []
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    for card in soup.select(".jobTuple"):
        title = card.select_one(".title")
        company = card.select_one(".companyInfo")
        location = card.select_one(".locWdth")
        desc = card.select_one(".job-desc")

        link = title["href"] if title else None

        if link:
            jobs.append(
                RawJobPosting(
                    title=title.text.strip() if title else None,
                    company=company.text.strip() if company else None,
                    location=location.text.strip() if location else None,
                    description=desc.text.strip() if desc else None,
                    url=link,
                    source="naukri"
                )
            )

    return jobs

def job_discovery_node(state: JobSearchState) -> dict:
    raw_jobs = []

    for target in state.search_targets:
        if target.source == "indeed":
            raw_jobs.extend(discover_from_indeed(target))
        elif target.source == "linkedin":
            raw_jobs.extend(discover_from_linkedin(target))
        elif target.source == "naukri":
            raw_jobs.extend(discover_from_naukri(target))

    return {"raw_job_postings": raw_jobs}


if __name__ == "__main__":
    load_dotenv()
    state = JobSearchState(
        career_state=career,
        job_search_targets = job_search_targets
    )
    # print(discover_jobs_from_targets(job_search_targets))

    target = JobSearchTarget(
        source='naukri',
        search_url='https://www.naukri.com/Automation+Specialist+AI+ML+jobs+in+Bangalore-jobs',
        query='Automation Specialist AI ML jobs in Bangalore')
    
    print(discover_from_naukri(target))

    # target = JobSearchTarget(
    #     source='linkedin',
    #     search_url='https://www.linkedin.com/jobs/search/?keywords=Junior+AI+Engineer+jobs+in+Bangalore',
    #     query='Junior AI Engineer jobs in Bangalore')
    
    # print(discover_from_linkedin(target))

    target = JobSearchTarget(
        source='indeed',
        search_url='https://www.indeed.com/jobs?q=Junior+AI+Engineer+jobs+in+Bangalore',
        query='Junior AI Engineer jobs in Bangalore')
    
    print(discover_from_indeed(target))