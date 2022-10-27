import PyPDF2

# creating a pdf file object 
pdfFileObj = open('./Test_B/1a21.pdf', 'rb') 
    
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)   

print(pdfReader.numPages)   

pageObj = pdfReader.getPage(0) 
   
#fetching the output of pdf file in string
res = pageObj.extractText()

#splitting the string based on end of line delimiter
out = res.splitlines()

print(len(out))

#performing operation on each line to fetch exact values
for i in range(0,46):
    if out[i].find('Type Certificate Holder') != -1:
        #print(out[i])
        tmp = out[i].replace("Type Certificate Holder" , "")
        new_str = tmp.replace("(See Note X)" , "")
        #new_out = out[i].split(" ")
        print("Type Certificate Holder:Name" + "     " + new_str)
        print("Type Certificate Holder:Address" + "       " + out[i+1] + out[i+2])
      
    elif out[i].find('Engine Lycoming') != -1:
        tmp = out[i].replace("Engine" , "")
        print("Engine:" + "     " + tmp)
        #print(out[i])
    elif out[i].find('Serial Nos. Eligible') != -1:
        tmp = out[i].replace("Serial Nos. Eligible" , "")
        print("Serial Nos. Eligible:" + "     " + tmp)

        break
        
   
# closing the pdf file object 
pdfFileObj.close()