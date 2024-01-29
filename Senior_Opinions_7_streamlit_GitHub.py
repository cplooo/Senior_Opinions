# -*- coding: utf-8 -*-
"""
112年大四畢業生離校意見分析
"""
import pandas as pd
import os
#import matplotlib.pyplot as plt
#import matplotlib
#import seaborn as sns
import numpy as np
import re
import streamlit as st 
import streamlit.components.v1 as stc 


#######  读取Pickle文件
df_senior_original = pd.read_pickle('df_senior.pkl')
#df_senior_original.shape  ## (1942, 70)
#df_senior_original.head()
#print(df_senior_original)

# ####### 读取Excel文件
# df_senior_original = pd.read_excel('df_senior.xlsx')



####### 設定呈現標題 
html_temp = """
		<div style="background-color:#3872fb;padding:10px;border-radius:10px">
		<h1 style="color:white;text-align:center;"> 112年大四畢業生離校意見分析 </h1>
		</div>
		"""
stc.html(html_temp)


####### 選擇學系
department_choice = st.selectbox('選擇學系', df_senior_original['畢業院系'].unique())
#department_choice = '國企系'
df_senior = df_senior_original[df_senior_original['畢業院系']==department_choice]


####### 調整滿意度次序
###### 定义期望的滿意度顺序
desired_order = ['非常滿意', '滿意', '普通', '不滿意', '非常不滿意']

###### 函数：调整 DataFrame 以包含所有滿意度值，且顺序正确
def adjust_df(df, order):
    # 确保 DataFrame 包含所有滿意度值
    for pp in order:
        if pp not in df['滿意度'].values:
            # df = df.append({'滿意度': pp, '人數': 0, '比例': 0}, ignore_index=True)
            # 创建一个新的 DataFrame，用于添加新的row
            new_row = pd.DataFrame({'滿意度': pp, '人數': 0, '比例': 0})
            # 使用 concat() 合并原始 DataFrame 和新的 DataFrame
            df = pd.concat([df, new_row], ignore_index=True)

    # 根据期望的顺序重新排列 DataFrame
    df = df.set_index('滿意度').reindex(order).reset_index()
    return df




df_streamlit = []
####### Part1  
###### Part1-1 系師資素質與專長
#df_senior.iloc[:,9] ## 1. 系師資素質與專長
#df_senior.columns[9][3:]  ## '系師資素質與專長'
#type(df_senior.iloc[:,9])  ## pandas.core.series.Series
##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,9].value_counts()  
#type(value_counts) ## pandas.core.series.Series


##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()


value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()



##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
# result_df = pd.DataFrame({'人數': value_counts,'比例': proportions.round(4)})
# #### 將 index 變column
# result_df_r = result_df.reset_index()
# #### 將新的 column 重新命名
# result_df_rr = result_df_r.rename(columns={'index': '滿意度'})

#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
# for satisfaction in desired_order:
#     if satisfaction not in result_df_r['Satisfaction'].values:
#         result_df_r = result_df_r.append({'Satisfaction': satisfaction, '人數': 0, '比例': 0}, ignore_index=True)
# ## 根据期望的顺序重新排列 DataFrame
# result_df_rr = result_df_r.set_index('滿意度').reindex(desired_order).reset_index()

# df_streamlit.append(result_df_rr)  
df_streamlit.append(result_df_r)  
#### 使用Streamlit展示DataFrame
# st.write("系師資素質與專長:", result_df_rr)  ##显示索引
# st.write("<b>系師資素質與專長:</b>", result_df_rr.to_html(index=False), unsafe_allow_html=True)  ##不显示索引
# st.write("")  ## 一个空白行
# st.markdown("###")  ## 更大的间隔

###### Part1-2 系的教學品質
#df_senior.iloc[:,10] ## 2. 系的教學品質
#df_senior.columns[10][3:]  ## '系的教學品質'
##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,10].value_counts()


##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()


value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()




##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
# result_df = pd.DataFrame({'人數': value_counts,'比例': proportions.round(4)})
# #### 將 index 變column
# result_df_r = result_df.reset_index()
# #### 將新的 column 重新命名
# result_df_rr = result_df_r.rename(columns={'index': '滿意度'})

#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
# for satisfaction in desired_order:
#     if satisfaction not in result_df_r['Satisfaction'].values:
#         result_df_r = result_df_r.append({'Satisfaction': satisfaction, '人數': 0, '比例': 0}, ignore_index=True)
# ## 根据期望的顺序重新排列 DataFrame
# result_df_rr = result_df_r.set_index('Satisfaction').reindex(desired_order).reset_index()

df_streamlit.append(result_df_r)
# df_streamlit.append(result_df_rr)
#### 使用Streamlit展示DataFrame
# st.write("系師資素質與專長:", result_df_rr)  ## 显示索引
# st.write("<b>系的教學品質:</b>", result_df_rr.to_html(index=False), unsafe_allow_html=True)  ## 不显示索引
# st.write("")  ## 一个空白行

