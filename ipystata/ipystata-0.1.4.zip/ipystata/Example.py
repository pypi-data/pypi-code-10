
# coding: utf-8

# ## Example notebook for the %%stata cell magic by the IPyStata package. 

# **Author:**   Ties de Kok <t.c.j.dekok@tilburguniversity.edu>  
# **Twitter:** @TiesdeKok <https://twitter.com/TiesdeKok/>  
# **Homepage:**    https://github.com/TiesdeKok/ipystata  
# **PyPi:** https://pypi.python.org/pypi/ipystata  

# ## Import packages

# In[1]:

import pandas as pd


# In[2]:

import ipystata


# ## Configure ipystata

# In[3]:

from ipystata.ipystata_magic import iPyStata
iPyStata.config_stata('C:\Program Files (x86)\Stata13\StataMP-64.exe') 


# Note, this is only required at the initial setup or when your Stata installation has changed. 

# ## Check whether IPyStata is working

# In[4]:

get_ipython().run_cell_magic(u'stata', u'', u'\ndisplay "Hello, I am printed by Stata."')


# # Some examples based on the Stata 13 manual

# ## Load the dataset "auto.dta" in Stata return it back to Python as a Pandas dataframe

# The code cell below runs the Stata command **`sysuse auto.dta`** to load the dataset and returns it back to Python via the **`-o car_df`** argument.

# In[5]:

get_ipython().run_cell_magic(u'stata', u'-o car_df', u'sysuse auto.dta')


# **`car_df`** is a regular Pandas dataframe on which Python / Pandas actions can be performed. 

# In[6]:

car_df.head()


# ## Basic descriptive statistics

# The argument **`-d or --data`** is used to define which dataframe should be set as dataset in Stata.  
# In the example below the Stata function **`tabulate`** is used to generate some descriptive statistics for the dataframe **`car_df`**.

# In[7]:

get_ipython().run_cell_magic(u'stata', u'-d car_df', u'tabulate foreign headroom')


# These descriptive statistics can be replicated in Pandas using the **`crosstab`** fuction, see the code below.

# In[8]:

pd.crosstab(car_df['foreign'], car_df['headroom'], margins=True)


# ## Use Python lists as Stata macros

# In many situations it is convenient to define values or variable names in a Python list or equivalently in a Stata macro.  
# The **`-i or --input`** argument makes a Python list available for use in Stata as a local macro.  
# For example, **`-i main_var`** converts the Python list **`['mpg', 'rep78']`** into the following Stata macro: **``main_var'`**.

# In[9]:

main_var = ['mpg', 'rep78']
control_var = ['gear_ratio', 'trunk', 'weight', 'displacement']


# In[10]:

get_ipython().run_cell_magic(u'stata', u'-d car_df -i main_var -i control_var', u'\ndisplay "`main_var\'"\ndisplay "`control_var\'"\n\nregress price `main_var\' `control_var\', vce(robust)')


# ## Modify dataset in Stata and return it to Python

# It is possible create new variables or modify the existing dataset in Stata and have it returned as a Pandas dataframe.  
# In the example below the output **`-o car_df`** will overwrite the data **`-d car_df`**, effectively modifying the dataframe in place.  
# Note, the argument **`-np or --noprint`** can be used to supress any output below the code cell.

# In[11]:

get_ipython().run_cell_magic(u'stata', u'-d car_df -o car_df -np', u'\ngenerate weight_squared = weight^2\ngenerate log_weight = log(weight)')


# In[12]:

car_df.head(3)


# ## An example case

# Create the variable **`large`** in Python and use it as the dependent variable for a binary choice estimation by Stata.

# In[13]:

car_df['large'] = [1 if x > 3 and y > 200 else 0 for x, y in zip(car_df['headroom'], car_df['length'])]


# In[14]:

car_df[['headroom', 'length', 'large']].head(7)


# In[15]:

get_ipython().run_cell_magic(u'stata', u'-d car_df -i main_var -i control_var', u"\nlogit large `main_var' `control_var', vce(cluster make)")

