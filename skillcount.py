import pymysql
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd


''' 連接資料庫查詢轉為df '''

def con_sql(db,sql):
    db = pymysql.connect(host="localhost", port=3306, user="root", passwd="root", db=db, charset="utf8",use_unicode = True)
    cursor = db.cursor()
    cursor.execute(sql)
    cursor.fetchall()
    df = pd.read_sql(sql,db)
    db.close()
    return df


def skillclear(jobcat):

    db = ''
    sql = f'SELECT jobcat,skill FROM job where jobcat ="{jobcat}";'
    df = con_sql(db,sql)

    # print(df)

    count = df['skill'].tolist()
    countstr="".join(count)
    # print(countstr)
    amount=countstr.replace("/",",")
    word=amount.split(",")
    # print(word)
    setword=set(word)
    skill=[]
    amount=[]
    for i in setword:
        count=word.count(i)
        skill.append(i)
        amount.append(count)
    # print(skill)
    # print(amount)

    df=pd.DataFrame({'skill':skill,'amount':amount})
    df['jobcat']=f"{jobcat}"
    print(df)
        
    ''' #新datafrrame匯入新table '''

    DB_HOST = 'localhost'
    DB_PORT = '3306'
    DATABASE = ''
    DB_USER = 'root'
    DB_PASS = 'root'

    connect_info = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(DB_USER, DB_PASS, DB_HOST, DB_PORT, DATABASE) 
    engine = create_engine(connect_info)

    try:
        pd.io.sql.to_sql(df,"skillcount",engine,index=False,if_exists='append')
    except Exception as e:
        print(e)

if __name__ == '__main__':
    f = open('jobcat_8.txt',"r",encoding="utf-8")
    for line in f.readlines():
        skillclear(line.strip())
        # print(line)
    f.close()