# -*- coding: utf-8 -*-

"""
112年大四畢業生離校意見分析
"""
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import re
import seaborn as sns
import streamlit as st 
import streamlit.components.v1 as stc 
#os.chdir(r'C:\Users\user\Dropbox\系務\校務研究IR\大一新生學習適應調查分析\112')

# ####### 資料前處理  (建立 'df_senior.pkl')
# ###### 讀入調查結果 2023靜宜大學校友對學校滿意度調查問卷 (回覆)(112.12.3 曉華提供)(Lo revised)
# df_senior = pd.read_excel(r'C:\Users\user\Dropbox\系務\校務研究IR\大四畢業生離校意見分析\112年\2023靜宜大學校友對學校滿意度調查問卷 (回覆)(112.12.3 曉華提供)(Lo revised 2).xlsx')
# df_senior.shape  ## (1951, 69)
# df_senior.columns
# df_senior.index  ## RangeIndex(start=0, stop=1951, step=1)
# #df_senior['科系']
# ###### 检查是否有缺失值
# print(df_senior.isna().any().any())  ## True
# df_senior.isna().sum(axis=0) 
# '''
# 時間戳記                         8
# 學號                           9
# 畢業院系                         9
# 組別                           9
# 部別                           9

# 2.  您畢業3個月內最主要之規劃?         398
# 3. 您目前是否已寫好履歷自傳?           398
# 4. 您是否已經寄出履歷自傳，並開始求職了?     398
# 是，何時投遞?                   1610
# 否， 預計何時?                   739
# Length: 69, dtype: int64
# ''' 
# ###### 找出行 '學號' 中含有NA的所有列
# na_rows = df_senior[df_senior['學號'].isna()]
# print(na_rows)
# ###### 删除行 '學號' 中含有NA的所有列
# df_senior = df_senior.dropna(subset=['學號'])
# df_senior.shape  ## (1942, 69), 1942 = 1951-9
# ###### 将行 '學號' 的数据类型更改为字符串 (原為float64)
# print(df_senior['學號'].dtypes) ## float64
# df_senior['學號'] = df_senior['學號'].astype(str)
# print(df_senior['學號'].dtypes) ## object

# df_senior['畢業院系'].unique()
# '''
# array(['國企系', '觀光系', '資傳系', '中文系', '社工系', '法律系', '財工系', '食營系', '企管系',
#        '應化系', '生態系', '英文系', '日文系', '資碩專班', '資科系(統資系)', '資管系', '台文系',
#        '西文系', '寰宇外語教育學士學位學程', '財金系', '資工系', '國際碩士學位學程', '寰宇管理學士學位學程',
#        '教研所', '創新與創業管理碩士學位學程', '社會企業與文化創意碩士學位學程', '會計系', '化科系',
#        '健康照顧社會工作學士學位學程原住民專班', '大傳系', '法律學士學位學程原住民專班', '管碩專班',
#        '犯罪防治碩士學位學程', '原住民族文化碩士學位學程'], dtype=object)
# '''


# ###### 定義系名到學院的映射
# #['Science', 'Management', 'Social','Information','Internation','Language']
# college_map =\
# {'台文系':'人社', 
#  '中文系':'人社', 
#  '英文系':'外語', 
#  '西文系':'外語', 
#  '日文系':'外語', 
#  '大傳系':'人社', 
#  '資傳系':'資訊',  
#  '會計系':'管理', 
#  '企管系':'管理', 
#  '國企系':'管理',
#  '財金系':'管理', 
#  '法律系':'人社', 
#  '生態系':'人社', 
#  '應化系':'理學', 
#  '資科系(統資系)':'理學', 
#  '財工系':'理學',
#  '資管系':'資訊', 
#  '資工系':'資訊', 
#  '食營系':'理學', 
#  '觀光系':'管理',
#  '化科系':'理學', 
#  '創新與創業管理碩士學位學程':'管理',  
#  '法律學士學位學程原住民專班':'人社',
#  '健康照顧社會工作學士學位學程原住民專班':'人社', 
#  '寰宇外語教育學士學位學程':'國際', 
#  '寰宇管理學士學位學程':'國際', 
#  '社工系':'人社',  
#  '管碩專班':'管理', 
#  '國際碩士學位學程':'資訊', 
#  '犯罪防治碩士學位學程':'人社',
#  '原住民族文化碩士學位學程':'人社',
#  '資碩專班':'資訊',
#  '教研所':'人社',
#  '社會企業與文化創意碩士學位學程':'人社'
 
# }

# ###### 使用映射來創建新的 '學院別' 欄位
# df_senior.columns
# df_senior['學院別'] = df_senior['畢業院系'].map(college_map)
# df_senior.shape  ## (1942, 70)
# # df_senior.head()
# # df_senior.tail(20)

# df_senior_理學 = df_senior[df_senior['學院別']=='理學'].reset_index(drop=True)
# df_senior_資訊 = df_senior[df_senior['學院別']=='資訊'].reset_index(drop=True)
# df_senior_管理 = df_senior[df_senior['學院別']=='管理'].reset_index(drop=True)
# df_senior_人社 = df_senior[df_senior['學院別']=='人社'].reset_index(drop=True)
# df_senior_國際 = df_senior[df_senior['學院別']=='國際'].reset_index(drop=True)
# df_senior_外語 = df_senior[df_senior['學院別']=='外語'].reset_index(drop=True)
# #df_senior_理學.columns

# ###### 将DataFrame保存为Pickle文件
# #df_senior.to_pickle('df_senior.pkl')
# ###### 将 DataFrame 保存为 Excel 文件
# #df_senior.to_excel('df_senior.xlsx', index=False)


@st.cache_data(ttl=3600, show_spinner="正在加載資料...")  ## Add the caching decorator
def load_data(path):
    df = pd.read_pickle(path)
    return df

## 以 "人次" 計算總數
@st.cache_data(ttl=3600, show_spinner="正在處理資料...")  ## Add the caching decorator
def Frequency_Distribution(df, column_index):
    ##### 将字符串按逗号分割并展平
    split_values = df.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    return result_df

## 以 "填答人數" 計算總數
@st.cache_data(ttl=3600, show_spinner="正在處理資料...")  ## Add the caching decorator
def Frequency_Distribution_1(df, column_index):
    ##### 将字符串按逗号分割并展平
    split_values = df.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/df.shape[0]
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    return result_df




#### 調整項目次序
###定义期望的項目顺序
### 函数：调整 DataFrame 以包含所有項目，且顺序正确
@st.cache_data(ttl=3600, show_spinner="正在加載資料...")  ## Add the caching decorator
def adjust_df(df, order):
    # 确保 DataFrame 包含所有滿意度值
    for item in order:
        if item not in df['項目'].values:
            # 创建一个新的 DataFrame，用于添加新的row
            new_row = pd.DataFrame({'項目': [item], '人數': [0], '比例': [0]})
            # 使用 concat() 合并原始 DataFrame 和新的 DataFrame
            df = pd.concat([df, new_row], ignore_index=True)

    # 根据期望的顺序重新排列 DataFrame
    df = df.set_index('項目').reindex(order).reset_index()
    return df


@st.cache_data(ttl=3600, show_spinner="正在處理資料...")  ## Add the caching decorator
#### 轉變資料型態為float:
### 定义一个函数来转换每一行为数值类型，非数值转为 NaN 
def to_numeric_ignore_special_str(column):
    return pd.to_numeric(column, errors='coerce')






#######  读取Pickle文件
df_senior_original = pd.read_pickle('df_senior.pkl')
#df_senior_original.shape  ## (1942, 70)
#df_senior_original.head()
#print(df_senior_original)

###### 更改系與院的欄位名稱: 畢業院系->科系   學院別->學院
df_senior_original.rename(columns={'畢業院系': '科系', '學院別': '學院'}, inplace=True)
# df_senior_original.columns

###### 更改 '資科系(統資系)' 的名稱: '資科系(統資系)'->'資科系'
df_senior_original['科系'] = df_senior_original['科系'].replace({'資科系(統資系)': '資科系'})

###### 更改院的名稱: 理學->理學院, 資訊->資訊學院, 管理->管理學院, 人社->人文暨社會科學院, 國際->國際學院, 外語->外語學院
##### 定义替换规则
replace_rules = {
    '理學': '理學院',
    '資訊': '資訊學院',
    '管理': '管理學院',
    '人社': '人文暨社會科學院',
    '國際': '國際學院',
    '外語': '外語學院'
}

