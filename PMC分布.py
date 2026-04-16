# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# from scipy import stats
#
#
# def analyze_pmc_distribution(file_path):
#     try:
#         # 读取Excel数据
#         df = pd.read_excel(file_path)
#
#         # 检查必要列是否存在
#         if '编码' not in df.columns or 'PMC指数' not in df.columns:
#             raise ValueError("数据中缺少'编码'或'PMC指数'列，请检查数据文件")
#
#         # 提取分析数据
#         pmc_data = df['PMC指数'].copy()
#
#         # 设置中文字体（解决中文显示问题）
#         plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC", "sans-serif"]
#         plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
#
#         # 计算基本分布特征
#         distribution_features = {
#             '样本量': len(pmc_data),
#             '最小值': pmc_data.min(),
#             '最大值': pmc_data.max(),
#             '均值': pmc_data.mean(),
#             '中位数': pmc_data.median(),
#             '标准差': pmc_data.std(),
#             '偏度': stats.skew(pmc_data),
#             '峰度': stats.kurtosis(pmc_data)
#         }
#
#         # 定义目标区间（用于分割线和统计）
#         target_bins = [0, 5, 7, 9, 10]
#         target_labels = ['[0,5)', '[5,7)', '[7,9)', '[9,10]']
#
#         # 生成区间分类列（用于统计）
#         df['区间'] = pd.cut(
#             pmc_data,
#             bins=target_bins,
#             labels=target_labels,
#             include_lowest=True,
#             right=False
#         )
#         interval_distribution = df['区间'].value_counts().sort_index().to_dict()
#
#         # 可视化设置
#         fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
#
#         # 直方图（使用stat='density'）
#         sns.histplot(
#             pmc_data,
#             kde=False,  # 暂时关闭KDE，避免参数冲突
#             stat='density',  # 将Y轴设为密度
#             bins=20,  # 分箱数量
#             ax=ax1,  # 指定子图
#             color='skyblue',  # 直方图颜色
#             edgecolor='darkblue',  # 边界颜色
#             linewidth=1.0  # 边界线宽
#         )
#
#         # 单独绘制KDE曲线（确保兼容性）
#         sns.kdeplot(
#             pmc_data,
#             ax=ax1,
#             linewidth=3,  # 加粗KDE曲线
#             color='skyblue',  # 与直方图颜色一致
#             alpha=0.8  # 透明度
#         )
#
#         # 添加区间分割垂线（标注关键区间边界）
#         for boundary in target_bins[1:-1]:  # 跳过首尾边界（0和10）
#             ax1.axvline(
#                 x=boundary,
#                 color='darkred',
#                 linestyle='--',
#                 linewidth=1.2,
#                 alpha=0.7
#             )
#             ax1.text(
#                 x=boundary + 0.1,
#                 y=ax1.get_ylim()[1] * 0.95,  # 放置在图表顶部95%高度
#                 s=f'分割点：{boundary}',
#                 color='darkred',
#                 fontsize=10,
#                 rotation=90  # 文字垂直显示
#             )
#
#         # 添加Y轴标签（明确是密度）
#         ax1.set_title('PMC指数分布直方图', fontsize=14)
#         ax1.set_xlabel('PMC指数', fontsize=12)
#         ax1.set_ylabel('密度', fontsize=12)
#
#         # 箱线图（保持原有逻辑）
#         sns.boxplot(y=pmc_data, ax=ax2, color='lightgreen')
#         ax2.set_title('PMC指数整体分布箱线图', fontsize=14)
#         ax2.set_ylabel('PMC指数', fontsize=12)
#
#         plt.tight_layout()
#         plt.show()
#
#         return distribution_features, interval_distribution
#
#     except FileNotFoundError:
#         print(f"错误：未找到文件 {file_path}，请检查文件路径是否正确")
#         return None, None
#     except Exception as e:
#         print(f"分析过程中发生错误：{str(e)}")
#         return None, None
#
#
# if __name__ == "__main__":
#     # 请根据实际情况修改文件路径
#     data_path = r'F:\python\pythonProject\PMC分布.xlsx'
#
#     # 执行分析
#     features, intervals = analyze_pmc_distribution(data_path)
#
#     # 输出结果
#     if features and intervals:
#         print("\n===== 分布特征统计 =====")
#         for key, value in features.items():
#             print(f"{key}: {value:.4f}" if isinstance(value, float) else f"{key}: {value}")
#
#         print("\n===== 区间分布统计 =====")
#         for interval, count in intervals.items():
#             print(f"{interval}: {count} 个（占比：{count / features['样本量']:.2%}）")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats


