import streamlit as st
import pandas as pd
import plotly.express as px

# Website ki settings
st.set_page_config(page_title="Missing Person Analysis Dashboard", layout="wide")

st.title("🛡️City-Pulse: Missing Person Analytics")
st.markdown("Yeh dashboard India ke missing person data ko analyze karta hai.")

# 1. Data Load
@st.cache_data # Isse website fast load hogi
def load_data():
    df = pd.read_csv('data.csv', encoding='unicode_escape')
    location_col = df.columns[1]
    value_col = 'Total - Total_18 years & Above'
    df_clean = df[~df[location_col].str.contains('Total|All India', case=False, na=False)].copy()
    df_grouped = df_clean.groupby(location_col)[value_col].sum().reset_index()
    return df_grouped, location_col, value_col

df_final, loc_col, val_col = load_data()

# 2. Sidebar Filters (Select State)
st.sidebar.header("Filter Options")
selected_state = st.sidebar.multiselect("Select State/UT to compare:", 
                                       options=df_final[loc_col].unique(),
                                       default=df_final[loc_col].unique()[:5])

filtered_df = df_final[df_final[loc_col].isin(selected_state)]

# 3. Layout: Two Columns (Graph and Stats)
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("State-wise Comparison")
    fig = px.bar(filtered_df, x=loc_col, y=val_col, color=val_col, text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Quick Insights")
    total_cases = df_final[val_col].sum()
    st.metric("Total Missing Reported", f"{total_cases:,}")
    top_state = df_final.iloc[0][loc_col]
    st.warning(f"High Alert: {top_state} has the highest cases.")

# 4. The Heatmap (Full Width)
st.divider()
st.subheader("📍 National Danger Zones (Heatmap)")
fig_map = px.choropleth(
    df_final,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d1a7df9754632c31478/raw/229a4a79649175373801f440536c4983a4216893/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations=loc_col,
    color=val_col,
    color_continuous_scale="Reds",
    scope="asia"
)
fig_map.update_geos(fitbounds="locations", visible=False)
st.plotly_chart(fig_map, use_container_width=True)

st.success("Analysis complete. Data source: data.gov.in")