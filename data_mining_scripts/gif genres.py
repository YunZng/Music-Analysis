import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import seaborn as sns

# 读取数据
df = pd.read_csv("top_10000_1950-now.csv")

# 数据预处理：转换日期，提取年份
df['Album Release Date'] = pd.to_datetime(df['Album Release Date'], errors='coerce')
df['Album Release Year'] = df['Album Release Date'].dt.year

# 清理并展开流派列：拆分逗号分隔的值为多行
df = df[['Album Release Year', 'Artist Genres']].dropna()
df = df.assign(Artist_Genres=df['Artist Genres'].str.split(',')).explode('Artist_Genres')
df['Artist_Genres'] = df['Artist_Genres'].str.strip()  # 去除多余空格

# 按年份和流派统计歌曲数量，并排名前10
df_grouped = df.groupby(['Album Release Year', 'Artist_Genres']).size().reset_index(name='count')
df_grouped['rank'] = df_grouped.groupby('Album Release Year')['count'].rank(method='first', ascending=False)
df_top10 = df_grouped[df_grouped['rank'] <= 10]

# 颜色映射：为每个流派分配颜色
genres = df_top10['Artist_Genres'].unique()
palette = sns.color_palette("husl", len(genres))
color_map = dict(zip(genres, palette))

# 绘制条形竞赛动画
fig, ax = plt.subplots(figsize=(10, 6))

def update(year):
    ax.clear()
    data = df_top10[df_top10['Album Release Year'] == year].sort_values(by='rank', ascending=True)
    ax.barh(data['Artist_Genres'], data['count'], color=[color_map[genre] for genre in data['Artist_Genres']])
    ax.set_title(f"Top Music Genres per Year: {year}", fontsize=18)
    ax.set_xlabel("Number of Tracks")
    ax.set_xlim(0, df_top10['count'].max())

# 生成动画
years = sorted(df_top10['Album Release Year'].dropna().unique())
ani = FuncAnimation(fig, update, frames=years, repeat=False)

# 保存为 GIF 文件
ani.save("top_genres_bar_race.gif", writer='pillow', fps=5)
print("GIF 动画已保存为 top_genres_bar_race.gif")






