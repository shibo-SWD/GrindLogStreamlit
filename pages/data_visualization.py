import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def display_visualizations():
    st.title("数据可视化")

    if 'df' not in st.session_state:
        st.warning("请先导入和选择数据")
        return
    
    df = st.session_state.df
    
    # 显示打磨完成情况的饼图
    if 'grinding_completed' in df.columns:
        completion_counts = df['grinding_completed'].value_counts()
        
        # 根据 completion_counts 的索引动态生成 labels
        labels = ['未完成', '完成'][:len(completion_counts)]
        
        fig, ax = plt.subplots()
        ax.pie(completion_counts, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

    # 选择日期、时间筛选进行显示
    if 'datetime' in df.columns:
        min_date = df['datetime'].min()
        max_date = df['datetime'].max()
        selected_date_range = st.slider("选择时间段", 
                                        min_value=min_date, 
                                        max_value=max_date, 
                                        value=(min_date, max_date))
        
        filtered_df = df[(df['datetime'] >= selected_date_range[0]) & (df['datetime'] <= selected_date_range[1])]
        
        st.write(f"筛选后的数据：{filtered_df.shape[0]} 行")

        if not filtered_df.empty:
            # 打磨次数可视化
            if 'grind_times' in filtered_df.columns:
                grind_times_counts = filtered_df['grind_times'].value_counts()
                fig, ax = plt.subplots()
                ax.bar(grind_times_counts.index, grind_times_counts.values)
                ax.set_xlabel('打磨次数')
                ax.set_ylabel('频次')
                st.pyplot(fig)
            
            # 打磨每点伸出量的可视化
            if 'agp_extension' in filtered_df.columns:
                agp_extension = filtered_df['agp_extension'].apply(lambda x: x if isinstance(x, list) else [])
                agp_extension_flatten = [item for sublist in agp_extension for item in sublist]
                fig, ax = plt.subplots()
                ax.hist(agp_extension_flatten, bins=20)
                ax.set_xlabel('伸出量')
                ax.set_ylabel('频次')
                st.pyplot(fig)