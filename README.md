# Live project link - https://e-commerce-sales-analytics-dashboard-amazon-mp5jhdejrceugjjg8m.streamlit.app/
# E-Commerce Sales Analytics Dashboard(AMAZON)

---

## Overview

This project is an end-to-end sales analytics pipeline built on 3,500 e-commerce transactions spanning 3 years (2022–2024). It covers the full workflow: raw data ingestion, feature engineering, unsupervised ML-based product segmentation, and an interactive Streamlit dashboard for business exploration.

The core problem it addresses is straightforward: raw transactional sales data tells you *what sold*, but not *what to act on*. This project transforms flat order records into actionable intelligence — identifying which product categories drive the most profit, how regional performance differs, and which products deserve more investment vs. which are dragging margins down.

The KMeans clustering layer adds a layer beyond simple reporting. Products are grouped by behavioral similarity across sales volume, profit, quantity, and margin — so stakeholders can make decisions based on product archetypes rather than individual SKU noise.

The Streamlit dashboard makes the analysis interactive: filter by category and region, inspect KPIs, drill into product-level rankings, and explore cluster segments — all without writing a single query.

---

## Features

- **Dynamic filtering** — slice the entire dashboard by product category (Electronics, Accessories, Office) and region (North, East, South, West) simultaneously
- **Live KPI cards** — total sales, total profit, order count, and best-performing product update in real time with applied filters
- **Monthly sales trend** — line chart showing revenue seasonality across 36 months
- **Category and region profit breakdown** — bar charts for quick cross-dimensional comparison
- **Profit vs. Quantity scatter** — identifies volume-driven vs. margin-driven products at a glance
- **Product leaderboard** — top 10 and bottom 10 products ranked by total profit
- **KMeans product segmentation** — 3-cluster grouping of all 10 products based on standardized sales, profit, quantity, and margin features
- **Cluster summary table** — average metrics per cluster with product count, for segment-level business decisions
- **Raw data explorer** — full filterable dataset and product-level aggregate table in a dedicated tab

---

## Tech Stack

**Data & Analysis**
- Python 3.10+
- Pandas — data cleaning, feature engineering, aggregations
- NumPy — numerical operations

**Machine Learning**
- scikit-learn — `StandardScaler` for feature normalization, `KMeans` for clustering (Elbow method used to select k=3)

**Visualization**
- Matplotlib — line charts, bar charts
- Seaborn — scatter plots, heatmaps, box plots

**Dashboard**
- Streamlit — multi-tab interactive web app with caching (`@st.cache_data`)

---

## System Architecture / Workflow

```
Raw Data (ecommerce_sales_data.csv)
        │
        ▼
[ Data Cleaning & Preprocessing ]  ← make.ipynb
  - Drop duplicates
  - Parse Order Date → Month, Year
  - Engineer: Price_per_unit, Profit_margin, Profit_per_unit
        │
        ▼
[ Exploratory Analysis ]
  - Sales trends by month, category, region
  - Correlation heatmap
  - Top/worst products by revenue and profit
        │
        ▼
[ KMeans Clustering ]
  - Features: Sales, Profit, Quantity, Profit_margin
  - StandardScaler normalization
  - Elbow method → k=3 clusters
  - Product-level cluster assignment
        │
        ▼
  processed_data.csv + product_data.csv  ← outputs
        │
        ▼
[ Streamlit Dashboard ]  ← app.py
  - Filters: Category, Region
  - Tabs: Overview | Product Analysis | Segmentation | Data Table
  - KPI metrics, charts, cluster visualization
```

---

## Dataset

**Source:** Synthetic e-commerce transaction dataset modeled after real-world retail patterns.

| Field | Description |
|---|---|
| `Order Date` | Transaction date (2022–2024) |
| `Product Name` | One of 10 products (Laptop, Camera, Tablet, etc.) |
| `Category` | Electronics, Accessories, Office |
| `Region` | North, East, South, West |
| `Quantity` | Units ordered (1–9) |
| `Sales` | Revenue in USD |
| `Profit` | Profit in USD |

**Engineered Features** (added during preprocessing):
- `Month`, `Year` — extracted from `Order Date`
- `Price_per_unit` — Sales / Quantity
- `Profit_margin` — Profit / Sales
- `Profit_per_unit` — Profit / Quantity
- `Cluster` — KMeans segment label (0, 1, or 2)

**Size:** 3,500 rows × 7 raw columns → 12 columns after feature engineering

---

## Installation & Setup

**Requirements:** Python 3.10+