##### 应用替换规则
df_senior_original['學院'] = df_senior_original['學院'].replace(replace_rules)


# ####### 读取Excel文件
# df_senior_original = pd.read_excel('df_senior.xlsx')





####### 預先設定
###### 預設定院或系之選擇
global 院_系, choice, df_senior, choice_faculty, df_senior_faculty, selected_options, collections, column_index, dataframes, desired_order, combined_df, unique_level0, df
# global 院_系
院_系=0
###### 預設定 df_senior 以防止在等待選擇院系輸入時, 發生後面程式df_senior讀不到資料而產生錯誤
choice='財金系' ##'化科系'
df_senior = df_senior_original[df_senior_original['科系']==choice]
# choice_faculty = df_senior['學院'][0]  ## 選擇學系所屬學院: '理學院'
choice_faculty = df_senior['學院'].values[0]  ## 選擇學系所屬學院: '理學院'
df_senior_faculty = df_senior_original[df_senior_original['學院']==choice_faculty]  ## 挑出全校所屬學院之資料
# df_senior_faculty['學院']  
###### 預設定 selected_options, collections
selected_options = ['化科系','企管系']
# collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
# collections = [df_senior, df_senior_faculty, df_senior_original]
# len(collections) ## 2
# type(collections[0])   ## pandas.core.frame.DataFrame
column_index = 9
dataframes = [Frequency_Distribution(df, column_index) for df in collections]  ## 
# len(dataframes)  ## 2
# len(dataframes[1]) ## 4
# len(dataframes[0]) ## 4
# dataframes
# '''
# [      項目  人數      比例
#  0     滿意  54  0.5806
#  1   非常滿意  23  0.2473
#  2     普通  13  0.1398
#  3    不滿意   2  0.0215
#  4  非常不滿意   1  0.0108,
#       項目  人數      比例
#  0    滿意  57  0.5278
#  1    普通  27  0.2500
#  2  非常滿意  24  0.2222]
# '''


##### 形成所有學系'項目'欄位的所有值
desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
# desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 

##### 缺的項目值加以擴充， 並統一一樣的項目次序
dataframes = [adjust_df(df, desired_order) for df in dataframes]
# len(dataframes)  ## 2
# len(dataframes[1]) ## 4
# len(dataframes[0]) ## 4
# dataframes[0]['項目']
# '''
# 0     不滿意
# 1      普通
# 2    非常滿意
# 3      滿意
# Name: 項目, dtype: object
# '''
# dataframes[1]['項目']
# '''
# 0     不滿意
# 1      普通
# 2    非常滿意
# 3      滿意
# Name: 項目, dtype: object
# '''
# dataframes
# '''
# [      項目  人數      比例
#  0     普通  13  0.1398
#  1   非常滿意  23  0.2473
#  2     滿意  54  0.5806
#  3    不滿意   2  0.0215
#  4  非常不滿意   1  0.0108,
#        項目  人數      比例
#  0     普通  27  0.2500
#  1   非常滿意  24  0.2222
#  2     滿意  57  0.5278
#  3    不滿意   0  0.0000
#  4  非常不滿意   0  0.0000]
# '''

combined_df = pd.concat(dataframes, keys=selected_options)
# combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])   ## 以上還沒有 '全校' 資料
# ''' 
#          項目  人數      比例
# 財金系 0   不滿意   5  0.0538
#     1    普通  27  0.2903
#     2  非常滿意  14  0.1505
#     3    滿意  47  0.5054
# 管理  0   不滿意   1  0.0093
#     1    普通  38  0.3519
#     2  非常滿意  26  0.2407
#     3    滿意  43  0.3981
# '''
# combined_df
# '''
#           項目  人數      比例
# 化科系 0     普通  13  0.1398
#     1   非常滿意  23  0.2473
#     2     滿意  54  0.5806
#     3    不滿意   2  0.0215
#     4  非常不滿意   1  0.0108
# 企管系 0     普通  27  0.2500
#     1   非常滿意  24  0.2222
#     2     滿意  57  0.5278
#     3    不滿意   0  0.0000
#     4  非常不滿意   0  0.0000
# '''
unique_level0 = combined_df.index.get_level_values(0).unique()  ## Index(['化科系', '企管系'], dtype='object')

df = combined_df.loc['化科系']
# df
# '''
#       項目  人數      比例
# 0     普通  13  0.1398
# 1   非常滿意  23  0.2473
# 2     滿意  54  0.5806
# 3    不滿意   2  0.0215
# 4  非常不滿意   1  0.0108
# '''

# df['比例']
# '''
# 0    0.1398
# 1    0.2473
# 2    0.5806
# 3    0.0215
# 4    0.0108
# Name: 比例, dtype: float64
# '''

# len(df)  ## 5


####### 設定呈現標題 
html_temp = """
		<div style="background-color:#3872fb;padding:10px;border-radius:10px">
		<h1 style="color:white;text-align:center;"> 112年大四畢業生離校意見分析 </h1>
		</div>
		"""
stc.html(html_temp)
# st.subheader("以下調查與計算母體為大四填答同學1942人")
###### 使用 <h3> 或 <h4> 标签代替更大的标题标签
# st.markdown("##### 以下調查與計算母體為大四填答同學1942人")

###### 或者，使用 HTML 的 <style> 来更精细地控制字体大小和加粗
st.markdown("""
<style>
.bold-small-font {
    font-size:18px !important;
    font-weight:bold !important;
}
</style>
<p class="bold-small-font">以下調查與計算母體為大四填答同學1942人</p>
""", unsafe_allow_html=True)

st.markdown("##")  ## 更大的间隔


# global 院_系
####### 選擇院系
###### 選擇 院 or 系:
院_系 = st.text_input('以學系查詢請輸入 0, 以學院查詢請輸入 1  (說明: (i).以學系查詢時同時呈現學院及全校資料. (ii)可以選擇比較單位): ')
if 院_系 == '0':
    choice = st.selectbox('選擇學系', df_senior_original['科系'].unique())
    #choice = '化科系'
    df_senior = df_senior_original[df_senior_original['科系']==choice]
    choice_faculty = df_senior['學院'].values[0]  ## 選擇學系所屬學院
    df_senior_faculty = df_senior_original[df_senior_original['學院']==choice_faculty]  ## 挑出全校所屬學院之資料

    # selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=['化科系','企管系'])
    # selected_options = ['化科系','企管系']
    # collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
    # dataframes = [Frequency_Distribution(df, 7) for df in collections]
    # combined_df = pd.concat(dataframes, keys=selected_options)
    # #### 去掉 level 1 index
    # combined_df_r = combined_df.reset_index(level=1, drop=True)
elif 院_系 == '1':
    choice = st.selectbox('選擇學院', df_senior_original['學院'].unique(),index=0)
    #choice = '管理'
    df_senior = df_senior_original[df_senior_original['學院']==choice]
    # selected_options = st.multiselect('選擇比較學的院：', df_senior_original['學院'].unique(), default=['理學院','資訊學院'])
    # collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
    # dataframes = [Frequency_Distribution(df, 7) for df in collections]
    # combined_df = pd.concat(dataframes, keys=selected_options)



# choice = st.selectbox('選擇學系', df_senior_original['科系'].unique())
# #choice = '化科系'
# df_senior = df_senior_original[df_senior_original['科系']==choice]
# selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique())
# # selected_options = ['化科系','企管系']
# collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
# dataframes = [Frequency_Distribution(df, 7) for df in collections]
# combined_df = pd.concat(dataframes, keys=selected_options)
# # combined_df = pd.concat([dataframes[0], dataframes[1]], axis=0)




df_streamlit = []
column_title = []




