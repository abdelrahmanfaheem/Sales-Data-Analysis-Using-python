#!/usr/bin/env python
# coding: utf-8

# # Read All Data And Concate it in one File

# In[1]:


import pandas as pd
import numpy as np
import plotly.express as px
import os

# Initialize an empty DataFrame
all_Sales_data = pd.DataFrame()

# Define the directory containing the files
data_directory = r'F:\Data Analysis\Data Project\Python Project\Pandas Sales Analysis\Sales_Data'

# List all files in the directory
files = os.listdir(data_directory)

# Loop through each file and concatenate the data
for file in files:
    # Ensure we are only processing CSV files
    if file.endswith('.csv'):
        # Construct the full file path
        file_path = os.path.join(data_directory, file)
        
        # Read the CSV file
        df1 = pd.read_csv(file_path)
        
        # Concatenate the data
        all_Sales_data = pd.concat([all_Sales_data, df1], ignore_index=True)



all_Sales_data.head()


# In[2]:


all_Sales_data.dtypes


# ## Clean Up The Data

# #### Drop Data With Nan

# In[3]:


all_Sales_data.dropna(inplace=True,how='any')


# In[21]:


all_Sales_data['Order Date']=pd.to_datetime(all_Sales_data['Order Date'])


# ### Convert Data Type of Columns 

# In[ ]:


all_Sales_data['Order ID']=all_Sales_data['Order ID'].astype('int64')
all_Sales_data['Product']=all_Sales_data['Product'].astype('str')
all_Sales_data['Price Each']=all_Sales_data['Price Each'].astype(float)
all_Sales_data['Quantity Ordered']=all_Sales_data['Quantity Ordered'].astype(int)
all_Sales_data['Order Date']=pd.to_datetime(all_Sales_data['Order Date'])


# In[32]:


all_Sales_data.dtypes


# # Augment data with additional columns

# ### Add Month Column

# In[34]:


all_Sales_data['Month']=all_Sales_data['Order Date'].str[0:2]
all_Sales_data=all_Sales_data [ all_Sales_data['Month']!='Or']
all_Sales_data['Month']=all_Sales_data['Month'].astype('int32')


# ###  Add Month Name Column

# In[35]:


all_Sales_data['Month Name']=pd.to_datetime(all_Sales_data['Order Date'],format='%m').dt.month_name()
##all_Sales_data [ all_Sales_data['Month Name']!='Or']


# ### Get the Year

# In[26]:


all_Sales_data['Year']=pd.to_datetime(all_Sales_data['Order Date']).dt.year


# ### Get The Quarter

# In[27]:


all_Sales_data['Quarter']=pd.to_datetime(all_Sales_data['Order Date']).dt.quarter

quarter_map = {1: 'Q1', 2: 'Q2', 3: 'Q3', 4: 'Q4'}
all_Sales_data['Quarter'] = all_Sales_data['Quarter'].map(quarter_map)


# ### Get the Hour 

# In[19]:


all_Sales_data['Hour']=all_Sales_data['Order Date'].dt.hour


# ### Get the Sales Amount

# In[40]:


all_Sales_data['Sales Amount']=all_Sales_data['Quantity Ordered']*all_Sales_data['Price Each']


# ### Get the City Column

# In[36]:


##all_Sales_data['City']=all_Sales_data['Purchase Address'].str.split(',') .str[1]
def get_city(address):
    return address.split(',')[1]
all_Sales_data['City']=all_Sales_data['Purchase Address'].apply(lambda x:get_city(x))


# ### Get State

# In[37]:


def get_state(address):
    return address.split(',')[2].split(' ')[1]

all_Sales_data['City']=all_Sales_data['Purchase Address'].apply(lambda x : get_city(x)+' ('+get_state(x)+') ')


# In[38]:


all_Sales_data


# ## Question 1: was the month for sales? How much was that month?

# In[41]:


Sales_For_Month=all_Sales_data.groupby('Month Name').agg(Month_sales =pd.NamedAgg(column='Sales Amount',aggfunc=np.sum))
Sales_For_Month.sort_values('Month_sales',ascending=False,inplace=True)


# In[42]:


# Create a color list
colors = ['darkblue' if i < 3 else 'gray' for i in range(len(Sales_For_Month))]

# Create the bar plot
fig = px.bar(data_frame=Sales_For_Month, 
             x=Sales_For_Month.index, 
             y='Month_sales',
             text='Month_sales',  # Add data labels
             title='Top 3 Month For Sales')

# Update the bar colors
fig.update_traces(marker_color=colors)

