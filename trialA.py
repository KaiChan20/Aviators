from gettext import install

import PyPDF2
import os
import re
import openpyxl as openpyxl
from pandas import DataFrame
resources = "/Users/rohitvarma/Desktop/CAPSTONE/tcds"
excel_output = "/Users/rohitvarma/Desktop/CAPSTONE/output"




def grapPDF(path):
    pdfFileObj = open(path, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    try:
    textinpage = pageObj.extractText()
    pdfFileObj.close()
    return textinpage




def transformToDf(text):
    t = ["Engines", "Fuel", "Engine Ratings", "Thrust Setting"]
    n = []
    for i in t:
        item = i.replace(' ', '[ ]').replace('(', '[(]').replace(')', '[)]')
        # This code is for regular exp to grab the figures (ERRORS, needs to be fixed!)
        keytermlist = re.compile(r'') #RE code in progress
        keylist = keytermlist.findall(text)
        n.append([i[0].replace('\n', '').replace(' ', '') for i in keylist])
    dictionary = dict(zip(t, n))
    return DataFrame(dictionary)





def loopAllPDF(PDFdirectory):
	alldf = DataFrame()
	for listePDF in os.listdir(PDFdirectory):
		if listePDF.endswith(".pdf"):
			df = transformToDf(grapPDF(PDFdirectory+'//'+listePDF))
			alldf = alldf.append(df)

	alldf.to_excel(excel_output + "//" + 'resultcds.xlsx', sheet_name='sheet1', index=False) #ERRORS! need to be fixed




loopAllPDF(resources)

