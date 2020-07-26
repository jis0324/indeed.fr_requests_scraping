import os
import csv
import re
import pandas
import requests
from bs4 import BeautifulSoup
base_dir = os.path.dirname(os.path.abspath(__file__))

search_keyword_list = [
    {
        'job' : 'chauffeur livreur',
        'location' : 'Île-de-France'
    },
]

for search_key in search_keyword_list:
    job_name = re.sub(r'\s', '+', search_key['job'])
    location = re.sub(r'\s', '+', search_key['location'])
    site_url = "https://www.indeed.fr/emplois?q=" + job_name + "&l=" + location
    
    res = requests.get(site_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.find_all('div', attrs={'data-tn-component': 'organicJob'})
    for result in results:
        temp_dict = {
            'job' : '',
            'company' : '',
            'location' : '',
            'salary' : '',
        }

        job = result.find('a', attrs={'data-tn-element': "jobTitle"})
        if job:
            print('job:', job.text.strip())
            temp_dict['job'] = job.text.strip()

        company = result.find('span', class_='company')
        if company:
            print('company:', company.text.strip())
            temp_dict['company'] = company.text.strip()
        
        location = result.find('span', class_='location')
        if location:
            print('location:', location.text.strip())
            temp_dict['location'] = location.text.strip()

        salary = result.find('span', class_='salaryText')
        if salary:
            print('salary:', salary.text.strip())
            temp_dict['salary'] = salary.text.strip()


        print('----------')

        file_exist = os.path.isfile(base_dir + '/output/result.csv')
        with open( base_dir + '/output/result.csv', 'a', newline="") as result_csv:
            fieldnames = ["job", "company", "location", "salary"]
            writer = csv.DictWriter(result_csv, fieldnames=fieldnames)
            if not file_exist:
                writer.writeheader()
            writer.writerow(temp_dict)
