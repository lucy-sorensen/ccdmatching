//Task: Link to NCES IDs for data with only school names
//Created by: Lucy Sorensen (lsorensen@albany.edu)
//Date created: June 22, 2023
//Stata/MP 17.0, packages: reclink

//Open CCD school directory data and consolidate to one observation per unique NCES ID, school name, city, and state
import delim schools_ccd_directory.csv, clear
duplicates drop ncessch school_name city_location state_location, force 
rename city_location city
replace state_location = state_mailing if state_location=="-1"|state_location=="."
rename state_location state
rename school_name schoolname
keep ncessch schoolname city state
gen ncesid = _n
save flat_ccd_data.dta, replace

//Upload python output of school webscraper matches
import delim "output.csv", clear
save "webform_matches.dta", replace

//Open data file with school names and locations and run reclink fuzzy matching procedure
import delim "input.csv", clear varn(1)
gen masterid = _n
reclink schoolname city state using flat_ccd_data.dta, idmaster(masterid) idusing(ncesid) gen(matchscore) wmatch(10 5 3) exactstr(state) required(state) minscore(0.8)
tab _merge

//Keep un-matched schools from reclink and cross-check with web scraper output
keep if _merge==1
keep schoolname city state
merge 1:m schoolname city state using "webform_matches.dta", gen(_webmerge)
tab _webmerge
