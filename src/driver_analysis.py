import pandas as pd


def analyze_driver_performance(df):

    print("\n===== DRIVER PERFORMANCE REPORT =====\n")

    drivers = df["DriverName"].unique()

    for driver in drivers:

        driver_data = df[df["DriverName"] == driver]

        total_orders = len(driver_data)

        late_deliveries = 0
        failed_deliveries = 0

        for _, row in driver_data.iterrows():

            if str(row["Status"]).lower() == "failed":
                failed_deliveries += 1

            if not pd.isna(row["ActualTime"]):

                if row["ActualTime"] > row["ExpectedTime"]:
                    late_deliveries += 1

        print(f"Driver: {driver}")
        print(f"Total Orders: {total_orders}")
        print(f"Late Deliveries: {late_deliveries}")
        print(f"Failed Deliveries: {failed_deliveries}")
        print("-" * 30)