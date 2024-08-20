import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import numpy as np

# 设置中文字体
mpl.font_manager.fontManager.addfont('./misc/font/SimHei.ttf') #临时注册新的全局字体
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False#用来正常显示负号

def display_visualizations():
    st.sidebar.title("数据可视化")
    st.title("数据可视化")


    # 确保数据已加载
    if 'filtered_df' not in st.session_state:
        st.warning("请先导入和选择数据")
        return
    
    df = st.session_state.filtered_df

    colsItem = [col for col in df.columns]
   
    # 用户选择的操作选项
    options = st.sidebar.multiselect(
        "选择你要进行的操作：",
        ['打磨成功率', '双变量联合分析', '三变量联合分析', '去除率分析']
    )

    # 打磨成功率分析
    if '打磨成功率' in options:
        st.subheader("打磨成功率")
        if 'grinding_completed' in df.columns:
            completion_counts = df['grinding_completed'].value_counts()
            labels = ['Failed', 'Successed'][:len(completion_counts)]
            fig, ax = plt.subplots()
            ax.pie(completion_counts, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            st.pyplot(fig)
        else:
            st.warning("数据中不包含 'grinding_completed' 列")
        
        if not selected_row.empty:
            st.write(f"选择的日志文件: {selected_filename}")

    # 双变量联合分析
    # 双变量联合分析
    if '双变量联合分析' in options:
        st.sidebar.subheader("双变量联合分析")
        
        # 提取数据列名
        colsItem = df.columns.tolist()
        
        parameter1 = st.sidebar.selectbox(
            "选择变量1",
            colsItem
        )
        parameter2 = st.sidebar.selectbox(
            "选择变量2",
            colsItem
        )
        
        if parameter1 and parameter2:
            # 生成双变量联合分析的 Seaborn 图
            if parameter1 in df.columns and parameter2 in df.columns:
                fig, ax = plt.subplots()
                sns.scatterplot(data=df, x=parameter1, y=parameter2, ax=ax)
                ax.set_xlabel(parameter1)
                ax.set_ylabel(parameter2)
                ax.set_title(f"{parameter1} vs {parameter2}")
                st.pyplot(fig)
            else:
                st.warning(f"数据中不包含 '{parameter1}' 或 '{parameter2}' 列")

    # 三变量联合分析
    if '三变量联合分析' in options:
        st.subheader("三变量联合分析")
        # 在此处添加你的三变量联合分析代码
        # 示例：分析 grind_times、grindForce 和 grindSpeed 的关系
        if all(col in selected_row.columns for col in ['grind_times', 'grindForce', 'grindSpeed']):
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(selected_row['grind_times'], selected_row['grindForce'], selected_row['grindSpeed'])
            ax.set_xlabel('打磨次数')
            ax.set_ylabel('打磨力')
            ax.set_zlabel('打磨速度')
            st.pyplot(fig)
        else:
            st.warning("数据中不包含 'grind_times'、'grindForce' 或 'grindSpeed' 列")


    # 打磨头伸出量分析

    # 选择是否显示去除率分析
    if '去除率分析' in options:
        st.sidebar.subheader("去除率分析")

        # 显示文件名并让用户选择
        df['filename'] = df['datetime'].apply(lambda x: x.strftime('%Y%m%d_%H%M%S.log'))
        selected_filename = st.sidebar.selectbox("选择日志文件", df['filename'].unique())
        selected_row = df[df['filename'] == selected_filename]
        all_records = selected_row['agp_extension'].apply(lambda x: x if isinstance(x, list) else [])
        agp_data = all_records.iloc[0]

        is_apg_extension_visualization = st.sidebar.checkbox("打磨头去除量可视化")
        is_apg_extension_analysis = st.sidebar.checkbox("打磨量分析")

        if is_apg_extension_visualization:
            st.subheader("打磨头去除量可视化")
            all_records = selected_row['agp_extension'].apply(lambda x: x if isinstance(x, list) else [])
            agp_data = all_records.iloc[0]

            # 选择具体的打磨记录
            if 'agp_extension' in selected_row.columns:
                # 提取所有的打磨记录
                # Prepare the data for plotting
                # 准备数据用于绘图
                data = []
                for i, extension_list in enumerate(agp_data):
                    for j, extension in enumerate(extension_list):
                        data.append({'打磨编号': i + 1, '检测点': j + 1, '伸出量': extension})

                melted_df = pd.DataFrame(data)

                # 使用滑块选择打磨编号
                selected_grind = st.slider('选择打磨编号以高亮显示', min_value=1, max_value=len(agp_data), value=1)

                # 绘制打磨头伸出量的图像
                fig, ax = plt.subplots(figsize=(10, 6))

                # 添加所有打磨次数为背景线
                sns.lineplot(
                    data=melted_df, x='检测点', y='伸出量', hue='打磨编号',
                    palette='Blues', linewidth=1, ax=ax, legend=False
                )

                # 高亮显示用户选择的打磨次数
                highlight_data = melted_df[melted_df['打磨编号'] == selected_grind]
                sns.lineplot(
                    data=highlight_data, x='检测点', y='伸出量',
                    color='red', linewidth=3, marker='o', ax=ax, label=f'打磨编号 {selected_grind}'
                )

                ax.set_title('打磨头伸出量分析')
                ax.set_xlabel('检测点')
                ax.set_ylabel('打磨头伸出量')
                ax.legend(title='打磨编号', loc='upper right')

                st.pyplot(fig)

            # # Bar plot of the average磨头伸出量
            # if mean_values:
            #     fig, ax = plt.subplots(figsize=(10, 6))
            #     sns.barplot(x=range(len(mean_values)), y=mean_values, ax=ax)
            #     ax.set_title('每次打磨的平均打磨头伸出量')
            #     ax.set_xlabel('打磨编号')
            #     ax.set_ylabel('平均打磨头伸出量')
            #     st.pyplot(fig)
            # else:
            #     st.warning("没有足够的数据来绘制平均打磨头伸出量的条形图"
            else:
                st.warning("数据中不包含 'agp_extension' 列")
        
        if is_apg_extension_analysis:
            st.subheader("去除量分析")
            # 计算每一遍打磨的平均值
            mean_values = []
            for extension_list in agp_data:
                if len(extension_list) > 2:  # 确保列表中有足够的数据去除极值
                    filtered_list = sorted(extension_list)[1:-1]  # 去除极大值和极小值
                    mean_value = sum(filtered_list) / len(filtered_list)
                else:
                    mean_value = sum(extension_list) / len(extension_list)  # 无法去除极值，直接取平均
                mean_values.append(mean_value)

            # 计算每次打磨的平均下降量
            descent_values = []
            for i in range(1, len(mean_values)):
                descent = mean_values[i - 1] - mean_values[i]
                descent_values.append(descent)

            # 绘制打磨次数及其平均下降量的barplot

            fig, ax = plt.subplots(figsize=(10, 6))

            # 使用 seaborn 的色调调色板 'OrRd'，根据 descent_values 进行颜色映射
            norm = plt.Normalize(min(descent_values), max(descent_values))
            sm = plt.cm.ScalarMappable(cmap="OrRd", norm=norm)
            sm.set_array([])

            sns.barplot(
                x=range(2, len(mean_values) + 1),
                y=descent_values,
                palette=sns.color_palette("OrRd", as_cmap=True),
                ax=ax,
                hue=descent_values,  # 按照值大小进行颜色绘制
                dodge=False
            )

            ax.set_title('每次打磨的平均下降量')
            ax.set_xlabel('打磨编号')
            ax.set_ylabel('平均下降量')

            st.pyplot(fig)

            # 打印打磨过程的统计信息
            st.write(f"打磨过程共经历了 {len(agp_data)} 遍")
            # st.write(f"打磨的平均下降量如下：")
            # for i, descent in enumerate(descent_values, start=2):
            #     st.write(f"第 {i} 遍打磨: 平均下降 {descent:.2f}")