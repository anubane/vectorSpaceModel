##########################################
##-----------Anurag Banerjee------------##
##---------------CS 7030----------------##
##-----------  Assignment 2  -----------##
##########################################

import string
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer, SnowballStemmer


# Some global variables
# path_to_data = "data//sci.med.train//"
# path_to_data = "workData2//"     # we are building index for this doc collection
path_to_data = "workData//"
docCount = 0
docIdList = []


def next_file_name_in(dirName):    # this is a simple generator function to read and return names of each file in dirName
    for filename in os.listdir(dirName):
        yield str(filename)


def stemmer(sentence):
    wordList = sentence.split()
    # stemProcessor = PorterStemmer()
    stemProcessor = SnowballStemmer('english')
    stemmedList = map(lambda x: unicode(stemProcessor.stem(x)).encode('UTF-8', 'strict'), wordList)   # ).encode('UTF-8')
    return stemmedList


def lemmatizer(sentence):       # super slow, so not using
    wordList = sentence.split()
    lemmatizer = WordNetLemmatizer()
    lemmatizedList = map(lambda x: unicode(lemmatizer.lemmatize(x)).encode('UTF-8', 'strict'), wordList)
    return lemmatizedList


def sentenceCleaner(sentence):
    stop_words = set(stopwords.words('english'))

    sentence = sentence.lower()
    sentence = sentence.translate(None, string.punctuation)
    word_tokens = word_tokenize(sentence)
    filtered_words = [w for w in word_tokens if w not in stop_words]

    return " ".join(filtered_words)


def read_file(nextFile):     # read a file and return a tuple of filename and nested list
    file_word_list = []   # list of wordlists
    filePath = path_to_data + nextFile
    try:
        with open(filePath, 'r') as inFile:   # , open('outputFile.txt', 'w') as outFile:
            # print("Performing Data cleaning and stemming...")
            for line in inFile.readlines():
                line = sentenceCleaner(line)    # clean whitespaces and punctuations
                # wordList = stemmer(line)        # now we have a list of stemmed words
                wordList = lemmatizer(line)
                file_word_list.append(wordList)

    except Exception as e:
        print "In file "+filePath
        print "Some God forsaken error happened!"
        raise e

    return (nextFile, file_word_list)   # returns the filename and nested list


def buildDocTerm():
    docTermDict = {}
    global docCount
    print("Building the Document-Term Matrix...")
    for nextFile in next_file_name_in(path_to_data):     # this works
        docCount += 1
        (docid, fileTerms) = read_file(nextFile)
        docTermDict[docid] = {}
        for termList in fileTerms:
            for term in termList:
                if term in docTermDict[docid]:
                    docTermDict[docid][term] += 1
                else:
                    docTermDict[docid][term] = 1
        docIdList.append(nextFile)
    return docTermDict


def buildInvIndx(docTermDict):
    tempInvIndx = {}
    invIndx = {}
    print("Building the inverted Term-Document index...")
    for docid, termDict in docTermDict.items():
        for term in termDict.keys():
            if term not in tempInvIndx:
                tempInvIndx[term] = {docid: docTermDict[docid][term]}
            else:
                tempInvIndx[term][docid] = docTermDict[docid][term]
    for term, valueDict in tempInvIndx.items():
        df = len(valueDict)
        invIndx[term] = [df, valueDict]
    return invIndx


def displayInvIndx(invIndxDict):
    for term in sorted(invIndxDict.keys()):
        print ("{} --> {}".format(term, invIndxDict[term]))


def writeInvIndxToFile(invIndxDict):
    # yet to implement
    pass


def getAllDocIds():
    return docIdList


def test():     # we write all our module testing code here
    # print stemmer(["walking", "read", "eatery", "notice", "gobble"])
    # print sentenceCleaner("This  >> << == -- ++   walking, read!  eatery;  : ~ `notice? \"gobble\"")
    for nextFile in next_file_name(path_to_data):     # this works
        # print "New File"
        docid = read_file(nextFile)[0]
        fileTerms = read_file(nextFile)[1]
        buildDocTerm(docid, fileTerms)
    # print(docTermDict)
    buildInvIndx(docTermDict)

    #pass


def main():     # we write all our starting code here
    docTermDict = buildDocTerm()
    invIndx = buildInvIndx(docTermDict)

    displayInvIndx(invIndx)

    writeInvIndxToFile(invIndx)


if __name__ == '__main__':
    # test()
    main()


# EOF

