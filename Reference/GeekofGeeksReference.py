#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules


# In[2]:


# Loading the Data
data = pd.read_excel('OnlineRetail.xlsx')
data.head()


# In[3]:


data.columns


# In[4]:


# Exploring the different regions of transactions
data.Country.unique()


# In[5]:


# Stripping extra spaces in the description
data['Description'] = data['Description'].str.strip()

# Dropping the rows without any invoice number
data.dropna(axis = 0, subset =['InvoiceNo'], inplace = True)
data['InvoiceNo'] = data['InvoiceNo'].astype('str')

# Dropping all transactions which were done on credit
data = data[~data['InvoiceNo'].str.contains('C')]


# In[6]:


# Transactions done in France
basket_France = (data[data['Country'] =="France"]
		.groupby(['InvoiceNo', 'Description'])['Quantity']
		.sum().unstack().reset_index().fillna(0)
		.set_index('InvoiceNo'))

# Transactions done in the United Kingdom
basket_UK = (data[data['Country'] =="United Kingdom"]
		.groupby(['InvoiceNo', 'Description'])['Quantity']
		.sum().unstack().reset_index().fillna(0)
		.set_index('InvoiceNo'))

# Transactions done in Portugal
basket_Por = (data[data['Country'] =="Portugal"]
		.groupby(['InvoiceNo', 'Description'])['Quantity']
		.sum().unstack().reset_index().fillna(0)
		.set_index('InvoiceNo'))

basket_Sweden = (data[data['Country'] =="Sweden"]
		.groupby(['InvoiceNo', 'Description'])['Quantity']
		.sum().unstack().reset_index().fillna(0)
		.set_index('InvoiceNo'))


# In[7]:


# Defining the hot encoding function to make the data suitable
# for the concerned libraries
def hot_encode(x):
	if(x<= 0):
		return 0
	if(x>= 1):
		return 1

# Encoding the datasets
basket_encoded = basket_France.applymap(hot_encode)
basket_France = basket_encoded
basket_France = basket_France.applymap(lambda x: True if x else False)

basket_encoded = basket_UK.applymap(hot_encode)
basket_UK = basket_encoded
basket_UK = basket_UK.applymap(lambda x: True if x else False)

basket_encoded = basket_Por.applymap(hot_encode)
basket_Por = basket_encoded
basket_Por = basket_Por.applymap(lambda x: True if x else False)

basket_encoded = basket_Sweden.applymap(hot_encode)
basket_Sweden = basket_encoded
basket_Sweden = basket_Sweden.applymap(lambda x: True if x else False)


# In[8]:


# Building the model
frq_items = apriori(basket_France, min_support = 0.05, use_colnames = True)

# Collecting the inferred rules in a dataframe
rules = association_rules(frq_items, metric ="lift", min_threshold = 1)
rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False])
print(rules.head())


# In[9]:


frq_items = apriori(basket_UK, min_support = 0.01, use_colnames = True)
rules = association_rules(frq_items, metric ="lift", min_threshold = 1)
rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False])
print(rules.head())


# In[10]:


frq_items = apriori(basket_Por, min_support = 0.05, use_colnames = True)
rules = association_rules(frq_items, metric ="lift", min_threshold = 1)
rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False])
print(rules.head())


# In[11]:


frq_items = apriori(basket_Sweden, min_support = 0.05, use_colnames = True)
rules = association_rules(frq_items, metric ="lift", min_threshold = 1)
rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False])
print(rules.head())

