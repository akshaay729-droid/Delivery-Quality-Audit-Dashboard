import pandas as pd


def analyze_routes(df):

    print("\n===== CITY / ROUTE PERFORMANCE REPORT =====\n")

    cities = df["Address"].dropna().unique()

    for city in cities:

        if str(city).lower() == "missing":
            continue

        city_data = df[df["Address"] == city]

        total_orders = len(city_data)

        late_deliveries = 0
        failed_deliveries = 0

        for _, row in city_data.iterrows():

            if str(row["Status"]).lower() == "failed":
                failed_deliveries += 1

            if not pd.isna(row["ActualTime"]):

                if row["ActualTime"] > row["ExpectedTime"]:
                    late_deliveries += 1

        print(f"City: {city}")
        print(f"Total Orders: {total_orders}")
        print(f"Late Deliveries: {late_deliveries}")
        print(f"Failed Deliveries: {failed_deliveries}")
        print("-" * 30)