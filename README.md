# ashp-shortage-ndc-web-scraper
ASHP's website for drug shortages (https://www.ashp.org/Drug-Shortages/Current-Shortages) does not have a way to grab all of the NDCs that listed on the website. This pulls all NDCs by using the RSS feed, going to each link and scraping the information using Beautiful Soup, then creates an output CSV with the fields:
1. Product description
2. NDC
3. Status (affected, discontinued or available)
4. Revision date
We use this if we need to check which NDCs on our formulary have been discontinued or affected by a drug shortage so we can tag them appropriately
