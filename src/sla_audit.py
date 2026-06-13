import pandas as pd


def audit_delivery_sla(df):

    late_deliveries = 0
    failed_deliveries = 0
    missing_actual_time = 0

    print("\n===== DELIVERY SLA AUDIT =====\n")

    for _, row in df.iterrows():

        order_id = row["OrderID"]

        expected_time = row["ExpectedTime"]
        actual_time = row["ActualTime"]
        status = row["Status"]

        # Missing delivery time
        if pd.isna(actual_time):
            missing_actual_time += 1
            print(f"[MISSING TIME] {order_id} -> Actual delivery time missing")

        # Failed delivery
        if str(status).lower() == "failed":
            failed_deliveries += 1
            print(f"[FAILED DELIVERY] {order_id}")

        # Late delivery
        if not pd.isna(actual_time):

            if actual_time > expected_time:
                late_deliveries += 1
                print(f"[LATE DELIVERY] {order_id}")

    print("\n===== SLA REPORT =====")

    print(f"Late Deliveries: {late_deliveries}")
    print(f"Failed Deliveries: {failed_deliveries}")
    print(f"Missing Actual Time: {missing_actual_time}")

    return {
        "late_deliveries": late_deliveries,
        "failed_deliveries": failed_deliveries,
        "missing_actual_time": missing_actual_time
    }