import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os

# Load data
df = pd.read_csv('C:/Users/Aditi Prashant/.cache/kagglehub/datasets/rohitsahoo/sales-forecasting/versions/2/cleaned_data.csv')

# 1. Customer Segmentation Pie Chart
types_of_customers = df['Segment'].unique()
print("The types of customers are:", types_of_customers)

number_of_customers = df['Segment'].value_counts().reset_index()
number_of_customers.columns = ['Segment', 'count']
print("The number of customers in each segment is:\n", number_of_customers)

plt.pie(number_of_customers['count'], labels=number_of_customers['Segment'], autopct='%1.1f%%')
plt.axis('equal')
plt.title('Customer Segmentation')
plt.show()

# 2. Sales by Segment
sales_by_segment = df.groupby('Segment')['Sales'].sum().reset_index()
sales_by_segment = sales_by_segment.rename(columns={'Sales': 'Total Sales by Segment'})
print("The total sales by segment is:\n", sales_by_segment)

plt.bar(sales_by_segment['Segment'], sales_by_segment['Total Sales by Segment'])
plt.xlabel('Type of Customers')
plt.ylabel('Sales per Segment')
plt.title('Sales by Customer Segment')
plt.show()

plt.pie(sales_by_segment['Total Sales by Segment'], labels=sales_by_segment['Segment'], autopct='%1.1f%%')
plt.axis('equal')
plt.title('Sales Distribution by Segment')
plt.show()

# 3. Customer Loyalty (Most Loyal Customers)
customer_order_frequency = df.groupby(['Customer ID', 'Customer Name', 'Segment'])['Order ID'].count().reset_index()
customer_order_frequency = customer_order_frequency.rename(columns={'Order ID': 'Order Frequency'})
repeat_customers = customer_order_frequency[customer_order_frequency['Order Frequency'] > 1]
repeat_customers = repeat_customers.sort_values(by='Order Frequency', ascending=False)
print("The 30 most loyal customers are:\n", repeat_customers.head(30))

customer_sales = df.groupby(['Customer ID', 'Customer Name', 'Segment'])['Sales'].sum().reset_index()
top_spenders = customer_sales.sort_values(by='Sales', ascending=False)
print("The top spenders are:\n", top_spenders.head(30))

# 4. Shipping Method Analysis
shipping_method = df.groupby('Ship Mode').agg({'Order ID': 'count'}).reset_index()
shipping_method = shipping_method.rename(columns={'Order ID': 'Order Frequency', 'Ship Mode': 'Shipping Method'})
print("The shipping method used by each customer is:\n", shipping_method)
plt.pie(shipping_method['Order Frequency'], labels=shipping_method['Shipping Method'], autopct='%1.1f%%')
plt.axis('equal')
plt.title('Shipping Method used by Customer')
plt.show()

# 5. Sales by State and City (Top 20)
state = df.groupby('State')['Sales'].sum().reset_index()
state = state.rename(columns={'Sales': 'Total Sales'})
state_top20 = state.sort_values(by='Total Sales', ascending=False).head(20)
print("The top 20 sales by state is:\n", state_top20)

plt.figure(figsize=(12,6))
plt.bar(state_top20['State'], state_top20['Total Sales'])
plt.xlabel('State')
plt.ylabel('Total Sales')
plt.title('Top 20 Sales by State')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

city = df.groupby('City')['Sales'].sum().reset_index()
city = city.rename(columns={'Sales': 'Total Sales'})
city_top20 = city.sort_values(by='Total Sales', ascending=False).head(20)
print("The top 20 sales by city is:\n", city_top20)

plt.figure(figsize=(14,6))
plt.bar(city_top20['City'], city_top20['Total Sales'])
plt.xlabel('City')
plt.ylabel('Total Sales')
plt.title('Top 20 Sales by City')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# 6. Product Popularity (Top 20)
product = df.groupby('Product Name')['Sales'].count().reset_index()
product = product.rename(columns={'Sales': 'Total Sales'})
product_top20 = product.sort_values(by='Total Sales', ascending=False).head(20)
print("The top 20 popular products are:\n", product_top20)

plt.figure(figsize=(14,6))
plt.bar(product_top20['Product Name'], product_top20['Total Sales'])
plt.xlabel('Product Name')
plt.ylabel('Total Sales')
plt.title('Top 20 Popular Products')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# 7. Unpopular Products (Bottom 20)
unpopular_product = product.sort_values(by='Total Sales', ascending=True).head(20)
print("The top 20 unpopular products are:\n", unpopular_product)

plt.figure(figsize=(14,6))
plt.bar(unpopular_product['Product Name'], unpopular_product['Total Sales'])
plt.xlabel('Product Name')
plt.ylabel('Total Sales')
plt.title('Top 20 Unpopular Products')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# 8. Quarterly Sales by Product
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
df['Quarter'] = df['Order Date'].dt.to_period('Q')
quarterly_sales = df.groupby(['Quarter', 'Product Name'])['Sales'].sum().reset_index()
quarterly_sales = quarterly_sales.rename(columns={'Sales': 'Total Sales'})
print("The quarterly sales by product is:\n", quarterly_sales)
# For visualization, aggregate by quarter
quarterly_total = quarterly_sales.groupby('Quarter')['Total Sales'].sum().reset_index()
plt.plot(quarterly_total['Quarter'].astype(str), quarterly_total['Total Sales'], marker='o')
plt.xlabel('Quarter')
plt.ylabel('Sales')
plt.title('Quarterly Sales (All Products)')
plt.show()

# 9. Annual Sales by Product
df['Year'] = df['Order Date'].dt.year
annual_sales = df.groupby(['Year', 'Product Name'])['Sales'].sum().reset_index()
annual_sales = annual_sales.rename(columns={'Sales': 'Total Sales'})
print("The annual sales by product is:\n", annual_sales)
# For visualization, aggregate by year
annual_total = annual_sales.groupby('Year')['Total Sales'].sum().reset_index()
plt.plot(annual_total['Year'].astype(str), annual_total['Total Sales'])
plt.xlabel('Year')
plt.ylabel('Sales')
plt.title('Annual Sales (All Products)')
plt.show()

# 10. Yearly Revenue by State Map (Requires US states shapefile)
state_yearly_revenue = df.groupby(['Year', 'State'])['Sales'].sum().reset_index()
state_yearly_revenue = state_yearly_revenue.rename(columns={'Sales': 'Total Revenue'})
print("The yearly revenue by state is:\n", state_yearly_revenue)

# Path to the extracted US states shapefile (update this path as needed)
shapefile_path = r"C:\Users\Aditi Prashant\OneDrive\Desktop\DataAnalysis\DataAnalysis\cb_2018_us_state_20m\cb_2018_us_state_20m.shp"

if os.path.exists(shapefile_path):
    states_gdf = gpd.read_file(shapefile_path)
    latest_year = state_yearly_revenue['Year'].max()
    revenue_map = state_yearly_revenue[state_yearly_revenue['Year'] == latest_year]
    merged = states_gdf.merge(revenue_map, left_on='NAME', right_on='State', how='left')

    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    merged.plot(column='Total Revenue', ax=ax, legend=True, cmap='OrRd', missing_kwds={"color": "lightgrey"})
    plt.title(f'Yearly Revenue by State ({latest_year})')
    plt.axis('off')
    ax.set_xlim([-130, -65])  # Longitude range for continental US
    ax.set_ylim([23, 50])     # Latitude range for continental US
    plt.show()
else:
    print("US states shapefile not found. Please download and extract it to your project folder.")
