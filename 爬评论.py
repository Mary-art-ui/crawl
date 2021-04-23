# !/usr/bin/env/python
# -*- coding:utf-8 -*-  #pycharm的编码方式
#需求：
#总结：
import requests
import os
from lxml import etree
import re

if __name__ == "__main__":
    if not os.path.exists('./评论图片库'):
        os.mkdir('./评论图片库')
    # 爬取每个详情页面的id号placeid ，用于爬评论
    url = 'http://s.lvmama.com/ticket/K653100P%d?'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
    }
    fp1 = open('./star+comment.txt', 'w', encoding='utf-8')
    for pageNum in range(1, 21):
        # 对应页码的url
        new_url = format(url % pageNum)
        print(new_url)  # 显示每一页的url（不加请求参数）
        param = {
            'keyword': '山西',  # 错了半天发现k没写！！！！啊啊啊啊啊
            'tabType': 'ticket',
        }
        response = requests.get(url=new_url, params=param, headers=headers)
        result = response.text
        tree = etree.HTML(result)
        div_list = tree.xpath('//div[@class="product-item product-ticket searchTicket clearfix"]/div[1]')
        for div in div_list:
            if len(div.xpath('./div[1]/a/@title')) != 0:
                title = div.xpath('./div[1]/a/@title')[0]
            else:
                title = '0'
            detail_url = div.xpath('./div[1]/a/@href')[0]
            placeid = detail_url.split('-')[-1]  ##!!!!!关键点！！！
            # print(placeid)
            ## 用获得的placeid爬评论
            #与评论有关的包的url,post请求
            comment_url = 'http://ticket.lvmama.com/scenic_front/comment/newPaginationOfComments'
            # page = input("输入一个页码：")
            count = 0
            for page in range(1,2):   #每个景点评论的页数不同，都有第一页，但不一定有第二页第三页，否则就报错了。这里怎么办？
                count = count + 1
                data = {
                    'type': 'all',
                    'currentPage': page,       #？？
                    'totalCount': '46',
                    # 'placeId': '10672249',   #发现只要修改url的post请求参数，就可以获取不同项目的评论数据
                    'placeId': placeid,        #可以爬每一个景点的评论数据
                    'productId':'',
                    'placeIdType': 'PLACE',
                    'isPicture':'',
                    'isBest':'',
                    'isPOI': 'Y',
                    'isELong': 'N',
                }
                response = requests.post(url=comment_url,data=data,headers=headers)
                page_text = response.text
                # print(page_text)
                tree = etree.HTML(page_text)
                comment_div = tree.xpath('//div[@class="comment-li"]')  #一页10条评论
                for div in comment_div:
                    if len( div.xpath('./div[1]/p/span[1]/i/@data-level'))!=0:
                        star = div.xpath('./div[1]/p/span[1]/i/@data-level')[0]
                    else:
                        star = '0'
                    comment = div.xpath('./div[2]/text()')[1].strip()
                    fp1.write('景点项目：'+title+'\n'+'star:'+star+'   评价：'+comment+'\n\n')
                    comment_li_list = div.xpath('./div[4]/div/ul/li')
                    for j in comment_li_list:
                        comment_img_url = j.xpath('./img/@src')[0]
                        comment_img_data = requests.get(url=comment_img_url,headers=headers).content
                        img_name = comment_img_url.split('/')[-1]
                        imgPath = './评论图片库/' + img_name + '.jpg'
                        with open(imgPath, 'wb') as fp:
                            fp.write(comment_img_data)
                            print(count, '页的图片下载成功！')
                print("第%d页评论爬取完毕！！！" % count)
                print('----------------------------------------------------------------------------------')