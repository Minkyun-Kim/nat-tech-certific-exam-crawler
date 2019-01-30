import os
import requests
from bs4 import BeautifulSoup


if __name__ == '__main__':
    urls = ["https://www.comcbt.com/xe/j4","https://www.comcbt.com/xe/index.php?mid=j4&page=2","https://www.comcbt.com/xe/index.php?mid=j4&page=3"]
    if not (os.path.isdir("기출")):
        os.makedirs(os.path.join("기출"))
    for url in urls:
        html_doc = requests.get(url)
        soup = BeautifulSoup(html_doc.text, 'html.parser')
        for link in soup.find_all('a', {'class':'hx'}):
            link = link.get('href')
            html = requests.get(link)
            parsed = BeautifulSoup(html.text, 'html.parser')
            for link2 in parsed.find_all('a'):
                if ".hwp" in link2.get_text():
                    filename = link2.get_text()
                    path = link2.get('href')
                    with open("기출/" + filename, "wb") as file:
                        response = requests.get(path)
                        file.write(response.content)