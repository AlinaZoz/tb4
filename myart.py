import requests
import bs4
class art:
    def __init__(self, pic):
        self.picURL = ""
        
    def getRandomFilm(self):
    url = "https://vk.com/albums-183412821"
    req_art = requests.get(url)
    if req_art.status_code == 200:
        soup = bs4.BeautifulSoup(req_art.text, "html.parser")
        result_find = soup.find('div', id='photo_row_', class_="photos_row ", style='background-image')
        images = []
        for img in result_find.findAll('img'):
            images.append(url + img.get('src'))
        art["art"] = images[0]