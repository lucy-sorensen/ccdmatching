import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

# Initialize Selenium webdriver
driver = webdriver.Firefox()  # or use Chrome(), etc.

# State abbreviation to full name mapping
states = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VI': 'Virgin Islands',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming',
}

# Open CSV file
with open('input.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    # Prepare output
    output = []

    # Loop through rows in CSV file
    for row in csv_reader:
        # Go to website
        driver.get('https://nces.ed.gov/ccd/schoolsearch/')

        # Fill in form
        select = Select(driver.find_element(By.NAME, 'State'))
        select.select_by_visible_text(states[row['state']])
        driver.find_element(By.NAME, 'City').send_keys(row['city'])
        school_name_element = driver.find_element(By.NAME, 'InstName')
        school_name_element.send_keys(row['schoolname'])

        # Submit form by pressing Enter key
        school_name_element.send_keys(Keys.ENTER)

        # Wait for the page to load
        time.sleep(1)

        # Use BeautifulSoup to parse the page
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Get the first link that starts with "school_detail.asp?Search=1"
        nces_id_link = soup.find('a', href=lambda href: href and href.startswith('school_detail.asp?Search=1'))

        # If no such link was found, set nces_id to '.'
        if nces_id_link is None:
            nces_id = '.'
        else:

            # Extract the string of numbers following "ID="
            nces_id = nces_id_link['href'].split('ID=')[1]

        # Add NCES ID to row
        row['nces_id'] = nces_id

        # Add row to output
        output.append(row)

# Write output to new CSV file
with open('output.csv', 'w') as csv_file:
    fieldnames = ['schoolname', 'city', 'state', 'nces_id']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    csv_writer.writeheader()
    for row in output:
        csv_writer.writerow(row)
