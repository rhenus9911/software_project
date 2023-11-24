import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import os
import time
import matplotlib.font_manager as fm
from recomm_service import recommService

fe = fm.FontEntry(fname='/usr/share/fonts/NanumFont/NanumGothic.ttf', name='NanumGothic')
fm.fontManager.ttflist.insert(0, fe) 
plt.rcParams.update({'font.size': 10, 'font.family': 'NanumGothic'}) # 폰트 설정

def table_info(dong):
    sales_dict, den_dict, card_dict, pop_dict = recommService(dong)
    sales_rank = pd.DataFrame(sales_dict.items(), columns = ['업종명', '당월매출금액'])
    colors = sb.color_palette('hls', len(sales_rank['업종명']))
    sales_rank.plot(kind = 'bar', x = '업종명', y = '당월매출금액', color = colors, edgecolor='black')
    plt.title('업종별 상위 매출 Top 5')
    plt.xticks(rotation = 0) # x 축에 표시되는 업종명이 세로로 90도 틀어져 표시되어 0도로 재조정

# =============================================================================
#     기존에 저장된 이미지가 있을 경우, 웹에서 old 이미지를 로드하는 문제 때문에
#     파일명에 시간을 추가하여 중복을 제거
#=============================================================================
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    sales_img = "sales_rank_" + str(time.time()) + ".png"
    for filename in os.listdir(BASE_DIR + '/static/images'):
        if filename.startswith('sales_rank_'):
            os.remove(BASE_DIR + '/static/images/' + filename)

    plt.savefig(BASE_DIR + '/static/images/' + sales_img)

    density_rank = pd.DataFrame(den_dict.items(), columns = ['업종명', '당월매출금액'])
    density_rank.plot(kind = 'bar', x = '업종명', y = '당월매출금액', color = colors, edgecolor='black')
    plt.title('밀집도별 상위 매출 Top 5')
    plt.xticks(rotation = 0)

    density_img = "density_rank_" + str(time.time()) + ".png"
    for filename in os.listdir(BASE_DIR + '/static/images'):
        if filename.startswith('density_rank_'):
            os.remove(BASE_DIR + '/static/images/' + filename)

    plt.savefig(BASE_DIR + '/static/images/' + density_img)

    trans_sales = {}
    trans_den = {}
    for key, val in sales_dict.items():
        val = format(val, ',')
        # c = dict(key, val)
        trans_sales[key] = val

    for key, val in den_dict.items():
        val = format(val, ',')
        # c = dict(key, val)
        trans_den[key] = val

    # 이미지 2장, dict 2개를 최종 반환
    return sales_img, density_img, card_dict, pop_dict, trans_sales, trans_den