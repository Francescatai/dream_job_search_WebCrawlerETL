import re
import random
import pandas as pd
import requests
from lxml import html
import re
import pymysql
from datetime import datetime
from fuzzywuzzy import process
from fake_useragent import UserAgent


conn = pymysql.connect(host="localhost", port=3306, user="root", password="root", database="")
cursor = conn.cursor()


def jobCategory(self,keyword):
    """判斷職務類別"""     
    with open(r'jobcategory.txt','r',encoding="utf-8") as f:
        lines = f.readlines()
        words2 = [word.strip() for word in lines]

    try:
        
        i = words2.index(keyword)
        if 12 >= i >= 0:
            jobCategory = keyword.replace(keyword, '數據分析師')
        elif 16 >= i >= 13:
            jobCategory = keyword.replace(keyword, '商業分析師')
        elif 21 >= i >= 17:
            jobCategory = keyword.replace(keyword, '數據工程師')
        elif 32 >= i >= 22:
            jobCategory = keyword.replace(keyword, '機器學習工程師')
        elif 40 >= i >= 33:
            jobCategory = keyword.replace(keyword, '數據庫工程師')
        elif 46 >= i >= 41:
            jobCategory = keyword.replace(keyword, '研究人員')
        elif 51 >= i >= 47:
            jobCategory = keyword.replace(keyword, '軟體開發工程師')
        elif 54 >= i >= 52:
            jobCategory = keyword.replace(keyword, '維運工程師')
        else:
            jobCategory = 'Null'
        
    except:
        # 移除字串中的空白符再判定是否為純英文
        keyword = re.sub(r"\s+", "", keyword)
        if keyword.isalpha() == True:
            if keyword == 'DataAnalyst':
                jobCategory = keyword.replace(keyword, '數據分析師')
            elif keyword == 'BusinessAnalyst':
                jobCategory = keyword.replace(keyword, '商業分析師')
            elif keyword == 'DataEngineer':
                jobCategory = keyword.replace(keyword, '數據工程師')
            elif keyword == 'DataScientist':
                jobCategory = keyword.replace(keyword, '機器學習工程師')
            elif keyword == 'DatabaseAdministrator':
                jobCategory = keyword.replace(keyword, '數據庫工程師')
            elif keyword == 'SoftwareEngineer':
                jobCategory = keyword.replace(keyword, '軟體開發工程師')
            elif keyword == 'OperationEngineer':
                jobCategory = keyword.replace(keyword, '維運工程師')
            else:
                jobCategory = 'Null'
        
        
    return jobCategory




def requirements(jd, jq, skill):
    pattern = r'IoT|Linux|Python|mySQL|SQL|API|Hadoop|InfluxDB|ELK|Elastic Search|Logstash|Kibana|Splunk|AWS|Tableau|Qlik|PowerBI|BI​|GCP|Oracle Data Visualization|Big Data|Machine Learning|ML|TensorFlow|Deep Learning|Crawler|Data Modeling|Data Mining|Data Cleaning|大數據|資料收集|爬蟲|機器學習|深度學習|資料工程|資料探勘|Flask|hiveSQL|sqoop|mongodb'
    jobRequired = str([jd] + [jq] + [skill])
    skills = re.findall(pattern, jobRequired, flags=re.I)
    conformity = set(sk.casefold() for sk in skills)
    conlist=list(conformity)
    constr="/".join(conlist)
    return constr

def requirementcount(jd, jq, skill):
    pattern = r'IoT|Linux|Python|mySQL|SQL|API|Hadoop|InfluxDB|ELK|Elastic Search|Logstash|Kibana|Splunk|AWS|Tableau|Qlik|PowerBI|BI​|GCP|Oracle Data Visualization|Big Data|Machine Learning|ML|TensorFlow|Deep Learning|Crawler|Data Modeling|Data Mining|Data Cleaning|大數據|資料收集|爬蟲|機器學習|深度學習|資料工程|資料探勘'
    jobRequired = str([jd] + [jq] + [skill])
    skills = re.findall(pattern, jobRequired, flags=re.I)
    conformity = len(set(sk.casefold() for sk in skills))
    return conformity




