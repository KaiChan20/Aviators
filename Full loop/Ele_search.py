import os
import PyPDF2
import re
path = "D:\TCDS\TCDS sample"
list_files = os.listdir(path)
print(list_files)
s = ""

for ele in list_files:
    #print(ele)
    os.chdir(path)
 
    pdfFileObj = open(ele, 'rb' ,) 
        
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
            if re.match("\A[Tt]ype\s[Cc]ertificate\s[Hh]older",out[j]):  
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
            elif re.match("\A[Ee]ngine",out[j]):
                try:
                    if re.match("[Ll]imits",out[j].split()[1]):
                        pass
                    else:
                        k = j
        ### working code to print everything between Engine and fuel                
                        while out[k].find('Fuel') == -1:
                            print(out[k])
                            s = s + out[k] + "\n"
                            k = k +1
                except IndexError:
                    print("Fuel Keyword not found")

            # code to print propeller    
            elif re.match("\A[Pp]ropeller",out[j]):
                try:
                    
                    k = j
    ### working code to print everything between Propeller and Airspeed and                
                    while out[k].find('Airspeed') == -1:
                        print(out[k])
                        s = s + out[k] + "\n"
                        k = k +1
                except IndexError:
                    print("Fuel Keyword not found")


            
            elif re.search('\ANOTE\s\d' , out[j]):
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

os.chdir("D:\TCDS")
with open('test.txt' , 'w') as file:  
    file.write(s)

