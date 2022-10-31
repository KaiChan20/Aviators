import fitz 
import pandas as pd 
import os, glob
 
#path = input("Enter the path from current directory: ")
#path = r'C:Users\lexua\OneDrive\Desktop\Work\DAEN 690\Aviators\Data\tcds'

os.chdir(os.getcwd())
path = r'.\tcds'

def see_readable():
    os.chdir(path)
    pdfs = []
    doc_name = []
    doc_type = []
    for file in glob.glob("*.pdf"):
        try:
            extracted_text = ''.join([page.get_text() for page in fitz.open(file)])
            if extracted_text:
                doc_name.append(file)
                doc_type.append("text")
            else:
                doc_name.append(file)
                doc_type.append("scan")
        except:
            doc_name.append(file)
            doc_type.append("broken")
            pass
        print(doc_name)
        print(doc_type)
    dict = {'name': doc_name, 'type': doc_type}
    
    readable = pd.DataFrame(dict, index=None)
    #print(readable)
    os.chdir('..')

#see_readable()

def get_all_text():
    os.chdir(path)
    word_box = []
    for file in glob.glob('*.pdf'):
        try:
            extracted_text = ''.join([page.get_text() for page in fitz.open(file)])
            if extracted_text:
                pdf = fitz.open(file)
                pc = pdf.page_count
                for i in range(0, pc):
                    ct = pdf.load_page(i)
                    gw = ct.get_text('words')
                    word_box += gw
                return word_box
            else:
                print(file)
                return print('this pdf is scanned')
        except:
            print(file)
            print("This file is broken")
    print(word_box)

get_all_text()

def word_groups(words_list):
    index = 0
    word_list = []
    output = [[]]
    for i in range(0,len(words_list)-1):
        if(words_list[i][-1]+1 == words_list[i+1][-1]):
            word_list += [words_list[i][-4]]  
        else:
            if(words_list[i+1][-1]==0):
                word_list += [words_list[i][-4]]
                word_list = [' '.join(word_list)]
                word_list += [words_list[i][-3],words_list[i][-2],words_list[i][-1]]
                word_list.insert( 0, words_list[i-words_list[i][-1]][0])
                word_list.insert( 1, words_list[i-words_list[i][-1]][1])
                word_list.insert( 2, words_list[i][2])
                word_list.insert( 3, words_list[i][3])
            print(word_list)

            output[index] += word_list
            index += 1
            word_list = []
            output += [[]]
    
    return output

