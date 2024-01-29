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
            new_row = pd.DataFrame({'滿意度': [pp], '人數': [0], '比例': [0]})
            # 使用 concat() 合并原始 DataFrame 和新的 DataFrame
            df = pd.concat([df, new_row], ignore_index=True)

    # 根据期望的顺序重新排列 DataFrame
    df = df.set_index('滿意度').reindex(order).reset_index()
    return df


####### 調整意願度次序
###### 定义期望的意願度顺序
desired_order_2 = ['絕對會', '應該會', '應該不會', '絕對不會']
### 函数：调整 DataFrame 以包含所有滿意度值，且顺序正确
def adjust_df_2(df, order):
    # 确保 DataFrame 包含所有滿意度值
    for qq in order:
        if qq not in df['意願度'].values:
            # df = df.append({'意願度': satisfaction, '人數': 0, '比例': 0}, ignore_index=True)
            # 创建一个新的 DataFrame，用于添加新的row
            new_row = pd.DataFrame({'意願度': [qq], '人數': [0], '比例': [0]})
            # 使用 concat() 合并原始 DataFrame 和新的 DataFrame
            df = pd.concat([df, new_row], ignore_index=True)


    # 根据期望的顺序重新排列 DataFrame
    df = df.set_index('意願度').reindex(order).reset_index()
    return df




df_streamlit = []
column_title = []
####### Part1  
###### Part1-1 系師資素質與專長
#df_senior.iloc[:,9] ## 1. 系師資素質與專長
#df_senior.columns[9][3:]  ## '系師資素質與專長'
column_title.append(df_senior.columns[9][3:])
#type(df_senior.iloc[:,9])  ## pandas.core.series.Series

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,9].value_counts()  
#type(value_counts) ## pandas.core.series.Series

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)  



###### Part1-2 系的教學品質
#df_senior.iloc[:,10] ## 2. 系的教學品質
#df_senior.columns[10][3:]  ## '系的教學品質'
column_title.append(df_senior.columns[10][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,10].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)



###### Part1-3 系上師生間的互動關係
# df_senior.iloc[:,11] ## 3. 系上師生間的互動關係
#df_senior.columns[11][3:]  ## '系上師生間的互動關係'
column_title.append(df_senior.columns[11][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,11].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)




###### Part1-4 系課程內容
# df_senior.iloc[:,12] ## 4. 系課程內容
column_title.append(df_senior.columns[12][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,12].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)




###### Part1-5 系對學生思辨與探究能力的培養
# df_senior.iloc[:,13] ## 5. 系對學生思辨與探究能力的培養
column_title.append(df_senior.columns[13][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,13].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)




###### Part1-6 系對學生創新或創造力的培養
# df_senior.iloc[:,14] ## 6. 系對學生創新或創造力的培養
column_title.append(df_senior.columns[14][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,14].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)




###### Part1-7 系對學生在專業領域中具競爭力的培育
# df_senior.iloc[:,15] ## 7. 系對學生在專業領域中具競爭力的培育
column_title.append(df_senior.columns[15][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,15].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)





###### Part1-8 系修課規定
# df_senior.iloc[:,16] ## 8.系修課規定
column_title.append(df_senior.columns[16][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,16].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)





###### Part1-9 系的學習風氣
# df_senior.iloc[:,17] ## 9. 系的學習風氣
column_title.append(df_senior.columns[17][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,17].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)




####### Part2  
###### Part2-1 系的空間環境與設備
# df_senior.iloc[:,19] ## 1. 系的空間環境與設備
column_title.append(df_senior.columns[19][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,19].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)




###### Part2-2 系行政人員的服務品質
# df_senior.iloc[:,20] ## 2. 系行政人員的服務品質
column_title.append(df_senior.columns[20][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,20].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)




###### Part2-3  系提供的工讀與獎助機會
# df_senior.iloc[:,21] ## 3. 系提供的工讀與獎助機會
column_title.append(df_senior.columns[21][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,21].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)




###### Part2-4 系提供的相關學習活動
# df_senior.iloc[:,22] ## 4. 系提供的相關學習活動
column_title.append(df_senior.columns[22][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,22].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)



