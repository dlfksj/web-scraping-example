import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"

def extract_pages():
  # Get URL
  resul = requests.get(URL)

  # Make soup
  soup = BeautifulSoup(resul.text, "html.parser")

  # Extract pages
  pagination = soup.find("div", {"class": "pagination"})
  links = pagination.find_all('a')
  pages = []

  for link in links[:-1]:
    pages.append(int(link.find("span").string))

  return pages[-1]


def extract_job_info(html):
  # Get the name of the Job
  title = html.find("h2", {"class": "title"}).find('a')["title"]
  
  # Get the company name
  company = html.find("div", {"class": "sjcl"}).find('div').find("span", {"class": "company"})
  if company:
    company_anchor = company.find('a')
    if company_anchor is not None:
      company = str(company_anchor.string)
    else:
      company = str(company.string)
    company = company.strip()
  else:
    company = None

  # Get the location
  location = html.find("div", {"class": "sjcl"}).find('div', {"class": "recJobLoc"})["data-rc-loc"]

  # Get the ID
  job_id = html["data-jk"]

  return {
    'title': title, 
    'company': company, 
    'location': location, 
    'link': f"https://www.indeed.com/viewjob?jk={job_id}"
    }


def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping Indeed: page {page}")

    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")

    htmls = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})

    for html in htmls:
      job = extract_job_info(html)
      jobs.append(job)

  return jobs


def get_jobs():
  last_pages = extract_pages()
  jobs = extract_jobs(last_pages)
  return jobs