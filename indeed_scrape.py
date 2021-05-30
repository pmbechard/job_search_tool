from bs4 import BeautifulSoup
import requests

# Prompt for user input: job title and location
job_to_search = input("Please enter the job title: ")
location_to_search = input("Please enter the location: ")

# Creating and accessing url to be scraped
url = f'https://ca.indeed.com/jobs?q={job_to_search.replace(" ", "+").title()}&l={location_to_search.title()}&sort=date'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

# Scarping single-instance data
if soup.find('h1', id="jobsInLocation") == None:
    print(f"Sorry, we didn't find any results for \"{job_to_search}\" in \"{location_to_search}\"")
    companies = ''
else:
    search = soup.find('h1', id="jobsInLocation").text
    total_count = soup.find('div', id='searchCountPages').text
    total_count = total_count.strip().split(' ')
    total_count = total_count[3]

    # Identifying large content areas where multiple instances can be scraped
    titles = soup.find_all('h2', class_='title')
    companies = soup.find_all('span', class_='company')
    locations = soup.find_all('span', class_='location')
    dates = soup.find_all('span', 'date')
    description_urls = soup.find_all('h2')

    # Empty dictionary to store results for later use
    search_results = {}

    # Search information
    print(f'\n========== Most Recent {search.strip()} ==========')
    print(f'\t\t\t\t\t\t\t\tShowing {len(companies)} of {total_count} jobs\n')

counter = 1
for i in range(0, len(companies)):
    title = titles[i].text
    company = companies[i].text
    location = locations[i].text
    date = dates[i].text
    description_url = description_urls[i]
    description_url = str(description_url)
    description_url = description_url.split(' ')
    description_url = description_url[5].replace('href=', '').replace('"', '').replace("'", '')

    result = (f'{counter}. Title: {title.strip().replace("new", "")} | Company: {company.strip()} | Location: '
              f'{location.strip()} | Posted: {date.strip()} | Apply Here: https://ca.indeed.com{description_url}').replace('\n', '')
    print(result)
    search_results[counter] = {'title': title.strip().replace("new", "").replace('\n', ''),
                               'company': company.strip(),
                               'location': location.strip(),
                               'date_posted': date.strip(),
                               'link': 'https://ca.indeed.com' + description_url
                               }
    counter += 1
print("")
print(search_results)
