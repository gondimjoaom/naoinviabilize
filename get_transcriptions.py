from selenium import webdriver
from selenium.webdriver.common.by import By

from tqdm import tqdm
from pathlib import Path

import re
import html
import json

# selenium setup
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

# get links folder path
links_folder = Path('./links')


# retrieve links from all files
all_links = dict()

for link_file in links_folder.iterdir():
    # get quadro from file name
    quadro = link_file.stem.split('-')[0]

    # read links from file
    with link_file.open('r') as links_file:
        links_plain = links_file.read()
        all_links[quadro] = links_plain.split('\n')[:-1]


# extract/crawl transcriptions
all_transcriptions = {}

for quadro, links in all_links.items():
    all_transcriptions[quadro] = []

    for link in tqdm(links):
        try:
            driver.get(link)

            # extract transcription from html
            texts_div = driver.find_element(By.CLASS_NAME, 'content-inner')

            html_content = texts_div.get_attribute("innerHTML") # get HTML content of text
            
            html_content = re.sub(re.compile('&nbsp;'), ' ', html_content) # replace &nbsp; (non-breaking spaces) with normal spaces
            html_content = re.sub(re.compile('<br>'), '\n', html_content) # replace new line HTML tag with new line character
            html_content = html.unescape(html_content) # unescape other HTML entities like &nbsp;
            
            html_content = re.sub(re.compile('<.*?>'), '', html_content) # remove all remaining HTML tags
            
            # set full transcription
            full_transcription = f"{html_content}"
            
            # split transcription into header and content
            if 'TRANSCRIÇÃO' in full_transcription:
                split_key = 'TRANSCRIÇÃO'
            elif '[vinheta]' in full_transcription:
                split_key = '[vinheta]'
            else:
                raise Exception('Could not find split key for transcription')
            
            raw_transcription_header, raw_transcription_content = full_transcription.split(split_key, maxsplit=1)
            transcription_header = raw_transcription_header.strip().split('\n')
            transcription_content = raw_transcription_content.strip()

            # indicate header metadata
            header_metadata = [
                {
                    'field': 'title',
                    'prefix': 'título: ',
                },
                {
                    'field': 'publishing_date',
                    'prefix': 'data de publicação: ',
                },
                {
                    'field': 'quadro',
                    'prefix': 'quadro: ',
                },
                {
                    'field': 'hashtag',
                    'prefix': 'hashtag: ',
                },
                {
                    'field': 'characters',
                    'prefix': 'personagens: ',
                }
            ]

            # get transcription attributes
            transcription = dict()
            for header in transcription_header:
                for metadata in header_metadata:
                    if header.startswith(metadata['prefix']):
                        transcription[metadata['field']] = header.removeprefix(metadata['prefix'])
            transcription['transcription'] = transcription_content
            
            # add episode transcription to all transcriptions
            all_transcriptions[quadro].append(transcription)

        except Exception as e:
            print(f'Error extracting transcription from: {link}. Error: {e}')


# save transcriptions to json file
for quadro, transcriptions in all_transcriptions.items():
    with open(f"./transcriptions/{quadro}.json", "w", encoding='utf-8') as jsonFile:
        json.dump(transcriptions, jsonFile, indent=4, ensure_ascii=False)