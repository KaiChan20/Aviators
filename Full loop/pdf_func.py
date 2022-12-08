import string
import pandas as pd
import fitz
#path = "C:/DAEN690/2A13.pdf"
#pdf = fitz.open(path)
#pdf.metadata
#### add page to all words
def add_page(in_put, value):
    inn = []
    out = [[]]
    index = 0
#    v = str(value+1)
    for i in range(0, len(in_put)):
        if(i < len(in_put)-1):
            inn += [in_put[i][0], in_put[i][1], in_put[i][2], in_put[i][3], in_put[i][4], in_put[i][5], in_put[i][6], in_put[i][7]]
            inn.insert( 8, value+1)
            out[index] = inn
            index += 1
            inn = []
            out += [[]]
        else:
            inn += [in_put[i][0], in_put[i][1], in_put[i][2], in_put[i][3], in_put[i][4], in_put[i][5], in_put[i][6], in_put[i][7]]
            inn.insert( 8, value+1)
            out[index] = inn

    return out
#--------------------------------------------------------------------------------------------------------
#get all text from given pdf file
def get_all_text(data):
    pc = data.page_count
    word_box = []
    for i in range(0,pc):
        ct = data.load_page(i)
        gw = ct.get_text('words')
        # If the df do not need page anymore, #agw = ... and make wor_box += gw
        agw = add_page(gw, i)
        word_box += agw
    
    return word_box
#--------------------------------------------------------------------------------------------------------
# merge the words by block_no and line_no
def word_line(in_put):
    index = 0
    word_list = []
    output = [[]]
    for i in range(0,len(in_put)-1):
        if(in_put[i][7]+1 == in_put[i+1][7]):
            word_list += [in_put[i][4]]  
        else:
            if(in_put[i+1][7]==0):
                word_list += [in_put[i][4]]
                word_list = [' '.join(word_list)]
                word_list += [in_put[i][5], in_put[i][6], in_put[i][7],in_put[i][8]]
                word_list.insert( 0, in_put[i-in_put[i][7]][0])
                word_list.insert( 1, in_put[i-in_put[i][7]][1])
                word_list.insert( 2, in_put[i][2])
                word_list.insert( 3, in_put[i][3])
            #print(word_list)

            output[index] += word_list
            index += 1
            word_list = []
            output += [[]]
    output.pop(-1)
    return output




#--------------------------------------------------------------------------------------------------------
# Get the X1 of Fuel
def get_fuel_x1(df):
    for i in range(0,len(df)):
        if(df[i][4].lower() == 'fuel') or (df[i][4].lower() == 'fuel:') or (df[i][4].lower() == '*fuel') or (df[i][4].lower() == 'fuel.'):
            return df[i][2]

#--------------------------------------------------------------------------------------------------------
# detect the word lines' class (key_term, header, info)
def detect_khi(in_put):
    index = 0
    temp_list= []
    out_put = [[]]
    for i in range(0,len(in_put)):
        ## old one add & (in_put[i][6] == 0) in both if & elif
        if(in_put[i][0] <= fuel_x1) & (in_put[i][7] < 5 ):
            temp_list += [in_put[i][0], in_put[i][1], in_put[i][2], in_put[i][3], in_put[i][4], in_put[i][5], in_put[i][6], in_put[i][7], in_put[i][8]]
            temp_list.insert(8, 'key_term')
            out_put[index] = temp_list
            temp_list = []
            out_put += [[]]
            index += 1
        elif(in_put[i][0] <= fuel_x1) & (in_put[i][4].lower().find('model') > 0):
            temp_list += [in_put[i][0], in_put[i][1], in_put[i][2], in_put[i][3], in_put[i][4], in_put[i][5], in_put[i][6], in_put[i][7], in_put[i][8]]
            temp_list.insert(8, 'header')
            out_put[index] = temp_list
            temp_list = []
            out_put += [[]]
            index += 1
        else:
            temp_list += [in_put[i][0], in_put[i][1], in_put[i][2], in_put[i][3], in_put[i][4], in_put[i][5], in_put[i][6], in_put[i][7], in_put[i][8]]
            temp_list.insert(8, 'info')
            out_put[index] = temp_list
            temp_list = []
            out_put += [[]]
            index += 1
    out_put.pop(-1)
    #print(out_put)
    return out_put
#--------------------------------------------------------------------------------------------------------
# Sometimes the header's number will be detect as key term, this function is used to solve it.
def hder(df):
    for i in range(1, len(df)-5):
        if(df[i+1][8] == "header") & (int(df[i][1]) == int(df[i+1][1])):
            df[i][8] = "header"
    return df
#--------------------------------------------------------------------------------------------------------
# 11/15
# This function is used to make sure the left side have are all header or keyterm
def all_header(df):
    for i in range(1 , len(df)-3):
        if(df[i-1][8] == 'header'):
            if(df[i][4].lower() == 'engine') or (df[i][4].lower() == 'engines'):
                pass
            else:
                df[i][8] = 'header'
    return df
#-------------------------------------------------------------------------------------------------------
#11/25
#Let 'all model' from key term to header
def allmodel_is_header(df):
    
    for i in range(0, len(df)-1):
        if(df[i][8] == 'key_term') & (df[i][4].lower().find('all') > 0):
            if(df[i][4].lower().find('model') > 0) or (df[i][4].lower().find('models') > 0 ):
                df[i][8] == 'header'
                #print(i, df[i][4])
    
    return df
#--------------------------------------------------------------------------------------------------------
# 11/19 define the model & revision info of top right in the first page as rev
def df_rev(df):
    fkt = -1
    for i in range(0, len(df)):
        if(df[i][8] == 'key_term') & (fkt < 0):
            fkt = i
#    print(fkt)        
    for i in range(0, fkt):
        if(df[i][0] > 300):
            df[i][8] = 'rev'
    
    return df

#--------------------------------------------------------------------------------------------------------
# find first line from page2
def firsty1(df):
    lst = []
    page = 1

    for i in range(0, len(df)-1):
        if(df[i][9] == page+1):
            lst += [df[i][3]]
            page += 1
#    print(lst)
    return lst

#--------------------------------------------------------------------------------------------------------
def drop_fline(df, fy):
    lst = []
    y1max = max(fy)+0.001
    for i in range(0, len(df)-1):
        if(df[i][9] > 1) & (df[i][3] < y1max):
            lst += [i]
#    print(lst)
    lst.reverse()
#    print(lst)
    for i in range(0, len(lst)):
        df.pop(lst[i])
    
    return df
#--------------------------------------------------------------------------------------------------------
#quick check functions
def seekt(df):
    for i in range(0, len(df)-1):
        if(df[i][8] == 'key_term'):
            print(df[i][4])

def seehd(df):
    for i in range(0, len(df)-1):
        if(df[i][8] == 'header'):
            print(df[i][4])   

def seeall(df):
    for i in range(0 ,len(df)-1):
        print(df[i])

def seeleft(df):
    for i in range(0,len(df)-1):
        if(df[i][0] <= 106):
            print(df[i][8])

def seerev(df):
    for i in range(0, len(df)):
        if(df[i][8] == 'rev'):
            print(df[i][8], df[i][4])
            
def merge_all(df):
    lst = []
    out = []
    index = 0
    num = 0
    for i in range(0, len(df)-1):
        if(df[i][8] == 'header'):
            if(df[i+1][8] == 'header'):
                lst += [df[i][4]]
                num += 1
            else:
                out += [[]]
                lst += [df[i][4]]
                lst = [' \n '.join(lst)]
                lst += [df[i][8]]
                lst.insert( 0, df[i-num][9])
                lst.insert( 1, df[i][1])
                lst.insert( 2, df[i][9])
                lst.insert( 3, df[i][3])
                # out put will be [start page, y start, end page, y end, text, class]
                out[index] = lst
                num = 0
                index += 1
                lst = []

        elif(df[i][8] == 'key_term'):
            out += [[]]
            lst += [df[i][9], df[i][1], df[i][9], df[i][3], df[i][4], df[i][8]]
            out[index] = lst
            index += 1
            lst = []
        
        elif(df[i][8] == 'info'):
            if(df[i+1][8] == 'info'):
                lst += [df[i][4]]
                num += 1
            else:
                out += [[]]
                lst += [df[i][4]]
                lst = [' \n '.join(lst)]
                lst += [df[i][8]]
                lst.insert( 0, df[i-num][9])
                lst.insert( 1, df[i][1])
                lst.insert( 2, df[i][9])
                lst.insert( 3, df[i][3])
                # out put will be [start page, y start, end page, y end, text, class]
                out[index] = lst
                num = 0
                index += 1
                lst = []
                
        elif(df[i][8] == 'rev'):
            if(df[i+1][8] == 'rev'):
                lst += [df[i][4]]
                num += 1
            else:
                out += [[]]
                lst += [df[i][4]]
                lst = [' \n '.join(lst)]
                lst += [df[i][8]]
                lst.insert( 0, df[i-num][9])
                lst.insert( 1, df[i][1])
                lst.insert( 2, df[i][9])
                lst.insert( 3, df[i][3])
                # out put will be [start page, y start, end page, y end, text, class]
                out[index] = lst
                num = 0
                index += 1
                lst = []
    return out


#def merge_all(df):
#    fill_lst = [0,0,0,0,0,0,0,0,0,0]
#    df += [[]]
#    df[-1] = fill_lst
#    lst = []
#    out = []
#    index = 0
#    num = 0
#    for i in range(0, len(df)-1):
#        if(df[i][8] == df[i+1][8]):
#            lst += [df[i][4]]
#            num += 1
#        else:
#            out += [[]]
#            lst += [df[i][4]]
#            lst = [' <\n> '.join(lst)]
#            lst += [df[i][8]]
#            lst.insert( 0, df[i-num][9])
#            lst.insert( 1, df[i][1])
#            lst.insert( 2, df[i][9])
#            lst.insert( 3, df[i][3])
            # out put will be [start page, y start, end page, y end, text, class]
#            out[index] = lst
#            num = 0
#            index += 1
#            lst = []
#    return out

#mall = merge_all(ah)
#for i in range(0, len(mall)):
#    print(mall[i])


def prep_final_output(df):
    index = 0
    lst = []
    out = []
    
    for i in range(0, len(df)-1):
        if(df[i][5] == 'rev') or (df[i][5] == 'header'):
            out += [[]]
            lst += [df[i][4], '']
            out[index] = lst
            
            lst = []
            index += 1
        
        elif(df[i][5] == 'key_term') & (df[i+1][5] == 'info'):
            lst += [df[i][4]]
        elif(df[i][5] == 'info') & (len(lst) > 0):
            out += [[]]
            lst += [df[i][4]]
            out[index] = lst
            
            lst =[]
            index += 1

    return out

