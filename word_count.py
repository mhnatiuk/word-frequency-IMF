
# This program is licesned under GNU/GPL 2.0
## Simple word counter
##
from __future__ import print_function
from collections import defaultdict
import os
import re
import nltk
from nltk.stem.wordnet import WordNetLemmatizer

def getKeys(lines):
    lmtzr = WordNetLemmatizer() #Lemmatizer instance 
    keys = dict() 
    #print ("LEN:" + str(len(lines)))
    for line in lines: #loop over each line and  decide whether it's a single word or a phrase if latter than treat the rest of the
			#words as a value to a key
        phrase = line.split(' ') 
        """
        if(len(phrase)>1):
            keys[(phrase[0])] = (" ".join(phrase[1:])) #lemmatize each word to make sure that the stop-word is a base form of this word
    	else:
            keys[(phrase[0])] = "" 
        """
        
    	if(len(phrase)>1):
            keys[lmtzr.lemmatize(phrase[0],'v')] = lmtzr.lemmatize(" ".join(phrase[1:]),'v') #lemmatize each word to make sure that the stop-word is a base form of this word
    	else:
            keys[lmtzr.lemmatize(phrase[0],'v')] = "" 
        
    #print(keys)
    return keys


def countKeywords(tokens,keys):
    lmtzr = WordNetLemmatizer() #Lemmatizer instance
    wordcounter = defaultdict(int)
    for i in range(0,len(tokens)): # loop over each token in the given string
        token = tokens[i] # current token
        nexttoken = None #next token : to deal with multiple-words stop phrase
        if i < len(tokens)-1: #make sure we don't read list element outside of the list
            nexttoken = tokens[i+1]
        lmt = lmtzr.lemmatize(token,'v') # lemmatize the token
        if lmt in keys: # if token is on the stopwords list than process it
            if keys[lmt] == "": #check whether it's a one-word phrase or multi-
	    		pass
            else:
                if keys[lmt] == nexttoken:
    			    lmt =  lmt + lmtzr.lemmatize(nexttoken,'v')
            wordcounter[lmt] += 1
       
    #print the data table
    for key in sorted(keys.iterkeys()):
        print("{};".format(wordcounter[key]),end='')
	


### Open keyfile to construct file header
keyfile = open('word-markers.txt','r')

lines = [line.strip() for line in keyfile]
keys = getKeys(lines)
print ("file;text-length;",end='') # First two columns header: name of the file and text-length in chars
for key in sorted(lines):
	# Print the rest of columns
	print ("{};".format(key),end='')

# Loop over current directory
for filename in os.listdir('.'):
    content = '' # content container
    #If filename does contain digits and '.txt' than process it
#    if re.search(r'^\d+\.txt', filename):
    if re.search(r'^\d+\.txt$', filename):
        fh = open(filename, 'rb')
        for line in fh:
            content += line
	    #Replace non-ascii files to deal with strange txt format that Adobe Reader produced
        content = content.decode('ascii', 'replace').replace(u'\ufffd', ' ')
	    # Tokenize the whole string
        tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+|[^\w\s]+')
        tokens = tokenizer.tokenize(content)
	    # print first two columns
        print ("\n{};{};".format(re.sub('\.txt','',filename),len(content)),end='')
	    #count the words
        wordcount = countKeywords(tokens,keys)