###### Part1-3 系上師生間的互動關係
# df_senior.iloc[:,11] ## 3. 系上師生間的互動關係
#df_senior.columns[11][3:]  ## '系上師生間的互動關係'
##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,11].value_counts()
## 更改 Series 的名称
value_counts.name = '滿意度'

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()


value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()


##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
# result_df = pd.DataFrame({'人數': value_counts,'比例': proportions.round(4)})
# #### 將 index 變column
# result_df_r = result_df.reset_index()
# #### 將新的 column 重新命名
# result_df_rr = result_df_r.rename(columns={'index': '滿意度'})

#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
# for satisfaction in desired_order:
#     if satisfaction not in result_df_r['Satisfaction'].values:
#         result_df_r = result_df_r.append({'Satisfaction': satisfaction, '人數': 0, '比例': 0}, ignore_index=True)
# ## 根据期望的顺序重新排列 DataFrame
# result_df_rr = result_df_r.set_index('Satisfaction').reindex(desired_order).reset_index()

df_streamlit.append(result_df_r)
# df_streamlit.append(result_df_rr)
#### 使用Streamlit展示DataFrame
# st.write("系師資素質與專長:", result_df_rr)  ## 显示索引
# st.write("<b>系上師生間的互動關係:</b>", result_df_rr.to_html(index=False), unsafe_allow_html=True)  ## 不显示索引
# st.write("")  ## 一个空白行


###### Part1-4 系課程內容
# df_senior.iloc[:,12] ## 4. 系課程內容
##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,12].value_counts()
## 更改 Series 的名称
value_counts.name = '滿意度'

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()


value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()


##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
# result_df = pd.DataFrame({'人數': value_counts,'比例': proportions.round(4)})
# #### 將 index 變column
# result_df_r = result_df.reset_index()
# #### 將新的 column 重新命名
# result_df_rr = result_df_r.rename(columns={'index': '滿意度'})

#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
# for satisfaction in desired_order:
#     if satisfaction not in result_df_r['Satisfaction'].values:
#         result_df_r = result_df_r.append({'Satisfaction': satisfaction, '人數': 0, '比例': 0}, ignore_index=True)
# ## 根据期望的顺序重新排列 DataFrame
# result_df_rr = result_df_r.set_index('Satisfaction').reindex(desired_order).reset_index()

df_streamlit.append(result_df_r)
# df_streamlit.append(result_df_rr)


###### Part1-5 系對學生思辨與探究能力的培養
# df_senior.iloc[:,13] ## 5. 系對學生思辨與探究能力的培養
##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,13].value_counts()
## 更改 Series 的名称
value_counts.name = '滿意度'

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()


value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()



##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
# result_df = pd.DataFrame({'人數': value_counts,'比例': proportions.round(4)})
# #### 將 index 變column
# result_df_r = result_df.reset_index()
# #### 將新的 column 重新命名
# result_df_rr = result_df_r.rename(columns={'index': '滿意度'})

#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
# for satisfaction in desired_order:
#     if satisfaction not in result_df_r['Satisfaction'].values:
#         result_df_r = result_df_r.append({'Satisfaction': satisfaction, '人數': 0, '比例': 0}, ignore_index=True)
# ## 根据期望的顺序重新排列 DataFrame
# result_df_rr = result_df_r.set_index('Satisfaction').reindex(desired_order).reset_index()

df_streamlit.append(result_df_r)
# df_streamlit.append(result_df_rr)



###### Part1-6 系對學生創新或創造力的培養
# df_senior.iloc[:,14] ## 6. 系對學生創新或創造力的培養
##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,14].value_counts()
## 更改 Series 的名称
value_counts.name = '滿意度'

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()


value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()



##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
# result_df = pd.DataFrame({'人數': value_counts,'比例': proportions.round(4)})
# #### 將 index 變column
# result_df_r = result_df.reset_index()
# #### 將新的 column 重新命名
# result_df_rr = result_df_r.rename(columns={'index': '滿意度'})

#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
# for satisfaction in desired_order:
#     if satisfaction not in result_df_r['Satisfaction'].values:
#         result_df_r = result_df_r.append({'Satisfaction': satisfaction, '人數': 0, '比例': 0}, ignore_index=True)
# ## 根据期望的顺序重新排列 DataFrame
# result_df_rr = result_df_r.set_index('Satisfaction').reindex(desired_order).reset_index()

df_streamlit.append(result_df_r)
# df_streamlit.append(result_df_rr)





# ###### Part1-7 系對學生在專業領域中具競爭力的培育
# df_senior.iloc[:,15] ## 7. 系對學生在專業領域中具競爭力的培育



# ###### Part1-8 系修課規定
# df_senior.iloc[:,16] ## 8.系修課規定



# ###### Part1-9 系的學習風氣
# df_senior.iloc[:,17] ## 9. 系的學習風氣





