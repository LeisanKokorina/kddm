import pandas as pd
from itertools import combinations


# Loading XLSX file into dictionary
def load_data(file_loc):
    # Initialize dictionary that holds transactions
    # key: index; value: transaction
    transactions = {}
    # Read XLSX file
    data = pd.read_excel(file_loc)

    # Iterate over rows in the table of transactions
    for ind, row in data.iterrows():
        # Get the 'InvoiceNo' and 'Description' columns
        invoice_no = row['InvoiceNo']
        description = row['Description']

        # Check if 'InvoiceNo' starts with 'c' indicating a cancellation
        if not str(invoice_no).startswith('c'):
            # If the invoice number is not a cancellation, add the description to the transaction
            if ind in transactions:
                transactions[ind].append(description)
            else:
                transactions[ind] = [description]

    return transactions


# Find item counts
def frequency(item_lst, transactions, check):
    # Initialize dictionary that holds itemset counts
    # key: itemset; value: count
    item_counts = {}
    # Iterate over all unique itemsets
    for itemset in item_lst:

        # In the first pass, these are 1-itemsets
        if check == False:
            temp_i = {itemset}
        # In later passes, these are k-itemsets
        else:
            temp_i = set(itemset)
        # Iterate over transactions
        for transaction in transactions.values():
            # Check whether the itemset appears in the transaction
            if temp_i.issubset(set(transaction)):
                if itemset in item_counts:
                    # If it appears, increment the counter
                    item_counts[itemset] += 1
                else:
                    # Otherwise, set the counter to 1
                    item_counts[itemset] = 1

    return item_counts


# Calculate support
def get_support(items_counts, transactions):
    # Initialize dictionary that holds support values of all itemsets
    # key: itemset; value: support
    support = {}
    # Number of transactions
    no_trans = len(transactions)
    # Iterate over all unique itemsets
    for itemset in items_counts:
        # Calculate support for the itemset
        support[itemset] = items_counts[itemset] / no_trans

    return support


def main(min_support, file_path):
    # Load dataset
    transactions = load_data(file_path)

    # Create set of unique items over all transactions
    items_lst = set()
    # Iterate over transactions
    for itemset in transactions.values():
        # Iterate over items in the transaction
        for item in itemset:
            items_lst.add(item)

    # Find counts of all 1-itemsets (check=False denotes the first pass)
    items_counts = frequency(items_lst, transactions, check=False)

    # Initialize the list that holds frequent itemsets
    freq_itemsets = list()
    # Find support of all 1-itemsets
    support = get_support(items_counts, transactions).items()
    # Iterate over 1-itemsets
    for j in support:
        # Check whether support is bigger or equal to min support
        if j[1] >= min_support:
            # Add the itemset to frequent itemsets
            freq_itemsets.append({j[0]: j[1]})

    # Find number of items in each transaction
    no_trans = [len(itemset) for itemset in transactions.values()]
    # Repeat for 2+ itemsets
    for k in range(2, max(no_trans) + 1):
        # All combinations of itemsets: k-length tuples, in sorted order, no repeated elements
        item_list = combinations(items_lst, k)
        # Find counts of all k-itemsets (check=True denotes the 2+ pass)
        items_counts = frequency(item_list, transactions, check=True)
        # Find support of all k-itemsets
        support = get_support(items_counts, transactions).items()
        # Iterate over k-itemsets
        for j in support:
            # Check whether support is bigger or equal to min support
            if j[1] >= min_support:
                freq_itemsets.append({j[0]: j[1]})

    return transactions, freq_itemsets


transactions, freq_itemsets = main(0.5, 'cleaned_data.xlsx')
print(transactions)
print(freq_itemsets)