###### Part2-5 系提供給學生的學習協助
# df_senior.iloc[:,23] ## 5.系提供給學生的學習協助
column_title.append(df_senior.columns[23][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,23].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)



###### Part2-6 系對學生的生涯輔導
# df_senior.iloc[:,24] ## 6. 系對學生的生涯輔導
column_title.append(df_senior.columns[24][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,24].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)



###### Part2-7 系對學生意見與需求的重視
# df_senior.iloc[:,25] ## 7. 系對學生意見與需求的重視
column_title.append(df_senior.columns[25][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,25].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)



####### Part3  
###### Part3-1 目前就讀系的聲譽
# df_senior.iloc[:,27] ## 1. 目前就讀系的聲譽
column_title.append(df_senior.columns[27][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,27].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)




###### Part3-2 系的進步程度
# df_senior.iloc[:,28] ## 2. 系的進步程度
column_title.append(df_senior.columns[28][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,28].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)




###### Part3-3 系定位與特色
# df_senior.iloc[:,29] ## 3. 系定位與特色
column_title.append(df_senior.columns[29][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,29].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)




###### Part3-4 整體而言，您對畢業系所在辦理教學上的評價如何？
# df_senior.iloc[:,30] ## 4. 整體而言，您對畢業系所在辦理教學上的評價如何？





###### Part3-5 和國內其他類似系所相較，您覺得畢業的系所競爭力如何？
# df_senior.iloc[:,31] ## 5. 和國內其他類似系所相較，您覺得畢業的系所競爭力如何？







####### Part4  
###### Part4-1 協助學生瞭解就業市場現況與產業發展趨勢
# df_senior.iloc[:,33] ## 1. 協助學生瞭解就業市場現況與產業發展趨勢
column_title.append(df_senior.columns[33][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,33].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)




###### Part4-2 協助學生生涯發展與規劃
# df_senior.iloc[:,34] ## 2. 協助學生生涯發展與規劃
column_title.append(df_senior.columns[34][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,34].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)





###### Part4-3 生涯與就業輔導服務品質
# df_senior.iloc[:,35] ## 3. 生涯與就業輔導服務品質
# df_senior.columns[35]
column_title.append(df_senior.columns[35][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,35].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)






####### Part5  課程規劃與教師教學滿意度(依多數課程情況回答)
###### Part5-1 提供國外修課、實習或交換學生機會
# df_senior.iloc[:,37] ## 1. 提供國外修課、實習或交換學生機會
column_title.append(df_senior.columns[37][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,37].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)



###### Part5-2 提供與外籍人士或國際社群互動交流的機會
# df_senior.iloc[:,38] ## 2. 提供與外籍人士或國際社群互動交流的機會
column_title.append(df_senior.columns[38][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,38].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)




###### Part5-3 外語學習機會與環境
# df_senior.iloc[:,39] ## 3.外語學習機會與環境
column_title.append(df_senior.columns[39][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,39].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)




###### Part5-4 提供瞭解外國政治、經濟、社會、文化情況的機會
# df_senior.iloc[:,40] ## 4. 提供瞭解外國政治、經濟、社會、文化情況的機會
column_title.append(df_senior.columns[40][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,40].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)




####### Part6  
###### Part6-1 校園環境規劃與維護
# df_senior.iloc[:,42] ## 1. 校園環境規劃與維護
column_title.append(df_senior.columns[42][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,42].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)



###### Part6-2 校園內的安全保障
# df_senior.iloc[:,43] ## 2. 校園內的安全保障
column_title.append(df_senior.columns[43][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,43].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)



###### Part6-3 學校各項收費
# df_senior.iloc[:,44] ## 3. 學校各項收費
column_title.append(df_senior.columns[44][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,44].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)



###### Part6-4 電腦網路設備
# df_senior.iloc[:,45] ## 4. 電腦網路設備
column_title.append(df_senior.columns[45][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,45].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)



###### Part6-5 運動休閒設施
# df_senior.iloc[:,46] ## 5. 運動休閒設施
column_title.append(df_senior.columns[46][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,46].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)



