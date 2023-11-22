import pandas as pd
import math, json
import matplotlib.pyplot as plt
import seaborn as sb
import os
import time
from sklearn.metrics.pairwise import cosine_similarity

dir = "data"

# 부산시 행정동별 유동인구
total_pop = pd.read_csv(f"{dir}/total_pop.csv")

# 부산시 행정동별 카드매출
card = pd.read_csv(f"{dir}/total_cards.csv")

# 부산시 행정동별 음식점
total_food = pd.read_csv(f"{dir}/total_food.csv")

# 행정동별 요식업 매출
total_sales = pd.read_csv(f"{dir}/total_sales.csv")

# 입력한 행정동별 요식업 분류

def similarity(dong):
  code_table = pd.DataFrame(total_sales['행정코드'].unique(), index=total_sales['행정동명'].unique(), columns=['상권코드'])
  foodCode_table = pd.DataFrame(total_food['상권업종소분류코드'].unique(), index=total_food['상권업종소분류명'].unique(), columns=['분류코드'])
  d_code = int(code_table.loc[dong].iloc[0])
  # 행정코드에 대한 상권분류

  dong_food = total_food[total_food['행정코드'] == d_code]
  dong_food = dong_food.reset_index(drop=True)

  f_code_dict = {} 

  index = foodCode_table.index
  f_code = foodCode_table['분류코드'].to_list()

  for i in range(len(index)):
    f_code_dict[f_code[i]] = index[i]

  # 유동인구비율을 고려하여 선택한 상권과 비슷한 상권 찾기
  data_pv =  pd.pivot_table(total_pop, index="행정코드", columns="class", values="val")
  data_sim = cosine_similarity(data_pv)
  data_sim2 = pd.DataFrame(data=data_sim, index=data_pv.index, columns=data_pv.index)
  rec = data_sim2[d_code].sort_values(ascending=False)[:51]

  list_of_index = [item for item in data_pv.loc[rec.index].index]

  list_df = pd.DataFrame(list_of_index, columns=['행정코드'])
  df_merge = pd.merge(total_sales, list_df, on='행정코드')

  merge_pv = pd.pivot_table(df_merge, index='행정코드', columns='상권업종소분류코드', values='매출')
  merge_pv.fillna(0, inplace=True)
  data_sim = cosine_similarity(merge_pv)
  data_sim = pd.DataFrame(data=data_sim, index=merge_pv.index, columns=merge_pv.index)

  # 추천함수
  recomm_top = data_sim[d_code].sort_values(ascending=False)[1:6]

  # 매출 데이터와 top 5 df 조인
  df_merge = pd.merge(total_sales, recomm_top, on='행정코드')

  data_pv = pd.pivot_table(df_merge, index='행정코드', columns='상권업종소분류코드', values='매출')

  score = pd.DataFrame(total_sales.상권업종소분류코드.unique(), columns=['상권업종소분류코드'])
  data_pv2 = pd.pivot_table(df_merge,index="상권업종소분류코드", values="매출")

  for i in [0, 1, 2, 3, 4]:
    data_sort = data_pv.iloc[i].sort_values(ascending=False)[data_pv.iloc[i] > 0]
    list_of_index = [item for item in data_pv2.loc[data_sort.index].index]
    list_df = pd.DataFrame(list_of_index, columns=['상권업종소분류코드'])
    score_series = pd.Series(
        range(22, 22 - len(data_pv.iloc[i].sort_values(ascending=False)[data_pv.iloc[i] > 0]), -1)
    )
    score_df = pd.DataFrame(score_series)

    if i == 0:
      list_df['score1'] = score_df
      score = pd.merge(score, list_df, 'outer')
    elif i == 1:
      list_df['score2'] = score_df
      score = pd.merge(score, list_df, 'outer')
    elif i == 2:
      list_df['score3'] = score_df
      score = pd.merge(score, list_df, 'outer')
    elif i == 3:
      list_df['score4'] = score_df
      score = pd.merge(score, list_df, 'outer')
    else:
      list_df['score5'] = score_df
      score = pd.merge(score, list_df, 'outer')

  score.fillna(0, inplace=True)
  score_sum = score['score1']+score['score2']+score['score3']+score['score4']+score['score5']
  score['score_sum'] = score_sum
  score.index = score.상권업종소분류코드
  score_sum_sort = score.score_sum.sort_values(ascending=False)[0:5]
  rec_sales = [item for item in data_pv2.loc[score_sum_sort.index].index]

  # 업종별 밀집도를 비교하여 밀집도가 낮은 업종 추천
  data_pv = pd.pivot_table(df_merge, index='행정코드', columns='상권업종소분류코드', values='점포수')
  data_pv2 = pd.pivot_table(df_merge, index='상권업종소분류코드', values='점포수')
  data_pv.fillna(0, inplace=True)

  # 5개 상권의 업종별 밀집도 계산
  # 밀집도 = 해당업종의 점포수 / 해당 상권 전체의 점포수
  score_den = pd.DataFrame(total_sales.상권업종소분류코드.unique(), columns=['상권업종소분류코드'])

  for i in [0, 1, 2, 3, 4]:
    score_den_reg = data_pv.iloc[i] / sum(data_pv.iloc[i])
    list_of_index = [item for item in data_pv2.loc[score_den_reg.index].index]
    list_df = pd.DataFrame(list_of_index, columns=['상권업종소분류코드'])
    if i == 0:
        list_df['den1'] = score_den_reg.values
        score_den = pd.merge(score_den, list_df, 'outer')
    elif i == 1:
        list_df['den2'] = score_den_reg.values
        score_den = pd.merge(score_den, list_df, 'outer')
    elif i == 2:
        list_df['den3'] = score_den_reg.values
        score_den = pd.merge(score_den, list_df, 'outer')
    elif i == 3:
        list_df['den4'] = score_den_reg.values
        score_den = pd.merge(score_den, list_df, 'outer')
    else:
        list_df['den5'] = score_den_reg.values
        score_den = pd.merge(score_den, list_df, 'outer')

  #5개 상권의 업종별 밀집도 평균 계산
  score_den_mean = (score_den['den1'] + score_den['den2'] + score_den['den3'] + score_den['den4'] + score_den['den5']) / 5
  score_den['den_mean'] = score_den_mean.values
  score_den.index = score_den.상권업종소분류코드

  # 선택한 상권의 현재 업종별 밀집도 계산
  pv_store = pd.pivot_table(total_sales, index='상권업종소분류코드', columns='행정코드', values='점포수')
  pv_store.fillna(0, inplace=True)

  score_select = pv_store[d_code]
  score_select_den = score_select / sum(score_select)
  score_diff = score_den['den_mean'] - score_select_den

  # 차이가 클수록 추천도 증가
  score_diff_sort = score_diff.sort_values(ascending=False)[0:5]
  rec_den = [item for item in pv_store.loc[score_diff_sort.index].index]

  sales = rec_sales[:5]
  den = rec_den[:5]

  com = total_sales['행정코드'] == d_code
  serv_sales = total_sales[com][['상권업종소분류코드', '매출']]

  def merge_two_dicts(x, y):
          z = x.copy()
          z.update(y)
          return z

  sales_dict = {}  # 매출 top5 결과 dict
  for i in sales:
      serv = serv_sales['상권업종소분류코드'] == i
      sales = serv_sales[serv][['상권업종소분류코드', '매출']]  # 업종 매출 df

      position_sales_dict = dict([(x, int(y)) for x, y in zip(sales['상권업종소분류코드'], sales['매출'])])
      sales_dict = merge_two_dicts(sales_dict, position_sales_dict)
      # print(sales_dict)

  den_dict = {}  # 밀집도 top5 결과 dict
  for i in den:
      serv = serv_sales['상권업종소분류코드'] == i
      den = serv_sales[serv][['상권업종소분류코드', '매출']]  # 업종 매출 df

      position_sales_dict = dict([(x, int(y)) for x, y in zip(den['상권업종소분류코드'], den['매출'])])
      den_dict = merge_two_dicts(den_dict, position_sales_dict)

  sd = {}
  dd = {}
  for key in sales_dict:
    sd[f_code_dict[key]] = sales_dict[key]

  for key in den_dict:
    dd[f_code_dict[key]] = den_dict[key]
  
  return sd, dd