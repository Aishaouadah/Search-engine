import re
import math
from typing import DefaultDict
# 1 Module de représentation des documents -> fichier inverse terme par doc (avec ponderation)

# terme + poids du terme ti dans doc dj:  poids(ti, dj)=(freq(ti,dj)/Max(freq(dj))*Log((N/ni) +1)

# get terms from all docs , identify docs first then (ignore stop words , poncutation ... )
# I T W , ingnorer le B , N , X , A 
docs = "C:\\Users\\User\\Desktop\\M2-S3\\RI\\PROJECT\\cacm\\cacm.all"

# 3204 docs 
def find_terms(docs):
    terms = []
    with open(docs,'r') as cacm:
        file = cacm.read()
        file = file.replace('\n' ,' ')
        # remove ppunctuations
        file = re.sub('[^A-Za-z0-9.]+', " ", file)
        #terms = file.split('.I ') # terms list with numDoc
        terms = re.split('.I [0-9]+',file) # withouht numDoc 
    stop_words="C:\\Users\\User\\Desktop\\M2-S3\\RI\\PROJECT\\cacm\\common_words"
    with open(stop_words,'r') as common_words:
        file = common_words.read()
         
    for i in range(len(terms)):
        #delete B A N X parts    
        terms[i]  = terms[i].split('.B ')[0]
        terms[i]  = terms[i].split('.A ')[0]
        terms[i]  = terms[i].split('.N ')[0]
        terms[i]  = terms[i].split('.X ')[0]
        terms[i]  = terms[i].split(' ') # a term is one doc , it is a list of words in doc num i 
        # delete stopwords 
        terms[i]  = [w for w in terms[i] if w not in file]
        # delete numDoc and T W and . then join the lists 
    l = []
    for term in terms:
        #delete from str ( .T .W  )
        if '.T' in term:
            term.remove('.T')
        if '.W' in term:
            term.remove('.W') 

        l.append(term)
    return(l)

# Make the terms of docs in one list 
def all_terms(l):
    #l = find_terms(docs)
    newList = []
    for a in l:
        newList = newList + a
    return newList
        
def freqs(doc): # input : doc is list of terms 
    # returns a dict of terms of a doc with the frequency  
    frequence_dict = DefaultDict()
    for i in range(len(doc)):
        doc[i]=doc[i].lower()
    for word in doc:
        if word not in frequence_dict:
            frequence_dict[word] = doc.count(word)
    return frequence_dict

#print(freqs(l[3000]))
def docsLower(docs):
    for doc in docs: 
        for i  in range(len(doc)):
            doc[i] = doc[i].lower()
            doc[i] = re.sub('[^A-Za-z0-9]+', " ", doc[i])
    return docs

def alltermsLower(docs):
    for i  in range(len(docs)):
        docs[i] = docs[i].lower()
        docs[i]  = re.sub('[^A-Za-z0-9]+', " ", docs[i] )
    return docs #list(set(all_terms))

l = find_terms(docs)
l = docsLower(l)
all_terms = all_terms(l)
all_terms = alltermsLower(all_terms)
all_terms = list(set(all_terms))
#print((len(all_terms)))


def docshave(term, docs):
    # returns the number of lists where the term appears 
    freq = 0
    term = term.lower()
    for list in docs:
        if term in list:
            freq +=1
    return freq

#print(docshave('verification', l))
        
def freq(term,doc):
    term = term.lower()
    frequence_dict = freqs(doc)
    return frequence_dict[term]

#print(freq('programs', l[3000] ))
    
    
        
#calculate weight of a term in a doc

####   TAKES A LOT OF TIME 
#  STILL HAVE . 
# ALL TERMS HAVE DUPLICATES  ITEMS 

def calculate_wieght(term , doc):
    term = term.lower()
    #weight of term in doc
    N = 3204 # nombre de doc total 
    m= max(freqs(doc).values() ) # m = Max(freq(t, dj) : La fréquence max dans le document j
    ni= docshave(term, l) #ni : le nombre de documents contenant le terme i
    if m==0:
        poid=0
    else:
        if ni==0:
            poid=0
        else:  # getFreqinDoc : freq(ti,dj) : la fréquence du terme i dans le document j
            if term in doc:
                f = freq(term,doc)
            else: f=0
            poid = (f/m)*math.log10((N/ni)+1)
    return poid

