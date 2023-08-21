# Simple extended boolean search engine: query module
# Hussein Suleman and Holly Judge
# 14 April 2016

import re
import math
import sys
import os
import collections
import porter
import parameters
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

query_words=''
stop_words=set(stopwords.words('english'))

# check parameter for collection name
if len(sys.argv)<3:
   print ("Syntax: query.py <collection> <query>")
   exit(0)
 
# construct collection and query
collection = sys.argv[1]
query = ''
arg_index = 2
while arg_index < len(sys.argv):
   query += sys.argv[arg_index] + ' '
   arg_index += 1

print("First search without blind relevance feedback:")

# search function to find top k documents
def search(query):
   # clean query
   if parameters.case_folding:
      query = query.lower ()
   query = re.sub (r'[^ a-zA-Z0-9]', ' ', query)
   query = re.sub (r'\s+', ' ', query)
   query_words = query.split (' ')

   # create accumulators and other data structures
   accum = {}
   filenames = []
   p = porter.PorterStemmer ()

   # get N
   f = open (collection+"_index_N", "r")
   N = eval (f.read ())
   f.close ()

   # get document lengths/titles
   titles = {}
   f = open (collection+"_index_len", "r")
   lengths = f.readlines ()
   f.close ()

   # get index for each term and calculate similarities using accumulators
   for term in query_words:
      if term != '':
         if parameters.stemming:
               term = p.stem (term, 0, len(term)-1)
         if not os.path.isfile (collection+"_index/"+term):
            continue
         f = open (collection+"_index/"+term, "r")
         lines = f.readlines ()
         idf = 1
         if parameters.use_idf:
            df = len(lines)
            idf = 1/df
            if parameters.log_idf:
               idf = math.log (1 + N/df)
         for line in lines:
               mo = re.match (r'([0-9]+)\:([0-9\.]+)', line)
               if mo:
                  file_id = mo.group(1)
                  tf = float (mo.group(2))
                  if not file_id in accum:
                     accum[file_id] = 0
                  if parameters.log_tf:
                     tf = (1 + math.log (tf))
                  accum[file_id] += (tf * idf)
         f.close()

# parse lengths data and divide by |N| and get titles
   for l in lengths:
      mo = re.match (r'([0-9]+)\:([0-9\.]+)\:(.+)', l)
      if mo:
         document_id = mo.group (1)
         length = eval (mo.group (2))
         title = mo.group (3)
         if document_id in accum:
            if parameters.normalization:
               accum[document_id] = accum[document_id] / length
            titles[document_id] = title

   # print top ten results
   global result 
   result= sorted (accum, key=accum.__getitem__, reverse=True)
   for i in range (min (len (result), 13)):
      print ("{0:10.8f} {1:5} {2}".format (accum[result[i]], result[i], titles[result[i]]))

# print top k documents without relevance feedback
search(query)

# read and parse input data - extract words, identifiers and titles
f = open (collection, "r")
identifier = ''
document = ''
title = ''
indocument = False
intitle = False
data = {}
titles = {}
for line in f:
    mo = re.match (r'\.I ([0-9]+)', line)
    if mo:
        if document!='':
            data[identifier] = document
        identifier = mo.group (1)
        indoc = False
    else:
        mo = re.match (r'\.T', line)
        if mo:
           title = ''
           intitle = True
        else:
           mo = re.match (r'\.W', line)
           if mo:
               document = ''
               indoc = True
           else:
               if intitle:
                   intitle = False
                   if identifier!='':
                      titles[identifier] = line[:-1][:50]
               elif indoc:
                   document += " "
                   if parameters.case_folding:
                       document += line.lower()
                   else:
                       document += line    
f.close ()

print("\n")
print("{0:10}".format("Second search using blind relevance feedback:"))
result_document_contents=[]

#append document content from top k results to a list
for item in data:
    if item in result:
        result_document_contents.append(data[item])

all_terms = []
N=5

# extract N common terms
for doc in result_document_contents:
    all_terms += doc.split()
terms = [term for term in all_terms if term not in stop_words]
top_terms = [term for term, count in collections.Counter(terms).most_common(N)]
new_query = query_words + " " + " ".join(top_terms)

# search top k documents using additional terms (relevance feedback)
search(new_query)