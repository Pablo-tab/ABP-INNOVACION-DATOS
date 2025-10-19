import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos
df_c = pd.read_csv('customer_data.csv')
df_s = pd.read_csv('sales_data.csv')
df = pd.merge(df_s, df_c, on='customer_id', how='left')

# Limpiar datos
df = df.dropna(subset=['age'])
df['total_sale'] = df['quantity'] * df['price']
df['invoice_date'] = pd.to_datetime(df['invoice_date'], format='%d-%m-%Y')
df['year'] = df['invoice_date'].dt.year
df['month'] = df['invoice_date'].dt.month
df['year_month'] = df['invoice_date'].dt.to_period('M')

print('=' * 100)
print('ANALISIS DETALLADO DE EVOLUCION DE MEDIOS DE PAGO')
print('=' * 100)

# 1. EVOLUCION TEMPORAL
print('\n1. EVOLUCION MENSUAL DE MEDIOS DE PAGO')
print('-' * 100)
monthly_payment = df.groupby(['year_month', 'payment_method']).size().unstack(fill_value=0)
print(monthly_payment)

# 2. EVOLUCION ANUAL
print('\n2. EVOLUCION ANUAL DE MEDIOS DE PAGO')
print('-' * 100)
yearly_payment = df.groupby(['year', 'payment_method']).agg({
    'invoice_no': 'count',
    'total_sale': 'sum'
}).round(2)
print(yearly_payment)

# 3. PORCENTAJES POR AÑO
print('\n3. PORCENTAJE DE USO POR AÑO')
print('-' * 100)
for year in sorted(df['year'].unique()):
    print(f'\nAÑO {year}:')
    year_data = df[df['year'] == year]
    payment_counts = year_data['payment_method'].value_counts()
    for method, count in payment_counts.items():
        pct = (count / len(year_data)) * 100
        print(f'  {method}: {count:,} transacciones ({pct:.1f}%)')

# 4. TENDENCIAS DE CRECIMIENTO
print('\n4. ANALISIS DE TENDENCIAS (Cambio año a año)')
print('-' * 100)
years = sorted(df['year'].unique())
for i in range(1, len(years)):
    prev_year = years[i-1]
    curr_year = years[i]
    
    print(f'\nCAMBIO DE {prev_year} A {curr_year}:')
    
    prev_data = df[df['year'] == prev_year]['payment_method'].value_counts()
    curr_data = df[df['year'] == curr_year]['payment_method'].value_counts()
    
    for method in ['Cash', 'Credit Card', 'Debit Card']:
        prev_count = prev_data.get(method, 0)
        curr_count = curr_data.get(method, 0)
        
        if prev_count > 0:
            change_pct = ((curr_count - prev_count) / prev_count) * 100
            change_abs = curr_count - prev_count
            direction = 'AUMENTO' if change_abs > 0 else 'DISMINUCION'
            print(f'  {method}:')
            print(f'    {prev_year}: {prev_count:,} | {curr_year}: {curr_count:,}')
            print(f'    Cambio: {change_abs:+,} transacciones ({change_pct:+.1f}%) - {direction}')

# 5. ANALISIS POR CATEGORIA Y METODO DE PAGO
print('\n5. METODO DE PAGO PREFERIDO POR CATEGORIA DE PRODUCTO')
print('-' * 100)
for category in sorted(df['category'].unique()):
    cat_data = df[df['category'] == category]
    most_used = cat_data['payment_method'].value_counts()
    print(f'\n{category}:')
    for method, count in most_used.items():
        pct = (count / len(cat_data)) * 100
        print(f'  {method}: {count:,} ({pct:.1f}%)')

# 6. ANALISIS POR RANGO DE PRECIO
print('\n6. METODO DE PAGO POR RANGO DE VALOR DE COMPRA')
print('-' * 100)
df['price_range'] = pd.cut(df['total_sale'], 
                            bins=[0, 100, 500, 1000, 5000, float('inf')],
                            labels=['< $100', '$100-500', '$500-1000', '$1000-5000', '> $5000'])

for range_label in df['price_range'].cat.categories:
    range_data = df[df['price_range'] == range_label]
    if len(range_data) > 0:
        print(f'\n{range_label}:')
        payment_dist = range_data['payment_method'].value_counts()
        for method, count in payment_dist.items():
            pct = (count / len(range_data)) * 100
            avg_sale = range_data[range_data['payment_method'] == method]['total_sale'].mean()
            print(f'  {method}: {count:,} transacciones ({pct:.1f}%) - Ticket promedio: ${avg_sale:.2f}')

# 7. METODO DE PAGO POR SHOPPING MALL
print('\n7. TOP 5 SHOPPING MALLS - DISTRIBUCION DE METODOS DE PAGO')
print('-' * 100)
top_malls = df['shopping_mall'].value_counts().head(5).index

