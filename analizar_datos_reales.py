import pandas as pd

# Cargar datos
df_c = pd.read_csv('customer_data.csv')
df_s = pd.read_csv('sales_data.csv')
df = pd.merge(df_s, df_c, on='customer_id', how='left')

# Limpiar datos de edad
df = df.dropna(subset=['age'])
df['total_sale'] = df['quantity'] * df['price']

print('=' * 80)
print('ANALISIS DE DATOS REALES - DATASET ESTAMBUL')
print('=' * 80)

print(f'\nTotal de registros validos: {len(df):,}')

print('\n--- METODOS DE PAGO ---')
payment = df['payment_method'].value_counts()
for method, count in payment.items():
    pct = (count / len(df)) * 100
    print(f'{method}: {count:,} ({pct:.1f}%)')

print('\n--- DISTRIBUCION POR GENERO ---')
gender = df['gender'].value_counts()
for gen, count in gender.items():
    pct = (count / len(df)) * 100
    print(f'{gen}: {count:,} ({pct:.1f}%)')

print('\n--- RANGO DE EDAD 25-35 AÑOS ---')
df_25_35 = df[(df['age'] >= 25) & (df['age'] <= 35)]
print(f'Transacciones: {len(df_25_35):,} ({len(df_25_35)/len(df)*100:.1f}% del total)')
payment_25_35 = df_25_35['payment_method'].value_counts()
print('Metodos de pago:')
for method, count in payment_25_35.items():
    print(f'  {method}: {count:,}')

print('\n--- METODOS DE PAGO - MUJERES ---')
df_female = df[df['gender'] == 'Female']
print(f'Transacciones de mujeres: {len(df_female):,}')
payment_female = df_female['payment_method'].value_counts()
for method, count in payment_female.items():
    pct = (count / len(df_female)) * 100
    print(f'{method}: {count:,} ({pct:.1f}%)')

print('\n--- TOP 5 CATEGORIAS POR VENTAS ---')
cat_sales = df.groupby('category')['total_sale'].sum().sort_values(ascending=False).head()
for cat, sales in cat_sales.items():
    print(f'{cat}: ${sales:,.2f}')

print('\n--- PRECIO PROMEDIO POR CATEGORIA ---')
cat_price = df.groupby('category')['price'].mean().sort_values(ascending=False)
for cat, price in cat_price.items():
    print(f'{cat}: ${price:.2f}')

print('\n--- ESTADISTICAS DE EDAD ---')
print(f'Edad promedio: {df["age"].mean():.1f} años')
print(f'Edad minima: {df["age"].min():.0f} años')
print(f'Edad maxima: {df["age"].max():.0f} años')
print(f'Mediana: {df["age"].median():.0f} años')

print('\n' + '=' * 80)
