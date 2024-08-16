import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

MAX_SPACES = 15
KEYWORDS = [
    "early career", "early in career", "internship", "new grad",
    "recent graduate", "entry", "software engineer",
    "university graduates", "associate software engineer"
]
# Exclude exact matches to ignore filters on career websites
EXCLUDE_MATCHES = [
    "add to favorites", "early in career", "early careers",
    "early career", "sr staff software engineer", "staff software engineer",
]
# Substrings to ignore
EXCLUDE_PHRASES = [
    "staff", "principal", "manag", "hardware", "marketing"
]

EXCLUDE_ELEMENTS = [
    "script", "style"
]

MATCHES_SET = set(EXCLUDE_MATCHES)
PHRASES_SET = set(EXCLUDE_PHRASES)
ELEMENTS_SET = set(EXCLUDE_ELEMENTS)


def scrape_jobs(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(
            f"Failed to retrieve the page. Status code: {response.status_code}")
        return set()

    with open('page_content.html', 'w', encoding='utf-8') as file:
        file.write(response.text)

    soup = BeautifulSoup(response.text, 'html.parser')

    pattern = re.compile("|".join(KEYWORDS), re.IGNORECASE)

    job_elements = soup.find_all(text=pattern)

    jobs = set()
    for job_element in job_elements:
        if job_element.parent.name in ELEMENTS_SET or job_element.find_parent(class_='a11y'):
            continue

        job_text = job_element.strip()
        text_lowered = job_text.lower()

        # Count spaces in the text
        space_count = job_text.count(' ')

        if (space_count <= MAX_SPACES) and (not any(phrase in text_lowered for phrase in PHRASES_SET)) and (text_lowered not in MATCHES_SET):
            jobs.add(job_text)

    # print(jobs)
    return jobs


def read_urls_from_file(filename):
    with open(filename, 'r') as file:
        urls = file.readlines()
        urls = [url.strip() for url in urls if url.strip()]
    return urls


def extract_domain(url):
    start = url.find("https://") + len("https://")
    end = url.find("/", start)
    return url[start:end]


if __name__ == "__main__":
    filename = 'urls.txt'
    urls = read_urls_from_file(filename)

    # Open the file in write mode to overwrite each time the script runs
    with open('output.txt', 'w', encoding='utf-8') as output_file:
        for url in urls:
            domain = extract_domain(url)
            output_file.write(f"Domain: {domain}\n")
            jobs = scrape_jobs(url)

            if jobs:
                output_file.write("Jobs Found:\n")
                for job in jobs:
                    output_file.write(f"{job}\n")
            else:
                output_file.write("No jobs found.\n")

            output_file.write(
                "_______________________________________________________________________________________________________________________\n\n")
