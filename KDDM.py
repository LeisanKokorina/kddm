#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


excel_file = 'OnlineRetail.xlsx'
data = pd.read_excel(excel_file)
data.info()


# In[3]:


from apyori import apriori


# In[4]:


data = data.dropna()
data.info


# In[5]:


transactions = data.groupby(['InvoiceNo'])['Description'].apply(list).values.tolist()


# In[11]:


transactions[0:10]


# In[12]:


rules = apriori(transactions, min_support = 0.003, min_confidence = 0.2, min_lift = 3, min_length = 2)


# In[13]:


association_rules = list(rules)


# In[15]:


# Convert rules into a list of dictionaries to facilitate sorting
rules_list = []
seen_rules = set()  # This set will store seen rules

for item in association_rules:
    # first index of the inner list
    # Contains base item and add item
    pair = item[0] 
    items = [x for x in pair]

    # Create a tuple representing the rule, ensuring the items are always in the same order
    rule_tuple = tuple(sorted(items))

    # Skip this rule if we've already seen it
    if rule_tuple in seen_rules:
        continue

    # Otherwise, remember this rule and proceed with adding it to the list
    seen_rules.add(rule_tuple)

    rule_dict = {'Rule': items[0] + " -> " + items[1],
                 'Support': item[1],
                 'Confidence': item[2][0][2],
                 'Lift': item[2][0][3]}

    rules_list.append(rule_dict)

# Now proceed as before, sorting and printing the rules
rules_list.sort(key=lambda x: x['Support'], reverse=True)

# Print top 50 rules
for i, rule in enumerate(rules_list[:50]):
    print(f"Rule {i+1}: {rule['Rule']}")
    print(f"Support: {rule['Support']}")
    print(f"Confidence: {rule['Confidence']}")
    print(f"Lift: {rule['Lift']}")
    print("=====================================")




