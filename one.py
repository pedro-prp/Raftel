import requests
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


if __name__ == '__main__':
    browser = webdriver.Firefox()
    manga_number = 5

    chapter_path = build_chapter_directory(manga_number)
    pages = get_chapter_pages(browser, manga_number)
    for page_data in iter_pages(browser, pages):
        save_page(chapter_path, *page_data)

    browser.close()
