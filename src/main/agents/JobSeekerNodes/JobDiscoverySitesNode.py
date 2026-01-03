import certifi
import requests
import warnings
from lxml import etree
from typing import List
from bs4 import BeautifulSoup
from dotenv import load_dotenv
warnings.filterwarnings("ignore")

from src.main.core.config import settings
from src.main.utils.textHelpers import normalize_text
from src.main.schemas.JobSearchState import (
    JobSearchTarget,
    JobSearchState,
    RawJobPosting
)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; MYTA/1.0)"
}

# ------------------------------------------------------------------
# CONFIG (DEBUG ONLY)
# ------------------------------------------------------------------
# ⚠️ Set this to False in production
SSL_VERIFY = False   # change to certifi.where() later


def safe_get(url: str) -> str | None:
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10,
            verify=certifi.where() if SSL_VERIFY else False
        )
        response.raise_for_status()
        return response.text
    except Exception:
        return None


# ------------------------------------------------------------------
# LINKEDIN (metadata only)
# ------------------------------------------------------------------
def discover_from_linkedin(target: JobSearchTarget) -> List[RawJobPosting]:
    html = safe_get(target.search_url)
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser").main
    tree = etree.HTML(str(soup))

    all_jobs = tree.xpath("//a[contains(@class,\"base-card__full-link\")]")

    links = [job.get('href') for job in all_jobs if job.get('href')][:settings.MAX_JOBS_FROM_LINKEDIN]

    jobs : list[RawJobPosting] = []

    for link in links:
        res = safe_get(link)
        if not res:
            continue
        
        e = etree.HTML(res)

        title = normalize_text(e.xpath("//h1/text()")[0])
        company_name = normalize_text(e.xpath("//a[contains(@class,'topcard__org-name-link')]/text()")[0])
        location = normalize_text(e.xpath("//span[contains(@class,'topcard__flavor--bullet')]/text()")[0])
        desc_node = e.xpath("//div[contains(@class,'description__text')]")
        description = normalize_text(
            BeautifulSoup(etree.tostring(desc_node[0]), "html.parser").get_text()
        ) if desc_node else None

        career_stage = []
        employment_type = []
        for li in e.xpath("//li[contains(@class,'description__job-criteria-item')]"):
            heading = li.xpath(".//h3/text()")
            value = li.xpath(".//span/text()")

            if not heading or not value:
                continue

            h = heading[0].lower()
            v = normalize_text(value[0])

            if "seniority" in h:
                career_stage.append(normalize_text(v))
            elif "employment type" in h:
                employment_type.append(normalize_text(v))


        jobs.append(
            RawJobPosting(
                title=title,
                company=company_name,
                location=location,
                description=description,
                career_stage=career_stage,
                employment_type=employment_type,
                job_type=None,
                url=link,
                source="linkedin"
            )
        )

    return jobs


# ------------------------------------------------------------------
# INDEED (best Phase-1A source)
# ------------------------------------------------------------------
def discover_from_indeed(target: JobSearchTarget) -> List[RawJobPosting]:
    html = safe_get(target.search_url)
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    jobs = []

    for card in soup.select(".job_seen_beacon"):
        title = card.select_one("h2 span")
        company = card.select_one(".companyName")
        location = card.select_one(".companyLocation")
        desc = card.select_one(".job-snippet")
        link = card.select_one("a")

        if not link:
            continue

        href = link.get("href", "")
        if href.startswith("/"):
            href = "https://www.indeed.com" + href

        jobs.append(
            RawJobPosting(
                title=title.text.strip() if title else None,
                company=company.text.strip() if company else None,
                location=location.text.strip() if location else None,
                description=desc.text.strip() if desc else None,
                url=href,
                source="indeed"
            )
        )

    return jobs


# ------------------------------------------------------------------
# NAUKRI (best-effort)
# ------------------------------------------------------------------
def discover_from_naukri(target: JobSearchTarget) -> List[RawJobPosting]:
    html = safe_get(target.search_url)
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    jobs = []

    for card in soup.select(".jobTuple"):
        title = card.select_one(".title")
        company = card.select_one(".companyInfo")
        location = card.select_one(".locWdth")
        desc = card.select_one(".job-desc")

        link = title.get("href") if title else None
        if not link:
            continue

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


# ------------------------------------------------------------------
# MAIN PHASE-1A NODE
# ------------------------------------------------------------------
def job_discovery_node(state: JobSearchState) -> dict:
    raw_jobs: List[RawJobPosting] = []

    for target in state.search_targets:
        if target.source == "indeed":
            raw_jobs.extend(discover_from_indeed(target))
        elif target.source == "linkedin":
            raw_jobs.extend(discover_from_linkedin(target))
        elif target.source == "naukri":
            raw_jobs.extend(discover_from_naukri(target))

    existing = state.raw_job_postings or []
    return {
        "raw_job_postings": existing + raw_jobs
        }


# ------------------------------------------------------------------
# LOCAL TESTING
# ------------------------------------------------------------------
if __name__ == "__main__":
    load_dotenv()

    from src.resources.mockData.careerState import career
    from src.resources.mockData.newData import new_urls

    state = JobSearchState(
        career_state=career,
        search_targets=new_urls
    )

    # result = job_discovery_node(state)
    # print(f"Discovered jobs: {result['raw_job_postings']}")

    print(discover_from_linkedin(new_urls[0]))