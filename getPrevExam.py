import os
import requests
from bs4 import BeautifulSoup

def getPreviousExam(url, dir):
    while 1:
        html_doc = requests.get(url)
        soup = BeautifulSoup(html_doc.text, 'html.parser')
        # located in subject board
        for link in soup.find_all('a', {'class':'hx'}):
            link = link.get('href')
            html = requests.get(link)
            parsed = BeautifulSoup(html.text, 'html.parser')
            # located in specific test board to get download
            for link2 in parsed.find_all('a', attrs={'class': 'bubble'}):
                if ".hwp"in link2.get_text() or "pdf" in link2.get_text():
                    filename = link2.get_text()
                    downloadURL = link2.get('href')
                    if not os.path.isfile(dir + "/" + filename):
                        print(filename + "파일을 다운로드 받습니다.")
                        with open(dir + "/" + filename, "wb") as file:
                            response = requests.get(downloadURL)
                            file.write(response.content)
                    else:
                        print(filename + "이 이미 존재합니다.")
        soup1 = soup.find('fieldset').find_all('a', attrs={'class': 'direction'})
        if soup1[0].get_text() != "Next ":
            if len(soup1) != 1:
                url = soup1[1].get('href')
            else :
                return
        else:
            url = soup1[0].get('href')


def run():
    url = "https://www.comcbt.com"
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    table = soup.find('table', attrs={'bgcolor': '#C0C0C0'})
    print("////////////////////////////////////////////////////////////////////////")
    print("////                                                                ////")
    print("////             국 가  시 험  기 출  문 제  다 운 로 드            ////")
    print("////                                                                ////")
    print("////       기능사 / 산업기사 / 기사 / 수능 / ERP / FAT / TAT        ////")
    print("////              한국사 / 컴퓨터활용능력 / 워드프로세서            ////")
    print("////                                                                ////")
    print("////////////////////////////////////////////////////////////////////////")
    print("")
    print("과목명을 입력해주세요(ex : 정보처리기사   전기기사) : ", end = '')
    subject = input()
    print("")
    print(subject + "과목을 찾는 중입니다.")
    print("")
    for subjectString in table.find_all('a'):
        if subject in subjectString.get_text():
            dir = subjectString.get_text()
            print(dir + "과목을 찾았습니다.")
            print("")
            if not (os.path.isdir(dir)):
                os.makedirs(os.path.join(dir))
            getPreviousExam("https://" + subjectString.get('href')[2:], dir)
    print("다운로드가 완료 되었습니다.")

if __name__ == '__main__':
    run()
