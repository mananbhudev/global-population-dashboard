import streamlit as st
import pandas as pd
import plotly.express as px
import os
import pycountry

# === Page Setup ===
st.set_page_config(page_title="🌍 Global Population Dashboard", layout="wide")
st.title("🌍 Global Population Analysis Dashboard (v7)")

# === Upload CSV File ===
st.sidebar.header("📂 Upload Data")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

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

# === Continent Mapping ===
continent_map = {
    # Asia
    "Afghanistan": "Asia", "China": "Asia", "India": "Asia", "Indonesia": "Asia",
    "Japan": "Asia", "Iran": "Asia", "Iraq": "Asia", "Israel": "Asia",
    "Jordan": "Asia", "Kazakhstan": "Asia", "North Korea": "Asia", "South Korea": "Asia",
    "Kuwait": "Asia", "Kyrgyzstan": "Asia", "Laos": "Asia", "Lebanon": "Asia",
    "Malaysia": "Asia", "Maldives": "Asia", "Myanmar": "Asia", "Nepal": "Asia",
    "Oman": "Asia", "Pakistan": "Asia", "Philippines": "Asia", "Qatar": "Asia",
    "Saudi Arabia": "Asia", "Singapore": "Asia", "Sri Lanka": "Asia", "Syria": "Asia",
    "Tajikistan": "Asia", "Thailand": "Asia", "Timor-Leste": "Asia", "Turkmenistan": "Asia",
    "United Arab Emirates": "Asia", "Uzbekistan": "Asia", "Vietnam": "Asia", "Yemen": "Asia",
    # Europe
    "Albania": "Europe", "Andorra": "Europe", "Armenia": "Europe", "Austria": "Europe",
    "Azerbaijan": "Europe", "Belarus": "Europe", "Belgium": "Europe", "Bosnia and Herzegovina": "Europe",
    "Bulgaria": "Europe", "Croatia": "Europe", "Cyprus": "Europe", "Czech Republic": "Europe",
    "Denmark": "Europe", "Estonia": "Europe", "Finland": "Europe", "France": "Europe",
    "Georgia": "Europe", "Germany": "Europe", "Greece": "Europe", "Hungary": "Europe",
    "Iceland": "Europe", "Ireland": "Europe", "Italy": "Europe", "Latvia": "Europe",
    "Lithuania": "Europe", "Luxembourg": "Europe", "Malta": "Europe", "Moldova": "Europe",
    "Monaco": "Europe", "Montenegro": "Europe", "Netherlands": "Europe", "North Macedonia": "Europe",
    "Norway": "Europe", "Poland": "Europe", "Portugal": "Europe", "Romania": "Europe",
    "Russia": "Europe", "San Marino": "Europe", "Serbia": "Europe", "Slovakia": "Europe",
    "Slovenia": "Europe", "Spain": "Europe", "Sweden": "Europe", "Switzerland": "Europe",
    "Turkey": "Europe", "Ukraine": "Europe", "United Kingdom": "Europe",
    # Africa
    "Algeria": "Africa", "Angola": "Africa", "Benin": "Africa", "Botswana": "Africa",
    "Burkina Faso": "Africa", "Burundi": "Africa", "Cape Verde": "Africa", "Cameroon": "Africa",
    "Central African Republic": "Africa", "Chad": "Africa", "Comoros": "Africa", "Congo": "Africa",
    "Democratic Republic of the Congo": "Africa", "Djibouti": "Africa", "Egypt": "Africa",
    "Equatorial Guinea": "Africa", "Eritrea": "Africa", "Eswatini": "Africa", "Ethiopia": "Africa",
    "Gabon": "Africa", "Gambia": "Africa", "Ghana": "Africa", "Guinea": "Africa",
    "Guinea-Bissau": "Africa", "Ivory Coast": "Africa", "Kenya": "Africa", "Lesotho": "Africa",
    "Liberia": "Africa", "Libya": "Africa", "Madagascar": "Africa", "Malawi": "Africa",
    "Mali": "Africa", "Mauritania": "Africa", "Mauritius": "Africa", "Morocco": "Africa",
    "Mozambique": "Africa", "Namibia": "Africa", "Niger": "Africa", "Nigeria": "Africa",
    "Rwanda": "Africa", "Senegal": "Africa", "Seychelles": "Africa", "Sierra Leone": "Africa",
    "Somalia": "Africa", "South Africa": "Africa", "South Sudan": "Africa", "Sudan": "Africa",
    "Tanzania": "Africa", "Togo": "Africa", "Tunisia": "Africa", "Uganda": "Africa",
    "Zambia": "Africa", "Zimbabwe": "Africa",
    # North America
    "United States": "North America", "Canada": "North America", "Mexico": "North America",
    "Cuba": "North America", "Costa Rica": "North America", "Panama": "North America",
    "Jamaica": "North America", "Haiti": "North America", "Dominican Republic": "North America",
    # South America
    "Brazil": "South America", "Argentina": "South America", "Colombia": "South America",
    "Chile": "South America", "Peru": "South America", "Ecuador": "South America",
    "Bolivia": "South America", "Paraguay": "South America", "Uruguay": "South America",
    "Venezuela": "South America", "Guyana": "South America", "Suriname": "South America",
    # Oceania
    "Australia": "Oceania", "New Zealand": "Oceania", "Fiji": "Oceania", "Papua New Guinea": "Oceania",
    "Samoa": "Oceania", "Tonga": "Oceania", "Vanuatu": "Oceania"
}

