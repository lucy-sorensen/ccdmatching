# ccdmatching
This folder provides code for methods to link school information (school name, city, and state abbreviation) to CCD data. This includes an example of the reclink procedure for linking with downloaded CCD data in a Stata do-file and also a Python web scraper using Selenium and Beautiful Soup to interact with and then scrape the NCES public school search website (https://nces.ed.gov/ccd/schoolsearch/). 

To get the CCD raw data that I used (schools_ccd_directory.csv), you can retrieve the full file from the CCD Directory Downloads from the Urban Institute Education Data Explorer here: https://educationdata.urban.org/documentation/schools.html#ccd_directory.

All other relevant files are uploaded here:
-- input.csv = the raw data file of school names and locations to merge to CCD
-- school_linking.do = Stata do-file for data management and reclink matching
-- school_search.py = Python code for scraping the NCES Public School Search page
