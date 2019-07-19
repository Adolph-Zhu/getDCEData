# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 10:39:48 2019

@author: tjiang
"""
import pandas as pd
import time
from lxml import etree
from selenium import webdriver

def getDCEData(start_date,end_date):
    
    start_year=start_date[:4]
    start_month=start_date[4:6]
    start_date=start_date[-2:]
    
    end_year=end_date[:4]
    end_month=end_date[4:6]
    end_date=end_date[-2:]
    
    driver=webdriver.Chrome()
    
    ###获取日度行情数据    
    driver.get('http://www.dce.com.cn/dalianshangpin/xqsj/tjsj26/rtj/rxq/index.html')
    time.sleep(5)
    frame=driver.find_element_by_xpath('//*[@id="12650"]/div[2]/div/iframe')
    driver.switch_to_frame(frame)
    for year in range(int(start_year),int(end_year)+1):
        year=str(year)
        #指定年份
        elem=driver.find_element_by_xpath('//*[@id="control"]/select[1]')
        elem.click()
        time.sleep(3)
    
        elem1=[x for x in elem.find_elements_by_tag_name('option') if x.text==year][0]
        elem1.click()
        time.sleep(3)
        
        for month in range(12):
            month+=1
            if year==start_year and month<int(start_month):
                continue
            if year==end_year and month>int(end_month):
                break
            if month<10:
                month='0'+str(month)
            elif month>=10:
                month=str(month)
            
            #指定月份
            elem=driver.find_element_by_xpath('//*[@id="control"]/select[2]')
            elem.click()
            time.sleep(3)
    
            elem1=[x for x in elem.find_elements_by_tag_name('option') if x.text==month][0]
            elem1.click()
            time.sleep(3)
            
            #依次每天下载数据
            for day in range(31):
                day+=1
                if day<10:
                    day='0'+str(day)
                else:
                    day=str(day)
                
                elems=driver.find_elements_by_class_name('week')
                
                subelems=[elem.find_elements_by_tag_name('td') for elem in elems]
                flag=False
                for elem in elems:
                    subelems=elem.find_elements_by_tag_name('td')
                    for x in subelems:
                        if x.text==day:
                            x.click()
                            time.sleep(3)
                            try:
                                elem_file=driver.find_element_by_xpath('//*[@id="dayQuotesForm"]/div/div[2]/ul[1]/li[2]/a')
                            except:
                                flag=True
                                break
                            else:
                                elem_file.click()
                                time.sleep(3)
                                print(year+month+day)
                            flag=True
                            break
                    if flag==True:
                        break
                
    
    driver.close()

def getDCEClearParams(start_date,end_date):
    start_year=start_date[:4]
    start_month=start_date[4:6]
    start_date=start_date[-2:]
    
    end_year=end_date[:4]
    end_month=end_date[4:6]
    end_date=end_date[-2:]
    
    driver=webdriver.Chrome()
    
    def parse(html):
        selector=etree.HTML(html)
        url_info=selector.xpath('//*[@id="printData"]/div/table/tbody')
        elems=url_info[0].xpath('tr')[2:]
        l=[]
        for elem in elems:
            subelems=elem.xpath('td')
            l_tmp=[x.text.strip().replace(',','') for x in subelems[:-4]]
            l.append(l_tmp)
        columns=['品种','合约代码','结算价','开仓手续费','平仓手续费','短线开仓手续费','短线平仓手续费','手续费收取方式']
        df=pd.DataFrame(l,columns=columns)
        
        return df
    
    ###获取日度的结算参数
    driver.get('http://www.dce.com.cn/dalianshangpin/yw/fw/ywcs/jscs/index.html')
    time.sleep(5)
    frame=driver.find_element_by_xpath('//*[@id="14614"]/div[2]/div/iframe')
    driver.switch_to_frame(frame)
    for year in range(int(start_year),int(end_year)+1):
        year=str(year)
        #指定年份
        elem=driver.find_element_by_xpath('//*[@id="control"]/select[1]')
        elem.click()
        time.sleep(3)
    
        elem1=[x for x in elem.find_elements_by_tag_name('option') if x.text==year][0]
        elem1.click()
        time.sleep(3)
        
        for month in range(12):
            month+=1
            if year==start_year and month<int(start_month):
                continue
            if year==end_year and month>int(end_month):
                break
            if month<10:
                month='0'+str(month)
            elif month>=10:
                month=str(month)
            
            #指定月份
            elem=driver.find_element_by_xpath('//*[@id="control"]/select[2]')
            elem.click()
            time.sleep(3)
    
            elem1=[x for x in elem.find_elements_by_tag_name('option') if x.text==month][0]
            elem1.click()
            time.sleep(3)
            
            #依次每天下载数据
            for day in range(31):
                day+=1
                if day<10:
                    day='0'+str(day)
                else:
                    day=str(day)
                
                elems=driver.find_elements_by_class_name('week')
                
                subelems=[elem.find_elements_by_tag_name('td') for elem in elems]
                flag=False
                for elem in elems:
                    subelems=elem.find_elements_by_tag_name('td')
                    for x in subelems:
                        if x.text==day:
                            x.click()
                            time.sleep(3)
                            html=driver.page_source
                            df=parse(html)
                            if df.empty:
                                flag=True
                                break
                            else:
                                date=year+month+day
                                df.to_excel(r'C:\Users\tjiang\Desktop\work\calcfee\FeeEsti\DCE\data\clearParams\ClearParams_%s.xls'%date,index=False)
                                #time.sleep(3)
                                print(date)
                            flag=True
                            break
                    if flag==True:
                        break     
       
    driver.close()

if __name__=='__main__':
    getDCEClearParams('20190101','20190531')
    
    