import pandas as pd
import plotly.express as px

# 1. Load Data
try:
    df = pd.read_csv('data.csv', encoding='unicode_escape')
    print("✅ Data Loaded!")
except Exception as e:
    print(f"❌ Error: {e}")
    exit()

# 2. Identify Columns
# Aapki screenshot ke hisaab se columns dhoondhte hain
location_col = df.columns[1] # 'State/UT' ya 'Andhra Pradesh' wala column
value_col = 'Total - Total_18 years & Above'

# 3. CLEANING & GROUPING
# 'Total' wali rows ko delete karein jo graph ka scale bigadti hain
df = df[df[location_col].str.contains('Total|All India', case=False) == False]

# Agar ek hi state ki multiple rows hain, unhe ek sath JOD (sum) dein
df_grouped = df.groupby(location_col)[value_col].sum().reset_index()

# Data ko bade se chote (descending) order mein lagayein
df_grouped = df_grouped.sort_values(by=value_col, ascending=False)

# 4. FINAL BAR CHART
fig = px.bar(
    df_grouped, 
    x=location_col, 
    y=value_col,
    title='State-wise Missing Persons Analysis (Merged & Cleaned)',
    color=value_col,
    text_auto='.2s', # Numbers ko short mein dikhayega (e.g. 1.1k)
    color_continuous_scale='Viridis'
)

# Design settings
fig.update_layout(
    xaxis_tickangle=-45,
    xaxis_title="State / Union Territory",
    yaxis_title="Total Missing Cases",
    margin=dict(b=150)
)

fig.show()