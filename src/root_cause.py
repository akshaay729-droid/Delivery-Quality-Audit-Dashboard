import pandas as pd


def root_cause_analysis(df):

    issue_counts = {
        "Address Issues": 0,
        "Coordinate Issues": 0,
        "Invalid Latitudes": 0,
        "Invalid Longitudes": 0,
        "Late Deliveries": 0,
        "Failed Deliveries": 0
    }

    for _, row in df.iterrows():

        # Address Issues
        if pd.isna(row["Address"]) or str(row["Address"]).strip().lower() == "missing":
            issue_counts["Address Issues"] += 1

        # Coordinate Issues
        if pd.isna(row["Latitude"]):
            issue_counts["Coordinate Issues"] += 1

        if pd.isna(row["Longitude"]):
            issue_counts["Coordinate Issues"] += 1

        # Invalid Latitude
        if not pd.isna(row["Latitude"]):
            if row["Latitude"] < -90 or row["Latitude"] > 90:
                issue_counts["Invalid Latitudes"] += 1

        # Invalid Longitude
        if not pd.isna(row["Longitude"]):
            if row["Longitude"] < -180 or row["Longitude"] > 180:
                issue_counts["Invalid Longitudes"] += 1

        # Failed Deliveries
        if str(row["Status"]).lower() == "failed":
            issue_counts["Failed Deliveries"] += 1

        # Late Deliveries
        if not pd.isna(row["ActualTime"]):
            if row["ActualTime"] > row["ExpectedTime"]:
                issue_counts["Late Deliveries"] += 1

    total_issues = sum(issue_counts.values())

    print("\n===== ROOT CAUSE ANALYSIS =====\n")

    for issue, count in issue_counts.items():

        percentage = (
            (count / total_issues) * 100
            if total_issues > 0 else 0
        )

        print(f"{issue}: {count} ({percentage:.2f}%)")

    return issue_counts