```bash
# 1. Clone the repository
git clone https://github.com/your-username/amazon-sales-dashboard.git
cd amazon-sales-dashboard

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install streamlit pandas numpy matplotlib seaborn scikit-learn

# 4. Run the preprocessing notebook (generates processed_data.csv and product_data.csv)
jupyter notebook make.ipynb
# Run all cells top to bottom

# 5. Launch the dashboard
streamlit run app.py
```

The app will open at `http://localhost:8501`.

> **Note:** `processed_data.csv` and `product_data.csv` are already included in the repo. You only need to re-run the notebook if you want to modify the preprocessing or clustering logic.

---

## Usage

Once the app is running:

1. **Use the top filters** to select a product category and/or region. All charts and KPI cards update immediately.
2. **Overview tab** — start here for the high-level picture: sales trend, category profit, regional performance, and profit-vs-quantity scatter.
3. **Product Analysis tab** — inspect which products are carrying the most profit and which are underperforming.
4. **Segmentation tab** — view the KMeans cluster scatter plot and cluster summary table to understand product archetypes.
5. **Data Table tab** — raw filtered transaction data and the product-level aggregate table, useful for manual verification.

---

## Results & Insights

**Dataset summary:**
- Total Revenue: **$10,667,881**
- Total Profit: **$1,844,665**
- Average Profit Margin: **~17.3%** across all products and regions
- 3,500 orders across 10 products, 3 categories, 4 regions, 3 years

**KMeans clustering (k=3) — product segments:**

| Cluster | Characteristics | Products |
|---|---|---|
| 0 | High profit, high sales volume | Headphones, Laptop |
| 1 | Mid-tier, consistent margin | Keyboard, Mouse, Printer, Smartphone, Smartwatch, Tablet |
| 2 | Top revenue generators | Camera, Monitor |

**Key observations:**
- Camera and Monitor (Cluster 2) lead in raw sales volume, making them the highest-revenue products
- Headphones and Laptop (Cluster 0) deliver strong profit relative to their volume, indicating healthy margin efficiency
- Tablet has the lowest average profit margin (~17.0%) among all products — a candidate for pricing review
- All four regions show broadly similar profit distributions, suggesting no major regional supply/demand distortions in this dataset
- Profit margin variance across categories is tight (16–18%), meaning category mix has limited impact on overall profitability

---

## Folder Structure

```
amazon-sales-dashboard/
├── app.py                      # Streamlit dashboard
├── make.ipynb                  # Preprocessing + EDA + clustering notebook
├── real.ipynb                  # Additional analysis notebook
├── ecommerce_sales_data.csv    # Raw dataset (3,500 rows)
├── ecommerce_sales.csv         # Smaller sample dataset
├── processed_data.csv          # Cleaned + feature-engineered output
├── product_data.csv            # Product-level aggregates with cluster labels
└── README.md
```

---



## Future Improvements

- **Time-series forecasting** — add a Prophet or ARIMA model to project monthly sales for the next 6–12 months
- **RFM segmentation** — if customer-level data is available, extend clustering to Recency/Frequency/Monetary analysis
- **Profitability alerting** — flag products whose rolling 3-month margin drops below a threshold
- **Export functionality** — add CSV/Excel download buttons for filtered data directly from the dashboard
- **Deployment** — host on Streamlit Community Cloud or containerize with Docker for persistent access
- **Dynamic k selection** — expose a slider in the Segmentation tab to let users interactively change the number of clusters and re-run KMeans in real time

---

## Learning Outcomes

**Technical:**
- End-to-end pandas workflow: ingestion → cleaning → feature engineering → aggregation → export
- Applying `StandardScaler` before KMeans — understanding why unscaled features produce biased clusters
- Using the Elbow method to select k empirically rather than arbitrarily
- Building a multi-tab Streamlit app with `@st.cache_data` to avoid redundant data loads on re-renders
- Structuring a data project cleanly: separating the analysis notebook from the serving layer

**Analytical:**
- Distinguishing between high-revenue and high-margin products — they are not always the same
- Understanding that cluster labels are relative, not absolute; interpretation requires examining cluster centroid values
- Recognizing the limits of product-level clustering with only 10 data points — a larger SKU catalog would yield more statistically stable segments

---

## Author

**[NEHA KANAKI]**
Data Analyst | Python Developer

- GitHub: [@your-username](https://github.com/Neha-0212)
- LinkedIn: [linkedin.com/in/your-profile](https://linkedin.com/in/neha-kanaki)
- Email: nehaakanaki0218@gmail.com

---

## License

This project is licensed under the [MIT License](LICENSE).

```
MIT License

Copyright (c) 2024 [Neha Kanaki]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