# ####### Part2  
# ###### Part2-1 系的空間環境與設備
# df_senior.iloc[:,19] ## 1. 系的空間環境與設備



# ###### Part2-2 系行政人員的服務品質
# df_senior.iloc[:,20] ## 2. 系行政人員的服務品質



# ###### Part2-3  系提供的工讀與獎助機會
# df_senior.iloc[:,21] ## 3. 系提供的工讀與獎助機會



# ###### Part2-4 系提供的相關學習活動
# df_senior.iloc[:,22] ## 4. 系提供的相關學習活動



# ###### Part2-5 系提供給學生的學習協助
# df_senior.iloc[:,23] ## 5.系提供給學生的學習協助



# ###### Part2-6 系對學生的生涯輔導
# df_senior.iloc[:,24] ## 6. 系對學生的生涯輔導



# ###### Part2-7 系對學生意見與需求的重視
# df_senior.iloc[:,25] ## 7. 系對學生意見與需求的重視



# ####### Part3  
# ###### Part3-1 目前就讀系的聲譽
# df_senior.iloc[:,27] ## 1. 目前就讀系的聲譽




# ###### Part3-2 系的進步程度
# df_senior.iloc[:,28] ## 2. 系的進步程度




# ###### Part3-3 系定位與特色
# df_senior.iloc[:,29] ## 3. 系定位與特色




# ###### Part3-4 整體而言，您對畢業系所在辦理教學上的評價如何？
# df_senior.iloc[:,30] ## 4. 整體而言，您對畢業系所在辦理教學上的評價如何？
# ##### 轉變資料型態為float:
# #### 定义一个函数来转换每一行为数值类型，非数值转为 NaN 
# def to_numeric_ignore_special_str(column):
#     return pd.to_numeric(column, errors='coerce')
# #### 将某行转换为数值类型float，忽略无法转换的值
# df_senior_SomeColumn_numeric = df_senior[df_senior.columns[30]].apply(to_numeric_ignore_special_str)  ## type(df_senior_Part3_4_numeric)  ## pandas.core.series.Series
# df_senior_理學_SomeColumn_numeric = df_senior_理學[df_senior_理學.columns[30]].apply(to_numeric_ignore_special_str)
# df_senior_資訊_SomeColumn_numeric = df_senior_資訊[df_senior_資訊.columns[30]].apply(to_numeric_ignore_special_str)
# df_senior_管理_SomeColumn_numeric = df_senior_管理[df_senior_管理.columns[30]].apply(to_numeric_ignore_special_str)
# df_senior_人社_SomeColumn_numeric = df_senior_人社[df_senior_人社.columns[30]].apply(to_numeric_ignore_special_str)
# df_senior_外語_SomeColumn_numeric = df_senior_外語[df_senior_外語.columns[30]].apply(to_numeric_ignore_special_str)
# df_senior_國際_SomeColumn_numeric = df_senior_國際[df_senior_國際.columns[30]].apply(to_numeric_ignore_special_str)
# ##### 畫盒鬚圖:
# #### 将这些 Series 合并为一个 DataFrame
# data = pd.DataFrame({'理學': df_senior_理學_SomeColumn_numeric, '資訊': df_senior_資訊_SomeColumn_numeric, '管理': df_senior_管理_SomeColumn_numeric,'人社': df_senior_人社_SomeColumn_numeric, '外語': df_senior_外語_SomeColumn_numeric, '國際': df_senior_國際_SomeColumn_numeric})
# #### 绘制盒须图
# ### 設置中文顯示
# ## 設置 matplotlib 支持中文的字體: 這裡使用的是 'SimHei' 字體，您也可以替換為任何支持中文的字體
# matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
# matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
# plt.figure(figsize=(10, 6))
# sns.boxplot(data=data)
# ### 标示平均值
# for i in range(data.shape[1]):
#     y = data.iloc[:, i].mean()
#     plt.text(i, y, f'{y:.2f}', ha='center', va='center',fontweight='bold', color='blue',fontsize = 14)
# plt.title('畢業系所教學評價盒鬚圖(範圍1-10, 數字為平均值)',fontsize = 17)
# plt.ylim(0, 11)
# plt.ylabel('分數',fontsize = 16)
# plt.xticks(fontsize=16)  #
# plt.show()



