import certifi
import warnings
import requests
from typing import List
from pathlib import Path
from bs4 import BeautifulSoup
warnings.filterwarnings("ignore")

from src.main.core.config import settings
from src.main.utils.textHelpers import normalize_url
from src.main.utils.companyLoader import load_company_registry
from src.main.schemas.JobSearchState import (
    JobSearchState,
    RawJobPosting
)

# ============================================================
# CONFIG
# ============================================================

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; MYTA/1.0)"
}

SSL_VERIFY = False  # ⚠️ DEBUG ONLY — set True later

COMPANY_REGISTRY_PATH = Path("src/resources/company_registry.json")

# ============================================================
# UTIL
# ============================================================

def safe_get(url: str) -> str | None:
    try:
        resp = requests.get(
            url,
            headers=HEADERS,
            timeout=12,
            verify=certifi.where() if SSL_VERIFY else False
        )
        resp.raise_for_status()
        return resp.text
    except Exception:
        return None

# ============================================================
# COMPANY REGISTRY
# ============================================================
def score_company(company: dict, career) -> int:
    score = 0

    for role in career.target_roles:
        if any(role.lower() in r.lower() for r in company["preferred_roles"]):
            score += 5

    skill_set = {s.lower() for s in career.skills_summary}
    domain_set = {
        d.lower() for d in company["domains"] + company["tech_focus"]
    }
    score += len(skill_set & domain_set) * 2

    if career.career_stage in company["career_stage_hiring"]:
        score += 3

    if career.preferred_locations:
        if any(
            loc.lower() in company["locations"]
            for loc in career.preferred_locations
        ):
            score += 1

    score += company.get("priority", 0)

    return score


def select_top_companies(career, companies: List[dict]) -> List[dict]:
    ranked = sorted(
        companies,
        key=lambda c: score_company(c, career),
        reverse=True
    )
    return ranked[:settings.MAX_COMPANIES]


# ============================================================
# CAREER PAGE CRAWLING
# ============================================================
def discover_job_links_from_career_page(career_url: str) -> List[str]:
    html = safe_get(career_url)
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    links = set()

    for a in soup.select("a[href]"):
        href = a["href"].lower()
        if any(k in href for k in ["job", "career", "opening", "position"]):
            links.add(a["href"])

    return list(links)


def is_relevant_role(title: str | None, target_roles: List[str]) -> bool:
    if not title:
        return False
    title_l = title.lower()
    return any(role.lower() in title_l for role in target_roles)


def extract_job_from_page(
    job_url: str,
    company_name: str,
    base_url: str
) -> RawJobPosting | None:

    html = safe_get(job_url)
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")

    title_tag = soup.find("h1")
    title = title_tag.text.strip() if title_tag else None

    description = soup.get_text(separator="\n")
    description = description.strip()[:8000]  # safety cap

    return RawJobPosting(
        title=title,
        company=company_name,
        location=None,
        description=description,
        url=job_url,
        source="company_site"
    )


# ============================================================
# COMPANY JOB DISCOVERY
# ============================================================
def discover_jobs_from_company(company: dict, career) -> List[RawJobPosting]:
    jobs = []

    job_links = discover_job_links_from_career_page(company["career_page"])

    for href in job_links:
        if len(jobs) >= settings.MAX_JOBS_PER_COMPANY:
            break

        full_url = normalize_url(company["career_page"], href)

        job = extract_job_from_page(
            job_url=full_url,
            company_name=company["name"],
            base_url=company["career_page"]
        )

        if job and is_relevant_role(job.title, career.target_roles):
            jobs.append(job)

    return jobs


# ============================================================
# PHASE-1B NODE
# ============================================================

def company_job_discovery_node(state: JobSearchState) -> dict:
    companies = load_company_registry()
    selected = select_top_companies(state.career_state, companies)

    raw_jobs: List[RawJobPosting] = []

    for company in selected:
        raw_jobs.extend(
            discover_jobs_from_company(company, state.career_state)
        )

    existing = state.raw_job_postings or []
    return {
        "raw_job_postings": existing + raw_jobs
    }

# ============================================================
# LOCAL TEST
# ============================================================
if __name__ == "__main__":
    from src.resources.mockData.careerState import career

    dummy_state = JobSearchState(
        career_state=career,
        search_targets=[]
    )

    result = company_job_discovery_node(dummy_state)
    print(f"Company jobs discovered: {len(result['raw_job_postings'])}")