####### Part4  
###### Part4-1 協助學生瞭解就業市場現況與產業發展趨勢
with st.expander("Part 4. 4-1 協助學生瞭解就業市場現況與產業發展趨勢滿意度:"):
    # df_senior.iloc[:,33] ## 1. 協助學生瞭解就業市場現況與產業發展趨勢
    column_index = 33
    item_name = "協助學生瞭解就業市場現況與產業發展趨勢滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'化科系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()
        
    # # 获取level 0索引的唯一值并保持原始顺序
    # unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        # rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
        rects = ax.bar(index, df['比例'], width=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    # ### 设置y轴刻度标签
    # ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    # ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)
    
    ### 设置x轴刻度标签
    ax.set_xticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题
    ax.set_title(item_name,fontsize=title_fontsize)
    
    # ### 设置x轴标签
    # # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    # ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    
    ### 设置y轴标签
    # ax.set_ylabel('满意度',fontsize=xlabel_fontsize)
    ax.set_ylabel('比例',fontsize=xlabel_fontsize)
    
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  



###### Part4-2 協助學生生涯發展與規劃
with st.expander("4-2 協助學生生涯發展與規劃滿意度:"):
    # df_senior.iloc[:,34] ## 2. 協助學生生涯發展與規劃
    column_index = 34
    item_name = "協助學生生涯發展與規劃滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()
        
    # # 获取level 0索引的唯一值并保持原始顺序
    # unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  



###### Part4-3 生涯與就業輔導服務品質
with st.expander("4-3 生涯與就業輔導服務品質滿意度:"):
    # df_senior.iloc[:,35] ## 3. 生涯與就業輔導服務品質
    column_index = 35
    item_name = "生涯與就業輔導服務品質滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()
        
    # # 获取level 0索引的唯一值并保持原始顺序
    # unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔




####### Part5  
###### Part5-1 提供國外修課、實習或交換學生機會
with st.expander("Part 5. 5-1 提供國外修課、實習或交換學生機會滿意度:"):
    # df_senior.iloc[:,37] ## 1. 提供國外修課、實習或交換學生機會
    column_index = 37
    item_name = "提供國外修課、實習或交換學生機會滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  



###### Part5-2 提供與外籍人士或國際社群互動交流的機會
with st.expander("5-2 提供與外籍人士或國際社群互動交流的機會滿意度:"):
    # df_senior.iloc[:,38] ## 2. 提供與外籍人士或國際社群互動交流的機會
    column_index = 38
    item_name = "提供與外籍人士或國際社群互動交流的機會滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  



###### Part5-3 外語學習機會與環境
with st.expander("5-3 外語學習機會與環境滿意度:"):
    # df_senior.iloc[:,39] ## 3.外語學習機會與環境
    column_index = 39
    item_name = "外語學習機會與環境滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  



###### Part5-4 提供瞭解外國政治、經濟、社會、文化情況的機會
with st.expander("5-4 提供瞭解外國政治、經濟、社會、文化情況的機會滿意度:"):
    # df_senior.iloc[:,40] ## 4. 提供瞭解外國政治、經濟、社會、文化情況的機會
    column_index = 40
    item_name = "提供瞭解外國政治、經濟、社會、文化情況的機會滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  




####### Part6  
###### Part6-1 校園環境規劃與維護
with st.expander("Part 6. 6-1 校園環境規劃與維護滿意度:"):
    #df_senior.iloc[:,42] ## 1. 校園環境規劃與維護
    column_index = 42
    item_name = "校園環境規劃與維護滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  



###### Part6-2 校園內的安全保障
with st.expander("6-2 校園內的安全保障滿意度:"):
    #df_senior.iloc[:,43] ## 2. 校園內的安全保障
    column_index = 43
    item_name = "校園內的安全保障滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  


###### Part6-3 學校各項收費
with st.expander("6-3 學校各項收費滿意度:"):
    #df_senior.iloc[:,44] ## 3. 學校各項收費
    column_index = 44
    item_name = "學校各項收費滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  



###### Part6-4 電腦網路設備
with st.expander("6-4 電腦網路設備滿意度:"):
    #df_senior.iloc[:,45] ## 4. 電腦網路設備
    column_index = 45
    item_name = "電腦網路設備滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  



###### Part6-5 運動休閒設施
with st.expander("6-5 運動休閒設施滿意度:"):
    #df_senior.iloc[:,46] ## 5. 運動休閒設施
    column_index = 46
    item_name = "運動休閒設施滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  



###### Part6-6 學校生活機能便利性
with st.expander("6-6 學校生活機能便利性滿意度:"):
    #df_senior.iloc[:,47] ## 6. 學校生活機能便利性
    column_index = 47
    item_name = "學校生活機能便利性滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  



###### Part6-7 學生宿舍數量
with st.expander("6-7 學生宿舍數量滿意度:"):
    #df_senior.iloc[:,48] ## 7. 學生宿舍數量
    column_index = 48
    item_name = "學生宿舍數量滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  




####### Part7  
###### Part7-1 學校的聲譽
with st.expander("Part 7. 7-1 學校的聲譽滿意度:"):
    #df_senior.iloc[:,50] ## 1. 學校的聲譽
    column_index = 50
    item_name = "學校的聲譽滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  



###### Part7-2 學校的進步程度
with st.expander("7-2 學校的進步程度滿意度:"):
    #df_senior.iloc[:,51] ## 2. 學校的進步程度
    column_index = 51
    item_name = "學校的進步程度滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  



###### Part7-3 學校定位與特色
with st.expander("7-3 學校定位與特色滿意度:"):
    #df_senior.iloc[:,52] ## 3. 學校定位與特色
    column_index = 52
    item_name = "學校定位與特色滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  


###### Part7-4 學校學風自由開放程度
with st.expander("7-4 學校學風自由開放程度滿意度:"):
    #df_senior.iloc[:,53] ## 4. 學校學風自由開放程度
    column_index = 53
    item_name = "學校學風自由開放程度滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  




####### Part8  
###### Part8-1 如果可以重來，您是否仍會就讀同一主修領域、學群或學類？
with st.expander("Part 8. 8-1 如果可以重來，您是否仍會就讀同一主修領域、學群或學類:"):
    #df_senior.iloc[:,55] ## 1. 如果可以重來，您是否仍會就讀同一主修領域、學群或學類？
    column_index = 55
    item_name = "如果可以重來，您是否仍會就讀同一主修領域、學群或學類"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  



###### Part8-2 如果可以重來，您是否仍會就讀本校的同一系？
with st.expander("8-2 如果可以重來，您是否仍會就讀本校的同一系:"):
    #df_senior.iloc[:,56] ## 2. 如果可以重來，您是否仍會就讀本校的同一系？
    column_index = 56
    item_name = "如果可以重來，您是否仍會就讀本校的同一系"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  



###### Part8-3 如果可以重來，您是否仍會就讀本校？
with st.expander("8-3 如果可以重來，您是否仍會就讀本校:"):
    #df_senior.iloc[:,57] ## 3. 如果可以重來，您是否仍會就讀本校？
    column_index = 57
    item_name = "如果可以重來，您是否仍會就讀本校"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  


# ###### Part8-4 整體而言，您對畢業母校在辦理教學上的評價如何？
# with st.expander("8-4 整體而言，您對畢業母校在辦理教學上的評價如何 (滿分10):"):
#     # df_senior.iloc[:,58] ## 4. 整體而言，您對畢業母校在辦理教學上的評價如何？
#     column_index = 58
#     item_name = "整體而言，您對畢業母校在辦理教學上的評價如何 (盒鬚圖,範圍1-10,數字為平均值)"
#     column_title.append(df_senior.columns[column_index][3:])
    
    
#     ##### 使用Streamlit畫單一圖
#     # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
#     if 院_系 == '0':
#         collections = [df_senior, df_senior_faculty, df_senior_original]
#         #### 将三組dataframes 對於 column_index 所在的行的資料, 將其转换为数值类型float，忽略无法转换的值
#         Series = [df[df.columns[column_index]].apply(to_numeric_ignore_special_str) for df in collections]
#         #### 将这些 Series 合并为一个 DataFrame. 将长度不相等的多个pandas.core.series.Series合并为一个DataFrame, 当合并长度不相等的Series时，缺失的数据会用NaN（Not a Number）来填充。
#         combined_df = pd.DataFrame({choice: Series[0], choice_faculty: Series[1], '全校': Series[2]})

#         #### 設置 matplotlib 支持中文的字體: 
#         # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
#         # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
#         # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
#         matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
#         matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

#         #### 设置字体大小
#         title_fontsize = 15
#         xlabel_fontsize = 14
#         ylabel_fontsize = 14
#         xticklabel_fontsize = 14
#         yticklabel_fontsize = 14
#         annotation_fontsize = 8
#         legend_fontsize = 14

#         plt.figure(figsize=(10, 6))
#         sns.boxplot(data=combined_df)

#         #### 标示平均值
#         for i in range(combined_df.shape[1]):
#             y = combined_df.iloc[:, i].mean()
#             plt.text(i, y, f'{y:.2f}', ha='center', va='center',fontweight='bold', color='blue',fontsize = 14)
#         plt.title(item_name,fontsize=title_fontsize)
#         plt.ylim(0, 11)
#         plt.ylabel('分數',fontsize=ylabel_fontsize)
#         plt.xticks(fontsize=xticklabel_fontsize)  #
#         # plt.show()
#         #### 在Streamlit中显示
#         st.pyplot(plt)


#     if 院_系 == '1':
#         collections = [df_senior,df_senior_original]
#         #### 将三組dataframes 對於 column_index 所在的行的資料, 將其转换为数值类型float，忽略无法转换的值
#         Series = [df[df.columns[column_index]].apply(to_numeric_ignore_special_str) for df in collections]
#         #### 将这些 Series 合并为一个 DataFrame. 将长度不相等的多个pandas.core.series.Series合并为一个DataFrame, 当合并长度不相等的Series时，缺失的数据会用NaN（Not a Number）来填充。
#         combined_df = pd.DataFrame({choice: Series[0], '全校': Series[1]})


#         #### 設置中文顯示
#         # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
#         # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
#         matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
#         matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

#         #### 设置字体大小
#         title_fontsize = 15
#         xlabel_fontsize = 14
#         ylabel_fontsize = 14
#         xticklabel_fontsize = 14
#         yticklabel_fontsize = 14
#         annotation_fontsize = 8
#         legend_fontsize = 14

#         plt.figure(figsize=(10, 6))
#         sns.boxplot(data=combined_df)
#         ### 标示平均值
#         for i in range(combined_df.shape[1]):
#             y = combined_df.iloc[:, i].mean()
#             plt.text(i, y, f'{y:.2f}', ha='center', va='center',fontweight='bold', color='blue',fontsize = 14)
#         plt.title(item_name,fontsize=title_fontsize)
#         plt.ylim(0, 11)
#         plt.ylabel('分數',fontsize=ylabel_fontsize)
#         plt.xticks(fontsize=xticklabel_fontsize)  #
#         # plt.show()
#         ### 在Streamlit中显示
#         st.pyplot(plt)


#     ##### 使用streamlit 畫比較圖
#     # st.subheader("不同單位比較")
#     if 院_系 == '0':
#         ## 使用multiselect组件让用户进行多重选择
#         selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
#         collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
       
        
#     elif 院_系 == '1':
#         ## 使用multiselect组件让用户进行多重选择
#         selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
#         collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]


#     #### 将所選擇的系或院的dataframes 對於 column_index 所在的行的資料, 將其转换为数值类型float，忽略无法转换的值
#     Series = [df[df.columns[column_index]].apply(to_numeric_ignore_special_str) for df in collections]
#     #### 将这些 Series 合并为一个 DataFrame (以selected_options為行名, Series為每一行的值). 将长度不相等的多个pandas.core.series.Series合并为一个DataFrame, 当合并长度不相等的Series时，缺失的数据会用NaN（Not a Number）来填充。
#     combined_df = pd.DataFrame(dict(zip(selected_options, Series)))
     
        
#     #### 設置 matplotlib 支持中文的字體: 
#     # matplotlib.rcParams['font.family']pd.DataFrame( = 'Microsoft YaHei'
#     # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
#     # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
#     matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
#     matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

#     #### 设置字体大小
#     title_fontsize = 15
#     xlabel_fontsize = 14
#     ylabel_fontsize = 14
#     xticklabel_fontsize = 14
#     yticklabel_fontsize = 14
#     annotation_fontsize = 8
#     legend_fontsize = 14

#     plt.figure(figsize=(10, 6))
#     sns.boxplot(data=combined_df)

#     #### 标示平均值
#     for i in range(combined_df.shape[1]):
#         y = combined_df.iloc[:, i].mean()
#         plt.text(i, y, f'{y:.2f}', ha='center', va='center',fontweight='bold', color='blue',fontsize = 14)
#     plt.title(item_name,fontsize=title_fontsize)
#     plt.ylim(0, 11)
#     plt.ylabel('分數',fontsize=ylabel_fontsize)
#     plt.xticks(fontsize=xticklabel_fontsize)  #
#     # plt.show()
#     #### 在Streamlit中显示
#     st.pyplot(plt)

# st.markdown("##")  ## 更大的间隔



# ###### Part8-5 和國內其他大學相較，您覺得畢業母校競爭力如何？
# with st.expander("8-5 和國內其他大學相較，您覺得畢業母校競爭力如何 (滿分10):"):
#     # df_senior.iloc[:,59] ## 5. 和國內其他大學相較，您覺得畢業母校競爭力如何？
#     column_index = 59
#     item_name = "和國內其他大學相較，您覺得畢業母校競爭力如何 (盒鬚圖,範圍1-10,數字為平均值)"
#     column_title.append(df_senior.columns[column_index][3:])
    
    
#     ##### 使用Streamlit畫單一圖
#     # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
#     if 院_系 == '0':
#         collections = [df_senior, df_senior_faculty, df_senior_original]
#         #### 将三組dataframes 對於 column_index 所在的行的資料, 將其转换为数值类型float，忽略无法转换的值
#         Series = [df[df.columns[column_index]].apply(to_numeric_ignore_special_str) for df in collections]
#         #### 将这些 Series 合并为一个 DataFrame. 将长度不相等的多个pandas.core.series.Series合并为一个DataFrame, 当合并长度不相等的Series时，缺失的数据会用NaN（Not a Number）来填充。
#         combined_df = pd.DataFrame({choice: Series[0], choice_faculty: Series[1], '全校': Series[2]})

#         #### 設置 matplotlib 支持中文的字體: 
#         # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
#         # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
#         # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
#         matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
#         matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

#         #### 设置字体大小
#         title_fontsize = 15
#         xlabel_fontsize = 14
#         ylabel_fontsize = 14
#         xticklabel_fontsize = 14
#         yticklabel_fontsize = 14
#         annotation_fontsize = 8
#         legend_fontsize = 14

#         plt.figure(figsize=(10, 6))
#         sns.boxplot(data=combined_df)

#         #### 标示平均值
#         for i in range(combined_df.shape[1]):
#             y = combined_df.iloc[:, i].mean()
#             plt.text(i, y, f'{y:.2f}', ha='center', va='center',fontweight='bold', color='blue',fontsize = 14)
#         plt.title(item_name,fontsize=title_fontsize)
#         plt.ylim(0, 11)
#         plt.ylabel('分數',fontsize=ylabel_fontsize)
#         plt.xticks(fontsize=xticklabel_fontsize)  #
#         # plt.show()
#         #### 在Streamlit中显示
#         st.pyplot(plt)


#     if 院_系 == '1':
#         collections = [df_senior,df_senior_original]
#         #### 将三組dataframes 對於 column_index 所在的行的資料, 將其转换为数值类型float，忽略无法转换的值
#         Series = [df[df.columns[column_index]].apply(to_numeric_ignore_special_str) for df in collections]
#         #### 将这些 Series 合并为一个 DataFrame. 将长度不相等的多个pandas.core.series.Series合并为一个DataFrame, 当合并长度不相等的Series时，缺失的数据会用NaN（Not a Number）来填充。
#         combined_df = pd.DataFrame({choice: Series[0], '全校': Series[1]})


#         #### 設置中文顯示
#         # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
#         # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
#         matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
#         matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

#         #### 设置字体大小
#         title_fontsize = 15
#         xlabel_fontsize = 14
#         ylabel_fontsize = 14
#         xticklabel_fontsize = 14
#         yticklabel_fontsize = 14
#         annotation_fontsize = 8
#         legend_fontsize = 14

#         plt.figure(figsize=(10, 6))
#         sns.boxplot(data=combined_df)
#         ### 标示平均值
#         for i in range(combined_df.shape[1]):
#             y = combined_df.iloc[:, i].mean()
#             plt.text(i, y, f'{y:.2f}', ha='center', va='center',fontweight='bold', color='blue',fontsize = 14)
#         plt.title(item_name,fontsize=title_fontsize)
#         plt.ylim(0, 11)
#         plt.ylabel('分數',fontsize=ylabel_fontsize)
#         plt.xticks(fontsize=xticklabel_fontsize)  #
#         # plt.show()
#         ### 在Streamlit中显示
#         st.pyplot(plt)


#     ##### 使用streamlit 畫比較圖
#     # st.subheader("不同單位比較")
#     if 院_系 == '0':
#         ## 使用multiselect组件让用户进行多重选择
#         selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
#         collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
       
        
#     elif 院_系 == '1':
#         ## 使用multiselect组件让用户进行多重选择
#         selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
#         collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]


#     #### 将所選擇的系或院的dataframes 對於 column_index 所在的行的資料, 將其转换为数值类型float，忽略无法转换的值
#     Series = [df[df.columns[column_index]].apply(to_numeric_ignore_special_str) for df in collections]
#     #### 将这些 Series 合并为一个 DataFrame (以selected_options為行名, Series為每一行的值). 将长度不相等的多个pandas.core.series.Series合并为一个DataFrame, 当合并长度不相等的Series时，缺失的数据会用NaN（Not a Number）来填充。
#     combined_df = pd.DataFrame(dict(zip(selected_options, Series)))
     
        
#     #### 設置 matplotlib 支持中文的字體: 
#     # matplotlib.rcParams['font.family']pd.DataFrame( = 'Microsoft YaHei'
#     # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
#     # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
#     matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
#     matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

#     #### 设置字体大小
#     title_fontsize = 15
#     xlabel_fontsize = 14
#     ylabel_fontsize = 14
#     xticklabel_fontsize = 14
#     yticklabel_fontsize = 14
#     annotation_fontsize = 8
#     legend_fontsize = 14

#     plt.figure(figsize=(10, 6))
#     sns.boxplot(data=combined_df)

#     #### 标示平均值
#     for i in range(combined_df.shape[1]):
#         y = combined_df.iloc[:, i].mean()
#         plt.text(i, y, f'{y:.2f}', ha='center', va='center',fontweight='bold', color='blue',fontsize = 14)
#     plt.title(item_name,fontsize=title_fontsize)
#     plt.ylim(0, 11)
#     plt.ylabel('分數',fontsize=ylabel_fontsize)
#     plt.xticks(fontsize=xticklabel_fontsize)  #
#     # plt.show()
#     #### 在Streamlit中显示
#     st.pyplot(plt)

# st.markdown("##")  ## 更大的间隔  

























####### Part1  
###### Part1-1 系師資素質與專長
with st.expander("Part 1. 1-1 系師資素質與專長滿意度:"):
    # df_senior.iloc[:,9] ## 1. 系師資素質與專長
    column_index = 9
    item_name = "系師資素質與專長滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔    




###### Part1-2 系的教學品質
with st.expander("1-2 系的教學品質滿意度:"):
    # df_senior.iloc[:,10] ## 2. 系的教學品質
    column_index = 10
    item_name = "系的教學品質滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  


###### Part1-3 系上師生間的互動關係
with st.expander("1-3 系上師生間的互動關係滿意度:"):
    # df_senior.iloc[:,11] ## 3. 系上師生間的互動關係
    column_index = 11
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔   



###### Part1-4 系課程內容
with st.expander("1-4 系課程內容滿意度:"):
    # df_senior.iloc[:,12] ## 4. 系課程內容
    column_index = 12
    item_name = "系課程內容滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔   



###### Part1-5 系對學生思辨與探究能力的培養
with st.expander("1-5 系對學生思辨與探究能力的培養滿意度:"):
    # df_senior.iloc[:,13] ## 5. 系對學生思辨與探究能力的培養
    column_index = 13
    item_name = "系對學生思辨與探究能力的培養滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  



###### Part1-6 系對學生創新或創造力的培養
with st.expander("1-6 系對學生創新或創造力的培養滿意度:"):
    # df_senior.iloc[:,14] ## 6. 系對學生創新或創造力的培養
    column_index = 14
    item_name = "系對學生創新或創造力的培養滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  



###### Part1-7 系對學生在專業領域中具競爭力的培育
with st.expander("1-7 系對學生在專業領域中具競爭力的培育滿意度:"):
    # df_senior.iloc[:,15] ## 7. 系對學生在專業領域中具競爭力的培育
    column_index = 15
    item_name = "系對學生在專業領域中具競爭力的培育滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔   



###### Part1-8 系修課規定
with st.expander("1-8 系修課規定滿意度:"):
    # df_senior.iloc[:,16] ## 8.系修課規定
    column_index = 16
    item_name = "系修課規定滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔    



###### Part1-9 系的學習風氣
with st.expander("1-9 系的學習風氣滿意度:"):
    # df_senior.iloc[:,17] ## 9. 系的學習風氣
    column_index = 17
    item_name = "系的學習風氣滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  




####### Part2  
###### Part2-1 系的空間環境與設備  
with st.expander("Part 2. 2-1 系的空間環境與設備滿意度:"):
    # df_senior.iloc[:,19] ## 1. 系的空間環境與設備
    column_index = 19
    item_name = "系的空間環境與設備滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  



###### Part2-2 系行政人員的服務品質 
with st.expander("2-2 系行政人員的服務品質滿意度:"):
    # df_senior.iloc[:,20] ## 2. 系行政人員的服務品質
    column_index = 20
    item_name = "系行政人員的服務品質滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  



###### Part2-3 系提供的工讀與獎助機會
with st.expander("2-3 系提供的工讀與獎助機會滿意度:"):
    # df_senior.iloc[:,21] ## 3. 系提供的工讀與獎助機會
    column_index = 21
    item_name = "系提供的工讀與獎助機會滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  



###### Part2-4 系提供的相關學習活動
with st.expander("2-4 系提供的相關學習活動滿意度:"):
    # df_senior.iloc[:,22] ## 4. 系提供的相關學習活動
    column_index = 22
    item_name = "系提供的相關學習活動滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  



###### Part2-5 系提供給學生的學習協助
with st.expander("2-5 系提供給學生的學習協助滿意度:"):
    # df_senior.iloc[:,23] ## 5.系提供給學生的學習協助
    column_index = 23
    item_name = "系提供給學生的學習協助滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  



###### Part2-6 系對學生的生涯輔導
with st.expander("2-6 系對學生的生涯輔導滿意度:"):
    # df_senior.iloc[:,24] ## 6. 系對學生的生涯輔導
    column_index = 24
    item_name = "系對學生的生涯輔導滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  



###### Part2-7 系對學生意見與需求的重視
with st.expander("2-7 系對學生意見與需求的重視滿意度:"):
    # df_senior.iloc[:,25] ## 7. 系對學生意見與需求的重視
    column_index = 25
    item_name = "系對學生意見與需求的重視滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  


####### Part3  
###### Part3-1 目前就讀系的聲譽
with st.expander("Part 3. 3-1 目前就讀系的聲譽滿意度:"):
    # df_senior.iloc[:,27] ## 1. 目前就讀系的聲譽
    column_index = 27
    item_name = "目前就讀系的聲譽滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  



###### Part3-2 系的進步程度
with st.expander("3-2 系的進步程度滿意度:"):
    # df_senior.iloc[:,28] ## 2. 系的進步程度
    column_index = 28
    item_name = "系的進步程度滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  



###### Part3-3 系定位與特色
with st.expander("3-3 系定位與特色滿意度:"):
    # df_senior.iloc[:,29] ## 3. 系定位與特色
    column_index = 29
    item_name = "系定位與特色滿意度"
    column_title.append(df_senior.columns[column_index][3:])
    ##### 将字符串按逗号分割并展平
    split_values = df_senior.iloc[:,column_index].str.split(',').explode()
    ##### 计算不同子字符串的出现次数
    value_counts = split_values.value_counts()
    ##### 计算不同子字符串的比例
    proportions = value_counts/value_counts.sum()
    # proportions = value_counts/df_senior.shape[0]   ## 
    ##### 轉換成 numpy array
    value_counts_numpy = value_counts.values
    proportions_numpy = proportions.values
    items_numpy = proportions.index.to_numpy()
    ##### 创建一个新的DataFrame来显示结果
    result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
    ##### 存到 list 'df_streamlit'
    df_streamlit.append(result_df)  


    ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
    # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
    st.write(result_df.to_html(index=False), unsafe_allow_html=True)
    st.markdown("##")  ## 更大的间隔


    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
        ## 形成所有學系'項目'欄位的所有值
        # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
        # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
        #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
        desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
        desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
        # 获取level 0索引的唯一值并保持原始顺序
        unique_level0 = combined_df.index.get_level_values(0).unique()

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 设置条形的宽度
        bar_width = 0.2
        #### 设置y轴的位置
        r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14
        #### 绘制条形
        fig, ax = plt.subplots(figsize=(10, 6))
        # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
        for i, college_name in enumerate(unique_level0):            
            df = combined_df.loc[college_name]
            # 计算当前分组的条形数量
            num_bars = len(df)
            # 生成当前分组的y轴位置
            index = np.arange(num_bars) + i * bar_width
            # index = r + i * bar_width
            rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
            # # 在每个条形上标示比例
            # for rect, ratio in zip(rects, df['比例']):
            #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
        ### 添加图例
        ax.legend(fontsize=legend_fontsize)

        # ### 添加x轴标签
        # ## 计算每个组的中心位置作为x轴刻度位置
        # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
        # # group_centers = np.arange(len(dataframes[0]))
        # ## 添加x轴标签
        # # ax.set_xticks(group_centers)
        # # dataframes[0]['項目'].values
        # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
        # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
        # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
        # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
        ### 设置y轴刻度标签
        ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
        ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


        ### 设置标题和轴标签
        ax.set_title(item_name,fontsize=title_fontsize)
        # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
        ax.set_xlabel('比例',fontsize=xlabel_fontsize)
        ### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        plt.tight_layout()
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)

    if 院_系 == '1':
        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        #### 创建图形和坐标轴
        plt.figure(figsize=(11, 8))
        #### 绘制条形图
        ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
        result_df = result_df.iloc[::-1].reset_index(drop=True)
        plt.barh(result_df['項目'], result_df['人數'], label=choice)
        #### 標示比例數據
        for i in range(len(result_df['項目'])):
            plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
        #### 添加一些图形元素
        plt.title(item_name, fontsize=15)
        plt.xlabel('人數', fontsize=14)
        #plt.ylabel('本校現在所提供的資源或支援事項')
        #### 调整x轴和y轴刻度标签的字体大小
        plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
        plt.legend(fontsize=14)
        #### 显示网格线
        plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
        #### 显示图形
        ### 一般顯示
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]
        combined_df = pd.concat(dataframes, keys=selected_options)
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
        dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
        ## 形成所有學系'項目'欄位的所有值
        desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
        ## 缺的項目值加以擴充， 並統一一樣的項目次序
        dataframes = [adjust_df(df, desired_order) for df in dataframes]        
        combined_df = pd.concat(dataframes, keys=selected_options)
        
    # 获取level 0索引的唯一值并保持原始顺序
    unique_level0 = combined_df.index.get_level_values(0).unique()

    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    #### 设置条形的宽度
    bar_width = 0.2
    #### 设置y轴的位置
    r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14
    #### 绘制条形
    fig, ax = plt.subplots(figsize=(10, 6))
    # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
    for i, college_name in enumerate(unique_level0):            
        df = combined_df.loc[college_name]
        # 计算当前分组的条形数量
        num_bars = len(df)
        # 生成当前分组的y轴位置
        index = np.arange(num_bars) + i * bar_width
        # index = r + i * bar_width
        rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

        # # 在每个条形上标示比例
        # for rect, ratio in zip(rects, df['比例']):
        #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
    ### 添加图例
    ax.legend(fontsize=legend_fontsize)

    # ### 添加x轴标签
    # ## 计算每个组的中心位置作为x轴刻度位置
    # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
    # # group_centers = np.arange(len(dataframes[0]))
    # ## 添加x轴标签
    # # ax.set_xticks(group_centers)
    # # dataframes[0]['項目'].values
    # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
    # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
    # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
    # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

    ### 设置y轴刻度标签
    ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
    ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


    ### 设置标题和轴标签
    ax.set_title(item_name,fontsize=title_fontsize)
    # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
    ax.set_xlabel('比例',fontsize=xlabel_fontsize)
    ### 显示网格线
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
    plt.tight_layout()
    # plt.show()
    ### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔  


