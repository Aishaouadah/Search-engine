import os 
import re
import pandas as pd 
import nltk
import numpy as np 
nltk.download('stopwords')
from nltk.corpus import stopwords
import re 


#__1__Indexation des documents
#----------lire le fichier des documents 
ids = []
titles = []
resumies = []


path = "C:\\Users\\User\\Desktop\\M2-S3\\RI\\PROJECT\\cacm\\cacm.all"
with open(path,'r') as cacm:
    # lire ligne par ligne et s'arreter au niveau de l'identificatuer de debut du document
    #lines = cacm.read()
    #lines = lines.strip()
    #print(lines)

    temp = [line for line in cacm.readlines()]
    file = " ".join(temp)
    ## find the I et T and W done : TO BE REFINED 
    ## .B appears sometimes instead of .W: the problem appears when there is no .W in the doc
    ## TO BE FIXED 
    
    i =0
    pattern = "\.([TWBANX]\n|I [0-9]+\n)"

    findW = 1
    while (i != len(temp)):
        r= re.findall(pattern, temp[i]) # premier pattern trouve' 
        ##print(r)
        info = ""
        #print(info)
        i+=1
        while (i != len(temp) and re.findall(pattern, temp[i]) == [] ):
             ## tq on trouve pas un autre, c'est la suite du premier 
             info = info+" "+ temp[i]
             i+=1
        ## classify the info: I, T, W or else 
        if ("I " in r[0]):
            ids.append(r[0])
            if (findW == 1):
                findW= 0
            else:
                resumies.append("") # no resumie for the previous doc, initially it's 1 
            #findT = 0 # the title is not found yet 

        elif ("T" in r[0]):
            titles.append(info)
            #findT =1
            #findW =0
        
        
        elif("W" in r[0]):
            resumies.append(info)
            findW = 1

    
print(len(ids))
print(len(titles))
print(len(resumies))


docs = []
for i in range(len(ids)):
    docs.append(" ".join([titles[i],resumies[i]]))



#--------tokenisations et stoplist + freq de chaque terme dans chaque document 

def find_terms_freq(text):

    #normalise text : write in lowcase 
    text = text.lower()

    #remove ponctuation and special chars 
    text = re.sub('[^A-Za-z0-9]+', " ", text)

    #make a list of all words
    listWord = list(text.split(" "))

    #remove stopwords
    stop_words = set(stopwords.words('english'))

    #fitered list of word 
    listWord = [w for w in listWord if w not in stop_words]



    ########### FIX HERE: NO NEED TO CLACULATE FREQ, JUST DO PRESENCE 
    wordsFreq_dic = {}
    for word in listWord:
        if word not in wordsFreq_dic.keys():
            wordsFreq_dic[word]= 1
        #else:
        #    wordsFreq_dic[word]+= 1

    return wordsFreq_dic



docs_dictionaries  = []

#loop over files and fill dictionaries
for i in range(len(docs)):
    docs_dictionaries.append(find_terms_freq(docs[i]))

#print(docs[2])
#print(docs_dictionaries[2])



#__2__Fichier inverse 

total_words = []

for dic in docs_dictionaries:
    total_words = total_words + list(dic.keys())

# remove duplicates 
total_words = list( dict.fromkeys(total_words) )
total_words = list( dict.fromkeys(total_words) )

inversted_fileDic= {}
for (file, dic) in zip(ids, docs_dictionaries):
    for word in dic.items():
        inversted_fileDic[(file,word[0])] = word[1]

    ## Si le terme n’existe pas dans ce document, sa valeur sera 0.
    for word in total_words:
        if word not in dic.keys():
            inversted_fileDic[(file,word)] = 0

print(" Inverted ")
print(len(inversted_fileDic.keys()))

#__3__Fonctions d'access
# numDoc = doc id

def get_listTermes(numDoc,inversted_fileDic):
    terms_list = []
    freq_list  = [] 
    for item in inversted_fileDic.items():
        if item[0][0] == numDoc+'.txt':
            print('in')
            terms_list.append(item[0][1])
            freq_list.append(item[1])


    return terms_list, freq_list
    

def get_listDocs(term, inversted_fileDic):
    docs_list  = []
    freq_list  = [] 
    for item in inversted_fileDic.items():
        if item[0][1] == term:
            docs_list.append(item[0][0])
            freq_list.append(item[1])

    return docs_list, freq_list



## creer la fct d'appariement

def appariment(doc, requete):
    #q = "t1 and (t2 or not t3)"

    q = requete
    """  remplaçer les termes dans la
    requête par leurs poids dans le
    document (0 ou 1),"""

    req_terms = re.findall("[a-z]+", q.replace(" and ", " ").replace(" or ", " ").replace(" not ", " ").replace("(", "").replace(")", ""))

    #print("Terms")
    #print(req_terms)

    ## get the weight of each term in the request from document doc  
    weights = []
    for term in req_terms:
        weights.append(inversted_fileDic[doc,term])

    ## replace terms by their correponding weights 
    for i in range(len(req_terms)):
        q = re.sub(req_terms[i], str(weights[i]), q)

    #print("Aftre ")
    #print(q)

    return q

def docs_appariment(req):

    print('calculating ... ')
    selected_docs = []
    for doc in ids:
        evaluation = eval(appariment(str(doc), req))
        if (evaluation == 1 ):
            selected_docs.append(doc)
            
    print("Done")
    return selected_docs