from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")

quadro = sys.argv[1]

quadro_link = f"https://naoinviabilize.com.br/quadros/{quadro}/"

driver = webdriver.Chrome(options=options)
driver.get(quadro_link)
pages = driver.find_elements(By.CLASS_NAME, 'page-numbers')
n_pages = pages[-2].get_attribute("text")
eps_links = ""
for i in range(1, int(n_pages)+1):
    driver.get(f"{quadro_link}page/{i}/")

    n_eps = driver.find_element(By.XPATH, '//*[@id="ajax-content-wrap"]/div[2]/div/div/div[1]/div[1]').get_attribute("childElementCount")
    
    for i in range(1, int(n_eps)+1):
        ep_link = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[3]/div[2]/div/div/div[1]/div[1]/article[{i}]/div/div/div/a').get_attribute("href")
        # eps_links.append(ep_link)
        eps_links += f"{ep_link}\n"

driver.close()

with open (f"{quadro}-links.txt", "w") as txtFile:
    txtFile.write(eps_links)