###### Part3-4 畢業系所在辦理教學上的評價
with st.expander("3-4 畢業系所在辦理教學上的評價 (滿分10):"):
    # df_senior.iloc[:,30] ## 4. 整體而言，您對畢業系所在辦理教學上的評價如何？
    column_index = 30
    item_name = "畢業系所在辦理教學上的評價 (盒鬚圖,範圍1-10,數字為平均值)"
    column_title.append(df_senior.columns[column_index][3:])
    
    
    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        #### 将三組dataframes 對於 column_index 所在的行的資料, 將其转换为数值类型float，忽略无法转换的值
        Series = [df[df.columns[column_index]].apply(to_numeric_ignore_special_str) for df in collections]
        #### 将这些 Series 合并为一个 DataFrame. 将长度不相等的多个pandas.core.series.Series合并为一个DataFrame, 当合并长度不相等的Series时，缺失的数据会用NaN（Not a Number）来填充。
        combined_df = pd.DataFrame({choice: Series[0], choice_faculty: Series[1], '全校': Series[2]})

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14

        plt.figure(figsize=(10, 6))
        sns.boxplot(data=combined_df)

        #### 标示平均值
        for i in range(combined_df.shape[1]):
            y = combined_df.iloc[:, i].mean()
            plt.text(i, y, f'{y:.2f}', ha='center', va='center',fontweight='bold', color='blue',fontsize = 14)
        plt.title(item_name,fontsize=title_fontsize)
        plt.ylim(0, 11)
        plt.ylabel('分數',fontsize=ylabel_fontsize)
        plt.xticks(fontsize=xticklabel_fontsize)  #
        # plt.show()
        #### 在Streamlit中显示
        st.pyplot(plt)


    if 院_系 == '1':
        collections = [df_senior,df_senior_original]
        #### 将三組dataframes 對於 column_index 所在的行的資料, 將其转换为数值类型float，忽略无法转换的值
        Series = [df[df.columns[column_index]].apply(to_numeric_ignore_special_str) for df in collections]
        #### 将这些 Series 合并为一个 DataFrame. 将长度不相等的多个pandas.core.series.Series合并为一个DataFrame, 当合并长度不相等的Series时，缺失的数据会用NaN（Not a Number）来填充。
        combined_df = pd.DataFrame({choice: Series[0], '全校': Series[1]})


        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14

        plt.figure(figsize=(10, 6))
        sns.boxplot(data=combined_df)
        ### 标示平均值
        for i in range(combined_df.shape[1]):
            y = combined_df.iloc[:, i].mean()
            plt.text(i, y, f'{y:.2f}', ha='center', va='center',fontweight='bold', color='blue',fontsize = 14)
        plt.title(item_name,fontsize=title_fontsize)
        plt.ylim(0, 11)
        plt.ylabel('分數',fontsize=ylabel_fontsize)
        plt.xticks(fontsize=xticklabel_fontsize)  #
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
       
        
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]


    #### 将所選擇的系或院的dataframes 對於 column_index 所在的行的資料, 將其转换为数值类型float，忽略无法转换的值
    Series = [df[df.columns[column_index]].apply(to_numeric_ignore_special_str) for df in collections]
    #### 将这些 Series 合并为一个 DataFrame (以selected_options為行名, Series為每一行的值). 将长度不相等的多个pandas.core.series.Series合并为一个DataFrame, 当合并长度不相等的Series时，缺失的数据会用NaN（Not a Number）来填充。
    combined_df = pd.DataFrame(dict(zip(selected_options, Series)))
     
        
    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family']pd.DataFrame( = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14

    plt.figure(figsize=(10, 6))
    sns.boxplot(data=combined_df)

    #### 标示平均值
    for i in range(combined_df.shape[1]):
        y = combined_df.iloc[:, i].mean()
        plt.text(i, y, f'{y:.2f}', ha='center', va='center',fontweight='bold', color='blue',fontsize = 14)
    plt.title(item_name,fontsize=title_fontsize)
    plt.ylim(0, 11)
    plt.ylabel('分數',fontsize=ylabel_fontsize)
    plt.xticks(fontsize=xticklabel_fontsize)  #
    # plt.show()
    #### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔
    