def analyze_pmc_distribution(file_path):
    try:
        # 读取Excel数据
        df = pd.read_excel(file_path)

        # 检查必要列是否存在
        if '编码' not in df.columns or 'PMC指数' not in df.columns:
            raise ValueError("数据中缺少'编码'或'PMC指数'列，请检查数据文件")

        # 提取分析数据
        pmc_data = df['PMC指数'].copy()
        n = len(pmc_data)  # 样本量

        # 设置中文字体（解决中文显示问题）
        plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC", "sans-serif"]
        plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

        # 计算基本分布特征
        distribution_features = {
            '样本量': n,
            '最小值': pmc_data.min(),
            '最大值': pmc_data.max(),
            '均值': pmc_data.mean(),
            '中位数': pmc_data.median(),
            '标准差': pmc_data.std(),
            '偏度': stats.skew(pmc_data),
            '峰度': stats.kurtosis(pmc_data)
        }

        # 定义目标区间（用于分割线和统计）
        target_bins = [0, 5, 7, 9, 10]
        target_labels = ['[0,5)', '[5,7)', '[7,9)', '[9,10]']

        # 生成区间分类列（用于统计）
        df['区间'] = pd.cut(
            pmc_data,
            bins=target_bins,
            labels=target_labels,
            include_lowest=True,
            right=False
        )
        interval_distribution = df['区间'].value_counts().sort_index().to_dict()

        # 可视化设置
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # 直方图（纵坐标为频数）
        sns.histplot(
            pmc_data,
            kde=False,  # 关闭默认KDE（避免单位冲突）
            stat='count',  # 纵坐标为频数
            bins=20,  # 分箱数量
            ax=ax1,  # 指定子图
            color='skyblue',  # 直方图颜色
            edgecolor='darkblue',  # 边界颜色
            linewidth=1.0  # 边界线宽
        )

        # 计算KDE曲线（转换为频数尺度）
        # 1. 计算默认密度KDE
        kde = stats.gaussian_kde(pmc_data)
        x = np.linspace(pmc_data.min(), pmc_data.max(), 200)  # 生成x轴坐标
        density = kde(x)

        # 2. 转换为频数：密度 * 样本量 * 分箱宽度（确保与直方图单位一致）
        bin_width = (pmc_data.max() - pmc_data.min()) / 20  # 直方图分箱宽度
        freq_kde = density * n * bin_width

        # 3. 绘制频数尺度的KDE曲线（淡蓝色趋势线）
        ax1.plot(
            x,
            freq_kde,
            color='skyblue',  # 与直方图颜色一致
            linewidth=2.5,  # 加粗趋势线
            alpha=0.8,  # 透明度
            label='分布趋势'  # 添加图例
        )
        ax1.legend()  # 显示图例

        # 添加区间分割垂线（标注关键区间边界）
        for boundary in target_bins[1:-1]:  # 跳过首尾边界（0和10）
            ax1.axvline(
                x=boundary,
                color='darkred',
                linestyle='--',
                linewidth=1.2,
                alpha=0.7
            )
            ax1.text(
                x=boundary + 0.1,
                y=ax1.get_ylim()[1] * 0.95,  # 放置在图表顶部95%高度
                s=f'分割点：{boundary}',
                color='darkred',
                fontsize=10,
                rotation=90  # 文字垂直显示
            )

        # 恢复纵坐标标签为"频数"
        ax1.set_title('PMC指数分布直方图', fontsize=14)
        ax1.set_xlabel('PMC指数', fontsize=12)
        ax1.set_ylabel('频数', fontsize=12)

        # 箱线图（保持原有逻辑）
        sns.boxplot(y=pmc_data, ax=ax2, color='lightgreen')
        ax2.set_title('PMC指数整体分布箱线图', fontsize=14)
        ax2.set_ylabel('PMC指数', fontsize=12)

        plt.tight_layout()
        plt.show()

        return distribution_features, interval_distribution

    except FileNotFoundError:
        print(f"错误：未找到文件 {file_path}，请检查文件路径是否正确")
        return None, None
    except Exception as e:
        print(f"分析过程中发生错误：{str(e)}")
        return None, None


if __name__ == "__main__":
    # 请根据实际情况修改文件路径
    data_path = r'F:\python\pythonProject\PMC分布.xlsx'

    # 执行分析
    features, intervals = analyze_pmc_distribution(data_path)

    # 输出结果
    if features and intervals:
        print("\n===== 分布特征统计 =====")
        for key, value in features.items():
            print(f"{key}: {value:.4f}" if isinstance(value, float) else f"{key}: {value}")

        print("\n===== 区间分布统计 =====")
        for interval, count in intervals.items():
            print(f"{interval}: {count} 个（占比：{count / features['样本量']:.2%}）")