###### Part6-6 學校生活機能便利性
# df_senior.iloc[:,47] ## 6. 學校生活機能便利性
column_title.append(df_senior.columns[47][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,47].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)


###### Part6-7 學生宿舍數量
# df_senior.iloc[:,48] ## 7. 學生宿舍數量
column_title.append(df_senior.columns[48][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,48].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)



####### Part7  
###### Part7-1 學校的聲譽
# df_senior.iloc[:,50] ## 1. 學校的聲譽
column_title.append(df_senior.columns[50][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,50].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)



###### Part7-2 學校的進步程度
# df_senior.iloc[:,51] ## 2. 學校的進步程度
column_title.append(df_senior.columns[51][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,51].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)



###### Part7-3 學校定位與特色
# df_senior.iloc[:,52] ## 3. 學校定位與特色
column_title.append(df_senior.columns[52][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,52].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)



###### Part7-4 學校學風自由開放程度
# df_senior.iloc[:,53] ## 4. 學校學風自由開放程度
column_title.append(df_senior.columns[53][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,53].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
satisfaction_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df(result_df, desired_order)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)




####### Part8  
###### Part8-1 如果可以重來，您是否仍會就讀同一主修領域、學群或學類？
# df_senior.iloc[:,55] ## 1. 如果可以重來，您是否仍會就讀同一主修領域、學群或學類？
column_title.append(df_senior.columns[55][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,55].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
willing_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'意願度':willing_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df_2(result_df, desired_order_2)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)






###### Part8-2 如果可以重來，您是否仍會就讀本校的同一系？
# df_senior.iloc[:,56] ## 2. 如果可以重來，您是否仍會就讀本校的同一系？
column_title.append(df_senior.columns[56][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,56].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
willing_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'意願度':willing_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df_2(result_df, desired_order_2)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)



###### Part8-3 如果可以重來，您是否仍會就讀本校？
# df_senior.iloc[:,57] ## 3. 如果可以重來，您是否仍會就讀本校？
column_title.append(df_senior.columns[57][3:])

##### 计算不同子字符串的出现次数
value_counts = df_senior.iloc[:,57].value_counts()

##### 计算不同子字符串的比例
proportions = value_counts / value_counts.sum()

##### 轉換成 numpy array
value_counts_numpy = value_counts.values
proportions_numpy = proportions.values
willing_numpy = proportions.index.to_numpy()