#print('weight')
#print(calculate_wieght('programs', l[3000]))

   
 
def inverse_doc(all_terms, docs):

    #each term in all_terms -> calculate its weight in the doc
    inverse_doc_matrix = DefaultDict()  #dict {[term , doc] :  wieght}
    #print(all_terms)
    #print(docs)
    for term in all_terms:
        for i in range(len(docs)):
            if (len(docs[i]) != 0):
                inverse_doc_matrix[ tuple([term,i])] = calculate_wieght(term,docs[i]) 
    print("calculating weight done ... ")
    return inverse_doc_matrix

inverse_doc_matrix = inverse_doc(all_terms, l)
#print(inverse_doc(all_terms, l))

  
    
# 2 Module de représentation des requêtes 
def get_terms_query(query):
    terms=[]
    # lower , delete pondcutation ,  stopwords
    query = query.lower()
    # remove ppunctuations
    query= re.sub('[^A-Za-z0-9.]+', " ", query)
    terms = query.split()
    return terms

#print(get_terms_query('hello world :!! aicha is here coding , may Allah help her !! '))
    
    
    
    

def calculate_terms_query_value(query , all_terms):
    #query = get_terms_query(query)
    dict =  DefaultDict()
    for term in all_terms:
        if term in query:
            dict[term] = 1
        else: 
            dict[term] = 0
    return dict
#print(calculate_terms_query_value('Preliminary Report-International aicha Language, ' ,all_terms ))
    


# 3 Module d’appariement 

def internal_product(inverse_doc_matrix, numDoc , query): 
    # multiplication du poids du terme du query avec poids du terme du doc 
    rsv = 0
    query = get_terms_query(query)
    poids_query =  calculate_terms_query_value(query , all_terms)
    # doc is a list 
    for term in query:
        if term in poids_query:
            rsv = rsv + inverse_doc_matrix[(term, numDoc)] * poids_query[term]
    return rsv

#inverse_doc_matrix =  inverse_doc(all_terms, l )
#print(internal_product(inverse_doc_matrix, 2, 'aicha, ouadah Subtractions' ))
        


def dice(inverse_doc_matrix, numDoc , query):
    rsv =  2*internal_product(inverse_doc_matrix, numDoc , query)
    wij=1
    wiq=0
    query = get_terms_query(query)
    poids_query =  calculate_terms_query_value(query , all_terms)
    for term in query:
        if term in poids_query:
            wiq = wiq + poids_query[term] # pas de puissance car c que des 1 !! 
    # somme des cares des poids d'un doc 
    doc = l[numDoc]
    for term in doc:
        wij= wij + calculate_wieght(term,l[numDoc])**2
    
    return rsv/(wij+wiq)

#print(dice(inverse_doc_matrix, 1, 'hello world Preliminary'))
        

def cosinus(inverse_doc_matrix, numDoc , query):
    rsv =  2*internal_product(inverse_doc_matrix, numDoc , query)
    wij=1
    wiq=0
    query = get_terms_query(query)
    poids_query =  calculate_terms_query_value(query , all_terms)
    for term in query:
        if term in poids_query:
            wiq = wiq + poids_query[term]
    # somme des cares des poids d'un doc 
    doc = l[numDoc]
    for term in doc:
        wij= wij + calculate_wieght(term,l[numDoc])**2
    return rsv/math.sqrt((wij)  * (wiq))

#print(cosinus(inverse_doc_matrix, 1, 'hello world Preliminary'))

    
    
      
def  jaccard(inverse_doc_matrix, numDoc , query):
    rsv =  internal_product(inverse_doc_matrix, numDoc , query)
    wij=1
    wiq=0
    wij2=1
    query = get_terms_query(query)
    poids_query =  calculate_terms_query_value(query , all_terms)
    for term in query:
        if term in poids_query:
            wiq = wiq + poids_query[term]
    # somme des cares des poids d'un doc 
    doc = l[numDoc]
    for term in doc:
        wij2= wij2 + calculate_wieght(term,l[numDoc])**2

    for term in doc:
        wij= wij + calculate_wieght(term,l[numDoc])
        
    return rsv/(wij2 + wiq - wij* wiq )
    
#print(jaccard(inverse_doc_matrix, 1, 'hello world Preliminary'))

 
 # 5. Evaluation du modèle vectoriel


    # rappel = Nombre de documents pertinents séléctionnés / Nombre total de documents pertinents
    # precision = Nombre de documents pertinents sélectionnés / Nombre total de documents sélectionnés
    

