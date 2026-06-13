import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(
    page_title="Delivery Quality Audit Dashboard",
    layout="wide"
)

st.title("🚚 Delivery Quality Audit Dashboard")

# File Upload
uploaded_file = st.file_uploader(
    "Upload Delivery Dataset",
    type=["xlsx"]
)

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
else:
    df = pd.read_excel("data/delivery_data.xlsx")

    # Filters
st.sidebar.header("Filters")

driver_filter = st.sidebar.selectbox(
    "Select Driver",
    ["All"] + sorted(df["DriverName"].unique().tolist())
)

if driver_filter != "All":
    df = df[df["DriverName"] == driver_filter]

# ==========================
# KPI CALCULATIONS
# ==========================

total_orders = len(df)

late_deliveries = 0

for _, row in df.iterrows():

    if pd.notna(row["ActualTime"]):

        expected = pd.to_datetime(
            row["ExpectedTime"],
            format="%H:%M:%S"
        )

        actual = pd.to_datetime(
            row["ActualTime"],
            format="%H:%M:%S"
        )

        if actual > expected:
            late_deliveries += 1

# Calculate SLA AFTER counting late deliveries
if total_orders > 0:
    sla_compliance = round(
        ((total_orders - late_deliveries) / total_orders) * 100,
        2
    )
else:
    sla_compliance = 0

failed_deliveries = len(
    df[df["Status"] == "Failed"]
)

address_issues = len(
    df[
        (df["Address"].isna()) |
        (df["Address"].astype(str).str.lower() == "missing")
    ]
)

driver_stats = (
    df.groupby("DriverName")
      .size()
      .reset_index(name="TotalOrders")
)

top_driver = driver_stats.loc[
    driver_stats["TotalOrders"].idxmax(),
    "DriverName"
]

worst_driver = driver_stats.loc[
    driver_stats["TotalOrders"].idxmin(),
    "DriverName"
]

# ==========================
# KPI CARDS
# ==========================

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

col1.metric("Total Orders", total_orders)
col2.metric("Late Deliveries", late_deliveries)
col3.metric("Failed Deliveries", failed_deliveries)
col4.metric("Address Issues", address_issues)
col5.metric("Top Driver", top_driver)
col6.metric("Worst Driver", worst_driver)
col7.metric("SLA Compliance", f"{sla_compliance}%")

st.header("📋 Executive Summary")

st.info(
    f"""
    Total Orders Audited: {total_orders}

    Late Deliveries: {late_deliveries}

    Failed Deliveries: {failed_deliveries}

    Address Issues: {address_issues}

    SLA Compliance: {sla_compliance}%
    """
)

st.divider()

# ==========================
# DATASET
# ==========================

st.subheader("Delivery Dataset")
st.dataframe(df)

csv = df.to_csv(index=False)

st.download_button(
    label="📥 Download Audit Report",
    data=csv,
    file_name="delivery_audit_report.csv",
    mime="text/csv"
)

st.divider()

# ==========================
# QUALITY ISSUES CHART
# ==========================

st.subheader("Quality Issues Overview")

issue_data = {
    "Issue Type": [
        "Address",
        "Coordinates",
        "Invalid Latitude",
        "Invalid Longitude",
        "Late Delivery",
        "Failed Delivery"
    ],
    "Count": [1, 2, 1, 1, 5, 1]
}

issue_df = pd.DataFrame(issue_data)

fig1, ax1 = plt.subplots(figsize=(8, 4))

ax1.bar(
    issue_df["Issue Type"],
    issue_df["Count"]
)

ax1.set_title("Delivery Quality Issues")
ax1.set_ylabel("Count")

st.pyplot(fig1)

st.divider()

# ==========================
# DRIVER PERFORMANCE
# ==========================

st.header("Driver Performance")

driver_stats = (
    df.groupby("DriverName")
      .size()
      .reset_index(name="TotalOrders")
)

# Create Driver Chart
fig2, ax2 = plt.subplots(figsize=(8, 4))

ax2.bar(
    driver_stats["DriverName"],
    driver_stats["TotalOrders"]
)

ax2.set_xlabel("Driver")
ax2.set_ylabel("Orders")
ax2.set_title("Orders Handled by Driver")

# Side-by-side layout
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Driver Summary")
    st.dataframe(driver_stats)

with col_right:
    st.subheader("Driver Order Distribution")
    st.pyplot(fig2)

# ==========================
# DRIVER SCORECARD
# ==========================

st.header("Driver Scorecard")

