##########################################
##-----------Anurag Banerjee------------##
##---------------CS 7030----------------##
##-----------  Assignment 4  -----------##
##########################################

from __future__ import division
from operator import itemgetter
import indexer
import string
import re
import numpy as np

'''
In this program we will show the working of the VSM Model for search

0. create query vector
1. From Document Term Matrix - create doc vectors
2. tw = (1+ln(tf))*(ln(N/df))   # tf from docterm matrix, N = number of docs in which term present, df from inverse
3. normalize all sqrt(sum(sqr(w_i)))    <--- skipped this
4. calculate cosine similarity between query and each doc
5. high value of cos similarity=> high rank
6. show top fifteen docs
'''


# The global variables
rows = 0    # number of documents in collection
cols = 0    # number of unique terms in collection
docList = []    # List of all documents in collection to provide integer count to name mapping
termList = []
termDfList = []


def getQuery():
    """
    This functions asks user to input a query and cleans/stems it.
    :return:
    """
    queryString = raw_input("Enter your query: ")
    queryString = queryString.translate(None, string.punctuation)     # removing all punctuation except parenthesis
    temp = ""
    for char in queryString:
        if char.isspace() or char.isalnum():
            temp += char
        else:
            temp += ' '+char+' '
    queryString = temp.strip()
    queryString = re.sub(ur' +', ' ', queryString.lower())    # remove extra spaces
    return indexer.stemmer(queryString)    # now performing stemming and returning list of terms in query


def getDocIndex():
    """
    In this dummy function we will simply call upon the functions we built in the indexer.py file
    :return:
    """
    docTermDict = indexer.buildDocTerm()    # the doc term matrix in a python dictionary
    termDocDict = indexer.buildInvIndx(docTermDict)     # the inverted, term-doc matrix in a python dictionary

    return (docTermDict, termDocDict)


def createQueryVector(qList):
    """
    This functions returns a vector for the query.
    :return:
    """
    global termList, termDfList, docList
    qVec = np.zeros((1, cols))
    for term in qList:
        index = termList.index(term)
        if termDfList[index]:
            qVec[0][termList.index(term)] = np.log(len(docList)/termDfList[index])
        else:
            qVec[0][termList.index(term)] = np.log(len(docList))
    return qVec


def createDocVectors(qTermList, docTermDict, termDocDict):
    """
    We will create the document vectors here
    :return: the inverted term-document index
    """
    global rows, cols, docList, termList, termDfList
    # modifying term-doc matrix for query terms not in collection
    for term in qTermList:
        if term not in termDocDict:
            termDocDict[term] = [0, {}]

    rows = len(docTermDict.keys())
    cols = len(termDocDict.keys())
    docList = [doc for doc in sorted(docTermDict.keys())]   # list of docs
    termList = [term for term in sorted(termDocDict.keys())]    # list of terms
    termDfList = [termDocDict[term][0] for term in sorted(termDocDict.keys())]

    print("Building the Document Vectors...")
    docVecs = np.zeros((rows, cols))
    for (docIndx, docId) in enumerate(docList):
        for term in docTermDict[docId].keys():
            docVecs[docIndx][termList.index(term)] = (1 + np.log(docTermDict[docId][term]))*(np.log(len(docList)/termDfList[termList.index(term)]))
    # print docVecs
    return docVecs


def rankDocAndShow(docScore, count):
    """
    This function will essentially sort my documents according to the score and display top fifteen
    :param docScore:
    :return:
    """
    global docList, rows
    '''sort_permutation = np.argsort(docScore)
    sorted_docList = docList[sort_permutation]'''
    # docScore (rows, 1), docList(rows,)
    print "Ranking the results..."
    docListnumpy = np.array(docList)
    joined = np.column_stack((docScore, docListnumpy.reshape(rows, 1)))
    # sorted_docList = np.sort(joined, axis=-1)
    sorted_docList = np.array(sorted(joined, key=itemgetter(0), reverse=True))

    print "Top fifteen documents for your query are:\n"
    for i in range(count):
        print "Rank."+str(i+1)+": "+sorted_docList[i][1]+"\t(match score: "+sorted_docList[i][0]+")"


def vsmsearch(qList, docTermDict, termDocDict):
    """
    In this function we will call functions to build the vectors, calculate similarity, and rank docs
    :param qList:
    :param docTermDict:
    :param termDocDict:
    :return:
    """
    global rows, cols
    docVec = createDocVectors(qList, docTermDict, termDocDict)
    qVec = createQueryVector(qList)
    # --------------------------------------------------------
    print "Looking for documents matching your query..."
    docScore = np.zeros((rows, 1))
    for i in range(rows):
        docScore[i] = np.asscalar(np.dot(qVec, docVec[i].reshape(cols, 1))) / (np.linalg.norm(docVec[i].reshape(1, cols)) * np.linalg.norm(qVec))
    rankDocAndShow(docScore, 15)
    # print "Done!"


def test():
    '''qList = getQuery()
    (docTermDict, termDocDict) = getDocIndex()
    docVec = createDocVectors(qList, docTermDict, termDocDict)
    qVec = createQueryVector(qList)
    print qVec'''
    pass


def main():
    """

    :return:
    """
    (docTermDict, termDocDict) = getDocIndex()
    ch = 'x'
    while ch != '2':
        ch = raw_input("\nEnter 1 to fire query\n\t\t2 to exit:")
        if ch == '1':
            qList = getQuery()
            vsmsearch(qList, docTermDict, termDocDict)
        elif ch not in ('1', '2'):
            print "\nWrong input! Try again."
            ch = 'x'


if __name__ == '__main__':
    # test()
    main()

# EOF