if "continent" not in df.columns:
    df["continent"] = df["country"].map(continent_map).fillna("Other")

# === Sidebar Filters ===
st.sidebar.header("🎯 Filter Options")
selected_continent = st.sidebar.multiselect(
    "Select Continent(s)",
    options=sorted(df["continent"].unique()),
    default=["Asia"]
)
filtered_df = df[df["continent"].isin(selected_continent)]

st.subheader("📊 Dataset Preview")
st.dataframe(filtered_df.head())

# === Numeric Columns ===
numeric_columns = filtered_df.select_dtypes(include=["float64", "int64"]).columns.tolist()

# === Bar Chart ===
st.subheader("📈 Bar Chart")
y_axis_bar = st.selectbox("Select numeric column for Bar Chart", numeric_columns, index=0)
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

# === World Map with formatted hover ===
st.subheader("🗺️ World Map (Enhanced Hover Info)")
map_metric = st.selectbox("Select numeric column for Map color", numeric_columns, index=0, key="map_metric")
hover_metrics = st.multiselect(
    "Select additional numeric columns for hover info",
    options=[col for col in numeric_columns if col != map_metric],
    default=[]
)

# --- ISO Alpha-3 codes ---
def get_iso3(country_name):
    try:
        return pycountry.countries.lookup(country_name).alpha_3
    except:
        return None

map_df = filtered_df.copy()
map_df["iso_alpha"] = map_df["country"].apply(get_iso3)
map_df = map_df.dropna(subset=["iso_alpha"])

# --- Format hover values ---
display_cols = [map_metric] + hover_metrics
map_df_display = map_df.copy()
for col in display_cols:
    if col.endswith("_pct"):
        map_df_display[col + "_display"] = map_df_display[col].map(lambda x: f"{x:.2f}%")
    else:
        map_df_display[col + "_display"] = map_df_display[col].map(lambda x: f"{int(x):,}")

customdata = map_df_display[[col + "_display" for col in display_cols]].values

# --- Build hover template ---
hover_template = "<b>%{hovertext}</b><br><br>"
hover_template += f"{map_metric.replace('_',' ').title()}: %{customdata[0]}<br>"
for idx, col in enumerate(hover_metrics):
    hover_template += f"{col.replace('_',' ').title()}: %{customdata[{idx+1}]}<br>"

# --- Create choropleth ---
fig_map = px.choropleth(
    map_df,
    locations="iso_alpha",
    color=map_metric,
    hover_name="country",
    color_continuous_scale="Viridis"
)
fig_map.update_traces(hovertemplate=hover_template, hovertext=map_df["country"], customdata=customdata)
st.plotly_chart(fig_map, use_container_width=True)
