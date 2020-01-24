import requests
import argparse
from selenium.webdriver.firefox.options import Options
from pathlib import Path
from selenium import webdriver


def get_chapter_pages(browser: webdriver, chapter: int) -> int:
    """Get the number of pages in the specified chapter"""
    browser.get(f'https://onepieceex.net/mangas/leitor/{chapter}/')
    pages = browser.find_element_by_xpath('//*[@id="mangapaginas"]')
    return pages.find_elements_by_tag_name("li")
    

def build_chapter_directory(chapter: int) -> Path:
    """Build directory structure to chapter"""
    chapter_path = Path(f'./chapters/{chapter}')
    if not chapter_path.exists():
        chapter_path.mkdir(parents=True, exist_ok=True)

    return chapter_path


def save_page(
    chapter_path: Path,
    page_url: str,
    page_number: int,
    image_ext: str
):
    """Download page and save"""
    mime_file = requests.get(page_url, allow_redirects=True)
    page = chapter_path / f'{page_number}.{image_ext}'
    page.open(mode='wb').write(mime_file.content)


def iter_pages(
    browser: webdriver,
    pages: list
):
    """Yields page data"""
    for i in range(len(pages)-1):
        pages[i].click()
        raw_src = browser.find_element_by_xpath(
            '/html/body/div[1]/div[3]/div[4]/a/img'
        )
        src = raw_src.get_attribute('outerHTML').split('src=')[1].split('"')[1]
        ext = src.split('.')[-1]
        url = f'https://onepieceex.net' + src
        page_number = i + 1
        yield (url, page_number, ext)


def build_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-c',
                      '--chapter',
                      action='store',
                      type=int,
                      dest='chapter_number')
    parser.add_argument('-a',
                      '--all',
                      dest='all',
                      action='store_true')
    parser.add_argument('-i',
                      '--interval',
                      nargs=2,
                      type=int,
                      action='store',
                      dest='interval')

    return parser.parse_args()


def build_browser():
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)

    return browser


def get_last_chapter(browser: webdriver):
    browser.get('https://onepieceex.net/mangas/')

    volume_elem = browser.find_element_by_xpath('//*[@id="volumes"]')
    volumes_list = volume_elem.find_elements_by_tag_name("li")
    vol_last_number = volumes_list[-1].get_attribute('outerHTML')

    vol_last_number = vol_last_number.split('span>')[1].split('.')[0]

    return int(vol_last_number)


def download_chapter(
    browser: webdriver,
    chapter: int
):
    """Download single chapter"""
    chapter_path = build_chapter_directory(chapter)
    pages = get_chapter_pages(browser, chapter)
    for page_data in iter_pages(browser, pages):
        save_page(chapter_path, *page_data)


def download_chapter_range(
    browser: webdriver,
    start: int,
    end: int
):
    """Download a list of chapters"""
    for chapter in range(start, (end-1)):
        download_chapter(browser, chapter)


def download_all_chapters(browser: webdriver):
    last_chapter = get_last_chapter(browser)
    for chapter in range(1, (last_chapter + 1)):
        download_chapter(browser, chapter)

if __name__ == '__main__':
    browser = build_browser()
    args = build_args()
    
    if args.all:
        download_all_chapters(browser)
    elif args.interval:
        download_chapter_range(browser, *args.interval)
    elif args.chapter_number:
        download_chapter(browser, args.chapter_number)

    # manga_number = 5

    # chapter_path = build_chapter_directory(manga_number)
    # pages = get_chapter_pages(browser, manga_number)
    # for page_data in iter_pages(browser, pages):
    #     save_page(chapter_path, *page_data)

    browser.close()

# ============================================================================= #

# from selenium import webdriver
# import argparse
# import requests
# import sys
# import os


# def main():
#     args = build_args()

#     browser = build_browser()

#     if args['all']:
#         last_chapter = get_last_chapter_number(browser)

#         download_all(browser, last_chapter)
#     elif args['interval']:
#         download_in_interval(
#             browser,
#             args['interval'][0],
#             args['interval'][1]
#         )
#     else:
#         chapter = args['chapter_number']

#         download_one(browser, chapter)

#     browser.close()


# def build_browser():
#     options = Options()
#     options.headless = True
#     browser = webdriver.Firefox(options=options)
#     # browser = webdriver.Firefox()

#     return browser


# def download_all(browser, last_chapter):
#     for i in range(1, (last_chapter+1)):
#         download_one(browser, i)


# def download_in_interval(browser, min, max):
#     for i in range(min, (max+1)):
#         download_one(browser, i)


# def download_one(browser, chapter):
#     print(f'Downloading chapter {chapter}')

#     try:
#         os.mkdir('cap-' + str(chapter))

#         browser.get(f'https://onepieceex.net/mangas/leitor/{chapter}/')

#         pages = browser.find_element_by_xpath('//*[@id="mangapaginas"]')
#         pages = pages.find_elements_by_tag_name("li")

#         for i in range(len(pages)-1):
#             print('.', end='')
#             sys.stdout.flush()

#             pages[i].click()

#             src = build_img_src(browser)

#             url = f'https://onepieceex.net' + src

#             path = build_path(src, chapter, i)

#             media = requests.get(url, allow_redirects=True)

#             open(path, 'wb').write(media.content)

#         sys.stdout.flush()
#         print('')

#     except Exception:
#         print('already downloaded')


# def build_args():
#     args = argparse.ArgumentParser()

#     args.add_argument('-c',
#                       '--chapter',
#                       action='store',
#                       type=int,
#                       dest='chapter_number')

#     args.add_argument('-a',
#                       '--all',
#                       action='store_true')

#     args.add_argument('-i',
#                       '--interval',
#                       nargs=2,
#                       type=int,
#                       action='store',
#                       dest='interval')

#     args = args.parse_args()

#     return vars(args)


# def get_last_chapter_number(browser):
#     browser.get('https://onepieceex.net/mangas/')

#     vol_elem = browser.find_element_by_xpath('//*[@id="volumes"]')
#     vol_list = vol_elem.find_elements_by_tag_name("li")
#     vol_last_number = vol_list[-1].get_attribute('outerHTML')

#     vol_last_number = vol_last_number.split('span>')[1].split('.')[0]

#     return int(vol_last_number)


# def build_img_src(browser):
#     src_elem = browser.find_element_by_xpath(
#                 '/html/body/div[1]/div[3]/div[4]/a/img'
#     )

#     str_src = src_elem.get_attribute('outerHTML')

#     str_src = str_src.split('src=')[1].split('"')[1]

#     return str_src


# def build_path(str_src, manga_number, i):
#     ext = str_src.split('.')[-1]

#     path = f'./cap-{manga_number}/{i+1}.{ext}'

#     return path


# if __name__ == '__main__':
#     main()
