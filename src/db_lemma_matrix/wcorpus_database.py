#!/usr/bin/python

# Finds all words which are similar to words in word_list.
# Searches similar words in the vocabulary 'vocab' of Word2Vec RusVectores.
# topn_around_words - number of nearest words to be searched in model.most_similar()
def findSimilarWords( word_list, vocab, topn_around_words ):
    "Finds words similar to word_list in the model vocabulary (vocab)"
    
    # result set of similar words
    result = set()
    
    for w in word_list:
        add_words_similarity = model.most_similar( w, [], topn_around_words)
        for aws in add_words_similarity:
            result.add( aws[0] )

        ## print u"most_similar ({0}) = {1}".format( w, u', '.join(result) )

    print "findSimilarWords: len(word_list)={0}, len(result)={1}".format( len(word_list), len(result) )
    print "findSimilarWords: found words are " + u', '.join(result) 

    return result
