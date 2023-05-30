import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import re

# Load the dataset
df = pd.read_excel('cleaned_data_3k.xlsx')

# Preprocess the data
df['InvoiceNo'] = df['InvoiceNo'].astype(str)  # Convert InvoiceNo to string type
df = df[~df['InvoiceNo'].str.startswith('c')]  # Excluding the rows corresponding to cancelled transactions
df['StockCode'] = df['StockCode'].apply(lambda x: re.sub('[^0-9]', '', str(x)))
df = df[df['StockCode'] != '']

# Group data by InvoiceNo and collect StockCodes into lists
grouped = df.groupby('InvoiceNo')['StockCode'].apply(list).reset_index(name='StockCodes')

# Use Apriori algorithm to find frequent itemsets
te = TransactionEncoder()
te_ary = te.fit(grouped['StockCodes']).transform(grouped['StockCodes'])
df_encoded = pd.DataFrame(te_ary, columns=te.columns_)

# Set minimum support threshold
min_support = 0.05  # Adjust as needed

# Run Apriori algorithm
frequent_itemsets = apriori(df_encoded, min_support=min_support, use_colnames=True)

# Sort frequent itemsets by support values in descending order
frequent_itemsets = frequent_itemsets.sort_values(by='support', ascending=False)

# Print the frequent itemsets with their counts
for _, itemset in frequent_itemsets.iterrows():
    stock_codes = ', '.join(itemset['itemsets'])
    support = itemset['support']

    # Calculate the count of the itemset
    count = df_encoded[itemset['itemsets']].all(axis=1).sum()

    print(f"Itemset: {stock_codes}\nSupport: {support}\nCount: {count}\n")