from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import argparse
import requests
import sys
import os


def main():
    args = build_args()

    browser = build_browser()

    if vars(args)['all']:
        download_all(browser)
    else:
        chapter = vars(args)['chapter_number']

        download_one(browser, chapter)

    browser.close()


def build_browser():
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    # browser = webdriver.Firefox()

    return browser


def download_all(browser):
    for i in range(1, 4):
        download_one(browser, i)


def download_one(browser, chapter):
    print(f'Downloading chapter {chapter}')

    try:
        os.mkdir('cap-' + str(chapter))

        browser.get(f'https://onepieceex.net/mangas/leitor/{chapter}/')

        pages = browser.find_element_by_xpath('//*[@id="mangapaginas"]')
        pages = pages.find_elements_by_tag_name("li")

        for i in range(len(pages)-1):
            print('.', end='')
            sys.stdout.flush()

            pages[i].click()

            src = build_img_src(browser)

            url = f'https://onepieceex.net' + src

            path = build_path(src, chapter, i)

            media = requests.get(url, allow_redirects=True)

            open(path, 'wb').write(media.content)

        print('')

    except Exception:
        print('already downloaded')


def build_args():
    args = argparse.ArgumentParser()

    args.add_argument('-c',
                      '--chapter',
                      action='store',
                      type=int,
                      dest='chapter_number')

    args.add_argument('-a',
                      '--all',
                      action='store_true')

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
