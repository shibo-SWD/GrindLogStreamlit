# import_data.py
import os
import json
import pandas as pd
import streamlit as st
from datetime import datetime

def extract_datetime_from_filename(filename):
    # 假设文件名格式为 'yyyymmdd-hhmmss.log'
    basename = os.path.basename(filename)
    timestamp_str = basename.split('.')[0]  # 去掉扩展名
    return pd.to_datetime(timestamp_str, format="%Y%m%d-%H%M%S")

def load_logs_from_directory(directory_path):
    logs = []
    filenames = []
    timestamps = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".log"):
            filepath = os.path.join(directory_path, filename)
            with open(filepath, 'r') as file:
                log_data = json.load(file)
                logs.append(log_data)
                filenames.append(filename)
                timestamps.append(extract_datetime_from_filename(filename))
    return logs, filenames, timestamps



def import_and_clean_data(folder_path):
    all_files = [f for f in os.listdir(folder_path) if f.endswith('.log')]
    
    dataframes = []
    
    for file in all_files:
        file_path = os.path.join(folder_path, file)
        
        # 读取文件内容并创建 DataFrame
        df = pd.read_json(file_path)  # 根据实际格式选择读取方式
        
        # 从文件名提取时间信息并添加到 DataFrame
        df['datetime'] = extract_datetime_from_filename(file)
        
        dataframes.append(df)
    
    # 合并所有 DataFrame
    combined_df = pd.concat(dataframes, ignore_index=True)
    return combined_df