###### Part3-5 和國內其他類似系所相較，畢業系所競爭力
with st.expander("3-5 和國內其他類似系所相較，畢業系所競爭力 (滿分10):"):
    # df_senior.iloc[:,31] ## 5. 和國內其他類似系所相較，您覺得畢業的系所競爭力如何？
    column_index = 31
    item_name = "和國內其他類似系所相較，畢業系所競爭力 (盒鬚圖,範圍1-10,數字為平均值)"
    column_title.append(df_senior.columns[column_index][3:])
    
    
    ##### 使用Streamlit畫單一圖
    # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
    if 院_系 == '0':
        collections = [df_senior, df_senior_faculty, df_senior_original]
        #### 将三組dataframes 對於 column_index 所在的行的資料, 將其转换为数值类型float，忽略无法转换的值
        Series = [df[df.columns[column_index]].apply(to_numeric_ignore_special_str) for df in collections]
        #### 将这些 Series 合并为一个 DataFrame. 将长度不相等的多个pandas.core.series.Series合并为一个DataFrame, 当合并长度不相等的Series时，缺失的数据会用NaN（Not a Number）来填充。
        combined_df = pd.DataFrame({choice: Series[0], choice_faculty: Series[1], '全校': Series[2]})

        #### 設置 matplotlib 支持中文的字體: 
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14

        plt.figure(figsize=(10, 6))
        sns.boxplot(data=combined_df)

        #### 标示平均值
        for i in range(combined_df.shape[1]):
            y = combined_df.iloc[:, i].mean()
            plt.text(i, y, f'{y:.2f}', ha='center', va='center',fontweight='bold', color='blue',fontsize = 14)
        plt.title(item_name,fontsize=title_fontsize)
        plt.ylim(0, 11)
        plt.ylabel('分數',fontsize=ylabel_fontsize)
        plt.xticks(fontsize=xticklabel_fontsize)  #
        # plt.show()
        #### 在Streamlit中显示
        st.pyplot(plt)


    if 院_系 == '1':
        collections = [df_senior,df_senior_original]
        #### 将三組dataframes 對於 column_index 所在的行的資料, 將其转换为数值类型float，忽略无法转换的值
        Series = [df[df.columns[column_index]].apply(to_numeric_ignore_special_str) for df in collections]
        #### 将这些 Series 合并为一个 DataFrame. 将长度不相等的多个pandas.core.series.Series合并为一个DataFrame, 当合并长度不相等的Series时，缺失的数据会用NaN（Not a Number）来填充。
        combined_df = pd.DataFrame({choice: Series[0], '全校': Series[1]})


        #### 設置中文顯示
        # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
        # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

        #### 设置字体大小
        title_fontsize = 15
        xlabel_fontsize = 14
        ylabel_fontsize = 14
        xticklabel_fontsize = 14
        yticklabel_fontsize = 14
        annotation_fontsize = 8
        legend_fontsize = 14

        plt.figure(figsize=(10, 6))
        sns.boxplot(data=combined_df)
        ### 标示平均值
        for i in range(combined_df.shape[1]):
            y = combined_df.iloc[:, i].mean()
            plt.text(i, y, f'{y:.2f}', ha='center', va='center',fontweight='bold', color='blue',fontsize = 14)
        plt.title(item_name,fontsize=title_fontsize)
        plt.ylim(0, 11)
        plt.ylabel('分數',fontsize=ylabel_fontsize)
        plt.xticks(fontsize=xticklabel_fontsize)  #
        # plt.show()
        ### 在Streamlit中显示
        st.pyplot(plt)


    ##### 使用streamlit 畫比較圖
    # st.subheader("不同單位比較")
    if 院_系 == '0':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
        collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
       
        
    elif 院_系 == '1':
        ## 使用multiselect组件让用户进行多重选择
        selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
        collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]


    #### 将所選擇的系或院的dataframes 對於 column_index 所在的行的資料, 將其转换为数值类型float，忽略无法转换的值
    Series = [df[df.columns[column_index]].apply(to_numeric_ignore_special_str) for df in collections]
    #### 将这些 Series 合并为一个 DataFrame (以selected_options為行名, Series為每一行的值). 将长度不相等的多个pandas.core.series.Series合并为一个DataFrame, 当合并长度不相等的Series时，缺失的数据会用NaN（Not a Number）来填充。
    combined_df = pd.DataFrame(dict(zip(selected_options, Series)))
     
        
    #### 設置 matplotlib 支持中文的字體: 
    # matplotlib.rcParams['font.family']pd.DataFrame( = 'Microsoft YaHei'
    # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    #### 设置字体大小
    title_fontsize = 15
    xlabel_fontsize = 14
    ylabel_fontsize = 14
    xticklabel_fontsize = 14
    yticklabel_fontsize = 14
    annotation_fontsize = 8
    legend_fontsize = 14

    plt.figure(figsize=(10, 6))
    sns.boxplot(data=combined_df)

    #### 标示平均值
    for i in range(combined_df.shape[1]):
        y = combined_df.iloc[:, i].mean()
        plt.text(i, y, f'{y:.2f}', ha='center', va='center',fontweight='bold', color='blue',fontsize = 14)
    plt.title(item_name,fontsize=title_fontsize)
    plt.ylim(0, 11)
    plt.ylabel('分數',fontsize=ylabel_fontsize)
    plt.xticks(fontsize=xticklabel_fontsize)  #
    # plt.show()
    #### 在Streamlit中显示
    st.pyplot(plt)

