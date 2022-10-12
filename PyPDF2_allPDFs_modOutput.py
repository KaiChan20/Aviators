#!/usr/bin/env python
# coding: utf-8

# In[1]:


import PyPDF2
import re
import glob

#your full path of directory
mypath = "/Users/poth/Documents/Fall2022/DEAN690/Coding/TCDS/"
for file in glob.glob(mypath + "/*.pdf"):
    print(file)
    if file.endswith('.pdf'):
        fileReader = PyPDF2.PdfFileReader(open(file, "rb"))
        count = 0
        count = fileReader.numPages
        while count >= 0:
            count -= 1
            pageObj = fileReader.getPage(count)
            text = pageObj.extractText()
            print(text)
        num = re.findall(r'[0-9]+', text)
        print(num)
    else:
        print("not in format")


# In[7]:


get_ipython().run_cell_magic('capture', 'cap --no-stderr', 'print(text)\n')


# In[8]:


with open('/Users/poth/Documents/Fall2022/DEAN690/Coding/output/new1.txt', 'w') as f:
    f.write(cap.stdout)


# In[ ]:




