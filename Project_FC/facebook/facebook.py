from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from login import get_user

SEARCH_URL = "https://www.facebook.com/search/videos/?q={}"
LOGIN_URL = "https://www.facebook.com/"
DRIVER_DIR = '/Users/temp/Project_FC/chromedriver'

ID, PW = get_user()

def facebook_scrap(keyword):
    try:
        driver = webdriver.Chrome(DRIVER_DIR)
        driver.implicitly_wait(10)
        driver.get(LOGIN_URL)
        time.sleep(1)
        e = driver.find_element_by_id('email')
        e.clear()
        e.send_keys(ID)
        e = driver.find_element_by_id('pass')
        e.clear()
        e.send_keys(PW)
        e.send_keys(Keys.ENTER)
        print('로그인')
        
        driver.get(SEARCH_URL.format(keyword))
                
        links = [] 
        for link in driver.find_elements_by_css_selector('div._14ax > a'): # 링크 a 태그 찾기             
            links.append(link.get_attribute('href'))
            break
        
        print('content-len:', len(links))

        for link in links:
            driver.implicitly_wait(10)
            driver.get(link) # 개별 링크 접속 
        
            author = driver.find_element_by_class_name('_371y').text # 작성자
            likes = driver.find_element_by_class_name('_1g5v').text # 좋아요 수
            com_share = driver.find_elements_by_class_name('_36_q') 
            com = com_share[0].text # 코멘트
            share = com_share[1].text # 공유수
            print('(글 정보) ->', author, likes, com, share)

            time.sleep(1.5) # 대기
            comment_btn = driver.find_element_by_class_name('_2xui') # 댓글 보기
            comment_btn.click() # 클릭
            time.sleep(1.5) # 대기
            try:
                view_more = driver.find_element_by_class_name('UFIPagerLink')
                view_more.click() # 댓글 더보기 클릭
            except:
                pass

            classes = driver.find_elements_by_class_name('UFICommentActorAndBodySpacing')

            for clas in classes:
                user = clas.find_element_by_css_selector('div.UFICommentActorAndBodySpacing > span > a').text # 글쓴이
                reply = clas.find_element_by_class_name('UFICommentBody').text # 댓글
                print("({}): {}".format(user, reply))
    except Exception as e:
        print(e)
    finally:
        driver.quit()

if __name__ == "__main__":
    keyword = input('keyword?')
    facebook_scrap(str(keyword))