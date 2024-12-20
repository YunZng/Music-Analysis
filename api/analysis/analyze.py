import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from mpl_toolkits.mplot3d import Axes3D

matplotlib.use('Agg')  # Ensure non-GUI backend is used
def analyze(columns, data):
    df = pd.DataFrame(data, columns=columns)
    image = []

    # Data Cleaning
    # Function to clean and parse dates
    def clean_and_parse_date(date):
        try:
            if len(date) == 4:
                return f"{date}-01-01"
            return pd.to_datetime(date, errors='coerce')
        except Exception:
            return None

    # Apply the cleaning function
    df['Cleaned Date'] = df['Album Release Date'].apply(clean_and_parse_date)

    # Extract and clean year
    df['Year'] = pd.to_datetime(df['Cleaned Date'], errors='coerce').dt.year

    # Drop rows with invalid or missing years
    df = df.dropna(subset=['Year'])

    # Filter data to start from 1950
    df = df[df['Year'] >= 1950]

    # Characteristics list
    characteristics = ['Danceability', 'Energy', 'Loudness', 'Speechiness', 'Acousticness', 
                    'Instrumentalness', 'Liveness', 'Valence', 'Tempo']

    # Group data by Year
    yearly_data = df.groupby('Year').agg({'Track Name': 'count', 'Popularity': 'mean'})
    yearly_data.rename(columns={'Track Name': 'Track Count', 'Popularity': 'Average Popularity'}, inplace=True)

    # Average characteristics by year
    average_characteristics_by_year = df.groupby('Year')[characteristics].mean()

    # # Calculate proportion of explicit tracks
    # yearly_data['Proportion of Explicit Tracks'] = df.groupby('Year')['Explicit'].mean()

    # Correlation matrix
    correlation_matrix = df[characteristics + ['Popularity']].corr()

    # Visualization
    sns.set(style="whitegrid")

    # Create a figure and axes for yearly data plots
    fig, axs = plt.subplots(2, 2, figsize=(20, 14))

    # Plot the top 10 artists with the most tracks
    top_artists = df['Artist Names'].value_counts().head(10)
    top_artists.plot(kind='barh', ax=axs[0, 0], color='skyblue', edgecolor='black')
    axs[0, 0].set_title('Top 10 Artists with the Most Tracks', fontsize=14)
    axs[0, 0].set_xlabel('Track Count', fontsize=12)
    axs[0, 0].invert_yaxis()

    # Plot the yearly track count
    yearly_data['Track Count'].plot(ax=axs[0, 1], color='skyblue', lw=2)
    axs[0, 1].set_title('Yearly Track Count', fontsize=14)
    axs[0, 1].set_xlabel('Year', fontsize=12)
    axs[0, 1].set_ylabel('Track Count', fontsize=12)
    axs[0, 1].set_xlim(1950, yearly_data.index.max())

    # Plot the yearly average popularity
    yearly_data['Average Popularity'].plot(ax=axs[1, 0], color='green', lw=2)
    axs[1, 0].set_title('Yearly Average Popularity', fontsize=14)
    axs[1, 0].set_xlabel('Year', fontsize=12)
    axs[1, 0].set_ylabel('Popularity', fontsize=12)
    axs[1, 0].set_xlim(1950, yearly_data.index.max())

    # Plot the correlation matrix heatmap
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', ax=axs[1, 1])
    axs[1, 1].set_title('Correlation Matrix Heatmap', fontsize=14)

    # Adjust the layout
    plt.tight_layout()
    plt.show()

    # Create a figure and axes for characteristics over time
    fig, axs = plt.subplots(3, 2, figsize=(20, 14))
    fig.tight_layout(pad=4.0)

    # Plot selected characteristics over time
    for i, characteristic in enumerate(characteristics[:6]):
        row, col = divmod(i, 2)
        average_characteristics_by_year[characteristic].plot(ax=axs[row, col], lw=2, color='skyblue')
        axs[row, col].set_title(f'Average {characteristic} Over Time', fontsize=14)
        axs[row, col].set_xlabel('Year', fontsize=12)
        axs[row, col].set_ylabel(characteristic, fontsize=12)
        axs[row, col].set_xlim(1950, yearly_data.index.max())

        
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    image = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()  # Free memory
    plt.close(fig)  # Free memory
    return image