import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

# ---------------------------------
# PAGE CONFIG
# ---------------------------------

st.set_page_config(
    page_title="Sri Lankan Job Market Analysis",
    page_icon="🇱🇰",
    layout="wide"
)

# ---------------------------------
# LOAD DATA
# ---------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned/jobs_cleaned.csv")

    df["posted_date"] = pd.to_datetime(
        df["posted_date"],
        errors="coerce"
    )

    df["closing_date"] = pd.to_datetime(
        df["closing_date"],
        errors="coerce"
    )

    return df

df = load_data()

@st.cache_resource
def load_model():
    return joblib.load("ml/job_classifier.pkl")

model = load_model()

# ---------------------------------
# TITLE
# ---------------------------------

st.title("🇱🇰 Sri Lankan Job Market Analysis Dashboard")

st.markdown("""
This dashboard analyzes job vacancies scraped from **TopJobs.lk** using:

- 🐍 Python
- 🌐 BeautifulSoup
- 🗄 SQLite
- 🤖 Machine Learning
- 📈 Streamlit
- 📊 Plotly
""")

st.divider()

# ---------------------------------
# SIDEBAR
# ---------------------------------

st.sidebar.header("🔎 Filter Jobs")

categories = sorted(df["category"].dropna().unique())
regions = sorted(df["region"].dropna().unique())

selected_category = st.sidebar.selectbox(
    "Category",
    ["All"] + categories
)

selected_region = st.sidebar.selectbox(
    "Region",
    ["All"] + regions
)

search_company = st.sidebar.text_input(
    "Company Name"
)

filtered_df = df.copy()

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["category"] == selected_category
    ]

if selected_region != "All":
    filtered_df = filtered_df[
        filtered_df["region"] == selected_region
    ]

if search_company:
    filtered_df = filtered_df[
        filtered_df["company"].str.contains(
            search_company,
            case=False,
            na=False
        )
    ]

st.sidebar.write(f"Jobs Found: **{len(filtered_df)}**")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.sidebar.download_button(
    "⬇ Download Filtered Data",
    csv,
    "filtered_jobs.csv",
    "text/csv"
)

st.sidebar.divider()

st.sidebar.info(
"""
### About

This project analyzes the Sri Lankan job market using data scraped from TopJobs.lk.

Developer:
**Nipuni Karunanayake**
"""
)

# ---------------------------------
# KPI CARDS
# ---------------------------------

st.subheader("📈 Dashboard Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Jobs",
    len(filtered_df)
)

col2.metric(
    "Companies",
    filtered_df["company"].nunique()
)

col3.metric(
    "Cities",
    filtered_df["city"].nunique()
)

col4.metric(
    "Categories",
    filtered_df["category"].nunique()
)

st.divider()

# ---------------------------------
# MACHINE LEARNING PREDICTION
# ---------------------------------

st.header("🤖 Job Category Prediction")

job_title = st.text_input(
    "Enter a Job Title",
    placeholder="Example: Data Analyst"
)

# ---------------------------------
# PREDICTION
# ---------------------------------

if st.button("Predict Category", use_container_width=True):

    if job_title.strip() == "":
        st.warning("Please enter a job title.")

    else:

        prediction = model.predict([job_title])[0]

        st.success(f"Predicted Category: **{prediction}**")

        # Confidence Score
        if hasattr(model, "predict_proba"):

            probability = model.predict_proba([job_title])[0]

            confidence = probability.max()

            st.progress(float(confidence))

            st.write(f"Confidence: **{confidence:.1%}**")

        st.subheader("💼 Similar Jobs")

        similar = df[
            df["category"] == prediction
        ][
            [
                "title",
                "company",
                "city",
                "region"
            ]
        ].head(5)

        st.dataframe(
            similar,
            use_container_width=True
        )

st.divider()

# ---------------------------------
# SEARCH JOBS
# ---------------------------------

st.header("🔍 Search Jobs")

search_title = st.text_input(
    "Search by Job Title",
    placeholder="Example: Software Engineer"
)

search_df = filtered_df.copy()

if search_title:

    search_df = search_df[
        search_df["title"].str.contains(
            search_title,
            case=False,
            na=False
        )
    ]

st.write(f"Jobs Found: **{len(search_df)}**")

st.dataframe(
    search_df[
        [
            "title",
            "company",
            "city",
            "region",
            "category"
        ]
    ],
    use_container_width=True
)

st.divider()

# ---------------------------------
# PREPARE CHART DATA
# ---------------------------------

category_counts = (
    filtered_df["category"]
    .value_counts()
    .reset_index()
)

category_counts.columns = [
    "Category",
    "Count"
]

company_counts = (
    filtered_df["company"]
    .value_counts()
    .head(10)
    .reset_index()
)

company_counts.columns = [
    "Company",
    "Count"
]

region_counts = (
    filtered_df["region"]
    .value_counts()
    .reset_index()
)

region_counts.columns = [
    "Region",
    "Count"
]

city_counts = (
    filtered_df["city"]
    .value_counts()
    .head(10)
    .reset_index()
)

city_counts.columns = [
    "City",
    "Count"
]

# ---------------------------------
# CHARTS
# ---------------------------------

