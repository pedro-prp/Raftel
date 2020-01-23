from selenium import webdriver
import requests
import os

browser = webdriver.Firefox()

manga_number = 1

browser.get(f'https://onepieceex.net/mangas/leitor/{manga_number}/')

num_page = browser.find_element_by_xpath('//*[@id="mangapaginas"]')

num_page = num_page.find_elements_by_tag_name("li")
try:
    os.mkdir('cap-' + str(manga_number))

    for i in range(len(num_page)-1):
        num_page[i].click()

        str_src = browser.find_element_by_xpath(
            '/html/body/div[1]/div[3]/div[4]/a/img'
        )

        src = str_src.get_attribute('outerHTML').split('src=')[1].split('"')[1]

        ext = src.split('.')[-1]

        url = f'https://onepieceex.net' + src

        mfile = requests.get(url, allow_redirects=True)

        open(f'./cap-{manga_number}/{i+1}.{ext}', 'wb').write(mfile.content)

except Exception as err:
    print(err)
    print('already downloaded')

browser.close()
