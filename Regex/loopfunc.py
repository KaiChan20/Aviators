!pip install pycryptodome
import os
import PyPDF2
path = r"" #folder with all PDFs

list_files = os.listdir(path)
print(list_files)
s = ""

for ele in list_files:
    #print(ele)
    os.chdir(path)
 
    pdfFileObj = open(ele, 'rb' ,) 
        
    #creating a pdf reader object 
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict = False) 

        
    # printing number of pages in pdf file 
    page_count = pdfReader.numPages
    #print(page_count)


    for i in range(0,page_count):
        pageObj = pdfReader.getPage(i)
        res = pageObj.extractText()
        out = res.splitlines()
        for j in range(0,len(out)):
            if out[j].find('Type Certificate Holder') != -1:
                tmp = out[j].replace("Type Certificate Holder" , "")
                new_str = tmp.replace("(See Note X)" , "")
              
                print("Type Certificate Holder:Name" + "     " + new_str)
                print("Type Certificate Holder:Address" + "       " + out[j+1] + out[j+2])
           
            elif out[j].find('Engine ') != -1:
                tmp = out[j].replace("Engine" , "")
                print("Engine:" + "     " + tmp)
  

    print("\n")
    
    pdfFileObj.close()