# ###### Part3-5 和國內其他類似系所相較，您覺得畢業的系所競爭力如何？
# df_senior.iloc[:,31] ## 5. 和國內其他類似系所相較，您覺得畢業的系所競爭力如何？
# ##### 轉變資料型態為float:
# #### 定义一个函数来转换每一行为数值类型，非数值转为 NaN 
# def to_numeric_ignore_special_str(column):
#     return pd.to_numeric(column, errors='coerce')
# #### 将某行转换为数值类型float，忽略无法转换的值
# df_senior_SomeColumn_numeric = df_senior[df_senior.columns[31]].apply(to_numeric_ignore_special_str)  ## type(df_senior_Part3_4_numeric)  ## pandas.core.series.Series
# df_senior_理學_SomeColumn_numeric = df_senior_理學[df_senior_理學.columns[31]].apply(to_numeric_ignore_special_str)
# df_senior_資訊_SomeColumn_numeric = df_senior_資訊[df_senior_資訊.columns[31]].apply(to_numeric_ignore_special_str)
# df_senior_管理_SomeColumn_numeric = df_senior_管理[df_senior_管理.columns[31]].apply(to_numeric_ignore_special_str)
# df_senior_人社_SomeColumn_numeric = df_senior_人社[df_senior_人社.columns[31]].apply(to_numeric_ignore_special_str)
# df_senior_外語_SomeColumn_numeric = df_senior_外語[df_senior_外語.columns[31]].apply(to_numeric_ignore_special_str)
# df_senior_國際_SomeColumn_numeric = df_senior_國際[df_senior_國際.columns[31]].apply(to_numeric_ignore_special_str)
# ##### 畫盒鬚圖:
# #### 将这些 Series 合并为一个 DataFrame
# data = pd.DataFrame({'理學': df_senior_理學_SomeColumn_numeric, '資訊': df_senior_資訊_SomeColumn_numeric, '管理': df_senior_管理_SomeColumn_numeric,'人社': df_senior_人社_SomeColumn_numeric, '外語': df_senior_外語_SomeColumn_numeric, '國際': df_senior_國際_SomeColumn_numeric})
# #### 绘制盒须图
# ### 設置中文顯示
# ## 設置 matplotlib 支持中文的字體: 這裡使用的是 'SimHei' 字體，您也可以替換為任何支持中文的字體
# matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
# matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
# plt.figure(figsize=(10, 6))
# sns.boxplot(data=data)
# ### 标示平均值
# for i in range(data.shape[1]):
#     y = data.iloc[:, i].mean()
#     plt.text(i, y, f'{y:.2f}', ha='center', va='center',fontweight='bold', color='blue',fontsize = 14)
# plt.title('畢業系所對比國內其他類似系所之競爭力盒鬚圖(範圍1-10, 數字為平均值)',fontsize = 17)
# plt.ylim(0, 11)
# plt.ylabel('分數',fontsize = 16)
# plt.xticks(fontsize=16)  #
# plt.show()


# ####### Part4  
# ###### Part4-1 協助學生瞭解就業市場現況與產業發展趨勢
# df_senior.iloc[:,33] ## 1. 協助學生瞭解就業市場現況與產業發展趨勢


# ###### Part4-2 協助學生生涯發展與規劃
# df_senior.iloc[:,34] ## 2. 協助學生生涯發展與規劃


# ###### Part4-3 生涯與就業輔導服務品質
# df_senior.iloc[:,35] ## 3. 生涯與就業輔導服務品質






# ####### Part5  課程規劃與教師教學滿意度(依多數課程情況回答)
# ###### Part5-1 提供國外修課、實習或交換學生機會
# df_senior.iloc[:,37] ## 1. 提供國外修課、實習或交換學生機會



# ###### Part5-2 提供與外籍人士或國際社群互動交流的機會
# df_senior.iloc[:,38] ## 2. 提供與外籍人士或國際社群互動交流的機會




# ###### Part5-3 外語學習機會與環境
# df_senior.iloc[:,39] ## 3.外語學習機會與環境




# ###### Part5-4 提供瞭解外國政治、經濟、社會、文化情況的機會
# df_senior.iloc[:,40] ## 4. 提供瞭解外國政治、經濟、社會、文化情況的機會




# ####### Part6  
# ###### Part6-1 校園環境規劃與維護
# df_senior.iloc[:,42] ## 1. 校園環境規劃與維護



# ###### Part6-2 校園內的安全保障
# df_senior.iloc[:,43] ## 2. 校園內的安全保障



# ###### Part6-3 您是否申請或參與過「職涯輔導」 學習輔導方案或輔導活動嗎?
# df_senior.iloc[:,44] ## 3. 學校各項收費



# ###### Part6-4 您是否申請或參與過「外語教學中心學習輔導」 學習輔導方案或輔導活動嗎?
# df_senior.iloc[:,45] ## 4. 電腦網路設備



# ###### Part6-5 您是否申請或參與過「諮商暨健康中心的諮商輔導」 學習輔導方案或輔導活動嗎?
# df_senior.iloc[:,46] ## 5. 運動休閒設施



# ###### Part6-6 學校生活機能便利性
# df_senior.iloc[:,47] ## 6. 學校生活機能便利性


# ###### Part6-7 學生宿舍數量
# df_senior.iloc[:,48] ## 7. 學生宿舍數量



# ####### Part7  
# ###### Part7-1 學校的聲譽
# df_senior.iloc[:,50] ## 1. 學校的聲譽



