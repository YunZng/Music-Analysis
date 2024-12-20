import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import seaborn as sns

# 读取数据
df = pd.read_csv("top_10000_1950-now.csv")

# 数据预处理：转换日期，提取年份
df['Album Release Date'] = pd.to_datetime(df['Album Release Date'], errors='coerce')
df['Album Release Year'] = df['Album Release Date'].dt.year

# 聚焦于年份和歌手流行度信息
df_artists = df[['Album Release Year', 'Artist Name(s)', 'Popularity']].dropna()

# 统计每年歌手的平均流行度（可用其他逻辑：如总流行度）
df_grouped = (df_artists
              .groupby(['Album Release Year', 'Artist Name(s)'], as_index=False)['Popularity']
              .mean())

# 排名前 10 歌手
df_grouped['rank'] = df_grouped.groupby('Album Release Year')['Popularity'].rank(method='first', ascending=False)
df_top10 = df_grouped[df_grouped['rank'] <= 10]

# 颜色映射：为每个歌手分配颜色
artists = df_top10['Artist Name(s)'].unique()
palette = sns.color_palette("husl", len(artists))
color_map = dict(zip(artists, palette))

# 绘制条形竞赛动画
fig, ax = plt.subplots(figsize=(10, 6))

def update(year):
    ax.clear()
    data = df_top10[df_top10['Album Release Year'] == year].sort_values(by='rank', ascending=True)
    ax.barh(data['Artist Name(s)'], data['Popularity'], color=[color_map[artist] for artist in data['Artist Name(s)']])
    ax.set_title(f"Top Artists per Year: {year}", fontsize=18)
    ax.set_xlabel("Average Popularity")
    ax.set_xlim(0, df_top10['Popularity'].max())

# 生成动画
years = sorted(df_top10['Album Release Year'].dropna().unique())
ani = FuncAnimation(fig, update, frames=years, repeat=False)

# 保存为 GIF 文件
ani.save("top_artists_bar_race.gif", writer='pillow', fps=5)
print("GIF 动画已保存为 top_artists_bar_race.gif")
