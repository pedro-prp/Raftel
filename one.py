from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import argparse
import requests
import sys
import os


def main():
    args = build_args()

    browser = build_browser()

    if args['all']:
        last_chapter = get_last_chapter_number(browser)

        download_all(browser, last_chapter)
    elif args['interval']:
        download_in_interval(
            browser,
            args['interval'][0],
            args['interval'][1]
        )
    else:
        chapter = args['chapter_number']

        download_one(browser, chapter)

    browser.close()


def build_browser():
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    # browser = webdriver.Firefox()

    return browser


def download_all(browser, last_chapter):
    for i in range(1, (last_chapter+1)):
        download_one(browser, i)


def download_in_interval(browser, min, max):
    for i in range(min, (max+1)):
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

        sys.stdout.flush()
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

    args.add_argument('-i',
                      '--interval',
                      nargs=2,
                      type=int,
                      action='store',
                      dest='interval')

    args = args.parse_args()

    return vars(args)


def get_last_chapter_number(browser):
    browser.get('https://onepieceex.net/mangas/')

    vol_elem = browser.find_element_by_xpath('//*[@id="volumes"]')
    vol_list = vol_elem.find_elements_by_tag_name("li")
    vol_last_number = vol_list[-1].get_attribute('outerHTML')

    vol_last_number = vol_last_number.split('span>')[1].split('.')[0]

    return int(vol_last_number)


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