# ###### Part7-2 學校的進步程度
# df_senior.iloc[:,51] ## 2. 學校的進步程度



# ###### Part7-3 學校定位與特色
# df_senior.iloc[:,52] ## 3. 學校定位與特色



# ###### Part7-4 學校學風自由開放程度
# df_senior.iloc[:,53] ## 4. 學校學風自由開放程度




# ####### Part8  
# ###### Part8-1 如果可以重來，您是否仍會就讀同一主修領域、學群或學類？
# df_senior.iloc[:,55] ## 1. 如果可以重來，您是否仍會就讀同一主修領域、學群或學類？
# #df_senior_理.iloc[:,9]
# ##### 计算不同子字符串的出现次数
# value_counts = df_senior.iloc[:,55].value_counts()
# value_counts_理學 = df_senior_理學.iloc[:,55].value_counts()
# value_counts_資訊 = df_senior_資訊.iloc[:,55].value_counts()
# value_counts_管理 = df_senior_管理.iloc[:,55].value_counts()
# value_counts_人社 = df_senior_人社.iloc[:,55].value_counts()
# value_counts_外語 = df_senior_外語.iloc[:,55].value_counts()
# value_counts_國際 = df_senior_國際.iloc[:,55].value_counts()
# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()
# proportions_理學 = value_counts_理學 / value_counts_理學.sum()
# proportions_資訊 = value_counts_資訊 / value_counts_資訊.sum()
# proportions_管理 = value_counts_管理 / value_counts_管理.sum()
# proportions_人社 = value_counts_人社 / value_counts_人社.sum()
# proportions_外語 = value_counts_外語 / value_counts_外語.sum()
# proportions_國際 = value_counts_國際 / value_counts_國際.sum()


# #%% (三?) 以下
# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({'人數': value_counts,'比例': proportions.round(4)})
# result_df_理學 = pd.DataFrame({'人數': value_counts_理學,'比例': proportions_理學.round(4)})
# result_df_資訊 = pd.DataFrame({'人數': value_counts_資訊,'比例': proportions_資訊.round(4)})
# result_df_管理 = pd.DataFrame({'人數': value_counts_管理,'比例': proportions_管理.round(4)})
# result_df_人社 = pd.DataFrame({'人數': value_counts_人社,'比例': proportions_人社.round(4)})
# result_df_外語 = pd.DataFrame({'人數': value_counts_外語,'比例': proportions_外語.round(4)})
# result_df_國際 = pd.DataFrame({'人數': value_counts_國際,'比例': proportions_國際.round(4)})

# #### 將 index 變column
# result_df_r = result_df.reset_index()
# result_df_理學_r = result_df_理學.reset_index()
# result_df_資訊_r = result_df_資訊.reset_index()
# result_df_管理_r = result_df_管理.reset_index()
# result_df_人社_r = result_df_人社.reset_index()
# result_df_外語_r = result_df_外語.reset_index()
# result_df_國際_r = result_df_國際.reset_index()
# #### 將新的 column 重新命名
# result_df_r.rename(columns={'index': '意願度'}, inplace=True)
# result_df_理學_r.rename(columns={'index': '意願度'}, inplace=True)
# result_df_資訊_r.rename(columns={'index': '意願度'}, inplace=True)
# result_df_管理_r.rename(columns={'index': '意願度'}, inplace=True)
# result_df_人社_r.rename(columns={'index': '意願度'}, inplace=True)
# result_df_外語_r.rename(columns={'index': '意願度'}, inplace=True)
# result_df_國際_r.rename(columns={'index': '意願度'}, inplace=True)

# #### 調整滿意度次序
# ###定义期望的滿意度顺序
# desired_order = ['絕對會', '應該會', '應該不會', '絕對不會']
# ### 函数：调整 DataFrame 以包含所有滿意度值，且顺序正确
# def adjust_df(df, order):
#     # 确保 DataFrame 包含所有滿意度值
#     for satisfaction in order:
#         if satisfaction not in df['意願度'].values:
#             df = df.append({'意願度': satisfaction, '人數': 0, '比例': 0}, ignore_index=True)

#     # 根据期望的顺序重新排列 DataFrame
#     df = df.set_index('意願度').reindex(order).reset_index()
#     return df
# ### 调整两个 DataFrame
# result_df_rr = adjust_df(result_df_r, desired_order)
# result_df_理學_rr = adjust_df(result_df_理學_r, desired_order)
# result_df_資訊_rr = adjust_df(result_df_資訊_r, desired_order)
# result_df_管理_rr = adjust_df(result_df_管理_r, desired_order)
# result_df_人社_rr = adjust_df(result_df_人社_r, desired_order)
# result_df_外語_rr = adjust_df(result_df_外語_r, desired_order)
# result_df_國際_rr = adjust_df(result_df_國際_r, desired_order)


