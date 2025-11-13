import pandas as pd

# Cargar datos
df_sales = pd.read_csv('sales_data.csv')
df_customers = pd.read_csv('customer_data.csv')

# Merge
df = pd.merge(df_sales, df_customers, on='customer_id', how='left')

print(f'Total antes del merge: {len(df)}')
print(f'\nNulos por columna:')
print(df.isnull().sum())

# Limpieza
df_clean = df.dropna(subset=['customer_id', 'price'])

print(f'\nTotal después de limpieza: {len(df_clean)}')
print(f'Registros eliminados: {len(df) - len(df_clean)}')
