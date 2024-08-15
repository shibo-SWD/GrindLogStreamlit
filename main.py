# main.py
import streamlit as st
from pages.import_data import import_and_clean_data
from pages.data_selection import display_logs_selection
from pages.data_visualization import display_visualizations

# 默认宽屏
st.set_page_config(page_title="打磨日志可视化", layout="wide")

st.title("打磨日志可视化")

# 导入数据
folder_path = st.text_input("输入文件夹路径", "./logs")
if st.button("导入数据") and folder_path:
    st.session_state.df = import_and_clean_data(folder_path)
    st.success("数据导入成功")

# 数据选择页面
display_logs_selection()

# 数据可视化页面
display_visualizations()
