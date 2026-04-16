import pandas as pd
import plotly.express as px

# 1. Data Load & Clean (Wahi logic jo bar chart mein kaam kar gaya)
df = pd.read_csv('data.csv', encoding='unicode_escape')
location_col = df.columns[1] 
value_col = 'Total - Total_18 years & Above'

df_clean = df[~df[location_col].str.contains('Total|All India', case=False, na=False)].copy()
df_grouped = df_clean.groupby(location_col)[value_col].sum().reset_index()

# 2. Map Name Matching (Aksar Govt data aur Map data mein names alag hote hain)
# Example: 'Andaman & Nicobar' vs 'Andaman and Nicobar Islands'
# Hum filhal standard names use karenge
print("🗺️ Creating National Heatmap...")

# 3. Final Map Code
fig = px.choropleth(
    df_grouped,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d1a7df9754632c31478/raw/229a4a79649175373801f440536c4983a4216893/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations=location_col,
    color=value_col,
    color_continuous_scale="Reds", 
    title='<b>India Missing Persons Danger Zones (Heatmap)</b>',
    labels={value_col: 'Missing Cases'}
)

fig.update_geos(fitbounds="locations", visible=False)

# Look and Feel
fig.update_layout(
    margin={"r":0,"t":50,"l":0,"b":0},
    title_x=0.5,
    geo=dict(bgcolor= 'rgba(0,0,0,0)')
)

fig.show()