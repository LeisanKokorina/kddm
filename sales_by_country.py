import pandas as pd
import plotly.express as px

# Load the dataset
data = pd.read_excel('cleaned_data.xlsx')

# Calculate sales by country
data['Sales'] = data['Quantity'] * data['UnitPrice']
country_sales = data.groupby('Country')['Sales'].sum().sort_values(ascending=False).reset_index()

# Calculate percentage of sales
country_sales['Percentage'] = (country_sales['Sales'] / country_sales['Sales'].sum()) * 100

# Create the percentage plot
fig1 = px.bar(country_sales, x='Country', y='Percentage', color='Country', title='Percentage of Total Sales by Country')
fig1.show()

# Select top 10 countries
top_10_countries = country_sales.head(10)

# Create the pie chart
fig2 = px.pie(top_10_countries, values='Percentage', names='Country', title='Percentage of Total Sales by Country')

# Add percentage labels inside the sectors
fig2.update_traces(textposition='inside', textinfo='percent+label')

fig2.show()






