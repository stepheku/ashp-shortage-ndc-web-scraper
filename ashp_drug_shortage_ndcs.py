import requests
import re
import csv
from bs4 import BeautifulSoup
import feedparser
import os.path

ndc_regex_pattern = r'\d{4,5}-\d{3,4}-\d{1,2}'
dced_regex_pattern = r'\) - discontinued'
# Page sections include affected and available
# Discontinued are suffixed in the affected section
ndc_dced_regex_pattern = r'(' + ndc_regex_pattern + r')' + \
                         dced_regex_pattern
output_file_name = 'output.csv'
current_shortages_url = 'https://www.ashp.org/rss/shortages/#current'
current_shortages_resp = requests.get(current_shortages_url)
current_shortages_html = current_shortages_resp.content
parsed_rss = feedparser.parse(current_shortages_html)

page_link_list = []
for entry in parsed_rss.entries:
    page_link_list.append(entry.link.replace('Type=Rss&',''))

ndc_status_types = ['affected','discontinued','available']
list_of_csv_entry_dict = []

def write_rows_to_csv(output_file_name, list_of_dict):
    csv_field_names = ['product_description', 'ndc', 'status', 'revision_date']
    with open(output_file_name, 'a') as f:
        writer = csv.DictWriter(f, fieldnames=csv_field_names)
        if not os.path.isfile(output_file_name):
            writer.writeheader()
        for csv_dict in list_of_dict:
            writer.writerow(csv_dict)

def find_ndcs_in_section(soup, section_id=None):
    if section_id == 'affected':
        ndcs_in_affected = re.findall(ndc_regex_pattern,
                                      soup.find_all(id='1_lblProducts')[0].text)
        dc_ndcs_in_affected = re.findall(dced_regex_pattern,
                                      soup.find_all(id='1_lblProducts')[0].text)
        return [ndc for ndc in ndcs_in_affected if ndc not in dc_ndcs_in_affected]
    elif section_id == 'discontinued':
        return re.findall(ndc_dced_regex_pattern,
                          str(soup.find_all(id='1_lblProducts')[0].text))
    elif section_id == 'available':
        return re.findall(ndc_regex_pattern,
                          str(soup.find_all(id='1_lblAvailable')[0].text))

def append_csv_dict_to_list(list_name, product_desc, 
                            ndc, status, revision_date):
    return list_name.append(
        {'product_description': product_desc,
        'ndc': ndc,
        'status': status, 
        'revision_date': revision_date}
        )

if __name__ == '__main__':
    for link in page_link_list:
        link_resp = requests.get(link)
        link_content = link_resp.content
        link_soup = BeautifulSoup(link_content, 'html.parser')
        for status_type in ndc_status_types:
            for ndc in find_ndcs_in_section(link_soup, section_id=status_type):
                append_csv_dict_to_list(list_of_csv_entry_dict,
                                    link_soup.find_all(id='1_lblDrug')[0].text,
                                    ndc,
                                    status_type,
                                    link_soup.find_all(id='1_lblDate')[0].text)
    write_rows_to_csv(output_file_name, list_of_csv_entry_dict)
