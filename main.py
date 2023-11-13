from bs4 import BeautifulSoup
from queue import Queue 
import re
from pprint import pprint
from requests_html import HTMLSession
session = HTMLSession()

# init queue
q = Queue()
q.put("https://vnexpress.net/thu-ngan-sach-dat-gan-1-4-trieu-ty-dong-4676363.html")

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "vi,en-US;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
}

# get all link in queue
while not q.empty():
    link = q.get()
    page = session.get(link, headers=headers)
    page.html.render()
    print(page.html.absolute_links)
    break
    soup = BeautifulSoup(page.text, 'html.parser')
    links = soup.find_all('a', attrs={'href': re.compile("^https:\/\/vnexpress\.net\/.+\.html$")})
    print(links)
    for link in links:
        q.put(link.get("href"))
    
    
    print("Queue size: ", q.qsize())
    print("Link: ", link)
    

    
    #
    title_detail = soup.select_one('.title-detail')
    title_detail = title_detail.get_text()
    
    description = soup.select_one('.description')
    description = description.get_text()
    
       
    content = soup.select_one('.fck_detail')
    
    figcaptions = content.select('figcaption')
    for figcaption in figcaptions:
        figcaption.decompose()
    
    content = content.get_text()
    content = content.replace('\n', '')
    pprint(content)
    input()
    
    