# #### 將各院 DataFrame合并为一个DataFrame
# dataframes = [result_df_理學_rr, result_df_資訊_rr, result_df_管理_rr, result_df_人社_rr, result_df_外語_rr, result_df_國際_rr]  # ... 添加所有学院的DataFrame
# combined_df = pd.concat(dataframes, keys=['理學', '資訊','管理', '人社','外語', '國際'])  # ... 添加所有学院的键
# #### 去掉 level 1 index
# combined_df_r = combined_df.reset_index(level=1, drop=True)
# #### 列印結果
# print("就讀同一主修領域、學群或學類 意願度")
# #print(combined_df_r)
# print(combined_df_r.iloc[0:4,:])
# print('---------------------------------')
# print(combined_df_r.iloc[4:8,:])
# print('---------------------------------')
# print(combined_df_r.iloc[8:12,:])
# print('---------------------------------')
# print(combined_df_r.iloc[12:16,:])
# print('---------------------------------')
# print(combined_df_r.iloc[16:20,:])
# print('---------------------------------')
# print(combined_df_r.iloc[20:24,:])
# print('---------------------------------')
# '''
# 就讀同一主修領域、學群或學類 意願度
#      意願度   人數      比例
# 理學   絕對會   56  0.1642
# 理學   應該會  212  0.6217
# 理學  應該不會   56  0.1642
# 理學  絕對不會   17  0.0499
# ---------------------------------
#      意願度   人數      比例
# 資訊   絕對會   51  0.2125
# 資訊   應該會  148  0.6167
# 資訊  應該不會   33  0.1375
# 資訊  絕對不會    8  0.0333
# ---------------------------------
#      意願度   人數      比例
# 管理   絕對會  104  0.1600
# 管理   應該會  358  0.5508
# 管理  應該不會  148  0.2277
# 管理  絕對不會   40  0.0615
# ---------------------------------
#      意願度   人數      比例
# 人社   絕對會  110  0.2576
# 人社   應該會  238  0.5574
# 人社  應該不會   67  0.1569
# 人社  絕對不會   12  0.0281
# ---------------------------------
#      意願度   人數      比例
# 外語   絕對會   40  0.1695
# 外語   應該會  132  0.5593
# 外語  應該不會   54  0.2288
# 外語  絕對不會   10  0.0424
# ---------------------------------
#      意願度  人數      比例
# 國際   絕對會  11  0.2292
# 國際   應該會  31  0.6458
# 國際  應該不會   6  0.1250
# 國際  絕對不會   0  0.0000
# ---------------------------------
# '''
# #%% (三?) 以上

# #%% (三圖?) 以下
# ##### 圖：系的教學品質 滿意度
# #### 設置中文顯示
# ### 設置 matplotlib 支持中文的字體: 這裡使用的是 'SimHei' 字體，您也可以替換為任何支持中文的字體
# matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
# matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
# #### 设置条形的宽度
# bar_width = 0.1
# #### 设置x轴的位置
# r = np.arange(len(result_df_理學_rr))
# #### 设置字体大小
# title_fontsize = 18
# xlabel_fontsize = 16
# ylabel_fontsize = 16
# xticklabel_fontsize = 16
# annotation_fontsize = 8
# legend_fontsize = 14
# #### 绘制条形
# fig, ax = plt.subplots(figsize=(10, 6))
# for i, (college_name, df) in enumerate(combined_df.groupby(level=0)):
#     index = r + i * bar_width
#     rects = ax.bar(index, df['比例'], width=bar_width, label=college_name)

#     # # 在每个条形上标示比例
#     # for rect, ratio in zip(rects, df['比例']):
#     #     ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height(), f'{ratio:.2%}', ha='center', va='bottom',fontsize=annotation_fontsize)
# ### 添加图例
# ax.legend(fontsize=legend_fontsize)
# ### 添加x轴标签
# ax.set_xticks(r + bar_width * (len(dataframes) / 2))
# ax.set_xticklabels(['絕對會', '應該會', '應該不會', '絕對不會'],fontsize=xticklabel_fontsize)
# ### 设置标题和轴标签
# ax.set_title('就讀同一主修領域、學群或學類 意願度',fontsize=title_fontsize)
# ax.set_xlabel('意願度',fontsize=xlabel_fontsize)
# ax.set_ylabel('比例',fontsize=ylabel_fontsize)
# ### 显示网格线
# plt.grid(True, linestyle='--', linewidth=0.5, color='gray')
# plt.tight_layout()
# plt.show()

# #%% (三圖?) 以上






# ###### Part8-2 如果可以重來，您是否仍會就讀本校的同一系？
# df_senior.iloc[:,56] ## 2. 如果可以重來，您是否仍會就讀本校的同一系？



# ###### Part8-3 如果可以重來，您是否仍會就讀本校？
# df_senior.iloc[:,57] ## 3. 如果可以重來，您是否仍會就讀本校？