def find_job_yourator(q):
    ua=UserAgent()
    headers = {'user-agent': ua.random}
    url=[]
    for i in range(1,100):
        resp=requests.post(f'https://www.yourator.co/api/v2/jobs?term[]={q}&sort=recent_updated&page={i}',headers=headers)
        print(resp)
        content=resp.json()
        print(content)
        pathurl='https://www.yourator.co'
        for i in content['jobs']:
            jurl=pathurl+i['path']#分頁網址
            url.append(jurl)
        resp.close()


    for i in list(set(url)):
        res=requests.get(i,headers=headers)
        tree=html.fromstring(res.text)
        for name in tree.xpath("//section/div/div/div/div/h1"):
            jname=name.text
        for com in tree.xpath("//h4/a"):
            company=com.text
        for local in tree.xpath("//div[2]/p/a"):
            city=local.text[3:]
        for update in tree.xpath("//p[@class='basic-info__last_updated_at']"):
            uptime=update.text[6:]

        resp=res.text
        jb_content=re.compile(r'<h2 class="job-heading">工作內容</h2>.*?<section class="content__area">.*?<p>(?P<jb>.*?)</p>',re.S)
        jb=jb_content.findall(resp)
        jbb="".join(jb).replace("<br>","").replace("</br>","").replace("<strong>","").replace("</strong>","").replace("<b>","").replace("</b>","")
        jdd=re.findall(r'\S+',jbb)
        jd="".join(jdd)
        # print(jd)

        jr_content=re.compile(r'<h2 class="job-heading">條件要求</h2>.*?<section class="content__area">.*?<p>(?P<jr>.*?)</section>',re.S)
        jrequest=jr_content.findall(resp)
        jrrr="".join(jrequest).replace("<br>","").replace("</br>","").replace("<strong>","").replace("</strong>","").replace("<b>","").replace("</b>","").replace("<p>","").replace("</p>","").replace("<ul>","").replace("</ul>","").replace("<li>","").replace("</li>","")
        jrr=re.findall(r'\S+',jrrr)
        jr="".join(jrr)
        # print(jr)

        wf_content=re.compile(r'<h2 data-nav-target="benefits" class="job-heading">員工福利</h2>.*?<section class="content__area">.*?<p>(?P<wf>.*?)</section>',re.S)
        wfff=jr_content.findall(resp)
        wel="".join(wfff).replace("<br>","").replace("</br>","").replace("<strong>","").replace("</strong>","").replace("<b>","").replace("</b>","").replace("<p>","").replace("</p>","").replace("<ul>","").replace("</ul>","").replace("<li>","").replace("</li>","")
        wff=re.findall(r'\S+',wel)
        wf="".join(wff)

        sa_content=re.compile(r'<h2 class="job-heading">薪資範圍</h2>.*?<section class="content__area">(?P<sa>.*?)</section>',re.S)
        ssa=sa_content.findall(resp)
        sa="".join(ssa)

        
        nsa="".join(sa).replace(",","")#轉字串+拿掉，
        nnsa=re.findall(r'\d+',nsa)#取數字(會變list)
        try:
            if len(nnsa)==2:
                if "月薪" in sa:
                    minsa=nnsa[0]
                    maxsa=nnsa[1]
                if "時薪" in sa:
                    minsa=nnsa[0]
                    maxsa=nnsa[1]
                elif "年薪" in sa:
                    minsa=float(nnsa[0])/12
                    maxsa=float(nnsa[1])/12
            elif len(nnsa)==1:
                if "面議" in sa:
                    minsa=0
                    maxsa=0
                elif "時薪" in sa:
                    minsa=nnsa[0]
                    maxsa=nnsa[0]
                elif "月薪" in sa:
                    minsa=nnsa[0]
                    maxsa=nnsa[0]
                elif "年薪" in sa:
                    minsa=float(nnsa[0])/12
                    maxsa=float(nnsa[0])/12
            else:
                minsa=0
                maxsa=0
        except Exception as e:
                print(e)
                continue
        print(sa)
        print(nnsa)
        print(minsa)
        print(maxsa)

        skill_content=re.compile(r'<a class="tag" href=.*?">(?P<skill>.*?)</a>',re.S)
        skilll=skill_content.findall(resp)
        # print(skilll)
        skill="/".join(skilll)

        systemtime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        

    #直接加入sql庫###
        if  requirementcount(jd, jr, skill)>0:
            with open(r'jobcategory.txt','r',encoding="utf-8") as f:
                lines = f.readlines()
                words2 = [word.strip() for word in lines]
            if process.extractOne(jname, words2)[1] > 50:                                 
                jobcat=jobCategory(process.extractOne(jname, words2)[0])       
            else:
                jobcat=jobCategory(q)
                   

            try:
                sql= f"INSERT INTO job (jobtitle,joburl,company,city,salary,minsalary,maxsalary,skill,jd,jr,welfare,source,updatetime,systemtime) VALUES ('{jname}','{i}','{company}','{city}','{sa}',{minsa},{maxsa},'{requirements(jd, jr, skill)}','{jd}','{jr}','{wf}','yourator','{uptime}','{systemtime}')"
                # print(sql)
                cursor.execute(sql)
                conn.commit()
            except Exception as e:
                print(e)
                continue
        res.close()
    

if __name__ == '__main__':
    
    with open(r'jobsearch.txt','r',encoding="utf-8") as f:
        lines = f.readlines()
        find_job_yourator(lines)
        
        
    

    
    # conn.close()
    
   
    