import random
import re
import urllib.request
import requests
from bs4 import BeautifulSoup
import sendEmail
from requests.adapters import HTTPAdapter
import os

class hot_topic(object):
    def __init__(self,spot_topic:str):
        self.spot_topic=spot_topic

    def getRandomAgent(self):
        USER_AGENTS = [
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11"
            "Mozilla/5.0 (iphone x Build/MXB48T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN"
            "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043807 Mobile Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN"
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)"
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        ]
        return USER_AGENTS[random.randint(0, 9)]

    def crawl_his_tops(self):
        headers={
            "user-agent":self.getRandomAgent(),
        }


        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=6))
        s.mount('https://', HTTPAdapter(max_retries=6))

        # print(time.strftime('%Y-%m-%d %H:%M:%S'))
        try:
            rp = s.get(self.spot_topic, headers=headers, timeout=6)
            # return r.text
        except requests.exceptions.RequestException as e:
            print(e)
        # print(time.strftime('%Y-%m-%d %H:%M:%S'))
        #     rp = s.get(self.spot_topic, headers=headers, timeout=5)



        soup = BeautifulSoup(rp.content,'lxml')
        his_feeds=soup.find_all(attrs={'class':'jc-c'})[1]
        spot_topic_set=[]
        for his_news in his_feeds.find_all('tr'):
            entry=his_news.find_all('td')
            entry_content={
                "标题":entry[1].get_text(),
                "热度":entry[2].get_text(),
                "链接":domain + entry[1].a.attrs['href']
            }
            spot_topic_set.append(entry_content)
        return spot_topic_set



if __name__ == '__main__':
    websites={
        # '新浪热搜': "https://tophub.today/n/KqndgxeLl9",  # 新浪热搜
        # '知乎热榜': "https://tophub.today/n/mproPpoq6O",  # 知乎热榜
        # '百度热榜': "https://tophub.today/n/Jb0vmloB1G",  # 百度热榜
        # '36氪': "https://tophub.today/n/Q1Vd5Ko85R",  # 36氪
        # '少数派': "https://tophub.today/n/Y2KeDGQdNP",  # 少数派
        # '虎嗅网': "https://tophub.today/n/5VaobgvAj1",  # 虎嗅网
        '虎扑社区 步行街热帖': "https://tophub.today/n/G47o8weMmN",  # 虎扑社区 步行街热帖
        '虎扑社区 影音娱乐热帖': "https://tophub.today/n/K7Gda2XeQy",  # 虎扑社区 影音娱乐热帖
        # '虎扑社区 恋爱区热帖': "https://tophub.today/n/wkvlEkYdz1",  # 虎扑社区 恋爱区热帖
        '吾爱破解 今日热帖': "https://tophub.today/n/NKGoRAzel6",  # 吾爱破解 今日热帖
        '吾爱破解 人气热门': "https://tophub.today/n/Ywv41YMdPa",  # 吾爱破解 人气热门
        '吾爱破解 精品软件区': "https://tophub.today/n/ENeYLEZdY4",  # 吾爱破解 精品软件区
        '吾爱破解 原创发布区': "https://tophub.today/n/qndgO7LdLl",  # 吾爱破解 原创发布区
        '哔哩哔哩 全站日榜': "https://tophub.today/n/74KvxwokxM",  # 哔哩哔哩 全站日榜
        'AppSo网': "https://tophub.today/n/YqoXQLXvOD",  # AppSo网
        '酷安 今日图文': "https://tophub.today/n/MZd7wnDdrO",  # 酷安 今日图文
        'V2EX 今日热议': "https://tophub.today/n/wWmoORe4EO",  # V2EX 今日热议
        'V2EX 分享创造': "https://tophub.today/n/4MdALJlvxD",  # V2EX 分享创造


    }

    domain="https://tophub.today"
    SCKEY = os.environ["SCKEY"]

    my_sender = '1449621606@qq.com'  # 发件人邮箱账号
    my_sender_alias = '爬虫机器人'  # 发件人邮箱别名
    my_pass = SCKEY  # 发件人邮箱密码
    my_user = '1449621606@qq.com'  # 收件人邮箱账号，我这边发送给自己
    my_user_alias = '一周热门新闻'  # 收件人邮箱账号别名
    websites_brief=""

    for key,value in websites.items():
        website_ttile = key
        spot_topic_set=hot_topic(websites[website_ttile]).crawl_his_tops()
        website_context="\n".join(["<tr><td>"+spot["热度"] + "<a href=" + spot["链接"] +">" + spot["标题"] + "</a></td></tr>" for spot in spot_topic_set ])
        website_section="<table><tr>{}</tr>{}</table>".format(website_ttile,website_context)
        websites_brief +=website_section
#         print(website_section)
    context_ttile="一周热门新闻"
    sd = sendEmail.send_mail(my_sender, my_pass, my_user, context=websites_brief, my_sender_alias=my_sender_alias, my_user_alias=my_user_alias,tittle=context_ttile)
    sd.make_message()
    sd.send_mail()
    print("完成{}邮件发送".format(context_ttile))
