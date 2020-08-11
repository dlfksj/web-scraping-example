import requests
from bs4 import BeautifulSoup

URL = f"https://stackoverflow.com/jobs?q=python"

def extract_pages():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")

  # Extract pages
  pagination = soup.find("div", {"class": "s-pagination"}).find_all('a')
  
  last_page = pagination[-2].get_text(strip=True)

  return int(last_page)


def extract_job_info(html):
  title = html.find("h2", {"class": "mb4 fc-black-800 fs-body3"}).find("a")["title"]

  company, location = html.find("h3", {"class": "fc-black-700 fs-body1 mb4"}).find_all("span", recursive=False)
  company = company.get_text(strip=True)
  location = location.get_text(strip=True)
  job_id = html['data-jobid']

  return {
    'title': title, 
    'company': company, 
    'location': location,
    'link': f"https://stackoverflow.com/jobs/{job_id}"
    }


def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping Stack overflow:  page {page}")
    result = requests.get(f"{URL}&pg={page+1}")
    soup = BeautifulSoup(result.text, "html.parser")

    htmls = soup.find_all("div", {"class": "-job"})

    for html in htmls:
      job = extract_job_info(html)
      jobs.append(job)

  return jobs

def get_jobs():
  last_page = extract_pages()
  jobs = extract_jobs(last_page)
  return jobs