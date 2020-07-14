# 下载网页
import requests
# 解析html
from bs4 import BeautifulSoup
# 保存为csv
import pandas as pd
# 美化打印
import pprint

# pageIndexs = range(0, 1, 25)
# 构造分页数据(我们要下载10个页面的数据，每个页面25条数据，总共250条)
pageIndexs = range(0, 250, 25)

# 1. 下载HTML
def downloadAllHTMLs():
    '''
    下载所有列表页面的HTML
    '''
    htmls = []
    for pageIndex in pageIndexs:
        # https://movie.douban.com/top250?start=0&filter=
        headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
        url = 'https://movie.douban.com/top250?start=' + str(pageIndex) + '&filter='
        print('craw html:', url)
        r = requests.get(url, headers = headers)
        if r.status_code != 200:
            raise r.raise_for_status()
        htmls.append(r.text)
    return htmls

# 2.解析html得到数据
def parseHTML(html):
    '''
    解析单个HTML，得到数据
    @return [{'rank', 'name', 'img_url', 'rating_num', 'comments'}]
    '''
    soup = BeautifulSoup(html, 'html.parser')
    # find()找到soup对象的一个标签入口
    # find_all()从文档中找到所有<div class='item'>的标签
    article_items = soup.find('div', class_='article').find('ol', class_='grid_view').find_all('div', class_='item')                         

    res = []
    for atricle_item in article_items:
        # get_text()从文档中获取所有文字内容:
        pic = atricle_item.find('div', class_='pic')
        rank = pic.find('em').get_text()
        img = pic.find('a').find('img')
        pic_url = img.get('src')
        name = img.get('alt')

        info = atricle_item.find('div', class_='info')
        stars = info.find('div', class_='bd').find('div', class_='star').find_all('span')
        rating_num = stars[1].get_text()
        comments = stars[-1].get_text()

        res.append({
            'rank': rank,
            'name': name,
            'rating_num': rating_num,
            'comments': comments,
            'img_url': pic_url                                   
        })
    return res

htmls = downloadAllHTMLs()        
datas = []
for html in htmls:
    data = parseHTML(html)
    datas.append(data)
pprint.pprint(datas)

# 3. 保存为csv
df = pd.DataFrame(datas)
df.to_csv("豆瓣电影TOP250.csv")
