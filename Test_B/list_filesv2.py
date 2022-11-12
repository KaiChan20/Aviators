from email.policy import strict
import os
import PyPDF2
import re
path = r"/Users/bbteela/Desktop/Work/DAEN 690/Aviators/Data/tcds"
list_files = os.listdir(path)
print(list_files)
s = ""

for ele in list_files:
    #print(ele)
    os.chdir(path)
 
    pdfFileObj = open(ele, 'rb' ,) 
    s = s + ele + "\n"  
    #creating a pdf reader object 
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 

        
    # printing number of pages in pdf file 
    page_count = pdfReader.numPages
    #print(page_count)


    for i in range(0,page_count):
        pageObj = pdfReader.getPage(i)
        res = pageObj.extractText()
        out = res.splitlines()
        for j in range(0,len(out)):

    # working code to fetch certficate holder data and print everthing until it gets model     
            if re.match("^[Tt]ype\s[Cc]ertificate\s[Hh]older",out[j]):  
                try:     
                    k = j 
                    while out[k].find('Model') == -1:
                        s = s + out[k] + "\n"
                        print(out[k])
                        k = k +1
                except IndexError:
                    print("model keyword not found")
                
#            print("\n")

                
               
            elif out[j].find('Model') != -1:
                print(out[j])
                s = s + "Model: " + "       " + out[j] + "\n"
                

        ## working on optimizing this condition    
            elif out[j].find('Engine') != -1:
                try:
                    k = j
    ### working code to print everything between Engine and fuel                
                    while out[k].find('Fuel') == -1:
                        print(out[k])
                        s = s + out[k]
                        k = k +1
                except IndexError:
                    print("Fuel Keyword not found")
               
                print("\n")


            
            elif re.search('NOTE\s\d' , out[j]):
                s = s + out[j] + "\n"
#                print(out[j])

            elif out[j].find('Serial Nos. eligible ') != -1:
                tmp = out[j].replace("Serial Nos. eligible" , "")
                s = s + "Serial Nos. eligible:" + "     " + tmp + "\n"
#                s = s + tmp + "\n"
#                print(tmp)

            elif out[j].find('No. of Seats ') != -1:
                tmp = out[j].replace("No. of Seats" , "")
                s = s + "No. of Seats:" + "     " + tmp + "\n"
#                print(tmp)


            elif out[j].find('Maximum Weight ') != -1:
                tmp = out[j].replace("Maximum Weight" , "")
                s = s + "Maximum Weight:" + "     " + tmp + "\n"
#                print(tmp)




        s = s + "\n"
    s = s + "\n"
#    print("\n") 
    pdfFileObj.close()

os.chdir(r"/Users/bbteela/Desktop/Work/DAEN 690")
with open('test.txt' , 'w', encoding="utf-8") as file:  
    file.write(s)

