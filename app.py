
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path
import io

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Weather Analytics Dashboard",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. PROFESSIONAL CSS DESIGN
# ==========================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg, #0B1020, #151B35, #211A3D
    );
    color: #F1F5F9;
}

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg, #111827, #1E1B3A
    );
    border-right: 1px solid #34365B;
}

[data-testid="stHeader"] {
    background: transparent;
}

h1, h2, h3 {
    color: #FFFFFF !important;
}

p, label {
    color: #CBD5E1;
}

/* KPI CARDS */

[data-testid="stMetric"] {
    background: linear-gradient(
        135deg, #20294A, #302653
    );
    border: 1px solid #41466B;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 5px 18px rgba(0,0,0,0.25);
}

[data-testid="stMetricLabel"] {
    color: #A5B4FC !important;
}

[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-size: 26px !important;
}

div[data-testid="stPlotlyChart"] {
    background: rgba(30,41,72,0.55);
    border: 1px solid #34365B;
    border-radius: 15px;
    padding: 8px;
}

.stButton > button {
    background: linear-gradient(
        90deg, #6366F1, #A855F7
    );
    color: white;
    border: none;
    border-radius: 10px;
}

[data-testid="stDataFrame"] {
    border: 1px solid #41466B;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. LOAD DATASET
# ==========================================

st.sidebar.markdown("# 🌤️ Weather Analytics")
st.sidebar.markdown("---")


@st.cache_data
def load_data(file_bytes):

    data = pd.read_csv(io.BytesIO(file_bytes))

    return data


file_path = Path(__file__).resolve().parent / "weather_data.csv"

if file_path.exists():

    try:
        df = load_data(file_path.read_bytes())

        st.sidebar.success(
            "Dataset loaded successfully!"
        )

    except Exception as e:

        st.error(f"CSV loading error: {e}")
        st.stop()

else:

    st.sidebar.warning(
        "CSV file not found in project folder."
    )

    uploaded_file = st.sidebar.file_uploader(
        "Upload weather_data.csv",
        type=["csv"]
    )

    if uploaded_file is None:

        st.info(
            "Please upload your weather_data.csv file "
            "using the sidebar."
        )

        st.stop()

    try:

        df = load_data(uploaded_file.getvalue())

        st.sidebar.success(
            "Dataset uploaded successfully!"
        )

    except Exception as e:

        st.error(f"CSV loading error: {e}")
        st.stop()


# ==========================================
# 4. DATA CLEANING
# ==========================================

required_columns = [
    "Temperature (C)",
    "Apparent Temperature (C)",
    "Humidity",
    "Wind Speed (km/h)",
    "Precip Type",
    "Visibility (km)",
    "Pressure (millibars)"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:

    st.error(
        f"Missing columns: {missing_columns}"
    )

    st.stop()


df["Precip Type"] = (
    df["Precip Type"]
    .fillna("No Precip")
    .astype(str)
    .str.strip()
    .str.title()
)

df = df.drop_duplicates().copy()

if df.empty:

    st.error("Dataset is empty.")
    st.stop()


# ==========================================
# 5. SIDEBAR FILTERS
# ==========================================

st.sidebar.markdown("## 🎛️ Dashboard Filters")

filtered_df = df.copy()

precip_options = ["All"] + sorted(
    df["Precip Type"].unique().tolist()
)

selected_precip = st.sidebar.selectbox(
    "Precipitation Type",
    precip_options
)

if selected_precip != "All":

    filtered_df = filtered_df[
        filtered_df["Precip Type"] == selected_precip
    ]


if "Year" in df.columns:

    years = sorted(
        df["Year"].dropna().unique().tolist()
    )

    if years:

        selected_year = st.sidebar.selectbox(
            "Select Year",
            ["All"] + years
        )

        if selected_year != "All":

            filtered_df = filtered_df[
                filtered_df["Year"] == selected_year
            ]


if "Month" in df.columns:

    months = sorted(
        df["Month"].dropna().unique().tolist()
    )

    if months:

        selected_month = st.sidebar.selectbox(
            "Select Month",
            ["All"] + months
        )

        if selected_month != "All":

            filtered_df = filtered_df[
                filtered_df["Month"] == selected_month
            ]


st.sidebar.markdown("---")

st.sidebar.markdown("""
### 📌 Project Information

**Project:** Weather Data Analysis

**Language:** Python

**Libraries:** Pandas, NumPy, Plotly

**Framework:** Streamlit

**Type:** Exploratory Data Analysis
""")

st.sidebar.markdown("---")

st.sidebar.caption(
    "Weather Analytics Dashboard | 2026"
)


# ==========================================
# 6. CHECK FILTERED DATA
# ==========================================

if filtered_df.empty:

    st.warning(
        "No records found for selected filters."
    )

    st.stop()


# ==========================================
# 7. DASHBOARD HEADER
# ==========================================

st.markdown(
    "# 🌤️ Weather Analytics Dashboard"
)

st.markdown(
    "### Explore Weather Patterns, Temperature & Environmental Conditions"
)

st.markdown(
    "An interactive dashboard to explore weather data "
    "and discover important patterns."
)

st.markdown("---")


# ==========================================
# 8. KPI CALCULATIONS
# ==========================================

total_records = len(filtered_df)

avg_temp = filtered_df[
    "Temperature (C)"
].mean()

avg_apparent = filtered_df[
    "Apparent Temperature (C)"
].mean()

avg_humidity = filtered_df[
    "Humidity"
].mean()

avg_wind = filtered_df[
    "Wind Speed (km/h)"
].mean()

avg_visibility = filtered_df[
    "Visibility (km)"
].mean()

rain_count = (
    filtered_df["Precip Type"] == "Rain"
).sum()

snow_count = (
    filtered_df["Precip Type"] == "Snow"
).sum()

no_precip_count = (
    filtered_df["Precip Type"] == "No Precip"
).sum()


# ==========================================
# 9. WEATHER OVERVIEW
# ==========================================

st.markdown("## 📊 Weather Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "📁 Total Records",
        f"{total_records:,}"
    )

with col2:

    st.metric(
        "🌡️ Average Temperature",
        f"{avg_temp:.2f} °C"
    )

with col3:

    st.metric(
        "💧 Average Humidity",
        f"{avg_humidity:.2%}"
    )

with col4:

    st.metric(
        "💨 Average Wind Speed",
        f"{avg_wind:.2f} km/h"
    )


col5, col6, col7, col8 = st.columns(4)

with col5:

    st.metric(
        "🌡️ Feels Like Temperature",
        f"{avg_apparent:.2f} °C"
    )

with col6:

    st.metric(
        "👁️ Average Visibility",
        f"{avg_visibility:.2f} km"
    )

with col7:

    st.metric(
        "🌧️ Rain Records",
        f"{rain_count:,}"
    )

with col8:

    st.metric(
        "❄️ Snow Records",
        f"{snow_count:,}"
    )


st.markdown("---")


# ==========================================
# 10. CHART STYLE FUNCTION
# ==========================================

def style_chart(fig, height=380):

    fig.update_layout(

        height=height,

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="#E2E8F0",
            family="Arial"
        ),

        margin=dict(
            l=30,
            r=25,
            t=60,
            b=40
        ),

        title_font=dict(
            size=18,
            color="#FFFFFF"
        )

    )

    return fig


# ==========================================
# 11. TEMPERATURE DISTRIBUTION
# ==========================================

st.markdown("## 🌡️ Temperature Analysis")

col1, col2 = st.columns(2)

with col1:

    fig = px.histogram(

        filtered_df,

        x="Temperature (C)",

        nbins=40,

        title="Temperature Distribution",

        color_discrete_sequence=["#818CF8"]

    )

    fig.update_layout(

        xaxis_title="Temperature (°C)",

        yaxis_title="Number of Records"

    )

    style_chart(fig)

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ==========================================
# 12. PRECIPITATION ANALYSIS
# ==========================================

with col2:

    precip_counts = (
        filtered_df["Precip Type"]
        .value_counts()
        .reset_index()
    )

    precip_counts.columns = [
        "Precipitation",
        "Count"
    ]

    fig = px.pie(

        precip_counts,

        names="Precipitation",

        values="Count",

        hole=0.55,

        title="Precipitation Type Distribution",

        color_discrete_sequence=[
            "#818CF8",
            "#38BDF8",
            "#C084FC"
        ]

    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    style_chart(fig)

    st.plotly_chart(
        fig,
        use_container_width=True
    )


st.markdown("---")


# ==========================================
# 13. TEMPERATURE VS APPARENT TEMPERATURE
# ==========================================

st.markdown(
    "## 🌡️ Temperature vs Apparent Temperature"
)

fig = px.scatter(

    filtered_df,

    x="Temperature (C)",

    y="Apparent Temperature (C)",

    color="Humidity",

    opacity=0.45,

    title="Actual Temperature vs Feels Like Temperature",

    color_continuous_scale="Purples"

)

style_chart(fig, 450)

st.plotly_chart(
    fig,
    use_container_width=True
)

correlation1 = filtered_df[
    "Temperature (C)"
].corr(
    filtered_df["Apparent Temperature (C)"]
)

st.info(
    f"📌 Correlation: {correlation1:.2f}"
)


# ==========================================
# 14. TEMPERATURE VS HUMIDITY
# ==========================================

st.markdown("## 💧 Temperature vs Humidity")

fig = px.scatter(

    filtered_df,

    x="Temperature (C)",

    y="Humidity",

    color="Humidity",

    opacity=0.4,

    color_continuous_scale="Teal",

    title="Relationship Between Temperature and Humidity"

)

style_chart(fig)

st.plotly_chart(
    fig,
    use_container_width=True
)

correlation2 = filtered_df[
    "Temperature (C)"
].corr(
    filtered_df["Humidity"]
)

st.info(
    f"📌 Temperature and Humidity Correlation: "
    f"{correlation2:.2f}"
)


st.markdown("---")


# ==========================================
# 15. VISIBILITY AND WIND ANALYSIS
# ==========================================

st.markdown("## 👁️ Visibility & Wind Analysis")

col1, col2 = st.columns(2)

with col1:

    fig = px.scatter(

        filtered_df,

        x="Temperature (C)",

        y="Visibility (km)",

        color="Visibility (km)",

        opacity=0.4,

        color_continuous_scale="Plasma",

        title="Temperature vs Visibility"

    )

    style_chart(fig)

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    fig = px.histogram(

        filtered_df,

        x="Wind Speed (km/h)",

        nbins=35,

        title="Wind Speed Distribution",

        color_discrete_sequence=["#C084FC"]

    )

    style_chart(fig)

    st.plotly_chart(
        fig,
        use_container_width=True
    )


correlation3 = filtered_df[
    "Temperature (C)"
].corr(
    filtered_df["Visibility (km)"]
)

st.info(
    f"📌 Temperature and Visibility Correlation: "
    f"{correlation3:.2f}"
)


st.markdown("---")


# ==========================================
# 16. CORRELATION HEATMAP
# ==========================================

st.markdown("## 🔥 Correlation Heatmap")

numeric_df = filtered_df.select_dtypes(
    include=np.number
)

correlation_matrix = numeric_df.corr()

fig = px.imshow(

    correlation_matrix,

    text_auto=".2f",

    aspect="auto",

    color_continuous_scale="RdBu_r",

    zmin=-1,

    zmax=1,

    title="Correlation Between Numerical Variables"

)

style_chart(fig, 550)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ==========================================
# 17. OUTLIER ANALYSIS
# ==========================================

st.markdown("---")

st.markdown("## 📌 Outlier Analysis")

outlier_counts = {}

for col in numeric_df.columns:

    Q1 = numeric_df[col].quantile(0.25)

    Q3 = numeric_df[col].quantile(0.75)

    IQR = Q3 - Q1

    outliers = (

        (numeric_df[col] < Q1 - 1.5 * IQR) |

        (numeric_df[col] > Q3 + 1.5 * IQR)

    ).sum()

    outlier_counts[col] = int(outliers)


outlier_df = pd.DataFrame(

    list(outlier_counts.items()),

    columns=[
        "Column",
        "Outlier Count"
    ]

)

fig = px.bar(

    outlier_df.sort_values(
        "Outlier Count",
        ascending=False
    ),

    x="Column",

    y="Outlier Count",

    color="Outlier Count",

    color_continuous_scale="Purples",

    title="Outliers in Numerical Columns"

)

fig.update_layout(
    xaxis_tickangle=-35
)

style_chart(fig, 450)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ==========================================
# 18. DATASET PREVIEW
# ==========================================

st.markdown("---")

st.markdown("## 📋 Weather Dataset Preview")

st.dataframe(

    filtered_df.head(100),

    use_container_width=True,

    height=300

)


# ==========================================
# 19. DOWNLOAD FILTERED DATASET
# ==========================================

csv = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(

    label="⬇️ Download Filtered Dataset",

    data=csv,

    file_name="weather_analysis.csv",

    mime="text/csv"

)


# ==========================================
# 20. KEY PROJECT FINDINGS
# ==========================================

st.markdown("---")

st.markdown("## 🎯 Key Project Findings")

st.markdown("""
### 1. Temperature Analysis

Temperature and Apparent Temperature have
a very strong positive relationship.

### 2. Precipitation Analysis

Rain is the most common precipitation type
in the original dataset.

### 3. Humidity Analysis

Temperature and Humidity have a negative
relationship.

### 4. Outlier Analysis

Wind Speed and Pressure contain a high
number of outliers.

### 5. Visibility Analysis

Temperature and Visibility show a moderate
positive relationship.
""")


# ==========================================
# 21. PROFESSIONAL FOOTER
# ==========================================

st.markdown("---")

st.markdown(
    "<h3 style='text-align:center; color:#A5B4FC;'>"
    "🌤️ Weather Analytics Dashboard"
    "</h3>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center; color:#94A3B8;'>"
    "Built with Python | Streamlit | Pandas | Plotly"
    "</p>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center; color:#94A3B8;'>"
    "Weather Data Analysis Project"
    "</p>",
    unsafe_allow_html=True
)
