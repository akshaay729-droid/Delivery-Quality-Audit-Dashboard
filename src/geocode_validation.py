import pandas as pd


def validate_geocodes(df):

    invalid_latitudes = 0
    invalid_longitudes = 0

    print("\n===== GEOCODE VALIDATION =====\n")

    for _, row in df.iterrows():

        order_id = row["OrderID"]

        latitude = row["Latitude"]
        longitude = row["Longitude"]

        if not pd.isna(latitude):

            if latitude < -90 or latitude > 90:
                invalid_latitudes += 1
                print(f"[INVALID LATITUDE] {order_id} -> {latitude}")

        if not pd.isna(longitude):

            if longitude < -180 or longitude > 180:
                invalid_longitudes += 1
                print(f"[INVALID LONGITUDE] {order_id} -> {longitude}")

    print("\n===== GEOCODE REPORT =====")
    print(f"Invalid Latitudes: {invalid_latitudes}")
    print(f"Invalid Longitudes: {invalid_longitudes}")

    return {
        "invalid_latitudes": invalid_latitudes,
        "invalid_longitudes": invalid_longitudes
    }