def precision_internal_product(inverse_doc_matrix, all_docs, query):     
    doc_pretinent_total = [] # sup a seuil  {'num de doc ' : val (rsv) }
    doc_pretinent_selectionne = [] # selectioner le t
    doc = {}
    seuil = 3
    t = 10  # doc retournés   #######because m testing with 
    # calculate the internal product of query  and all docs 
    # get t first best docs depending on internal product ...
    for i in range(len(all_docs)-1):
        doc[i]=internal_product(inverse_doc_matrix, i+1 , query)
    doc = sorted(doc.items(), key = lambda kv: kv[1])
    i=0
    while( i<len(doc)):
        if (doc[i][1]>seuil):
            doc_pretinent_total.append(doc[i])
        i+=1
    doc_pretinent_selectionne = doc_pretinent_total[len(doc_pretinent_total)-t:]
    if len(doc)== 0:
        return 0
    return len(doc_pretinent_selectionne)/len(doc)
    

def rappel_internal_product(inverse_doc_matrix, all_docs, query):    
    doc_pretinent_total = [] # sup a seuil  {'num de doc ' : val (rsv) }
    doc_pretinent_selectionne = [] # selectioner le t
    doc = {}
    seuil = 3
    t = 10  # doc retournés   #######because m testing with 
    # calculate the internal product of query  and all docs 
    # get t first best docs depending on internal product ...
    for i in range(len(all_docs)-1):
        doc[i]=internal_product(inverse_doc_matrix, i+1 , query)
    doc = sorted(doc.items(), key = lambda kv: kv[1])
    i=0
    while( i<len(doc)):
        if (doc[i][1]>seuil):
            doc_pretinent_total.append(doc[i])
        i+=1
    doc_pretinent_selectionne = doc_pretinent_total[len(doc_pretinent_total)-t:]
    if len(doc_pretinent_total)== 0:
        return 0
    return len(doc_pretinent_selectionne)/len(doc_pretinent_total)
    
    
def precision_dice(inverse_doc_matrix, all_docs, query): 
         
    doc_pretinent_total = [] # sup a seuil  {'num de doc ' : val (rsv) }
    doc_pretinent_selectionne = [] # selectioner le t
    doc = {}
    seuil = 3
    t = 10  # doc retournés   #######because m testing with 
    # calculate the internal product of query  and all docs 
    # get t first best docs depending on internal product ...
    for i in range(len(all_docs)-1):
        doc[i]=dice(inverse_doc_matrix, i+1 , query)
    doc = sorted(doc.items(), key = lambda kv: kv[1])
    i=0
    while( i<len(doc)):
        if (doc[i][1]>seuil):
            doc_pretinent_total.append(doc[i])
        i+=1
    doc_pretinent_selectionne = doc_pretinent_total[len(doc_pretinent_total)-t:]
    if len(doc)== 0:
        return 0
    return len(doc_pretinent_selectionne)/len(doc)
     
def rappel_dice(inverse_doc_matrix, all_docs, query):
        
    doc_pretinent_total = [] # sup a seuil  {'num de doc ' : val (rsv) }
    doc_pretinent_selectionne = [] # selectioner le t
    doc = {}
    seuil = 3
    t = 10  # doc retournés   #######because m testing with 
    # calculate the internal product of query  and all docs 
    # get t first best docs depending on internal product ...
    for i in range(len(all_docs)-1):
        doc[i]=dice(inverse_doc_matrix, i+1 , query)
    doc = sorted(doc.items(), key = lambda kv: kv[1])
    i=0
    while( i<len(doc)):
        if (doc[i][1]>seuil):
            doc_pretinent_total.append(doc[i])
        i+=1
    doc_pretinent_selectionne = doc_pretinent_total[len(doc_pretinent_total)-t:]
    if len(doc_pretinent_total)== 0:
        return 0
    return len(doc_pretinent_selectionne)/len(doc_pretinent_total)
    
    
