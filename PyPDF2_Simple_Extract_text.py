#!/usr/bin/env python
# coding: utf-8

# In[1]:


import PyPDF2 


# In[5]:


pdfopen = open('/Users/poth/Downloads/PDFEX/A16WE_Rev71.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfopen, strict = False)
print(pdfReader.numPages)
pageObj = pdfReader.getPage(0)
print(pageObj.extractText())


# In[ ]:




