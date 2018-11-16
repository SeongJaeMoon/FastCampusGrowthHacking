import time
from selenium import webdriver

URL = 'https://www.instagram.com/explore/tags/{}'
DRIVER_DIR = '/Users/temp/Project_FC/chromedriver'

def instagram_scrap(keyword):
    try:
        driver = webdriver.Chrome(DRIVER_DIR)
        driver.implicitly_wait(10)
        driver.get(URL.format(keyword))
    
        new_links = driver.find_elements_by_css_selector('div.v1Nh3 > a')            
        links = [i.get_attribute('href') for i in new_links]
        print('content-length: ',  len(links))
        
        for link in links:
            driver.get(link)
            time.sleep(1)
            for li in driver.find_elements_by_class_name('C4VMK'):
                user = li.find_element_by_tag_name('a').text # 작성자
                reply = li.find_element_by_tag_name('span').text # 댓글, 해시태그
                print("({}) {}".format(user, reply))
    except Exception as e:
        print(e)
    finally:
        driver.quit()

if __name__ == "__main__":
    keyword = input('keyword(tag)') # 키워드
    instagram_scrap(str(keyword))



    