def precision_cosinus(inverse_doc_matrix, all_docs, query):
         
    doc_pretinent_total = [] # sup a seuil  {'num de doc ' : val (rsv) }
    doc_pretinent_selectionne = [] # selectioner le t
    doc = {}
    seuil = 3
    t = 10  # doc retournés   #######because m testing with 
    # calculate the internal product of query  and all docs 
    # get t first best docs depending on internal product ...
    for i in range(len(all_docs)-1):
        doc[i]=cosinus(inverse_doc_matrix, i+1 , query)
    doc = sorted(doc.items(), key = lambda kv: kv[1])
    i=0
    while( i<len(doc)):
        if (doc[i][1]>seuil):
            doc_pretinent_total.append(doc[i])
        i+=1
    doc_pretinent_selectionne = doc_pretinent_total[len(doc_pretinent_total)-t:]
    if len(doc)== 0:
        return 0
    return len(doc_pretinent_selectionne)/len(doc)
       
def rappel_cosinus(inverse_doc_matrix, all_docs, query):   
    doc_pretinent_total = [] # sup a seuil  {'num de doc ' : val (rsv) }
    doc_pretinent_selectionne = [] # selectioner le t
    doc = {}
    seuil = 3
    t = 10  # doc retournés   #######because m testing with 
    # calculate the internal product of query  and all docs 
    # get t first best docs depending on internal product ...
    for i in range(len(all_docs)-1):
        doc[i]=cosinus(inverse_doc_matrix, i+1 , query)
    doc = sorted(doc.items(), key = lambda kv: kv[1])
    i=0
    while( i<len(doc)):
        if (doc[i][1]>seuil):
            doc_pretinent_total.append(doc[i])
        i+=1
    doc_pretinent_selectionne = doc_pretinent_total[len(doc_pretinent_total)-t:]
    if len(doc_pretinent_total)== 0:
        return 0
    return len(doc_pretinent_selectionne)/len(doc_pretinent_total)
    
    
def precision_jaccard(inverse_doc_matrix, all_docs, query):
    doc_pretinent_total = [] # sup a seuil  {'num de doc ' : val (rsv) }
    doc_pretinent_selectionne = [] # selectioner le t
    doc = {}
    seuil = 3
    t = 10  # doc retournés   #######because m testing with 
    # calculate the internal product of query  and all docs 
    # get t first best docs depending on internal product ...
    for i in range(len(all_docs)-1):
        doc[i]=jaccard(inverse_doc_matrix, i+1 , query)
    doc = sorted(doc.items(), key = lambda kv: kv[1])
    i=0
    while( i<len(doc)):
        if (doc[i][1]>seuil):
            doc_pretinent_total.append(doc[i])
        i+=1
    doc_pretinent_selectionne = doc_pretinent_total[len(doc_pretinent_total)-t:]
    if len(doc)== 0:
        return 0
    return len(doc_pretinent_selectionne)/len(doc)
     
     
def rappel_jaccard(inverse_doc_matrix, all_docs, query):
    doc_pretinent_total = [] # sup a seuil  {'num de doc ' : val (rsv) }
    doc_pretinent_selectionne = [] # selectioner le t
    doc = {}
    seuil = 3
    t = 10  # doc retournés   #######because m testing with 
    # calculate the internal product of query  and all docs 
    # get t first best docs depending on internal product ...
    for i in range(len(all_docs)-1):
        doc[i]=jaccard(inverse_doc_matrix, i+1 , query)
    doc = sorted(doc.items(), key = lambda kv: kv[1])
    i=0
    while( i<len(doc)):
        if (doc[i][1]>seuil):
            doc_pretinent_total.append(doc[i])
        i+=1
    doc_pretinent_selectionne = doc_pretinent_total[len(doc_pretinent_total)-t:]
    if len(doc_pretinent_total)== 0:
        return 0
    return len(doc_pretinent_selectionne)/len(doc_pretinent_total)
    
    
'''
print(precision_internal_product(inverse_doc_matrix, l , 'programs and computers'))
print(rappel_internal_product(inverse_doc_matrix, l , 'programs and computers'))
print(precision_cosinus(inverse_doc_matrix, l , 'programs and computers'))
print(rappel_cosinus(inverse_doc_matrix, l , 'programs and computers'))
print(precision_dice(inverse_doc_matrix, l , 'programs and computers'))
print(rappel_dice(inverse_doc_matrix, l , 'programs and computers'))
print(precision_jaccard(inverse_doc_matrix, l , 'programs and computers'))
print(rappel_jaccard(inverse_doc_matrix, l , 'programs and computers'))
'''
    

