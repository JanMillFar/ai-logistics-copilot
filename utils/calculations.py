import pandas as pd


def calculate_inventory_value(df):
    return (df["Stock"] * df["Price"]).sum()


def calculate_days_left(df):

    return df.apply(
        lambda row:
        row["Stock"] / row["DailySales"]
        if row["DailySales"] > 0
        else 999,
        axis=1
    ).round(1)