# Update the layout to show data labels
fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')

# Customize the layout
fig.update_layout(
    xaxis_title='Month',
    yaxis_title='Sales Amount',
    showlegend=False
)

# Show the plot
fig.show()


# ### What City  had  the highest number of  sales

# In[48]:


# Assuming all_Sales_data is your DataFrame
# Group by City and aggregate Sales Amount
SalesForCity_Data = all_Sales_data.groupby('City').agg(SalesForCity=pd.NamedAgg(column='Sales Amount', aggfunc=np.sum))
SalesForCity_Data.sort_values(by='SalesForCity', ascending=False, inplace=True)

# Create a color list
colors = ['darkblue' if i < 3 else 'gray' for i in range(len(SalesForCity_Data))]

# Create the bar plot
fig = px.bar(data_frame=SalesForCity_Data, 
             x=SalesForCity_Data.index, 
             y='SalesForCity',
             text='SalesForCity',  # Add data labels
             title='Top 3 Sales for Each City ')

# Update the bar colors
fig.update_traces(marker_color=colors)

# Update the layout to show data labels
fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')

# Customize the layout
fig.update_layout(
    xaxis_title='City',
    yaxis_title='Sales Amount',
    showlegend=False
)

# Show the plot
fig.show()


# ### Sales Traffic for Hour 

# In[49]:


Sales_for_hour=all_Sales_data.groupby('Hour').agg(Hour_traffic=pd.NamedAgg(column='Quantity Ordered',aggfunc=np.count_nonzero))
Sales_for_hour


# In[50]:


# Create the line chart
fig = px.line(data_frame=Sales_for_hour, 
              x=Sales_for_hour.index, 
              y='Hour_traffic', 
              title='Sales Traffic by Hour', 
              markers=True,  # Adds markers to the line
              text='Hour_traffic')  # Adds data labels

# Update the line and marker colors to dark blue
fig.update_traces(line_color='darkblue', marker_color='darkblue')

# Update the layout to show data labels
fig.update_traces(texttemplate='%{text}', textposition='top center')

# Customize the layout
fig.update_layout(
    xaxis_title='Hour',
    yaxis_title='Quantity Ordered',
    showlegend=False
)

# Show the plot
fig.show()


# # What Product Most Often Sold Together 

# In[51]:


## transform is similar to applay
df1=all_Sales_data[all_Sales_data['Order ID'].duplicated(keep=False)]
df1['Grouped']=df1.groupby('Order ID')['Product'].transform(lambda x:','.join(x) )
df1=df1[['Order ID','Grouped']].drop_duplicates()

df1.dropna(inplace=True)

##df1.sort_values('Order ID')
##df.dropna(axis=0,inplace=True)
##df.sort_values('Order ID')
##df=df[df['Order ID'].duplicated(keep='first')]



df1


# In[52]:


##df1.groupby("Grouped").agg(np.count_nonzero).sort_values(ascending=False,by='Order ID')


# In[46]:


from itertools import combinations
from collections import Counter

count = Counter()

for row in df1['Grouped']:
    row_list=row.split(',')
    # Counter(list of data ,pairs need to count )->  
    #count.update(Counter(combinations(row_list,3))) # Count the 3 pairs 
    
    count.update(Counter(combinations(row_list,2))) # Count the 2 pairs 

## most_common get the most Redundant value 
for key , value in count.most_common(10):
    print (key, value)


# # What is Proudct Sold the most & Why you think it sold the most ?
# 

# In[53]:


Proudct_Sold=all_Sales_data.groupby('Product').agg(product_sum=pd.NamedAgg(column='Quantity Ordered',aggfunc=np.sum))
Proudct_Sold.sort_values(by='product_sum',ascending=False ,inplace=True)

#colors = ['darkblue' if i < 3 else 'gray' for i in range(len(SalesForCity_Data))]

colors=['darkblue'if i<5 else 'gray'for i in range (len (Proudct_Sold))]

#Create the bar plot
fig = px.bar(data_frame=Proudct_Sold, 
             x=Proudct_Sold.index, 
             y='product_sum',
             text='product_sum',  # Add data labels
             title='Top 5 Sales for Each Product ')

# Update the bar colors
fig.update_traces(marker_color=colors)

# Update the layout to show data labels
fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')

# Customize the layout
fig.update_layout(
    xaxis_title='Product',
    yaxis_title='Sales Amount',
    showlegend=False
)

# Show the plot
fig.show()


# In[ ]:





# In[ ]:





# In[ ]:




