import pandas as pd

def validate_schema(df, required_columns):
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        return {"status": "blocked_schema", "row_count": len(df), "missing_columns": missing}
    return {"status": "validated", "row_count": len(df), "missing_columns": []}

def clean_data():
    df = pd.read_csv("pharmeasy_orders_raw.csv")
    
    # 1. Remove exact duplicates
    initial_len = len(df)
    df = df.drop_duplicates()
    print(f"Removed {initial_len - len(df)} exact-duplicate rows.")

    # 2. Normalize region text
    df['region'] = df['region'].str.strip().str.title()

    # 3. Impute missing category mapping from product
    prod_cat_map = df.dropna(subset=['category']).set_index('product')['category'].to_dict()
    df['category'] = df['category'].fillna(df['product'].map(prod_cat_map))

    # 4. Impute missing profit_inr based on category mean margin
    # Convert empty strings to NaN first if they exist
    df['profit_inr'] = pd.to_numeric(df['profit_inr'], errors='coerce')
    df_valid = df.dropna(subset=['profit_inr'])
    cat_margins = (df_valid['profit_inr'] / df_valid['sales_inr']).groupby(df_valid['category']).mean()
    
    def impute_profit(row):
        if pd.isna(row['profit_inr']):
            return round(row['sales_inr'] * cat_margins[row['category']], 2)
        return row['profit_inr']
    
    df['profit_inr'] = df.apply(impute_profit, axis=1)
    
    df.to_csv("orders_clean.csv", index=False)
    return df

if __name__ == "__main__":
    df_clean = clean_data()
    req_cols = ["order_id", "order_date", "region", "category", "product", "quantity", "sales_inr", "profit_inr"]
    
    print("Clean Data:", validate_schema(df_clean, req_cols))
    
    # Broken copy test
    df_broken = df_clean.drop(columns=['profit_inr'])
    print("Broken Data:", validate_schema(df_broken, req_cols))