# !/usr/bin/env/python
# -*- coding:utf-8 -*-  #pycharm的编码方式
#需求：
#总结：
import requests
import os
from lxml import etree
import re

if __name__ == "__main__":
    if not os.path.exists('./景点图片库'):
        os.mkdir('./景点图片库')
    #爬取页面源码数据
    url = 'http://s.lvmama.com/ticket/K653100P%d?'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
    }
    count = 0
    fp1 = open('./info.txt', 'w', encoding='utf-8')
    for pageNum in range(1,20):
        # 对应页码的url
        new_url = format(url%pageNum)
        print(new_url)
        param = {
            'keyword': '山西',   #错了半天发现k没写！！！！啊啊啊啊啊
            'tabType': 'ticket',
        }
        response = requests.get(url=new_url,params=param,headers=headers)
        result = response.text
        count += 1

        tree = etree.HTML(result)
        div_list = tree.xpath('//div[@class="product-item product-ticket searchTicket clearfix"]/div[1]')
        for div in div_list:
            if len(div.xpath('./div[1]/a/@href')) != 0:
                detail_url = div.xpath('./div[1]/a/@href')[0]

            else:
                detail_url = '0'
            if len(div.xpath('./div[1]/a/@title')) != 0:
                title = div.xpath('./div[1]/a/@title')[0]
            else:
                title = '0'
            if len(div.xpath('./div[2]/dl[1]/dd/text()')) != 0:
                address = div.xpath('./div[2]/dl[1]/dd/text()')[0].strip()
            else:
                address = '0'
            if len(div.xpath('./div[2]/dl[2]/dd//text()')) != 0:
                strinfo = re.compile('\n')
                open_time = div.xpath('./div[2]/dl[2]/dd//text()')[2].strip()
                open_time = strinfo.sub('', open_time)
                open_time = open_time.replace(' ', '')
            else:
                open_time = '0'
            if len(div.xpath('./div[2]/dl[3]/dd/text()')) != 0:
                topic = div.xpath('./div[2]/dl[3]/dd/text()')[0].strip()
            else:
                topic = '0'
            ##景点简介这里，不同页数对应的dl不同，从第6页开始只有3个dl，第六页之前有4个dl
            if pageNum < 6:
                if len(div.xpath('./div[2]/dl[4]/dd/div/text()')) != 0:
                    des = div.xpath('./div[2]/dl[4]/dd/div/text()')[1].strip()
                else:
                    des = '0'
            else:
                if len(div.xpath('./div[2]/dl[3]/dd/div/text()')) != 0:
                    des = div.xpath('./div[2]/dl[3]/dd/div/text()')[1].strip()
                else:
                    des = '0'
            if len(div.xpath('./div[3]/div/em/text()')) != 0:
                price = div.xpath('./div[3]/div/em/text()')[0]
            else:
                price = '0'
            if len(div.xpath('./div[3]/ul/li[1]/b/text()')) != 0:
                grade = div.xpath('./div[3]/ul/li[1]/b/text()')[0]
            else:
                grade = '0'
            if len(div.xpath('./div[3]/ul/li[2]/a/@href')) != 0:
                grade_url = div.xpath('./div[3]/ul/li[2]/a/@href')[0]
            else:
                grade_url = '0'
            if len(div.xpath('./div[3]/ul/li[2]/a/text()')) != 0:
                grade_from = div.xpath('./div[3]/ul/li[2]/a/text()')[0]
            else:
                grade_from = '0'

            print('\n'+title+'\n'+'主题:'+topic+'\n'+'详情页地址：'+detail_url+'\n'+'景点地址：'+address+'\n'+'开放时间：'+open_time)
            print('景点简介：'+des)
            print('价格：'+price)
            print('评分及评分链接：'+grade+'分 '+grade_from+':  '+grade_url)

            fp1.write(title+'\n'+'主题:'+topic+'\n'
                      +'详情页地址：'+detail_url+'\n'+'景点地址：'+address+'\n'
                      +'开放时间：'+open_time+'\n'+'景点简介：'+des+'\n'
                      +'评分及评分链接：'+grade+'分 '+grade_from+':  '+grade_url+'\n\n')
            img_url = div.xpath('./div[1]/a/img/@src')[0]
            img_data = requests.get(url=img_url,headers=headers).content
            imgPath = './景点图片库/' + title+'.jpg'
            with open(imgPath, 'wb') as fp:  # 每个项目5张图，总共50张图
                fp.write(img_data)
                print(title, '图片下载成功！')
        print("第%d页爬取完毕！！！" % count)
        print("-------------------------------------------------------------------------------------")


















