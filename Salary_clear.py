import pymysql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime


class SalaryClear:
    ''' 薪資清洗標準 '''
    def process(all_data):
        
        feature_list=['minsalary','maxsalary']
        
        for col in feature_list:
    
            ulimit=np.percentile(all_data[col].values.astype(np.int64), 75) 
            llimit=np.percentile(all_data[col].values.astype(np.int64), 25)
            
            # 將超出1.5倍離群值移除
            n=1.5
            IQR=ulimit-llimit
            
            # # outlier=ulimit±n*IQR
            all_data=all_data[all_data[col]<ulimit+n*IQR]
            all_data=all_data[all_data[col]>llimit-n*IQR]
            
            
        return all_data
    
    
    ''' 連接資料庫查詢轉為df '''
    
    def con_sql(db,sql):
        db = pymysql.connect(host="", port=3306, user="admin", passwd="12345678", db="dream", charset="utf8",use_unicode = True)
        cursor = db.cursor()
        cursor.execute(sql)
        cursor.fetchall()
        df = pd.read_sql(sql,db)
        db.close()
        return df
    
    def newsalary(jobcat):
        
        date_now = datetime.date.today()
        date_30days = date_now - datetime.timedelta(30)
    
        db = 'dream'
        sql = f'SELECT jobtitle,jobcat,minsalary,maxsalary FROM `job` where `jobcat` = "{jobcat}" and (`salary` like"%月%" or salary like "month" or salary like "%年%" or salary like "%year%") and (`updatetime` > {date_30days});'
        df = SalaryClear.con_sql(db,sql)
        # print(df.describe())
        print("--------最低薪資---------")
        print('最小值為 Minimum：',np.quantile(df['minsalary'], q=0))
        print('較小四分位數為 Q1：', np.quantile(df['minsalary'], q=0.25))
        print('中位數為 Q2：', np.quantile(df['minsalary'], q=0.5))
        print('較大四分位數為 Q3：', np.quantile(df['minsalary'], q=0.75))
        print('最大值為 Maximum：', np.quantile(df['minsalary'], q=1))
    
        print("---------最高薪資--------")
        print('最小值為 Minimum：',np.quantile(df['maxsalary'], q=0))
        print('較小四分位數為 Q1：', np.quantile(df['maxsalary'], q=0.25))
        print('中位數為 Q2：', np.quantile(df['maxsalary'], q=0.5))
        print('較大四分位數為 Q3：', np.quantile(df['maxsalary'], q=0.75))
        print('最大值為 Maximum：', np.quantile(df['maxsalary'], q=1))
        plt.title("adjusment minsalary")
        sns.distplot(df['minsalary'])
        plt.show()
    
        ''' 數據處理 '''
    
        ##去除薪資為0欄位##
        
        df.drop(df.loc[df['minsalary']==0].index, inplace=True)
        df.drop(df.loc[df['maxsalary']==0].index, inplace=True)
    
        ##顯示0 DROP掉後的分布趨勢圖表##
        plt.title("zerodrop minsalary")
        sns.distplot(df['minsalary'])
        plt.show()
    
    
        print("--------最低薪資---------")
        print('最小值為 Minimum：',np.quantile(df['minsalary'], q=0))
        print('較小四分位數為 Q1：', np.quantile(df['minsalary'], q=0.25))
        print('中位數為 Q2：', np.quantile(df['minsalary'], q=0.5))
        print('較大四分位數為 Q3：', np.quantile(df['minsalary'], q=0.75))
        print('最大值為 Maximum：', np.quantile(df['minsalary'], q=1))
    
        print("---------最高薪資--------")
        print('最小值為 Minimum：',np.quantile(df['maxsalary'], q=0))
        print('較小四分位數為 Q1：', np.quantile(df['maxsalary'], q=0.25))
        print('中位數為 Q2：', np.quantile(df['maxsalary'], q=0.5))
        print('較大四分位數為 Q3：', np.quantile(df['maxsalary'], q=0.75))
        print('最大值為 Maximum：', np.quantile(df['maxsalary'], q=1))
        
        
        data_new = SalaryClear.process(df)
        max50 = data_new.describe()['maxsalary']['50%']
        min50 = data_new.describe()['minsalary']['50%']
        
        print("--------最低薪資---------")
        print('最小值為 Minimum：',np.quantile(data_new['minsalary'], q=0))
        print('較小四分位數為 Q1：', np.quantile(data_new['minsalary'], q=0.25))
        print('中位數為 Q2：', np.quantile(data_new['minsalary'], q=0.5))
        print('較大四分位數為 Q3：', np.quantile(data_new['minsalary'], q=0.75))
        print('最大值為 Maximum：', np.quantile(data_new['minsalary'], q=1))
    
        print("---------最高薪資--------")
        print('最小值為 Minimum：',np.quantile(data_new['maxsalary'], q=0))
        print('較小四分位數為 Q1：', np.quantile(data_new['maxsalary'], q=0.25))
        print('中位數為 Q2：', np.quantile(data_new['maxsalary'], q=0.5))
        print('較大四分位數為 Q3：', np.quantile(data_new['maxsalary'], q=0.75))
        print('最大值為 Maximum：', np.quantile(data_new['maxsalary'], q=1))
        plt.title("adjusment minsalary")
        sns.distplot(data_new['minsalary'])
        plt.show()

        return max50, min50
    

if __name__ == '__main__':
    SalaryClear.newsalary("數據分析師")

