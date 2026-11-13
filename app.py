import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(page_title="Netflix Analytics Dashboard", layout="wide")
st.title("🎬 Netflix Movies & TV Shows Dashboard")
st.markdown("An interactive dashboard built with Streamlit, Pandas, and Seaborn.")


@st.cache_data  
def load_data():
    df = pd.read_csv("netflix_titles.csv")

    df['country'] = df['country'].fillna('Unknown')
    return df

df = load_data()


st.sidebar.header("Filter the Data")


content_types = ["All"] + list(df['type'].unique())
selected_type = st.sidebar.selectbox("Select Content Type", content_types)


min_year = int(df['release_year'].min())
max_year = int(df['release_year'].max())
selected_years = st.sidebar.slider("Select Release Year Range", min_year, max_year, (2010, max_year))


filtered_df = df[(df['release_year'] >= selected_years[0]) & (df['release_year'] <= selected_years[1])]

if selected_type != "All":
    filtered_df = filtered_df[filtered_df['type'] == selected_type]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Titles Displayed", len(filtered_df))
with col2:
    movie_count = len(filtered_df[filtered_df['type'] == 'Movie'])
    st.metric("Total Movies", movie_count)
with col3:
    tv_count = len(filtered_df[filtered_df['type'] == 'TV Show'])
    st.metric("Total TV Shows", tv_count)

st.markdown("---")


col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Content Growth Over Time")
    fig, ax = plt.subplots(figsize=(6, 4))

    sns.histplot(data=filtered_df, x='release_year', hue='type', multiple='stack', bins=20, ax=ax, palette="Reds_r")
    ax.set_xlabel("Release Year")
    ax.set_ylabel("Count of Titles")
    
    
    st.pyplot(fig)

with col_chart2:
    st.subheader("Top 10 Ratings Distribution")
    fig, ax = plt.subplots(figsize=(6, 4))
    
    
    top_ratings = filtered_df['rating'].value_counts().head(10)
    
    
    sns.barplot(x=top_ratings.values, y=top_ratings.index, ax=ax, palette="viridis")
    ax.set_xlabel("Number of Titles")
    ax.set_ylabel("Rating")
    
    st.pyplot(fig)


if st.checkbox("Show Raw Data Table"):
    st.subheader("Filtered Dataset View")
    st.dataframe(filtered_df[['title', 'type', 'director', 'country', 'release_year', 'rating']])