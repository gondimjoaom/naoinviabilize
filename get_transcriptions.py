from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys, json
from tqdm import tqdm

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")

links_file = sys.argv[1]

quadro = links_file.split(".")[0]

with open(links_file, 'r') as txtLinks:
    links = txtLinks.read()
driver = webdriver.Chrome(options=options)

transcriptions = {}

for link in tqdm(links.split("\n")[:-1]):
    
    driver.get(link)
    try:
        # texts_div = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div[2]/div/div[1]/div/article/div/div/div')
        # content-inner
        texts_div = driver.find_element(By.CLASS_NAME, 'content-inner')
    except:
        print(link)
    texts = texts_div.find_elements(By.CSS_SELECTOR, "p")
    # print(text)
    # print(len(text))
    n_texts = len(texts)
    # /html/body/div[1]/div/div[3]/div[2]/div/div[1]/div/article/div/div/div/p[17]
    transcription = ""
    for n in range(1, n_texts+1):
        # try:
        #     # text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div[3]/div[2]/div/div[1]/div/article/div/div/div/p[{n}]")
        #     #                                         /html/body/div[1]/div/div[3]/div[1]/div/div[1]/div/article/div/div/div/p[1]
        #     #                                         /html/body/div[1]/div/div[3]/div[1]/div/div[1]/div/article/div/div/div/p[2]
        # except:
        #     print(link)
        text_content = texts[n-1].get_attribute("innerHTML")
        transcription += f"{text_content}\n"
    
    name = link.split("/")[-2]
    transcriptions[name] = {
        "link" : link,
        "quadro" : quadro,
        "transcrição" : transcription
    }
    # break

with open(f"{quadro}.json", "w", encoding='utf-8') as jsonFile:
    json.dump(transcriptions, jsonFile, indent=4, ensure_ascii=False)

#     break
# print(transcriptions)
    # texts = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div[3]/div[2]/div/div[1]/div/article/div/div/div/p[1]')
                                            # /html/body/div[1]/div/div[3]/div[2]/div/div[1]/div/article/div/div/div/p[2]
# /html/body/div[1]/div/div[3]/div[2]/div/div[1]/div/article/div/div/div/p[1]