for mall in top_malls:
    mall_data = df[df['shopping_mall'] == mall]
    print(f'\n{mall} ({len(mall_data):,} transacciones):')
    payment_dist = mall_data['payment_method'].value_counts()
    for method, count in payment_dist.items():
        pct = (count / len(mall_data)) * 100
        print(f'  {method}: {count:,} ({pct:.1f}%)')

# 8. PATRON POR DIA DE LA SEMANA
print('\n8. METODO DE PAGO POR DIA DE LA SEMANA')
print('-' * 100)
df['day_of_week'] = df['invoice_date'].dt.day_name()
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

for day in day_order:
    day_data = df[df['day_of_week'] == day]
    if len(day_data) > 0:
        most_used = day_data['payment_method'].value_counts().iloc[0]
        most_used_name = day_data['payment_method'].value_counts().index[0]
        pct = (most_used / len(day_data)) * 100
        print(f'{day}: {most_used_name} dominante ({most_used:,} transacciones, {pct:.1f}%)')

# 9. INSIGHTS CLAVE
print('\n' + '=' * 100)
print('INSIGHTS CLAVE - MEDIOS DE PAGO')
print('=' * 100)

# Metodo mas usado globalmente
overall_most = df['payment_method'].value_counts()
print(f'\n1. DOMINANCIA GLOBAL:')
print(f'   {overall_most.index[0]} es el metodo MAS usado: {overall_most.iloc[0]:,} ({overall_most.iloc[0]/len(df)*100:.1f}%)')

# Tendencia en compras de alto valor
high_value = df[df['total_sale'] > 1000]
high_most = high_value['payment_method'].value_counts()
print(f'\n2. COMPRAS DE ALTO VALOR (> $1000):')
print(f'   {high_most.index[0]} domina: {high_most.iloc[0]:,} ({high_most.iloc[0]/len(high_value)*100:.1f}%)')

# Metodo con mayor ticket promedio
avg_by_method = df.groupby('payment_method')['total_sale'].mean().sort_values(ascending=False)
print(f'\n3. TICKET PROMEDIO POR METODO:')
for method, avg in avg_by_method.items():
    print(f'   {method}: ${avg:.2f}')

# Crecimiento año a año
if len(years) > 1:
    first_year = years[0]
    last_year = years[-1]
    
    print(f'\n4. CAMBIO TOTAL ({first_year} -> {last_year}):')
    
    first_data = df[df['year'] == first_year]['payment_method'].value_counts()
    last_data = df[df['year'] == last_year]['payment_method'].value_counts()
    
    for method in ['Cash', 'Credit Card', 'Debit Card']:
        first_count = first_data.get(method, 0)
        last_count = last_data.get(method, 0)
        
        if first_count > 0:
            change_pct = ((last_count - first_count) / first_count) * 100
            print(f'   {method}: {change_pct:+.1f}% de cambio')

print('\n' + '=' * 100)

# CREAR GRAFICOS
print('\nGenerando graficos de evolucion...')

# Grafico 1: Evolucion mensual
plt.figure(figsize=(14, 6))
monthly_payment_pct = monthly_payment.div(monthly_payment.sum(axis=1), axis=0) * 100
monthly_payment_pct.plot(kind='line', marker='o', linewidth=2)
plt.title('Evolucion Mensual de Metodos de Pago (%)', fontsize=14, fontweight='bold')
plt.xlabel('Periodo')
plt.ylabel('Porcentaje (%)')
plt.legend(title='Metodo de Pago')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('visualizaciones/evolucion_mensual_pagos.png', dpi=300, bbox_inches='tight')
print('Guardado: evolucion_mensual_pagos.png')
plt.close()

# Grafico 2: Comparacion anual
fig, axes = plt.subplots(1, len(years), figsize=(15, 5))
if len(years) == 1:
    axes = [axes]

for idx, year in enumerate(years):
    year_data = df[df['year'] == year]['payment_method'].value_counts()
    axes[idx].pie(year_data.values, labels=year_data.index, autopct='%1.1f%%', startangle=90)
    axes[idx].set_title(f'Año {year}', fontweight='bold')

plt.tight_layout()
plt.savefig('visualizaciones/comparacion_anual_pagos.png', dpi=300, bbox_inches='tight')
print('Guardado: comparacion_anual_pagos.png')
plt.close()

# Grafico 3: Por rango de precio
plt.figure(figsize=(12, 6))
price_payment = pd.crosstab(df['price_range'], df['payment_method'], normalize='index') * 100
price_payment.plot(kind='bar', stacked=True)
plt.title('Metodos de Pago por Rango de Precio (%)', fontsize=14, fontweight='bold')
plt.xlabel('Rango de Precio')
plt.ylabel('Porcentaje (%)')
plt.legend(title='Metodo de Pago')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('visualizaciones/pago_por_rango_precio.png', dpi=300, bbox_inches='tight')
print('Guardado: pago_por_rango_precio.png')
plt.close()

print('\nAnalisis completo!')
