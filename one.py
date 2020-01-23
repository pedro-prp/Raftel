from selenium import webdriver
import requests
import os


def main():
    browser = webdriver.Firefox()

    manga_number = 353

    browser.get(f'https://onepieceex.net/mangas/leitor/{manga_number}/')

    num_page = browser.find_element_by_xpath('//*[@id="mangapaginas"]')

    num_page = num_page.find_elements_by_tag_name("li")
    try:
        os.mkdir('cap-' + str(manga_number))

        for i in range(len(num_page)-1):
            num_page[i].click()

            src_elem = browser.find_element_by_xpath(
                '/html/body/div[1]/div[3]/div[4]/a/img'
            )

            str_src = (
                src_elem.get_attribute('outerHTML')
                .split('src=')[1]
                .split('"')[1]
            )

            url = f'https://onepieceex.net' + str_src
            media = requests.get(url, allow_redirects=True)

            ext = str_src.split('.')[-1]

            path = f'./cap-{manga_number}/{i+1}.{ext}'

            open(path, 'wb').write(media.content)

    except Exception:
        print('already downloaded')

    browser.close()


if __name__ == '__main__':
    main()
