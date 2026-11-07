from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ==================================================
# CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Enterprise Scraper | Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "scraper" / "data"


# ==================================================
# CUSTOM STYLING
# ==================================================

st.markdown("""
<style>

.stApp {
    background-color: #0e1117;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

[data-testid="stSidebar"] {
    background-color: #161b25;
}

[data-testid="stMetric"] {
    background-color: #1b2331;
    padding: 18px;
    border-radius: 10px;
    border: 1px solid #293548;
}

[data-testid="stMetricLabel"] {
    color: #aab7c9;
}

[data-testid="stMetricValue"] {
    color: #ffffff;
}

h1, h2, h3 {
    color: #ffffff;
}

p {
    color: #b8c4d6;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# DATA LOADING
# ==================================================

@st.cache_data(ttl=60)
def load_csv(filename):

    filepath = DATA_DIR / filename

    if not filepath.exists() or filepath.stat().st_size == 0:
        return pd.DataFrame()

    try:
        return pd.read_csv(filepath)

    except (pd.errors.EmptyDataError, pd.errors.ParserError):
        return pd.DataFrame()


products = load_csv("products.csv")
history = load_csv("price_history.csv")
price_drops = load_csv("price_drops.csv")
price_increases = load_csv("price_increases.csv")
top_drops = load_csv("top_price_drops.csv")


# ==================================================
# DATA PREPARATION
# ==================================================

if not products.empty:

    products["Price (USD)"] = pd.to_numeric(
        products["Price (USD)"],
        errors="coerce"
    )

if not history.empty:

    history["price_usd"] = pd.to_numeric(
        history["price_usd"],
        errors="coerce"
    )

    history["scraped_at"] = pd.to_datetime(
        history["scraped_at"],
        errors="coerce"
    )


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("📊 Enterprise Scraper")

    st.caption("Product Intelligence Platform")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Overview",
            "Price Analytics",
            "Product Catalog",
            "Price Alerts"
        ]
    )

    st.divider()

    st.markdown("### System Information")

    st.write("**Data Source:** CSV")

    st.write("**Currency:** USD")

    st.write("**Products:**", len(products))

    st.write("**Platform:** Streamlit")

    st.divider()

    st.caption("Enterprise Scraper v2.0")


# ==================================================
# DATA VALIDATION
# ==================================================

if products.empty:

    st.error(
        "Product data is unavailable. "
        "Run the scraper to generate products.csv."
    )

    st.stop()


required_columns = [
    "Product Name",
    "Price (USD)",
    "Product URL"
]

missing_columns = [
    column for column in required_columns
    if column not in products.columns
]

if missing_columns:

    st.error(f"Missing columns: {missing_columns}")

    st.stop()


valid_prices = products["Price (USD)"].dropna()

if valid_prices.empty:

    st.error("No valid product prices are available.")

    st.stop()


# ==================================================
# HEADER
# ==================================================

st.title("Enterprise Product Intelligence")

st.markdown(
    "Automated product monitoring, pricing intelligence, "
    "and historical market analysis."
)

st.divider()


# ==================================================
# OVERVIEW PAGE
# ==================================================

if page == "Overview":

    st.subheader("Business Overview")

    total_products = len(products)

    average_price = valid_prices.mean()

    lowest_price = valid_prices.min()

    highest_price = valid_prices.max()

    total_drops = len(price_drops)

    total_increases = len(price_increases)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Products Monitored",
        f"{total_products:,}"
    )

    col2.metric(
        "Average Product Price",
        f"${average_price:,.2f}"
    )

    col3.metric(
        "Highest Product Price",
        f"${highest_price:,.2f}"
    )

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "Lowest Product Price",
        f"${lowest_price:,.2f}"
    )

    col5.metric(
        "Price Drops",
        total_drops
    )

    col6.metric(
        "Price Increases",
        total_increases
    )

    st.divider()

    st.subheader("Product Price Distribution")

    fig = px.histogram(
        products,
        x="Price (USD)",
        nbins=25,
        title="Distribution of Product Prices",
        labels={
            "Price (USD)": "Price in USD"
        }
    )

    fig.update_layout(
        template="plotly_dark",
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Most Expensive Products")

    expensive = products.nlargest(
        10,
        "Price (USD)"
    )

    st.dataframe(
        expensive[
            ["Product Name", "Price (USD)", "Product URL"]
        ],
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# PRICE ANALYTICS PAGE
# ==================================================

elif page == "Price Analytics":

    st.subheader("Historical Price Analytics")

    if history.empty:

        st.info("Historical price data is not available yet.")

    else:

        history = history.dropna(
            subset=["scraped_at", "price_usd"]
        )

        if history.empty:

            st.info("No valid historical records found.")

        else:

            if "product_url" in history.columns:

                product_options = (
                    history[["product_name", "product_url"]]
                    .dropna()
                    .drop_duplicates()
                    .sort_values("product_name")
                )

                selected_product = st.selectbox(
                    "Select a product",
                    product_options["product_name"].tolist()
                )

                selected_url = product_options.loc[
                    product_options["product_name"] == selected_product,
                    "product_url"
                ].iloc[0]

                selected_history = history[
                    history["product_url"] == selected_url
                ].sort_values("scraped_at")

            else:

                product_options = sorted(
                    history["product_name"].dropna().unique()
                )

                selected_product = st.selectbox(
                    "Select a product",
                    product_options
                )

                selected_history = history[
                    history["product_name"] == selected_product
                ].sort_values("scraped_at")

            fig = px.line(
                selected_history,
                x="scraped_at",
                y="price_usd",
                markers=True,
                title=f"Price History: {selected_product}",
                labels={
                    "scraped_at": "Date",
                    "price_usd": "Price (USD)"
                }
            )

            fig.update_layout(
                template="plotly_dark",
                hovermode="x unified"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.metric(
                "Recorded Price Points",
                len(selected_history)
            )


# ==================================================
# PRODUCT CATALOG PAGE
# ==================================================

elif page == "Product Catalog":

    st.subheader("Product Catalog")

    search = st.text_input(
        "Search product catalog",
        placeholder="Enter product name..."
    )

    filtered = products.copy()

    if search:

        filtered = filtered[
            filtered["Product Name"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    min_price = float(valid_prices.min())

    max_price = float(valid_prices.max())

    if min_price < max_price:

        price_range = st.slider(
            "Price Range",
            min_value=min_price,
            max_value=max_price,
            value=(min_price, max_price)
        )

        filtered = filtered[
            filtered["Price (USD)"].between(
                price_range[0],
                price_range[1]
            )
        ]

    st.write(
        f"Displaying {len(filtered):,} products."
    )

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Product URL": st.column_config.LinkColumn(
                "Product Link",
                display_text="View Product"
            ),
            "Price (USD)": st.column_config.NumberColumn(
                "Price (USD)",
                format="$%.2f"
            )
        }
    )


# ==================================================
# PRICE ALERTS PAGE
# ==================================================

elif page == "Price Alerts":

    st.subheader("Price Monitoring Alerts")

    left, right = st.columns(2)

    with left:

        st.markdown("### 📉 Price Drops")

        if not price_drops.empty:

            st.dataframe(
                price_drops,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.success("No price drops detected.")

    with right:

        st.markdown("### 📈 Price Increases")

        if not price_increases.empty:

            st.dataframe(
                price_increases,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info("No price increases detected.")

    st.divider()

    st.subheader("Largest Price Drops")

    if not top_drops.empty:

        st.dataframe(
            top_drops,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No top price-drop records available.")


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "Enterprise Scraper | Product Intelligence "
    "and Automated Price Monitoring"
)