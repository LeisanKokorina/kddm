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

# Find the maximum CustomerID
max_customer_id = data['CustomerID'].max()

# Create a dictionary to store the mapping of unique InvoiceNo to a new CustomerID
unique_invoice_mapping = {}

# Generate unique CustomerIDs for missing values based on unique InvoiceNo
current_customer_id = max_customer_id + 1
for index, row in data.iterrows():
    invoice_no = row['InvoiceNo']
    customer_id = row['CustomerID']
    if pd.isnull(customer_id):
        if invoice_no not in unique_invoice_mapping:
            unique_invoice_mapping[invoice_no] = current_customer_id
            current_customer_id += 1

# Update the CustomerID column with the new unique CustomerIDs
data['CustomerID'] = data.apply(lambda row: unique_invoice_mapping[row['InvoiceNo']]
if pd.isnull(row['CustomerID']) else row['CustomerID'], axis=1)

# Fill empty cells in Description column based on StockCode
data['Description'] = data.groupby('StockCode')['Description'].transform(
    lambda x: x.fillna(x.mode().iloc[0]) if not x.mode().empty else '')

# Trim values in Description column
data['Description'] = data['Description'].str.strip(' ,.')

# Remove extra whitespace in the "Description" column
data['Description'] = data['Description'].str.replace(r'\s+', ' ', regex=True)

# Find duplicate rows based on all columns except "Quantity"
duplicate_rows = data.duplicated(subset=data.columns.difference(['Quantity']), keep='first')

# Update the "Quantity" column for unique rows by summing the values
data['Quantity'] = data.groupby(data.columns.tolist()[:-1])['Quantity'].transform('sum')

# Remove the duplicate rows
data = data[~duplicate_rows]

# Save the updated DataFrame to a new Excel file
data.to_excel('cleaned_data.xlsx', index=False)