st.markdown("##")  ## 更大的间隔




# ####### Part4  
# ###### Part4-1 協助學生瞭解就業市場現況與產業發展趨勢
# with st.expander("Part 4. 4-1 協助學生瞭解就業市場現況與產業發展趨勢滿意度:"):
#     # df_senior.iloc[:,33] ## 1. 協助學生瞭解就業市場現況與產業發展趨勢
#     column_index = 33
#     item_name = "協助學生瞭解就業市場現況與產業發展趨勢滿意度"
#     column_title.append(df_senior.columns[column_index][3:])
#     ##### 将字符串按逗号分割并展平
#     split_values = df_senior.iloc[:,column_index].str.split(',').explode()
#     ##### 计算不同子字符串的出现次数
#     value_counts = split_values.value_counts()
#     ##### 计算不同子字符串的比例
#     proportions = value_counts/value_counts.sum()
#     # proportions = value_counts/df_senior.shape[0]   ## 
#     ##### 轉換成 numpy array
#     value_counts_numpy = value_counts.values
#     proportions_numpy = proportions.values
#     items_numpy = proportions.index.to_numpy()
#     ##### 创建一个新的DataFrame来显示结果
#     result_df = pd.DataFrame({'項目':items_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#     ##### 存到 list 'df_streamlit'
#     df_streamlit.append(result_df)  


