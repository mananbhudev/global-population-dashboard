import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Optional: pycountry for ISO Alpha-3 codes
try:
    import pycountry
    PYCOUNTRY_AVAILABLE = True
except ModuleNotFoundError:
    PYCOUNTRY_AVAILABLE = False

# === Page Setup ===
st.set_page_config(page_title="🌍 Global Population Dashboard", layout="wide")
st.title("🌍 Global Population Analysis Dashboard (Final v1)")

# === Upload CSV File ===
st.sidebar.header("📂 Upload Data")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"], key="main_uploader")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Data uploaded successfully!")
else:
    csv_path = os.path.join(os.path.dirname(__file__), "population_data.csv")
    try:
        df = pd.read_csv(csv_path)
        st.info("ℹ️ Using default dataset (population_data.csv)")
    except Exception as e:
        st.error(f"❌ Could not load CSV file: {e}")
        st.stop()

# === Clean column names ===
df.columns = (
    df.columns.str.strip()
    .str.replace(r"[()]", "", regex=True)
    .str.replace(" ", "_")
    .str.replace("%", "pct")
    .str.lower()
)

# === Continent Mapping (fallback if pycountry not used) ===
continent_map = {
    # simplified mapping
    "Asia": ["Afghanistan", "China", "India", "Japan", "Iran", "Iraq", "Israel", "Pakistan", "Nepal", "Thailand"],
    "Europe": ["France", "Germany", "Italy", "United Kingdom", "Spain"],
    "Africa": ["Nigeria", "Egypt", "South Africa", "Kenya"],
    "North America": ["United States", "Canada", "Mexico"],
    "South America": ["Brazil", "Argentina", "Colombia"],
    "Oceania": ["Australia", "New Zealand", "Fiji"]
}

def map_continent(country_name):
    for continent, countries in continent_map.items():
        if country_name in countries:
            return continent
    return "Other"

if "continent" not in df.columns:
    df["continent"] = df["country"].apply(map_continent)

# === Sidebar Filters ===
st.sidebar.header("🎯 Filter Options")
selected_continent = st.sidebar.multiselect(
    "Select Continent(s)",
    options=sorted(df["continent"].unique()),
    default=["Asia"],
    key="continent_filter"
)
filtered_df = df[df["continent"].isin(selected_continent)]

st.subheader("📊 Dataset Preview")
st.dataframe(filtered_df.head())

# === Numeric Columns ===
numeric_columns = filtered_df.select_dtypes(include=["float64", "int64"]).columns.tolist()

# === Bar Chart ===
st.subheader("📈 Bar Chart")
y_axis_bar = st.selectbox("Select numeric column for Bar Chart", numeric_columns, index=0, key="bar_chart")
fig_bar = px.bar(
    filtered_df,
    x="country",
    y=y_axis_bar,
    color="continent",
    title=f"{y_axis_bar.replace('_',' ').title()} by Country and Continent"
)
st.plotly_chart(fig_bar, use_container_width=True)

# === Line Chart ===
st.subheader("📊 Line Chart")
y_axis_line = st.selectbox("Select numeric column for Line Chart", numeric_columns, index=0, key="line_chart")
fig_line = px.line(
    filtered_df,
    x="country",
    y=y_axis_line,
    color="continent",
    markers=True,
    title=f"{y_axis_line.replace('_',' ').title()} Trend by Country"
)
st.plotly_chart(fig_line, use_container_width=True)

# === Correlation Heatmap ===
st.subheader("🔥 Correlation Heatmap")
if len(numeric_columns) > 1:
    corr = filtered_df[numeric_columns].corr()
    fig_corr = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        title="Correlation Between Numeric Features"
    )
    st.plotly_chart(fig_corr, use_container_width=True)
else:
    st.info("Not enough numeric columns for correlation heatmap.")

# === World Map ===
st.subheader("🗺️ World Map")
map_metric = st.selectbox("Select numeric column for Map color", numeric_columns, index=0, key="map_metric")
hover_metrics = st.multiselect(
    "Select additional numeric columns for hover info",
    options=[col for col in numeric_columns if col != map_metric],
    default=[],
    key="map_hover"
)

if PYCOUNTRY_AVAILABLE:
    def get_iso3(country_name):
        try:
            return pycountry.countries.lookup(country_name).alpha_3
        except:
            return None
    map_df = filtered_df.copy()
    map_df["iso_alpha"] = map_df["country"].apply(get_iso3)
    map_df = map_df.dropna(subset=["iso_alpha"])

    display_cols = [map_metric] + hover_metrics
    map_df_display = map_df.copy()
    for col in display_cols:
        if col.endswith("_pct"):
            map_df_display[col + "_display"] = map_df_display[col].map(lambda x: f"{x:.2f}%")
        else:
            map_df_display[col + "_display"] = map_df_display[col].map(lambda x: f"{int(x):,}")

    customdata = map_df_display[[col + "_display" for col in display_cols]].values

    hover_template = "<b>%{hovertext}</b><br><br>"
    hover_template += f"{map_metric.replace('_',' ').title()}: %{customdata[0]}<br>"
    for idx, col in enumerate(hover_metrics):
        hover_template += f"{col.replace('_',' ').title()}: %{customdata[{idx+1}]}<br>"

    fig_map = px.choropleth(
        map_df,
        locations="iso_alpha",
        color=map_metric,
        hover_name="country",
        color_continuous_scale="Viridis"
    )
    fig_map.update_traces(hovertemplate=hover_template, hovertext=map_df["country"], customdata=customdata)
    st.plotly_chart(fig_map, use_container_width=True)
else:
    st.info("pycountry not installed: World Map disabled. Install it with `pip install pycountry`")
