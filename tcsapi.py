# -*- coding: utf-8 -*-
import requests
import pandas as pd
from datetime import date, timedelta
import time
import sqlite3


class tcsapi:
  def __init__(self):
    self.__url = "http://data.ex.co.kr/openapi/trafficapi/nationalTrafficVolumn"
    self.__rtype = "json"
    self.__rkey = "8440600649"
    self.__headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
    self.__DB = "tscdb.db"
    self.__TCSDATA = "tcsdata"
    self.sleep_time = 0.5

  def daterange(self, start_date, end_date):
      for n in range(int((end_date - start_date).days)+1):
          yield start_date + timedelta(n)

  def dateGenerator(self, from_date, to_date):
    start_date = date(int(from_date[0:4]), int(from_date[4:6]), int(from_date[6:]))
    end_date = date(int(to_date[0:4]), int(to_date[4:6]), int(to_date[6:]))
    result = []
    for single_date in self.daterange(start_date, end_date):
      result.append(single_date.strftime("%Y%m%d"))
    return result

  def checkData(self, req_date: str) -> int:
    try:
      conn = sqlite3.connect(self.__DB)
      cur = conn.cursor()
      query = f"select exists(select 1 from {self.__TCSDATA} where req_date = '{req_date}' limit 1)"
      cur.execute(query)
      exist = cur.fetchall()[0][0]
      return exist
    except Exception as err:
        print('Query Failed: %s\nError: %s' % (query, str(err)))
        return 0
    finally:
        conn.close()

  def getDataFrame(self, from_date: str, to_date: str, download_option=False):
    conn = sqlite3.connect(self.__DB)
    try:
      date_list = []
      req_dates = self.dateGenerator(from_date, to_date)
      df_result = pd.DataFrame(columns=['Date', 'SUM'])
      cur = conn.cursor()
      for req_d in req_dates:
        rdate = str(req_d)
        # if data exists in db
        query = f"select exists(select 1 from {self.__TCSDATA} where req_date = '{rdate}' limit 1)"
        cur.execute(query)
        exist = cur.fetchall()[0][0]
        if exist:
          date_list.append(rdate)
          if download_option:
            params = {'key':self.__rkey, 'type':self.__rtype, 'sumDate':rdate}
            res = requests.get(self.__url, headers=self.__headers, params=params)
            if res.status_code == 200:
              data = eval(res.text)
              df_temp = pd.DataFrame(data['list'])
              sum_data = df_temp['trafficVolumn'].astype(int).sum()
              cur.execute(f"update {self.__TCSDATA} set sum={sum_data} where req_date = '{rdate}'")
              conn.commit()
            else:
              print(res.status_code)
          continue
        else:
          time.sleep(self.sleep_time)    
          params = {'key':self.__rkey, 'type':self.__rtype, 'sumDate':rdate}
          res = requests.get(self.__url, headers=self.__headers, params=params)
          if res.status_code == 200:
            data = eval(res.text)
            df_temp = pd.DataFrame(data['list'])
            sum_data = df_temp['trafficVolumn'].astype(int).sum()
            cur.execute(f"insert into {self.__TCSDATA} values ('{req_d}', {sum_data})")
            conn.commit()
          else:
            print(res.status_code)
      q_date = "','".join(date_list)
      query = f"select req_date, sum from {self.__TCSDATA} where req_date in ('{q_date}')"
      df_result = pd.read_sql_query(query, conn)
      return df_result
    except Exception as err:
        print('Failed: %s' % str(err))
        return 0
    finally:
      conn.close()


if __name__ == "__main__":
  tcs = tcsapi()
  print(tcs.getDataFrame("20220101", "20220527"))

# df_result = getDataFrame("20220523", "20220527")
# df_result