# ###### Part8-4 整體而言，您對畢業母校在辦理教學上的評價如何？
# df_senior.iloc[:,58] ## 4. 整體而言，您對畢業母校在辦理教學上的評價如何？
# ##### 轉變資料型態為float:
# #### 定义一个函数来转换每一行为数值类型，非数值转为 NaN 
# def to_numeric_ignore_special_str(column):
#     return pd.to_numeric(column, errors='coerce')
# #### 将某行转换为数值类型float，忽略无法转换的值
# df_senior_SomeColumn_numeric = df_senior[df_senior.columns[58]].apply(to_numeric_ignore_special_str)  ## type(df_senior_Part3_4_numeric)  ## pandas.core.series.Series
# df_senior_理學_SomeColumn_numeric = df_senior_理學[df_senior_理學.columns[58]].apply(to_numeric_ignore_special_str)
# df_senior_資訊_SomeColumn_numeric = df_senior_資訊[df_senior_資訊.columns[58]].apply(to_numeric_ignore_special_str)
# df_senior_管理_SomeColumn_numeric = df_senior_管理[df_senior_管理.columns[58]].apply(to_numeric_ignore_special_str)
# df_senior_人社_SomeColumn_numeric = df_senior_人社[df_senior_人社.columns[58]].apply(to_numeric_ignore_special_str)
# df_senior_外語_SomeColumn_numeric = df_senior_外語[df_senior_外語.columns[58]].apply(to_numeric_ignore_special_str)
# df_senior_國際_SomeColumn_numeric = df_senior_國際[df_senior_國際.columns[58]].apply(to_numeric_ignore_special_str)
# ##### 畫盒鬚圖:
# #### 将这些 Series 合并为一个 DataFrame
# data = pd.DataFrame({'理學': df_senior_理學_SomeColumn_numeric, '資訊': df_senior_資訊_SomeColumn_numeric, '管理': df_senior_管理_SomeColumn_numeric,'人社': df_senior_人社_SomeColumn_numeric, '外語': df_senior_外語_SomeColumn_numeric, '國際': df_senior_國際_SomeColumn_numeric})
# #### 绘制盒须图
# ### 設置中文顯示
# ## 設置 matplotlib 支持中文的字體: 這裡使用的是 'SimHei' 字體，您也可以替換為任何支持中文的字體
# matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
# matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
# plt.figure(figsize=(10, 6))
# sns.boxplot(data=data)
# ### 标示平均值
# for i in range(data.shape[1]):
#     y = data.iloc[:, i].mean()
#     plt.text(i, y, f'{y:.2f}', ha='center', va='center',fontweight='bold', color='blue',fontsize = 14)
# plt.title('畢業母校在辦理教學上的評價盒鬚圖(範圍1-10, 數字為平均值)',fontsize = 17)
# plt.ylim(0, 11)
# plt.ylabel('分數',fontsize = 16)
# plt.xticks(fontsize=16)  #
# plt.show()


# ###### Part8-5 和國內其他大學相較，您覺得畢業母校競爭力如何？
# df_senior.iloc[:,59] ## 5. 和國內其他大學相較，您覺得畢業母校競爭力如何？
# ##### 轉變資料型態為float:
# #### 定义一个函数来转换每一行为数值类型，非数值转为 NaN 
# def to_numeric_ignore_special_str(column):
#     return pd.to_numeric(column, errors='coerce')
# #### 将某行转换为数值类型float，忽略无法转换的值
# df_senior_SomeColumn_numeric = df_senior[df_senior.columns[59]].apply(to_numeric_ignore_special_str)  ## type(df_senior_Part3_4_numeric)  ## pandas.core.series.Series
# df_senior_理學_SomeColumn_numeric = df_senior_理學[df_senior_理學.columns[59]].apply(to_numeric_ignore_special_str)
# df_senior_資訊_SomeColumn_numeric = df_senior_資訊[df_senior_資訊.columns[59]].apply(to_numeric_ignore_special_str)
# df_senior_管理_SomeColumn_numeric = df_senior_管理[df_senior_管理.columns[59]].apply(to_numeric_ignore_special_str)
# df_senior_人社_SomeColumn_numeric = df_senior_人社[df_senior_人社.columns[59]].apply(to_numeric_ignore_special_str)
# df_senior_外語_SomeColumn_numeric = df_senior_外語[df_senior_外語.columns[59]].apply(to_numeric_ignore_special_str)
# df_senior_國際_SomeColumn_numeric = df_senior_國際[df_senior_國際.columns[59]].apply(to_numeric_ignore_special_str)
# ##### 畫盒鬚圖:
# #### 将这些 Series 合并为一个 DataFrame
# data = pd.DataFrame({'理學': df_senior_理學_SomeColumn_numeric, '資訊': df_senior_資訊_SomeColumn_numeric, '管理': df_senior_管理_SomeColumn_numeric,'人社': df_senior_人社_SomeColumn_numeric, '外語': df_senior_外語_SomeColumn_numeric, '國際': df_senior_國際_SomeColumn_numeric})
# #### 绘制盒须图
# ### 設置中文顯示
# ## 設置 matplotlib 支持中文的字體: 這裡使用的是 'SimHei' 字體，您也可以替換為任何支持中文的字體
# matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
# matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
# plt.figure(figsize=(10, 6))
# sns.boxplot(data=data)
# ### 标示平均值
# for i in range(data.shape[1]):
#     y = data.iloc[:, i].mean()
#     plt.text(i, y, f'{y:.2f}', ha='center', va='center',fontweight='bold', color='blue',fontsize = 14)
# plt.title('畢業母校相較國內其他大學之競爭力盒鬚圖(範圍1-10, 數字為平均值)',fontsize = 17)
# plt.ylim(0, 11)
# plt.ylabel('分數',fontsize = 16)
# plt.xticks(fontsize=16)  #
# plt.show()


