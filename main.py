import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def scrape_jobs(url, keywords, exclude_phrases):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return set()
    
    # with open('page_content.html', 'w', encoding='utf-8') as file:
    #     file.write(response.text)

    soup = BeautifulSoup(response.text, 'html.parser')
    
    pattern = re.compile("|".join(keywords), re.IGNORECASE)

    print(pattern.pattern)
    
    job_elements = soup.find_all(text=pattern)

    exclude_set = set(phrase.lower() for phrase in exclude_phrases)

    print("TRYING")

    jobs = set()
    for job_element in job_elements:
        if job_element.parent.name in ['script', 'style']:
            continue
        
        job_text = job_element.get_text(strip=True)
        if not any(excluded_phrase in job_text.lower() for excluded_phrase in exclude_set):
            jobs.add(job_text)
    
    print(jobs)
    return jobs


def save_jobs_to_csv(jobs, filename='jobs.csv'):
    df = pd.DataFrame(jobs)
    df.to_csv(filename, index=False)
    print(f"Job data saved to {filename}")

if __name__ == "__main__":
    company_careers_url = 'https://jobs.apple.com/en-us/search?sort=relevance&location=united-states-USA&team=corporate-STDNT-CORP+apple-store-STDNT-ASTR+apple-store-leader-program-STDNT-ASLP+apple-retail-partner-store-STDNT-ARPS+apple-support-college-program-STDNT-ACCP+apple-campus-leader-STDNT-ACR+internships-STDNT-INTRN'
    keywords = ["internship", "new grad", "early career"] 
    exclude_phrases = ["Add to Favorites"]
    jobs = scrape_jobs(company_careers_url, keywords, exclude_phrases)

    # save_jobs_to_csv(jobs)
