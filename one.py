import requests
import os
from pathlib import Path
from selenium import webdriver

browser = webdriver.Firefox()
manga_number = 1
browser.get(f'https://onepieceex.net/mangas/leitor/{manga_number}/')
num_page = browser.find_element_by_xpath('//*[@id="mangapaginas"]')
num_page = num_page.find_elements_by_tag_name("li")

try:
    chap_path = Path(f'./chapters/{manga_number}')
    if not chap_path.exists():
        chap_path.mkdir(parents=True, exist_ok=True)
    for i in range(len(num_page)-1):
        num_page[i].click()
        str_src = browser.find_element_by_xpath(
            '/html/body/div[1]/div[3]/div[4]/a/img'
        )
        src = str_src.get_attribute('outerHTML').split('src=')[1].split('"')[1]
        ext = src.split('.')[-1]
        url = f'https://onepieceex.net' + src
        mfile = requests.get(url, allow_redirects=True)
        page = chap_path / f'{i+1}.{ext}'
        page.open(mode='wb').write(mfile.content)
except Exception as err:
    print(err)
    print('already downloaded')

browser.close()
