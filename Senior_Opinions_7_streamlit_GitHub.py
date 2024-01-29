# -*- coding: utf-8 -*-
"""
112年大四畢業生離校意見分析
"""
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib
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


####### Part1  
###### Part1-1 系師資素質與專長
#df_senior.iloc[:,9] ## 1. 系師資素質與專長

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,9].value_counts()   
# type(value_counts)  ## pandas.core.series.Series
# type(value_counts.index) ## pandas.core.indexes.base.Index

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()
# type(proportions)  ## pandas.core.series.Series
# type(proportions.index) ## pandas.core.indexes.base.Index

value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
# result_df = pd.DataFrame({'人數': value_counts,'比例': proportions.round(4)})
# type(result_df)  ## pandas.core.frame.DataFrame
# result_df.index  ## Index(['滿意', '非常滿意', '普通'], dtype='object')
# result_df.columns  ## Index(['人數', '比例'], dtype='object')



# #### 將 index 變column
# result_df_r = result_df.reset_index()



# #### 將新的 column 重新命名
# result_df_r.rename(columns={'index': '滿意度'}, inplace=True)

# result_df_rr =  pd.DataFrame(result_df_r.values, columns=result_df_r.columns, index=result_df_r.index)

st.write("系師資素質與專長:", result_df.to_html(index=False), unsafe_allow_html=True)





###### Part1-2 系的教學品質
# df_senior.iloc[:,10] ## 2. 系的教學品質
#df_senior_理.iloc[:,9]
##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,10].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()


##### 创建一个新的DataFrame来显示结果
#result_df = pd.DataFrame({'人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
# result_df = pd.DataFrame({'人數': value_counts,'比例': proportions.round(4)})

# #### 將 index 變column
# result_df_r = result_df.reset_index()

# #### 將新的 column 重新命名
# result_df_r.rename(columns={'index': '滿意度'}, inplace=True)

# result_df_rr =  pd.DataFrame(result_df_r.values, columns=result_df_r.columns, index=result_df_r.index)

# #### 使用Streamlit展示DataFrame
# st.write("系師資素質與專長:", result_df_rr)
#### 使用Streamlit展示DataFrame，但不显示索引
# st.write("系的教學品質:", result_df_rr.to_html(index=False), unsafe_allow_html=True)
st.write("系的教學品質:", result_df.to_html(index=False), unsafe_allow_html=True)