driver_scorecard = []

for driver in df["DriverName"].unique():

    driver_df = df[df["DriverName"] == driver]

    total_orders = len(driver_df)

    failed_orders = len(
        driver_df[
            driver_df["Status"] == "Failed"
        ]
    )

    late_orders = 0

    for _, row in driver_df.iterrows():

        if (
            pd.notna(row["ActualTime"])
            and row["Status"] == "Delivered"
        ):

            expected = pd.to_datetime(
                row["ExpectedTime"],
                format="%H:%M:%S"
            )

            actual = pd.to_datetime(
                row["ActualTime"],
                format="%H:%M:%S"
            )

            if actual > expected:
                late_orders += 1

    score = (
        (
            total_orders
            - late_orders
            - failed_orders
        )
        / total_orders
    ) * 100

    driver_scorecard.append([
        driver,
        total_orders,
        late_orders,
        failed_orders,
        round(score, 2)
    ])

scorecard_df = pd.DataFrame(
    driver_scorecard,
    columns=[
        "Driver",
        "Total Orders",
        "Late Deliveries",
        "Failed Deliveries",
        "Performance Score (%)"
    ]
)

def highlight_score(val):
    if val >= 80:
        return "background-color: green"
    elif val >= 50:
        return "background-color: orange"
    else:
        return "background-color: red"

styled_df = scorecard_df.style.map(
    highlight_score,
    subset=["Performance Score (%)"]
)

st.dataframe(styled_df)

# ==========================
# CITY PERFORMANCE
# ==========================

st.header("City Performance")

city_df = df[
    (df["Address"].notna()) &
    (df["Address"].astype(str).str.lower() != "missing")
]

city_stats = (
    city_df.groupby("Address")
           .size()
           .reset_index(name="Total Orders")
)

st.dataframe(city_stats)

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8,4))

ax.bar(
    city_stats["Address"],
    city_stats["Total Orders"]
)

ax.set_title("Orders by City")
ax.set_xlabel("City")
ax.set_ylabel("Orders")

st.header("Issue Severity Analysis")

severity_df = pd.DataFrame({
    "Severity": ["Critical", "Medium", "Low"],
    "Count": [3, 5, 1]
})

fig, ax = plt.subplots(figsize=(5, 2.8))

bars = ax.barh(
    severity_df["Severity"],
    severity_df["Count"],
    color=["red", "orange", "green"]
)

ax.invert_yaxis()

ax.set_title("Issue Severity Distribution")
ax.set_xlabel("Count")

for bar in bars:
    width = bar.get_width()
    ax.text(
        width + 0.1,
        bar.get_y() + bar.get_height()/2,
        str(int(width)),
        va="center"
    )

plt.tight_layout()

col1, col2 = st.columns([2, 1])

with col1:
    st.pyplot(fig)

with col2:
    st.subheader("Severity Summary")
    st.metric("🔴 Critical Issues", 3)
    st.metric("🟠 Medium Issues", 5)
    st.metric("🟢 Low Issues", 1)

st.divider()

st.header("🔍 Root Cause Analysis")

root_causes = pd.DataFrame({
    "Issue": [
        "Late Deliveries",
        "Address Issues",
        "Failed Deliveries"
    ],
    "Count": [
        late_deliveries,
        address_issues,
        failed_deliveries
    ]
})

st.bar_chart(
    root_causes.set_index("Issue")
)

st.divider()

st.header("🚨 Orders Requiring Attention")

attention_df = df[
    (df["Status"] == "Failed") |
    (df["Address"].astype(str).str.lower() == "missing")
]

col1, col2 = st.columns([1, 4])

with col1:
    st.metric(
        "Flagged Orders",
        len(attention_df)
    )

with col2:
    st.dataframe(
        attention_df,
        use_container_width=True
    )

    st.divider()

st.header("💡 Recommendations")

if late_deliveries > 0:
    st.warning(
        "Investigate route planning and driver scheduling to reduce late deliveries."
    )

if address_issues > 0:
    st.warning(
        "Implement address validation before dispatch."
    )

if failed_deliveries > 0:
    st.warning(
        "Review failed delivery cases and improve customer communication."
    )

if (
    late_deliveries == 0
    and address_issues == 0
    and failed_deliveries == 0
):
    st.success(
        "No major delivery quality issues detected."
    )

st.divider()

st.caption(
    "Delivery Quality Audit Dashboard | Built with Python, Pandas, Streamlit and Matplotlib"
)