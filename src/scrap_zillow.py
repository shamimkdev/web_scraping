# Filename: scrap_zillow.py
# Author: Shamim Khan
# Date: January 16, 2024
# Description: This script demonstrates how to scrap the data from website (https://www.zillow.com/dexter-ks/)
    # using request and BeautifulSoup libraries to get the property details from this website
# Script File Structure - Used web_scrap_zillow_poc.ipyn for poc on this website, Input\website_list.txt for inputting url
    #Output folder for generating output json and html files


import requests
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime
import re


class WebScraper:
    def __init__(self):
        self.file_base_path = os.getcwd()
        self.input_file_path = "\\Input\\"
        self.output_file_path = "\\Output\\"
        self.input_file_complete_path = self.file_base_path + self.input_file_path
        self.output_file_complete_path = self.file_base_path + self.output_file_path
        self.input_file_name = "website_list.txt"
        self.input_file = os.path.join(self.input_file_complete_path, self.input_file_name)
        self.output_file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.output_response = {}

    def extract_text_from_website(self, urlpath):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'authority': 'www.google.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0'
        }
        try:
            response = requests.get(urlpath, headers=headers, verify=True)
            if response.status_code == 200:
                property_list = []
                soup = BeautifulSoup(response.text, 'html.parser')
                properties = soup.find_all("div", class_="StyledPropertyCardDataWrapper-c11n-8-84-3__sc-1omp4c3-0 bKpguY property-card-data")

                for property in properties:
                    data = property.text

                    # Extracting the price
                    price_match = re.search(r'\$\d+(,\d{3})*', data)
                    price = price_match.group(0) if price_match else None

                    # Extracting the address search till first fullstop or dollar sign
                    pattern = re.compile(r'(.*?)(\.|\$)')
                    match = pattern.search(data)

                    if match:
                        address = match.group(1)
                    else:
                        address = 'Not Found'

                    property_dict = {
                        'address': address,
                        'price': price
                    }

                    property_list.append(property_dict)
            else:
                self.output_response[urlpath] = 'Status code:' + str(response.status_code)
        except Exception as e:
            self.output_response[urlpath] = 'Error Exception:' + str(e)
        self.output_response[urlpath] = property_list

    def generate_output_json(self, data, file_path):
        output_file_path = self.output_file_name+".json"
        json_file = file_path + output_file_path
        with open(json_file, 'w') as file:
            json.dump(data, file, indent=4)

    def run(self):
        with open(self.input_file, "r") as file:
            for line in file:
                web_link = line.strip()
                self.extract_text_from_website(web_link)
        self.generate_output_json(self.output_response, self.output_file_complete_path)

if __name__ == '__main__':
    scraper = WebScraper()
    scraper.run()