##### 创建一个新的DataFrame来显示结果
result_df = pd.DataFrame({'意願度':willing_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
#### 調整滿意度次序
result_df_r = adjust_df_2(result_df, desired_order_2)
#### 存到 list 'df_streamlit'
df_streamlit.append(result_df_r)




###### Part8-4 整體而言，您對畢業母校在辦理教學上的評價如何？
# df_senior.iloc[:,58] ## 4. 整體而言，您對畢業母校在辦理教學上的評價如何？



###### Part8-5 和國內其他大學相較，您覺得畢業母校競爭力如何？
# df_senior.iloc[:,59] ## 5. 和國內其他大學相較，您覺得畢業母校競爭力如何？






# ###### Part8-6 您對於系所有何建議？
# # df_senior.iloc[:,60] ## 6. 您對於系所有何建議？

# ##### 计算不同子字符串的出现次数
# value_counts = df_senior.iloc[:,60].value_counts()

# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# ##### 轉換成 numpy array
# value_counts_numpy = value_counts.values
# proportions_numpy = proportions.values
# satisfaction_numpy = proportions.index.to_numpy()

# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
# #### 調整滿意度次序
# result_df_r = adjust_df(result_df, desired_order)
# #### 存到 list 'df_streamlit'
# df_streamlit.append(result_df_r)



# ###### Part8-7 您對於學校有何建議？
# # df_senior.iloc[:,61] ## 7. 您對於學校有何建議？

# ##### 计算不同子字符串的出现次数
# value_counts = df_senior.iloc[:,61].value_counts()

# ##### 计算不同子字符串的比例
# proportions = value_counts / value_counts.sum()

# ##### 轉換成 numpy array
# value_counts_numpy = value_counts.values
# proportions_numpy = proportions.values
# satisfaction_numpy = proportions.index.to_numpy()

# ##### 创建一个新的DataFrame来显示结果
# result_df = pd.DataFrame({'滿意度':satisfaction_numpy, '人數': value_counts_numpy,'比例': proportions_numpy.round(4)})
# #### 調整滿意度次序
# result_df_r = adjust_df(result_df, desired_order)
# #### 存到 list 'df_streamlit'
# df_streamlit.append(result_df_r)






###### Part9  
##### Part9-1 您目前是否已有工作
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
for i in range(0, 39, 3):   ## end: 1, 4, 7, 10,13,16,19,22,25,28,31,34,37,40; start: 0,3,6,9,12,15,18,21,24,27,30,33,36
    
    ## 使用Streamlit的列布局
    col1, col2, col3 = st.columns(3)
    
    with col1:
        #st.write("<b>系師資素質與專長:</b>", result_df_rr.to_html(index=False), unsafe_allow_html=True)  ##不显示索引
        ## 创建带有HTML标签的字符串
        # column_title = df_senior.columns[i+0+9][3:]
        html_content = f"<div style='text-align: center;'><b style='font-size: 13px;'>{column_title[i+0]}</b></div>{df_streamlit[i+0].to_html(index=False)}"
        ## 自定义样式，包括表格宽度、字体大小和列名居中
        html_content = html_content.replace('<table border="1" class="dataframe">', 
                                            '<table style="width:105%; font-size: 12px; margin-left: auto; margin-right: auto;" align="center">')
        html_content = html_content.replace('<th>', '<th style="text-align: center;">')
        ## 使用 st.markdown 显示内容
        st.markdown(html_content, unsafe_allow_html=True)
    with col2:
        #st.write("<b>系的教學品質:</b>", result_df_rr.to_html(index=False), unsafe_allow_html=True)  ## 不显示索引
        ## 创建带有HTML标签的字符串
        # column_title = df_senior.columns[i+1+9][3:]
        html_content = f"<div style='text-align: center;'><b style='font-size: 13px;'>{column_title[i+1]}</b></div>{df_streamlit[i+1].to_html(index=False)}"
        ## 自定义样式，包括表格宽度、字体大小和列名居中
        html_content = html_content.replace('<table border="1" class="dataframe">', 
                                            '<table style="width:105%; font-size: 12px; margin-left: auto; margin-right: auto;" align="center">')
        html_content = html_content.replace('<th>', '<th style="text-align: center;">')
        ## 使用 st.markdown 显示内容
        st.markdown(html_content, unsafe_allow_html=True)
    with col3:
        #st.write("<b>系上師生間的互動關係:</b>", result_df_rr.to_html(index=False), unsafe_allow_html=True)  ## 不显示索引
        ## 创建带有HTML标签的字符串
        # column_title = df_senior.columns[i+2+9][3:]
        html_content = f"<div style='text-align: center;'><b style='font-size: 13px;'>{column_title[i+2]}</b></div>{df_streamlit[i+2].to_html(index=False)}"
        ## 自定义样式，包括表格宽度、字体大小和列名居中
        html_content = html_content.replace('<table border="1" class="dataframe">', 
                                            '<table style="width:105%; font-size: 12px; margin-left: auto; margin-right: auto;" align="center">')
        html_content = html_content.replace('<th>', '<th style="text-align: center;">')
        ## 使用 st.markdown 显示内容
        st.markdown(html_content, unsafe_allow_html=True)
        st.markdown("##")  ## 更大的间隔


html_content = f"<div style='text-align: center;'><b style='font-size: 13px;'>{column_title[39+0]}</b></div>{df_streamlit[39+0].to_html(index=False)}"
## 自定义样式，包括表格宽度、字体大小和列名居中
html_content = html_content.replace('<table border="1" class="dataframe">', 
                                    '<table style="width:105%; font-size: 12px; margin-left: auto; margin-right: auto;" align="center">')
html_content = html_content.replace('<th>', '<th style="text-align: center;">')
## 使用 st.markdown 显示内容
st.markdown(html_content, unsafe_allow_html=True)


