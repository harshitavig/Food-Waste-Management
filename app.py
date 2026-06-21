import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------
# PAGE CONFIG
# ---------------------------------

st.set_page_config(
    page_title="Food Waste Management Dashboard",
    page_icon="🍲",
    layout="wide"
)

# ---------------------------------
# LOAD DATA
# ---------------------------------

df = pd.read_csv("merged_data.csv")

# ---------------------------------
# SIDEBAR FILTERS
# ---------------------------------

st.sidebar.title("Filters")

food_type = st.sidebar.multiselect(
    "Food Type",
    df["Food_Type"].dropna().unique()
)

meal_type = st.sidebar.multiselect(
    "Meal Type",
    df["Meal_Type"].dropna().unique()
)

provider_type = st.sidebar.multiselect(
    "Provider Type",
    df["Provider_Type"].dropna().unique()
)

status = st.sidebar.multiselect(
    "Claim Status",
    df["Status"].dropna().unique()
)

city = st.sidebar.multiselect(
    "City",
    df["City"].dropna().unique()
)

filtered_df = df.copy()

if food_type:
    filtered_df = filtered_df[
        filtered_df["Food_Type"].isin(food_type)
    ]

if meal_type:
    filtered_df = filtered_df[
        filtered_df["Meal_Type"].isin(meal_type)
    ]

if provider_type:
    filtered_df = filtered_df[
        filtered_df["Provider_Type"].isin(provider_type)
    ]

if status:
    filtered_df = filtered_df[
        filtered_df["Status"].isin(status)
    ]

if city:
    filtered_df = filtered_df[
        filtered_df["City"].isin(city)
    ]

# ---------------------------------
# TITLE
# ---------------------------------

st.title("🍲 Food Waste Management Dashboard")

# ---------------------------------
# KPI SECTION
# ---------------------------------

st.subheader("Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Food Listings",
    filtered_df["Food_ID"].nunique()
)

col2.metric(
    "Total Quantity",
    int(filtered_df["Quantity"].sum())
)

col3.metric(
    "Providers",
    filtered_df["Provider_ID"].nunique()
)

col4.metric(
    "Receivers",
    filtered_df["Receiver_ID"].nunique()
)

col5.metric(
    "Claims",
    len(filtered_df)
)

# ---------------------------------
# CHART 1
# Provider Type Distribution
# ---------------------------------

st.subheader("1. Provider Type Distribution")

fig, ax = plt.subplots()
filtered_df["Provider_Type"].value_counts().plot(
    kind="bar",
    ax=ax
)
st.pyplot(fig)

# ---------------------------------
# CHART 2
# Receiver Type Distribution
# ---------------------------------

st.subheader("2. Receiver Type Distribution")

fig, ax = plt.subplots()
filtered_df["Type_y"].value_counts().plot(
    kind="bar",
    ax=ax
)
st.pyplot(fig)

# ---------------------------------
# CHART 3
# Food Type Distribution
# ---------------------------------

st.subheader("3. Food Type Distribution")

fig, ax = plt.subplots()
filtered_df["Food_Type"].value_counts().plot(
    kind="bar",
    ax=ax
)
st.pyplot(fig)

# ---------------------------------
# CHART 4
# Meal Type Distribution
# ---------------------------------

st.subheader("4. Meal Type Distribution")

fig, ax = plt.subplots()
filtered_df["Meal_Type"].value_counts().plot(
    kind="bar",
    ax=ax
)
st.pyplot(fig)

# ---------------------------------
# CHART 5
# City vs Food Listings
# ---------------------------------

st.subheader("5. City vs Food Listings")

city_listing = (
    filtered_df.groupby("City")
    .size()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(8,5))
city_listing.plot(kind="bar", ax=ax)
st.pyplot(fig)

# ---------------------------------
# CHART 6
# Provider Type vs Quantity
# ---------------------------------

st.subheader("6. Provider Type vs Quantity")

provider_qty = (
    filtered_df.groupby("Provider_Type")["Quantity"]
    .sum()
)

