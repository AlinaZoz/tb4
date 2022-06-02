
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


def get_meme():
    url = ""
    images = []
    page_link = 'https://knowyourmeme.com/random'.format(get_meme)
    response = requests.get(page_link, headers={'User-Agent': UserAgent().chrome})

    if page_link.status_code == 200:
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')

        meme_links = soup.findAll(lambda tag: tag.name == 'a' and tag.get('class') == ['photo'])
        meme_links = ['http://knowyourmeme.com' + link.attrs['href'] for link in meme_links]
        for img in meme_links.findAll('img'):
            images.append(img.get('src'))





