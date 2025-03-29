import requests
from bs4 import BeautifulSoup

def transform(soup):
    # Parsing the job card info (title, company, location, date, job_url) from the beautiful soup object
    joblist = []
    try:
        divs = soup.find_all('div', class_='base-search-card__info')
    except:
        print("Empty page, no jobs found")
        return joblist
    for item in divs:
        title = item.find('h3').text.strip()
        company = item.find('a', class_='hidden-nested-link')
        location = item.find('span', class_='job-search-card__location')
        parent_div = item.parent
        entity_urn = parent_div['data-entity-urn']
        job_posting_id = entity_urn.split(':')[-1]
        job_url = 'https://www.linkedin.com/jobs/view/'+job_posting_id+'/'

        date_tag_new = item.find('time', class_ = 'job-search-card__listdate--new')
        date_tag = item.find('time', class_='job-search-card__listdate')
        date = date_tag['datetime'] if date_tag else date_tag_new['datetime'] if date_tag_new else ''
        job_description = BeautifulSoup(requests.get(job_url).content,'html.parser').find('div', class_="show-more-less-html__markup show-more-less-html__markup--clamp-after-5 relative overflow-hidden").text.strip()



        job = {
            'title': title,
            'company': company.text.strip().replace('\n', ' ') if company else '',
            'location': location.text.strip() if location else '',
            'date': date,
            'job_url': job_url,
            'job_description': f'{job_description[:100]}...',
            'applied': 0,
            'hidden': 0,
            'interview': 0,
            'rejected': 0
        }
        joblist.append(job)
    return joblist

# Function to search for jobs
def search_jobs_adzuna(zip_code, radius, job_title, country="us"):
    API_APP_ID = "6e46cbcd"  
    API_KEY = "a5ec6087fb09356a2f74194fbd9bd82e"
    """
    Searches for jobs using the Adzuna API.

    Parameters:
        zip_code (str): The ZIP code to search around.
        radius (int): The search radius in miles.
        job_title (str): The job title or keyword to search for.
        country (str): The country to search in. Default is "us".
    
    Returns:
        list: A list of job postings.
    """
    base_url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
    params = {
        "app_id": API_APP_ID,
        "app_key": API_KEY,
        "where": zip_code,
        "distance": radius,
        "what": job_title,
        "content-type": "application/json",
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []
    
def search_jobs_linkedin(keywords, location, f_TPR, f_JT, f_PP, f_WT, f_E, f_SB2):
    pages_to_scrape = 1
    soup_r  =""
    #query guidlines for linkedin

    #keywords - this is what you type in the search bar
    #location - this is the country
    #geoId    - TBD
    #trk      - TBD
    #position - TBD
    #f_TPR    - post relivance
    #                         past month = r2592000      
    #                         past week = r604800  
    #                         past 24hrs = r86400                      
    #f_JT     - this is for jobtype 
    #                         F = fulltime
    #                         P = Parttime
    #                         I = Internship
    #                         C = Contract
    #                         T = Temp
    #                         V = Volunteer
    #f_PP     - 9 digit city code as of now that is independent to linkedin  ( they can be put together by adding a space between them )
    #f_WT     - single digit code assigned to remote, in-person, or hybrid working ( they can be added together by putting spaces between them )
    #                         1 = On Site
    #                         2 = Remote
    #                         3 = Hybrid
    #f_E      - single digit code assigned to experience level (they can be added together by putting spaces between them )    
    #                         1 = Internship
    #                         2 = Entry Level
    #                         3 = Associate
    #                         4 = Mid-Senior Level
    #                         5 = Director
    #f_SB2    - single digit code assigned to salary expectations
    #                         1 = 40K+
    #                         2 = 60K+
    #                         3 = 80K+
    #                         4 = 100K+
    #                         5 = 120K+
    #
    #
    for i in range(pages_to_scrape):
        url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={keywords}&location={location}&f_JT={f_JT}&f_PP={f_PP}&f_E={f_E}&f_SB2={f_SB2}&f_WT={f_WT}&geoId=&f_TPR={f_TPR}&start={i}"
        r = requests.get(url).content
        soup_r = BeautifulSoup(r, 'html.parser')

    print('')
    print(transform(soup_r))
    for item in transform(soup_r):
        print(item)

# Example usage for adzuna
if __name__ == "__main__":
    zip_code = "19701"  # Bear, DE City ZIP code
    radius = 100        # 100 miles
    job_title = "Software Engineer"
    
    jobs1 = search_jobs_adzuna(zip_code, radius, job_title)
    
    if jobs1:
        print(f"Found {len(jobs1)} jobs within {radius} miles of {zip_code}:\n")
        for job in jobs1[:10]:  # Show the first 10 jobs
            print(f"Title: {job['title']}")
            print(f"Company: {job.get('company', {}).get('display_name', 'N/A')}")
            print(f"Location: {job['location'].get('display_name', 'N/A')}")
            print(f"Description: {job['description'][:100]}...")
            print(f"Apply here: {job['redirect_url']}\n")
    else:
        print("No jobs found.")

    search_jobs_linkedin("Software%Engineer", "United%States", "1", "1", "","1","2","3")