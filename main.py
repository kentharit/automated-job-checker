import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

MAX_SPACES = 15
KEYWORDS = ["internship", "new grad", "early career"] 
EXCLUDE_PHRASES = ["Add to Favorites"]

def scrape_jobs(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return set()
    
    # with open('page_content.html', 'w', encoding='utf-8') as file:
    #     file.write(response.text)

    soup = BeautifulSoup(response.text, 'html.parser')
    
    pattern = re.compile("|".join(KEYWORDS), re.IGNORECASE)

    print(pattern.pattern)
    
    job_elements = soup.find_all(text=pattern)

    exclude_set = set(phrase.lower() for phrase in EXCLUDE_PHRASES)

    print("TRYING")

    jobs = set()
    for job_element in job_elements:
        if job_element.parent.name in ['script', 'style'] or job_element.find_parent(class_='a11y'):
            continue
        
        job_text = job_element.strip()
        
        # Count spaces in the text
        space_count = job_text.count(' ')

        if space_count <= MAX_SPACES and not any(excluded_phrase in job_text.lower() for excluded_phrase in exclude_set):
            jobs.add(job_text)
    
    print(jobs)
    return jobs


def save_jobs_to_csv(jobs, filename='jobs.csv'):
    df = pd.DataFrame(jobs)
    df.to_csv(filename, index=False)
    print(f"Job data saved to {filename}")

if __name__ == "__main__":
    company_careers_url = 'https://jobs.apple.com/en-us/search?sort=relevance&location=united-states-USA&team=corporate-STDNT-CORP+apple-store-STDNT-ASTR+apple-store-leader-program-STDNT-ASLP+apple-retail-partner-store-STDNT-ARPS+apple-support-college-program-STDNT-ACCP+apple-campus-leader-STDNT-ACR+internships-STDNT-INTRN'
    
    jobs = scrape_jobs(company_careers_url)

    # save_jobs_to_csv(jobs)
