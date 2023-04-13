# carsales 爬虫
from cgi import print_exception
from dataclasses import replace
from distutils.log import info
import requests
import cloudscraper
import os
import re
import numpy
import json
import random


class CarsalesSpider:
    def __init__(self):
        self.session = requests.Session() #下载器
        self.scraper = cloudscraper.create_scraper() #实例化一个scraper对象

    def get_data(self, url, brand):

        imgList = []
        infoList = []
        priceList=[]
        odometerList = []
        locationList = []
        bodyStyleList = []
        transmissionList = []
        engineList = []
        
        for i in range(1,35):
            temp_url = url + "/?offset="+ str(i*12)
            
            # 下载首页面的html
            index_html = self.download(temp_url, encoding= 'gbk')

            imgList = numpy.concatenate((imgList,self.get_image_list(index_html)),axis=0)
            infoList = numpy.concatenate((infoList,self.get_info_list(index_html)),axis=0)
            priceList = numpy.concatenate((priceList,self.get_price_list(index_html)),axis=0)
            odometerList = numpy.concatenate((odometerList,self.get_odometer_list(index_html)),axis=0)
            locationList = numpy.concatenate((locationList,self.get_location_list(index_html)),axis=0)
            bodyStyleList = numpy.concatenate((bodyStyleList,self.get_body_style_list(index_html)),axis=0)
            transmissionList = numpy.concatenate((transmissionList,self.get_transmission_list(index_html)),axis=0)
            engineList = numpy.concatenate((engineList,self.get_engine_list(index_html)),axis=0)



        # 判断是否存在路径，创建文件夹
        if (os.path.exists("D:\\carsalesData") == False):
            os.mkdir("D:\\carsalesData")

        print(len(imgList))
        print(len(infoList))
        print(len(priceList))
        print(len(odometerList))
        print(len(locationList))
        print(len(bodyStyleList))
        print(len(transmissionList))
        print(len(engineList))
        json_str_list=[]
        for i in range(0,408):
            json_str_list.append(
                json.dumps(
                    dict(zip(['information','year','price','image','odometer','location','bodyStyle','transmission','engine','state','brand'],
                    [infoList[i],infoList[i][0:4],priceList[i],imgList[i],odometerList[i],locationList[i],bodyStyleList[i],transmissionList[i],engineList[i],"ONSALE",brand]))))
        
        return json_str_list




    def download(self, url, encoding):

        while (True):

            temp = self.scraper.get(url).content
            str_content = temp.decode('utf-8')

            # new_file = open("D:\\生物学习资料\\html.html",'w',encoding='utf-8')
            # new_file.write(str_content)
            # new_file.close
            
            return str_content
    
    def get_image_list(self, index_html):

        img_divs = re.findall(r'<div\sclass="carousel-item\sactive\simage">\s+<img class="d-block\sw-100"\s+src="(.*?)"', index_html, re.S)
        # print(img_divs)

        return img_divs
    
    def get_info_list(self, index_html):
        info_divs= re.findall(r'"sv-title">(.*?)</a>', index_html, re.S)
        # print(info_divs)
        
        return info_divs

# 价格
    def get_price_list(self, index_html):
        price_divs= re.findall(r'data-webm-clickvalue="sv-price">(.*?)</a>', index_html, re.S)
        # print(info_divs)
        while len(price_divs)<12 :
            price_divs.append("Unavailable")
        for i in range(0,12):
            price_divs[i] = str(price_divs[i]).replace("$","").replace("*","").replace(",","")
        return price_divs


# 里程表
    def get_odometer_list(self, index_html):
        odometer_divs= re.findall(r'data-type="Odometer">(.*?)</li>', index_html, re.S)
        # print(info_divs)
        while len(odometer_divs)<12 :
            odometer_divs.append("Unavailable")
        for i in range(0,12):
            odometer_divs[i] = str(odometer_divs[i]).replace("km","").replace(",","").replace(" ","")
        return odometer_divs
    
    # 车型
    def get_body_style_list(self, index_html):
        info_divs= re.findall(r'data-type="Body\sStyle">(.*?)</li>', index_html, re.S)
        # print(info_divs)

        while len(info_divs)<12 :
            info_divs.append("Unavailable")

        return info_divs

        # gearType
    def get_transmission_list(self, index_html):
        info_divs= re.findall(r'data-type="Transmission">(.*?)</li>', index_html, re.S)
        # print(info_divs)

        while len(info_divs)<12 :
            info_divs.append("Unavailable")
        return info_divs

        # 引擎
    def get_engine_list(self, index_html):
        info_divs= re.findall(r'data-type="Engine">(.*?)</li>', index_html, re.S)
        # print(info_divs)

        while len(info_divs)<12 :
            info_divs.append("Unavailable")

        return info_divs

        # 地区
    def get_location_list(self, index_html):
        location_divs= re.findall(r'seller-location\sd-flex">(.*?)</div>', index_html, re.S)
        # print(info_divs)

        while len(location_divs)<12 :
            location_divs.append("Unavailable")
        return location_divs

    
    
if __name__ == "__main__":
    # brand = input("Please enter the brand of car: ")
    brands=['mazda']
    spider = CarsalesSpider() # instantiate
    new_file = open("D:\\carsalesData\\car_data.json",'a',encoding='utf-8')
    data_list = []
    for i in range(0,len(brands)):
        url = "https://www.carsales.com.au/cars/"+brands[i]
        data_list = numpy.concatenate((data_list,spider.get_data(url,brands[i])),axis=0)
    random.shuffle(data_list)
    

    new_file.write(str(data_list).replace("'",""))

    new_file.close