# data_selection.py
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from streamlit_datetime_range_picker import datetime_range_picker

def display_logs_selection():
    st.title("数据选择")
    
    if 'df' not in st.session_state:
        st.warning("请先导入数据")
        return
    
    df = st.session_state.df
    
    # 确保 'datetime' 列存在
    if 'datetime' not in df.columns:
        st.error("'datetime' 列未找到，请检查数据导入步骤。")
        return
    
    # 确保 'datetime' 列是 datetime64 类型
    df['datetime'] = pd.to_datetime(df['datetime'])
    
    # 获取数据的最小和最大日期
    min_datetime = df['datetime'].min().to_pydatetime()
    max_datetime = df['datetime'].max().to_pydatetime()
    
    # 让用户选择日期范围
    start_date = st.date_input("开始日期", value=min_datetime.date())
    end_date = st.date_input("结束日期", value=max_datetime.date())
    
    # 确保结束日期不早于开始日期
    if end_date < start_date:
        st.error("结束日期不能早于开始日期")
        return
    
    # 过滤数据
    filtered_df = df[(df['datetime'] >= datetime.combine(start_date, datetime.min.time())) &
                     (df['datetime'] <= datetime.combine(end_date, datetime.max.time()))]
    
    st.write(f"筛选后的数据：{filtered_df.shape[0]} 行")
    st.dataframe(filtered_df)

    # 可选: 处理 apg_extension 列的可视化或其他操作
    if 'apg_extension' in filtered_df.columns:
        # 将 apg_extension 列处理为合适的格式
        # 假设 apg_extension 是一个嵌套列表
        st.write("apg_extension 列的部分数据：")
        st.write(filtered_df['apg_extension'].head())


# def display_logs_selection():
#     st.title("数据选择")
    
#     if 'df' not in st.session_state:
#         st.warning("请先导入数据")
#         return
    
#     df = st.session_state.df
    
#     # 确保 'datetime' 列存在
#     if 'datetime' not in df.columns:
#         st.error("'datetime' 列未找到，请检查数据导入步骤。")
#         return
    
#     # 确保 'datetime' 列是 datetime64 类型
#     df['datetime'] = pd.to_datetime(df['datetime'])
    
#     # 转换 datetime 为时间戳
#     min_timestamp = df['datetime'].min().timestamp()
#     max_timestamp = df['datetime'].max().timestamp()
    
#     selected_date_range = st.slider(
#         "选择时间段", 
#         min_value=min_timestamp, 
#         max_value=max_timestamp, 
#         value=(min_timestamp, max_timestamp),
#         format="YYYY-MM-DD HH:MM:SS"
#     )

    
#     # 将选择的时间戳范围转换回 datetime
#     selected_date_range = (pd.to_datetime(selected_date_range[0], unit='s'), 
#                            pd.to_datetime(selected_date_range[1], unit='s'))
    
#     filtered_df = df[(df['datetime'] >= selected_date_range[0]) & (df['datetime'] <= selected_date_range[1])]
    
#     st.write(f"筛选后的数据：{filtered_df.shape[0]} 行")
#     st.dataframe(filtered_df)