# ###### Part8-6 您對於系所有何建議？
# df_senior.iloc[:,60] ## 6. 您對於系所有何建議？



# ###### Part8-7 您對於學校有何建議？
# df_senior.iloc[:,61] ## 7. 您對於學校有何建議？




# ####### Part9  
# ###### Part9-1 您目前是否已有工作
# df_senior.iloc[:,63] ## 1. 您目前是否已有工作



# ###### Part9-2 您畢業3個月內最主要之規劃?
# df_senior.iloc[:,64] ## 2. 您畢業3個月內最主要之規劃?



# ###### Part9-3 您目前是否已寫好履歷自傳?
# df_senior.iloc[:,65] ## 3. 您目前是否已寫好履歷自傳?



# ###### Part9-4 您是否已經寄出履歷自傳，並開始求職了?
# df_senior.iloc[:,66] ## 4. 您是否已經寄出履歷自傳，並開始求職了?



# ###### Part9-5 是，何時投遞?,
# df_senior.iloc[:,67] ## 5. 是，何時投遞?,



# ###### Part9-6 否， 預計何時?
# df_senior.iloc[:,68] ## 6. 否， 預計何時?




####### Streamlit 呈現
# 每行显示3个DataFrame
for i in range(0, 4, 3):
    ## 使用Streamlit的列布局
    col1, col2, col3 = st.columns(3)
    
    with col1:
        #st.write("<b>系師資素質與專長:</b>", result_df_rr.to_html(index=False), unsafe_allow_html=True)  ##不显示索引
        ## 创建带有HTML标签的字符串
        column_title = df_senior.columns[i+0+9][3:]
        html_content = f"<div style='text-align: center;'><b style='font-size: 15px;'>{column_title}</b></div>{df_streamlit[i+0].to_html(index=False)}"
        ## 自定义样式，包括表格宽度、字体大小和列名居中
        html_content = html_content.replace('<table border="1" class="dataframe">', 
                                            '<table style="width:105%; font-size: 12px; margin-left: auto; margin-right: auto;" align="center">')
        html_content = html_content.replace('<th>', '<th style="text-align: center;">')
        ## 使用 st.markdown 显示内容
        st.markdown(html_content, unsafe_allow_html=True)
    with col2:
        #st.write("<b>系的教學品質:</b>", result_df_rr.to_html(index=False), unsafe_allow_html=True)  ## 不显示索引
        ## 创建带有HTML标签的字符串
        column_title = df_senior.columns[i+1+9][3:]
        html_content = f"<div style='text-align: center;'><b style='font-size: 15px;'>{column_title}</b></div>{df_streamlit[i+1].to_html(index=False)}"
        ## 自定义样式，包括表格宽度、字体大小和列名居中
        html_content = html_content.replace('<table border="1" class="dataframe">', 
                                            '<table style="width:105%; font-size: 12px; margin-left: auto; margin-right: auto;" align="center">')
        html_content = html_content.replace('<th>', '<th style="text-align: center;">')
        ## 使用 st.markdown 显示内容
        st.markdown(html_content, unsafe_allow_html=True)
    with col3:
        #st.write("<b>系上師生間的互動關係:</b>", result_df_rr.to_html(index=False), unsafe_allow_html=True)  ## 不显示索引
        ## 创建带有HTML标签的字符串
        column_title = df_senior.columns[i+2+9][3:]
        html_content = f"<div style='text-align: center;'><b style='font-size: 15px;'>{column_title}</b></div>{df_streamlit[i+2].to_html(index=False)}"
        ## 自定义样式，包括表格宽度、字体大小和列名居中
        html_content = html_content.replace('<table border="1" class="dataframe">', 
                                            '<table style="width:105%; font-size: 12px; margin-left: auto; margin-right: auto;" align="center">')
        html_content = html_content.replace('<th>', '<th style="text-align: center;">')
        ## 使用 st.markdown 显示内容
        st.markdown(html_content, unsafe_allow_html=True)
        st.markdown("###")  ## 更大的间隔




