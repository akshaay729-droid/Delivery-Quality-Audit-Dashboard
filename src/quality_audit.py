import pandas as pd

def audit_addresses(df):

    address_issues = 0
    coordinate_issues = 0

    print("\n===== ADDRESS AUDIT =====\n")

    for _, row in df.iterrows():

        order_id = row["OrderID"]

        if pd.isna(row["Address"]) or str(row["Address"]).strip().lower() == "missing":
            address_issues += 1
            print(f"[ADDRESS ISSUE] {order_id} -> Missing Address")

        if pd.isna(row["Latitude"]):
            coordinate_issues += 1
            print(f"[COORDINATE ISSUE] {order_id} -> Missing Latitude")

        if pd.isna(row["Longitude"]):
            coordinate_issues += 1
            print(f"[COORDINATE ISSUE] {order_id} -> Missing Longitude")

    print("\n===== QUALITY AUDIT REPORT =====")
    print(f"Total Orders: {len(df)}")
    print(f"Address Issues: {address_issues}")
    print(f"Coordinate Issues: {coordinate_issues}")