#     ##### 使用Streamlit展示DataFrame "result_df"，但不显示索引
#     # st.write(item_name, result_df.to_html(index=False), unsafe_allow_html=True)
#     st.write(result_df.to_html(index=False), unsafe_allow_html=True)
#     st.markdown("##")  ## 更大的间隔


#     ##### 使用Streamlit畫單一圖
#     # st.markdown(f"圖形中項目(由下至上): {result_df['項目'].values.tolist()}")
#     if 院_系 == '0':
#         collections = [df_senior, df_senior_faculty, df_senior_original]
#         dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]  ## 'dataframes' list 中的各dataframe已經是按照次數高至低的項目順序排列
#         ## 形成所有學系'項目'欄位的所有值
#         # desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()]))
#         # desired_order  = list(set([item for item in dataframes[0]['項目'].tolist()])) 
#         #### 只看所選擇學系的項目(已經是按照次數高至低的項目順序排列), 並且反轉次序使得表與圖的項目次序一致
#         desired_order  = [item for item in dataframes[0]['項目'].tolist()]  ## 只看所選擇學系的項目
#         desired_order = desired_order[::-1]  ## 反轉次序使得表與圖的項目次序一致
#         ## 缺的項目值加以擴充， 並統一一樣的項目次序
#         dataframes = [adjust_df(df, desired_order) for df in dataframes]
#         combined_df = pd.concat(dataframes, keys=[choice,choice_faculty,'全校'])
#         # 获取level 0索引的唯一值并保持原始顺序
#         unique_level0 = combined_df.index.get_level_values(0).unique()