left, right = st.columns(2)

with left:

    st.subheader("📊 Jobs by Category")

    fig = px.bar(
        category_counts,
        x="Category",
        y="Count",
        color="Category",
        text="Count"
    )

    fig.update_layout(
        xaxis_title="Category",
        yaxis_title="Jobs"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("🥧 Category Distribution")

    fig = px.pie(
        category_counts,
        names="Category",
        values="Count",
        hole=0.45
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

left, right = st.columns(2)

with left:

    st.subheader("🏢 Top 10 Companies")

    fig = px.bar(
        company_counts,
        x="Count",
        y="Company",
        orientation="h",
        color="Count",
        text="Count"
    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("🌍 Jobs by Region")

    fig = px.bar(
        region_counts,
        x="Region",
        y="Count",
        color="Region",
        text="Count"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

st.subheader("🏙️ Top Cities")

fig = px.bar(
    city_counts,
    x="Count",
    y="City",
    orientation="h",
    color="Count",
    text="Count"
)

fig.update_layout(
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ---------------------------------
# MONTHLY JOB TREND
# ---------------------------------

st.header("📈 Monthly Job Posting Trend")

monthly_jobs = (
    filtered_df
    .dropna(subset=["posted_date"])
    .groupby(filtered_df["posted_date"].dt.to_period("M"))
    .size()
    .reset_index(name="Jobs")
)

monthly_jobs["posted_date"] = monthly_jobs["posted_date"].astype(str)

fig = px.line(
    monthly_jobs,
    x="posted_date",
    y="Jobs",
    markers=True,
    title="Jobs Posted Per Month"
)

fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Number of Jobs"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ---------------------------------
# INTERACTIVE JOB TABLE
# ---------------------------------

st.header("📋 Browse Job Listings")

table_category = st.selectbox(
    "Filter Table by Category",
    ["All"] + sorted(df["category"].dropna().unique())
)

table_df = filtered_df.copy()

if table_category != "All":
    table_df = table_df[
        table_df["category"] == table_category
    ]

st.dataframe(
    table_df[
        [
            "title",
            "company",
            "city",
            "region",
            "category"
        ]
    ],
    use_container_width=True,
    height=450
)

st.divider()

# ---------------------------------
# RANDOM JOB RECOMMENDATION
# ---------------------------------

st.header("🎲 Discover a Random Job")

if st.button("Recommend a Job"):

    random_job = filtered_df.sample(1).iloc[0]

    st.success(random_job["title"])

    col1, col2 = st.columns(2)

    with col1:
        st.write("**🏢 Company**")
        st.write(random_job["company"])

        st.write("**📍 City**")
        st.write(random_job["city"])

    with col2:
        st.write("**🌍 Region**")
        st.write(random_job["region"])

        st.write("**📂 Category**")
        st.write(random_job["category"])

st.divider()

# ---------------------------------
# CATEGORY LEADERBOARD
# ---------------------------------

st.header("🏆 Job Category Leaderboard")

leaderboard = (
    filtered_df["category"]
    .value_counts()
    .reset_index()
)

leaderboard.columns = [
    "Category",
    "Jobs"
]

leaderboard.index = leaderboard.index + 1

st.table(leaderboard)

st.divider()

# ---------------------------------
# DATASET OVERVIEW
# ---------------------------------

st.header("📊 Dataset Overview")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Rows", len(filtered_df))
    st.metric("Columns", len(filtered_df.columns))

with c2:
    st.metric("Companies", filtered_df["company"].nunique())
    st.metric("Cities", filtered_df["city"].nunique())

with c3:
    st.metric("Regions", filtered_df["region"].nunique())
    st.metric("Categories", filtered_df["category"].nunique())

st.divider()

# ---------------------------------
# DATA PREVIEW
# ---------------------------------

with st.expander("👀 View Dataset Preview"):

    st.dataframe(
        filtered_df.head(20),
        use_container_width=True
    )

st.divider()

# ---------------------------------
# PROJECT INFORMATION
# ---------------------------------

st.header("ℹ️ About This Project")

st.markdown("""
### Sri Lankan Job Market Analysis

This dashboard was developed to analyze Sri Lankan job vacancies scraped from **TopJobs.lk**.

### Technologies Used

- 🐍 Python
- 🌐 BeautifulSoup
- 🗄 SQLite
- 📊 Pandas
- 🤖 Scikit-learn
- 📈 Plotly
- 🎨 Streamlit

### Machine Learning

A **Multinomial Naive Bayes** classifier combined with **TF-IDF Vectorization** predicts the category of a job title.

### Dashboard Features

- Job Category Prediction
- Confidence Score
- Similar Job Recommendation
- Interactive Filters
- Job Search
- Company Analysis
- Region Analysis
- City Analysis
- Monthly Job Trends
- Download Filtered Dataset
""")

st.divider()

# ---------------------------------
# FOOTER
# ---------------------------------

st.markdown(
    """
---
<div style='text-align:center'>

### 🇱🇰 Sri Lankan Job Market Analysis

Developed by **Nipuni Karunanayake**

Made with ❤️ using Python, Streamlit, Plotly, Scikit-learn & SQLite

</div>
""",
    unsafe_allow_html=True
)