import streamlit as st
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Data Collection
if 'queries' not in st.session_state:
    st.session_state.queries = []
if 'satisfaction_ratings' not in st.session_state:
    st.session_state.satisfaction_ratings = []
if 'topics' not in st.session_state:
    st.session_state.topics = []

query = st.text_input("Ask me something:")
if query:
    st.session_state.queries.append(query)
    topics = ["AI", "Healthcare", "Education", "Finance"]
    selected_topic = st.selectbox("Select the topic of your query", topics)
    st.session_state.topics.append(selected_topic)
    rating = st.slider("Rate your satisfaction with the response", 1, 5)
    st.session_state.satisfaction_ratings.append(rating)

queries_df = pd.DataFrame(st.session_state.queries, columns=["Query"])
ratings_df = pd.DataFrame(st.session_state.satisfaction_ratings, columns=["Rating"])
topics_df = pd.DataFrame(st.session_state.topics, columns=["Topic"])

# 2. Data Analysis
num_queries = len(st.session_state.queries)
most_common_topics = Counter(st.session_state.topics).most_common(5)
avg_rating = ratings_df["Rating"].mean()
rating_distribution = ratings_df["Rating"].value_counts().sort_index()

# 3. Dashboard Visualization
st.title("Chatbot Analytics Dashboard")

st.header("Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Queries", num_queries)
col2.metric("Average Satisfaction", f"{avg_rating:.2f} / 5")
col3.metric("Most Common Topic", most_common_topics[0][0] if most_common_topics else "N/A")

st.header("Most Common Topics")
topics_chart = pd.DataFrame(most_common_topics, columns=['Topic', 'Count'])
st.bar_chart(topics_chart.set_index('Topic'))

st.header("Satisfaction Rating Distribution")
fig, ax = plt.subplots()
sns.barplot(x=rating_distribution.index, y=rating_distribution.values, palette="viridis", ax=ax)
ax.set_title("Distribution of Satisfaction Ratings")
ax.set_xlabel("Rating")
ax.set_ylabel("Count")
st.pyplot(fig)

st.subheader("All Queries")
st.dataframe(queries_df)

st.subheader("User Satisfaction Ratings")
st.dataframe(ratings_df)
