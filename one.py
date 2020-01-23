from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import argparse
import requests
import os


def main():
    args = build_args()

    manga_number = vars(args)['chapter_number']

    browser = build_browser()

    browser.get(f'https://onepieceex.net/mangas/leitor/{manga_number}/')

    pages = browser.find_element_by_xpath('//*[@id="mangapaginas"]')
    pages = pages.find_elements_by_tag_name("li")

    try:
        os.mkdir('cap-' + str(manga_number))

        for i in range(len(pages)-1):
            pages[i].click()

            src = build_img_src(browser)

            url = f'https://onepieceex.net' + src

            path = build_path(src, manga_number, i)

            media = requests.get(url, allow_redirects=True)

            open(path, 'wb').write(media.content)

    except Exception:
        print('already downloaded')

    browser.close()


def build_browser():
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)

    return browser


def build_args():
    args = argparse.ArgumentParser()

    args.add_argument('-c',
                      '--chapter',
                      action='store',
                      type=int,
                      dest='chapter_number')

    args = args.parse_args()

    return args


def build_img_src(browser):
    src_elem = browser.find_element_by_xpath(
                '/html/body/div[1]/div[3]/div[4]/a/img'
    )

    str_src = src_elem.get_attribute('outerHTML')

    str_src = str_src.split('src=')[1].split('"')[1]

    return str_src


def build_path(str_src, manga_number, i):
    ext = str_src.split('.')[-1]

    path = f'./cap-{manga_number}/{i+1}.{ext}'

    return path


if __name__ == '__main__':
    main()
