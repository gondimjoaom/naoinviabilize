from selenium import webdriver
from selenium.webdriver.common.by import By

from pathlib import Path
from tqdm import tqdm

# selenium setup
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)


# set file path
quadros_file_path = Path('./quadros.txt')


# get quadros from file
quadros = []

with quadros_file_path.open('r') as quadros_file:
    text = quadros_file.read()
    quadros = text.split('\n')[:-1]


# retrieve all episodes for each quadro
all_episodes = dict()

for quadro in tqdm(quadros):
    quadro_link = f"https://naoinviabilize.com.br/quadros/{quadro}/"

    try:
        driver.get(quadro_link)

        pages = driver.find_elements(By.CLASS_NAME, 'page-numbers')
        n_pages = pages[-2].get_attribute("text")
        eps_links = []

        for i in range(1, int(n_pages)+1):
            driver.get(f"{quadro_link}page/{i}")

            n_eps = driver.find_element(By.XPATH, '//*[@id="ajax-content-wrap"]/div[2]/div/div/div[1]/div[1]').get_attribute("childElementCount")
            
            for i in range(1, int(n_eps)+1):
                ep_link = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[3]/div[2]/div/div/div[1]/div[1]/article[{i}]/div/div/div/a').get_attribute("href")
                eps_links.append(ep_link)

        all_episodes[quadro] = eps_links
    except Exception as e:
        print(f'Error retrieving episodes from: {quadro_link}. Error: {e}')


driver.close()

# save episode links from each quadro
for quadro, episodes_links in all_episodes.items():
    links_file = Path(f"./links/{quadro}.txt")
    links_file.parent.mkdir(exist_ok=True, parents=True)
    
    with links_file.open("w") as text_file:
        txt_episodes_links = '\n'.join(episodes_links)
        text_file.write(txt_episodes_links)