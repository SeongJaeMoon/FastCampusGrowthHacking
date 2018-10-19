from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time 
from login import get_user

URL = "https://nid.naver.com/nidlogin.login"
DRIVER_DIR = '/Users/temp/Project_FC/chromedriver'

ID, PW = get_user()

def naver_scrap():
    try:
        driver = webdriver.Chrome(DRIVER_DIR)
        driver.implicitly_wait(10)
        driver.get(URL)
        print("로그인 페이지에 접근")

        e = driver.find_element_by_id("id")
        e.clear()
        e.send_keys(ID)

        e = driver.find_element_by_id("pw")
        e.clear()
        e.send_keys(PW)

        form = driver.find_element_by_css_selector("input.btn_global[type=submit]")
        form.submit()
        print("로그인 버튼을 클릭")

        # BASE 시작 냥이네 자유게시판 
        driver.get('https://cafe.naver.com/clubpet?iframe_url=/ArticleList.nhn%3Fsearch.clubid=10625072%26search.menuid=221%26search.boardtype=L%26search.questionTab=A%26search.totalCount=151%26search.page=1')
        driver.switch_to.frame('cafe_main')
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        BASE = 'https://cafe.naver.com/'
        spans = []
        # link 주소 
        for span_tag in soup.select('table.board-box > tbody span.aaa'):
            spans.append(BASE + str(span_tag.find('a')['href']))

        for idx, span in enumerate(spans):
            driver.get(span) # 하나의 페이지
            driver.switch_to.frame('cafe_main') # iframe 가져오기    
            html = driver.page_source # 페이지 소스 가져오기
            soup = BeautifulSoup(html, 'html.parser') # 페이지 소스 html 코드로 파싱

            t = soup.select('div#main-area div.inbox')[0] # 본문 내용 가져오기
            author = t.select('div.fl td.p-nick a')[0].get_text() # 글쓴이
            print('(글쓴이)-> ', author) 
                    
            cmt_list = t.find('ul', attrs={'id':'cmt_list'}) # 댓글 목록
            for com in cmt_list.select('li'):
                user = com.find('a', attrs={'class': '_nickUI'}) # 댓글 작성자
                date = com.find('span', attrs={'class', 'date'}) # 작성 날짜
                comm = com.find('span', attrs={'class', 'comm_body'}) # 작성 글
                if user is not None: # 사용자가 있다면
                    print(user.get_text(), date.get_text(), comm.get_text())
    except Exception as e:
        print(e)
    finally:
        driver.close()

if __name__ == "__main__":
    naver_scrap()