import pandas as pd

# Specify the path to your Excel file
excel_file = 'Online_Retail.xlsx'

# Read the Excel file into a pandas DataFrame
data = pd.read_excel(excel_file)

# Convert 'InvoiceDate' column to string
data['InvoiceDate'] = data['InvoiceDate'].astype(str)

# Split 'InvoiceDate' column into 'InvoiceDate' and 'InvoiceTime' columns
data[['InvoiceDate', 'InvoiceTime']] = data['InvoiceDate'].str.split(pat=' ', n=1, expand=True)

# Move 'InvoiceTime' column right after 'InvoiceDate'
data.insert(data.columns.get_loc('InvoiceDate') + 1, 'InvoiceTime', data.pop('InvoiceTime'))

# Remove data without CustomerID
data = data[~(data.CustomerID.isnull())]

# Fill empty cells in Description column based on StockCode
data['Description'] = data.groupby('StockCode')['Description'].transform(
    lambda x: x.fillna(x.mode().iloc[0]) if not x.mode().empty else '')

# Drop rows with blank Description
data = data[data['Description'] != '']

# Trim values in Description column
data['Description'] = data['Description'].str.strip(' ,.')

# Remove extra whitespace in the "Description" column
data['Description'] = data['Description'].str.replace(r'\s+', ' ', regex=True)

# Convert 'InvoiceNo' column to string
data['InvoiceNo'] = data['InvoiceNo'].astype('str')

# Remove rows with InvoiceNo starting with 'C' (indicating cancellations)
data = data[~data['InvoiceNo'].str.contains('C')]

# Remove rows with negative or equal to 0 UnitPrice
data = data[~(data["UnitPrice"] <= 0)]

# Remove rows with negative Quantity
data = data[~(data["Quantity"] < 0)]

# Save the updated DataFrame to a new Excel file
data.to_excel('cleaned_data.xlsx', index=False)
