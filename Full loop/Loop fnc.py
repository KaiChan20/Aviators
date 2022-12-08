import os 
import fitz
import pandas as pd 
import string
import pdf_func as pf

path = "/Users/bbteela/Desktop/Work/DAEN 690/Aviators/Data/dataset_tcds"
list_files = os.walk(path)
dfinal = pd.DataFrame() 
a = []
nof = []

for root, dirs, files in os.walk(path):
    for file in files:
        if not file.startswith("."):
            p = os.path.join(root,file)
            print(p)
            pdf = fitz.open(p)
            if pdf == None:
                pass
            else:

                #--------------------------------------------------------------------------------------------------------
                #get all text [x0, y0, x1, y1, word, block_no, line_no, word_no, page]
                all_text = pf.get_all_text(pdf)
                
                
                # merge text by block_no & line_no
                out = pf.word_line(all_text)
                #print(out)
                
                fuel_x1 = pf.get_fuel_x1(out)
                #sorted key + lambda 
                # ref: https://blog.csdn.net/w417950004/article/details/86253721
                # reorder the word lines by coordinates (page > y0 > x0)
                pall = sorted(out, key = lambda x:(int(x[8]), float(x[1]), float(x[0])))
                # print pall to check
                #        for i in range(0, len(pall)):
                #            print(pall[i][8], pall[i][1], pall[i][0], pall[i][4])
                #----------------------------------------------------------------------------------------
                # classify the word to (header , key_term, info), 
                #the output will be [x0, y0, x1, y1, word, block_no, line_no, word_no, class, page]
                khi = pf.detect_khi(pall)
                #------------------------------------------------------------------------------------------
                #fy1 function will retun the y1 of the first lines
                fy1 = pf.firsty1(khi)
                #use the max value to clean the tc titles which has been detect as KT
                pf.drop_fline(khi, fy1)
                #---------------------------------------------------------------------------------------
                # Sometimes the header's number will be detect as key term, this function is used to solve it.
                #example: real header == I. Model xyz....  and the df might be ['I.', 'key_term'], ['Model xyz...', 'header']
                # hder function is to catch 'I.' form keyterm to header.       
                pf.hder(khi)
                #--------------------------------------------------------------------------------------
                # drop  (cont’d)
                # the exact text (cont'd) may change by tcds.
                for i in range(0, len(khi)-20):
                    if(khi[i][4].find('(cont’d)') > 0):
                        khi.pop(i)
                        i = i-1
                #---------------------------------------------------------------------------------------------------
                #drop punctuation
                #https://datagy.io/python-remove-punctuation-from-string/
                for i in range(0, len(khi)-1):
                    if(khi[i][8] == 'key_term'):
                        khi[i][4] = khi[i][4].translate(str.maketrans('', '', string.punctuation))
                #        print(khi[i][4])
                #-------------------------------------------------------------------------------------------------
                ah = pf.all_header(khi)
                #-------------------------------------------------------------------------------------------------
                pf.df_rev(ah)
                
                mall = pf.merge_all(ah)
                #for i in range(0, len(mall)):
                #    print(mall[i])
                fout = pf.prep_final_output(mall)
                
                b = pd.DataFrame(fout)
                b.to_csv(rf'/Users/bbteela/Desktop/Work/DAEN 690/csv/{file}.csv', index=False)
                a.append(b)
    
                #dfinal.loc[len(dfinal)] = fout
                pdf.close()

                #for i in range(0, len(fout)):
                #    print(fout[i])
                
                #dfinal = pd.DataFrame(fout, columns=['L', 'R'])
                #dfinal  