#         #### 設置 matplotlib 支持中文的字體: 
#         # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
#         # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
#         # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
#         matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
#         matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
#         #### 设置条形的宽度
#         bar_width = 0.2
#         #### 设置y轴的位置
#         r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
#         #### 设置字体大小
#         title_fontsize = 15
#         xlabel_fontsize = 14
#         ylabel_fontsize = 14
#         xticklabel_fontsize = 14
#         yticklabel_fontsize = 14
#         annotation_fontsize = 8
#         legend_fontsize = 14
#         #### 绘制条形
#         fig, ax = plt.subplots(figsize=(10, 6))
#         # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
#         for i, college_name in enumerate(unique_level0):            
#             df = combined_df.loc[college_name]
#             # 计算当前分组的条形数量
#             num_bars = len(df)
#             # 生成当前分组的y轴位置
#             index = np.arange(num_bars) + i * bar_width
#             # index = r + i * bar_width
#             rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)
    
#             # # 在每个条形上标示比例
#             # for rect, ratio in zip(rects, df['比例']):
#             #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
#         ### 添加图例
#         ax.legend(fontsize=legend_fontsize)

#         # ### 添加x轴标签
#         # ## 计算每个组的中心位置作为x轴刻度位置
#         # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
#         # # group_centers = np.arange(len(dataframes[0]))
#         # ## 添加x轴标签
#         # # ax.set_xticks(group_centers)
#         # # dataframes[0]['項目'].values
#         # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
#         # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
#         # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
#         # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)
        
#         ### 设置y轴刻度标签
#         ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
#         ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


#         ### 设置标题和轴标签
#         ax.set_title(item_name,fontsize=title_fontsize)
#         # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
#         ax.set_xlabel('比例',fontsize=xlabel_fontsize)
#         ### 显示网格线
#         plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
#         plt.tight_layout()
#         # plt.show()
#         ### 在Streamlit中显示
#         st.pyplot(plt)

#     if 院_系 == '1':
#         #### 設置中文顯示
#         # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
#         # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
#         matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
#         matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
#         #### 创建图形和坐标轴
#         plt.figure(figsize=(11, 8))
#         #### 绘制条形图
#         ### 反轉 dataframe result_df 的所有行的值的次序,  使得表與圖的項目次序一致
#         result_df = result_df.iloc[::-1].reset_index(drop=True)
#         plt.barh(result_df['項目'], result_df['人數'], label=choice)
#         #### 標示比例數據
#         for i in range(len(result_df['項目'])):
#             plt.text(result_df['人數'][i]+1, result_df['項目'][i], f'{result_df.iloc[:, 2][i]:.1%}', fontsize=14)
#         #### 添加一些图形元素
#         plt.title(item_name, fontsize=15)
#         plt.xlabel('人數', fontsize=14)
#         #plt.ylabel('本校現在所提供的資源或支援事項')
#         #### 调整x轴和y轴刻度标签的字体大小
#         plt.tick_params(axis='both', labelsize=14)  # 同时调整x轴和y轴
#         plt.legend(fontsize=14)
#         #### 显示网格线
#         plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
#         #### 显示图形
#         ### 一般顯示
#         # plt.show()
#         ### 在Streamlit中显示
#         st.pyplot(plt)


#     ##### 使用streamlit 畫比較圖
#     # st.subheader("不同單位比較")
#     if 院_系 == '0':
#         ## 使用multiselect组件让用户进行多重选择
#         selected_options = st.multiselect('選擇比較學系：', df_senior_original['科系'].unique(), default=[choice,'企管系'],key=str(column_index)+'d')  ## # selected_options = ['化科系','企管系']
#         collections = [df_senior_original[df_senior_original['科系']==i] for i in selected_options]
#         dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
#         ## 形成所有學系'項目'欄位的所有值
#         desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
#         ## 缺的項目值加以擴充， 並統一一樣的項目次序
#         dataframes = [adjust_df(df, desired_order) for df in dataframes]
#         combined_df = pd.concat(dataframes, keys=selected_options)
#     elif 院_系 == '1':
#         ## 使用multiselect组件让用户进行多重选择
#         selected_options = st.multiselect('選擇比較學院：', df_senior_original['學院'].unique(), default=[choice,'資訊學院'],key=str(column_index)+'f')
#         collections = [df_senior_original[df_senior_original['學院']==i] for i in selected_options]
#         dataframes = [Frequency_Distribution_1(df, column_index) for df in collections]
#         ## 形成所有學系'項目'欄位的所有值
#         desired_order  = list(set([item for df in dataframes for item in df['項目'].tolist()])) 
#         ## 缺的項目值加以擴充， 並統一一樣的項目次序
#         dataframes = [adjust_df(df, desired_order) for df in dataframes]        
#         combined_df = pd.concat(dataframes, keys=selected_options)
        
#     # 获取level 0索引的唯一值并保持原始顺序
#     unique_level0 = combined_df.index.get_level_values(0).unique()

#     #### 設置 matplotlib 支持中文的字體: 
#     # matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
#     # matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
#     # matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
#     matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
#     matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
#     #### 设置条形的宽度
#     bar_width = 0.2
#     #### 设置y轴的位置
#     r = np.arange(len(dataframes[0]))  ## len(result_df_理學_rr)=6, 因為result_df_理學_rr 有 6個 row: 非常滿意, 滿意, 普通, 不滿意, 非常不滿意
#     #### 设置字体大小
#     title_fontsize = 15
#     xlabel_fontsize = 14
#     ylabel_fontsize = 14
#     xticklabel_fontsize = 14
#     yticklabel_fontsize = 14
#     annotation_fontsize = 8
#     legend_fontsize = 14
#     #### 绘制条形
#     fig, ax = plt.subplots(figsize=(10, 6))
#     # for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
#     for i, college_name in enumerate(unique_level0):            
#         df = combined_df.loc[college_name]
#         # 计算当前分组的条形数量
#         num_bars = len(df)
#         # 生成当前分组的y轴位置
#         index = np.arange(num_bars) + i * bar_width
#         # index = r + i * bar_width
#         rects = ax.barh(index, df['比例'], height=bar_width, label=college_name)

#         # # 在每个条形上标示比例
#         # for rect, ratio in zip(rects, df['比例']):
#         #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.1%}', ha='center', va='bottom',fontsize=annotation_fontsize)
#     ### 添加图例
#     ax.legend(fontsize=legend_fontsize)

#     # ### 添加x轴标签
#     # ## 计算每个组的中心位置作为x轴刻度位置
#     # # group_centers = r + bar_width * (num_colleges / 2 - 0.5)
#     # # group_centers = np.arange(len(dataframes[0]))
#     # ## 添加x轴标签
#     # # ax.set_xticks(group_centers)
#     # # dataframes[0]['項目'].values
#     # # "array(['個人興趣', '未來能找到好工作', '落點分析', '沒有特定理由', '家人的期望與建議', '師長推薦'],dtype=object)"
#     # ax.set_xticks(r + bar_width * (len(dataframes) / 2))
#     # ax.set_xticklabels(dataframes[0]['項目'].values, fontsize=xticklabel_fontsize)
#     # # ax.set_xticklabels(['非常滿意', '滿意', '普通', '不滿意','非常不滿意'],fontsize=xticklabel_fontsize)

#     ### 设置y轴刻度标签
#     ax.set_yticks(r + bar_width*(len(dataframes) / 2))  # 调整位置以使标签居中对齐到每个条形
#     ax.set_yticklabels(dataframes[0]['項目'].values, fontsize=yticklabel_fontsize)


#     ### 设置标题和轴标签
#     ax.set_title(item_name,fontsize=title_fontsize)
#     # ax.set_xlabel('满意度',fontsize=xlabel_fontsize)
#     ax.set_xlabel('比例',fontsize=xlabel_fontsize)
#     ### 显示网格线
#     plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
#     plt.tight_layout()
#     # plt.show()
#     ### 在Streamlit中显示
#     st.pyplot(plt)

# st.markdown("##")  ## 更大的间隔 