fig, ax = plt.subplots()
provider_qty.plot(kind="bar", ax=ax)
st.pyplot(fig)

# ---------------------------------
# CHART 7
# Food Type vs Quantity
# ---------------------------------

st.subheader("7. Food Type vs Quantity")

food_qty = (
    filtered_df.groupby("Food_Type")["Quantity"]
    .sum()
)

fig, ax = plt.subplots()
food_qty.plot(kind="bar", ax=ax)
st.pyplot(fig)

# ---------------------------------
# CHART 8
# Meal Type vs Quantity
# ---------------------------------

st.subheader("8. Meal Type vs Quantity")

meal_qty = (
    filtered_df.groupby("Meal_Type")["Quantity"]
    .sum()
)

fig, ax = plt.subplots()
meal_qty.plot(kind="bar", ax=ax)
st.pyplot(fig)

# ---------------------------------
# CHART 9
# City + Provider Type + Quantity
# ---------------------------------

st.subheader("9. City + Provider Type + Quantity")

pivot1 = pd.pivot_table(
    filtered_df,
    values="Quantity",
    index="City",
    columns="Provider_Type",
    aggfunc="sum",
    fill_value=0
)

fig, ax = plt.subplots(figsize=(10,6))
sns.heatmap(pivot1, cmap="Blues")
st.pyplot(fig)

# ---------------------------------
# CHART 10
# Food Type + Meal Type + Quantity
# ---------------------------------

st.subheader("10. Food Type + Meal Type + Quantity")

pivot2 = pd.pivot_table(
    filtered_df,
    values="Quantity",
    index="Food_Type",
    columns="Meal_Type",
    aggfunc="sum",
    fill_value=0
)

fig, ax = plt.subplots(figsize=(8,5))
sns.heatmap(pivot2, cmap="YlGnBu")
st.pyplot(fig)

# ---------------------------------
# CHART 11
# Provider + Claims + Quantity
# ---------------------------------

st.subheader("11. Provider + Claims + Quantity")

provider_claims = (
    filtered_df.groupby("Name")
    .agg(
        Claims=("Food_ID","count"),
        Quantity=("Quantity","sum")
    )
    .sort_values("Claims",ascending=False)
    .head(10)
)

st.bar_chart(provider_claims)

# ---------------------------------
# CHART 12
# Receiver + Claims + Quantity
# ---------------------------------

st.subheader("12. Receiver + Claims + Quantity")

receiver_claims = (
    filtered_df.groupby("Receiver_ID")
    .agg(
        Claims=("Food_ID","count"),
        Quantity=("Quantity","sum")
    )
    .sort_values("Claims",ascending=False)
    .head(10)
)

st.bar_chart(receiver_claims)

# ---------------------------------
# CHART 13
# Claim Status Distribution
# ---------------------------------

st.subheader("13. Claim Status Distribution")

fig, ax = plt.subplots()
filtered_df["Status"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%",
    ax=ax
)
st.pyplot(fig)

# ---------------------------------
# CHART 14
# Top Receivers
# ---------------------------------

st.subheader("14. Top Receivers")

top_receivers = (
    filtered_df.groupby("Receiver_ID")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots()
top_receivers.plot(kind="bar", ax=ax)
st.pyplot(fig)

# ---------------------------------
# CHART 15
# Top Providers
# ---------------------------------

st.subheader("15. Top Providers")

top_providers = (
    filtered_df.groupby("Name")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots()
top_providers.plot(kind="bar", ax=ax)
st.pyplot(fig)

# ---------------------------------
# DATASET
# ---------------------------------

st.subheader("Dataset Preview")

st.dataframe(filtered_df)

# ---------------------------------
# INSIGHTS
# ---------------------------------

st.subheader("Key Findings")

st.write("""
• Restaurants and grocery stores contribute major food quantities.

• Some cities have significantly higher food listings than others.

• Certain receivers claim food more frequently.

• Completed, Pending and Cancelled claims are fairly distributed.

• Top providers contribute a large portion of total food donations.
""")
