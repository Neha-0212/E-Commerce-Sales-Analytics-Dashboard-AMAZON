import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# -----------------------------
# CSS (Clean Portfolio UI)
# -----------------------------
st.markdown("""
<style>
.main {
background-color: #f5f7fb;
}

.card {
background-color: white;
padding: 20px;
border-radius: 10px;
box-shadow: 0 2px 8px rgba(0,0,0,0.08);
margin-bottom: 20px;
}

.title {
font-size:28px;
font-weight:600;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("processed_data.csv")
    product_df = pd.read_csv("product_data.csv")
    return df, product_df

df, product_df = load_data()

# -----------------------------
# Title
# -----------------------------
st.markdown(
    '<div class="title">E-Commerce Sales Analytics Dashboard</div>',
    unsafe_allow_html=True
)

st.divider()

# -----------------------------
# Filters
# -----------------------------
col1, col2 = st.columns(2)

category = col1.selectbox(
    "Category",
    ["All"] + list(df['Category'].unique())
)

region = col2.selectbox(
    "Region",
    ["All"] + list(df['Region'].unique())
)

filtered_df = df.copy()

if category != "All":
    filtered_df = filtered_df[
        filtered_df['Category'] == category
    ]

if region != "All":
    filtered_df = filtered_df[
        filtered_df['Region'] == region
    ]

# -----------------------------
# KPIs
# -----------------------------
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
total_orders = len(filtered_df)

best_product = product_df.loc[
    product_df['Profit'].idxmax()
]['Product Name']

worst_product = product_df.loc[
    product_df['Profit'].idxmin()
]['Product Name']

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Sales", f"{total_sales:,.0f}")
c2.metric("Total Profit", f"{total_profit:,.0f}")
c3.metric("Orders", total_orders)
c4.metric("Best Product", best_product)

st.divider()

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "Overview",
    "Product Analysis",
    "Segmentation",
    "Data Table"
])

# -----------------------------
# TAB 1 — Overview
# -----------------------------
with tab1:

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Sales Trend")

        monthly = filtered_df.groupby(
            'Month'
        )['Sales'].sum()

        fig, ax = plt.subplots()
        monthly.plot(ax=ax)

        st.pyplot(fig)

    with col2:
        st.subheader("Profit by Category")

        cat = filtered_df.groupby(
            'Category'
        )['Profit'].sum()

        fig, ax = plt.subplots()
        cat.plot(kind='bar', ax=ax)

        st.pyplot(fig)

    st.divider()

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Region Performance")

        region_data = filtered_df.groupby(
            'Region'
        )['Profit'].sum()

        fig, ax = plt.subplots()
        region_data.plot(kind='bar', ax=ax)

        st.pyplot(fig)

    with col4:
        st.subheader("Profit vs Quantity")

        fig, ax = plt.subplots()

        sns.scatterplot(
            x='Quantity',
            y='Profit',
            data=product_df,
            ax=ax
        )

        st.pyplot(fig)

# -----------------------------
# TAB 2 — Product Analysis
# -----------------------------
with tab2:

    st.subheader("Top Profit Products")

    top_products = product_df.sort_values(
        'Profit',
        ascending=False
    ).head(10)

    fig, ax = plt.subplots(figsize=(8,5))

    sns.barplot(
        y='Product Name',
        x='Profit',
        data=top_products,
        ax=ax
    )

    st.pyplot(fig)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Best Product")

        st.dataframe(
            product_df.sort_values(
                'Profit',
                ascending=False
            ).head(5)
        )

    with col2:
        st.subheader("Worst Product")

        st.dataframe(
            product_df.sort_values(
                'Profit'
            ).head(5)
        )

# -----------------------------
# TAB 3 — Segmentation
# -----------------------------
with tab3:

    st.subheader("Product Segments")

    fig, ax = plt.subplots()

    sns.scatterplot(
        x=product_df['Sales'],
        y=product_df['Profit'],
        hue=product_df['Cluster'],
        ax=ax
    )

    st.pyplot(fig)

    st.divider()

    st.subheader("Cluster Summary")

    cluster_summary = product_df.groupby('Cluster').agg({
        'Sales':'mean',
        'Profit':'mean',
        'Quantity':'mean',
        'Profit_margin':'mean',
        'Product Name':'count'
    })

    st.dataframe(cluster_summary)

# -----------------------------
# TAB 4 — Data
# -----------------------------
with tab4:

    st.subheader("Full Dataset")

    st.dataframe(filtered_df)

    st.subheader("Product Table")

    st.dataframe(product_df)