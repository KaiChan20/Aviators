#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os
import pdfplumber
import sys
import subprocess
directory = r'/Users/poth/Downloads/PDFEX'
for filename in os.listdir(directory):
    if filename.endswith('.pdf'):
        fullpath = os.path.join(directory, filename)
        all_text = ""
        with pdfplumber.open(fullpath) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                all_text += '\\n' + text
        print(all_text)


# In[ ]:




