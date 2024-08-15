# import_data.py
import os
import json
import pandas as pd
import streamlit as st
from datetime import datetime

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



def extract_datetime_from_filename(filename):
    """
    从文件名中提取日期时间信息。假设文件名中包含日期时间信息，格式为 'YYYYMMDD_HHMMSS.log'。
    """
    try:
        # 假设文件名格式为 'YYYYMMDD_HHMMSS.log'
        # 去除文件扩展名
        timestamp_str = filename.replace('.log', '')
        # 提取日期时间部分
        return datetime.strptime(timestamp_str, "%Y%m%d-%H%M%S")
    except (IndexError, ValueError):
        # 如果格式不匹配，则返回当前时间
        return datetime.now()


def import_and_clean_data(folder_path):
    all_files = [f for f in os.listdir(folder_path) if f.endswith('.log')]
    
    dataframes = []
    
    for file in all_files:
        file_path = os.path.join(folder_path, file)
        
        with open(file_path, 'r') as f:
            # 读取 JSON 数据
            data = json.load(f)
        
        # 创建 DataFrame，只包含其他字段
        df = pd.DataFrame([data])
        
        # 确保 'apg_extension' 列不被包括在 DataFrame 中
        if 'apg_extension' in df.columns:
            df = df.drop(columns=['apg_extension'])
        
        # 从文件名提取时间信息并添加到 DataFrame
        df['datetime'] = extract_datetime_from_filename(file)
        
        dataframes.append(df)
        print(df)
        print(df.shape)
        print(df.iloc[0].to_dict())
    
    # 合并所有 DataFrame
    combined_df = pd.concat(dataframes, ignore_index=True)
    return combined_df
