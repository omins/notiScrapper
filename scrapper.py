from bs4 import BeautifulSoup
from datetime import date, timedelta
import requests
import time
import telegram
import myToken

TOKEN = myToken.TOKEN
CHAT_ID = myToken.CHAT_ID
# Fixed values

url = "https://teaching.korea.ac.kr/teaching/community/notice1.do"

# Telegram bot
bot = telegram.Bot(token=TOKEN)

# request, bs4
res = requests.get(url)
res.raise_for_status()
soup = BeautifulSoup(res.text, "html.parser")


# 클래스 구분이 명확하지 않은 페이지에서 공지사항 리스트(ul) 추출(사이트 구조 변경 시 수정 필요)
toFindNotice = soup.findAll("ul", attrs={"class": "m"})
grabedNotice = toFindNotice[1]

# 각 공지사항의 element에 접근하기 위해 공지사항 li elements를 리스트 자료구조로 변환
noticeList = grabedNotice.findAll('li')

# 오늘 날짜
today = date.today().isoformat().replace('-', '.')

# 공지사항 전송
for notice in noticeList:
    postDate = notice.span.get_text().replace('교직팀', '')

    if(today == postDate):  # 오늘 게시글이 있으면
        title = notice.a.get_text()
        noticeUrl = 'https://teaching.korea.ac.kr/teaching/community/notice1.do' + \
            notice.a['href']
        feed = f'{title}\n\n게시일: {postDate}\n\n링크: {noticeUrl}'

        bot.send_message(text=feed, chat_id=CHAT_ID)
        time.sleep(2)
    else:
        continue
