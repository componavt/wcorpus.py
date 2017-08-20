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



# Filters words, skip words which are absent in the vocabulary 'vocab'.
# word_similarity_list is a list (([word1][similarity1]),  ([word2][similarity2]), ...)
def filterVocabWordSimilarity( word_similarity_list, vocab ):
    "Skip words which are absent in the model vocabulary"    
    
    # result filtered list
    result = []
    
    for word_similarity in word_similarity_list:
        
        w = word_similarity [0]
        
        if w in vocab:
            result.append( word_similarity )
            
        #if w not in vocab:
        #if w.decode('UTF-8') not in vocab:
        #    word_list.remove( w )
        #    print u"My KeyError: '{}' does not indexed by word2vec model.".format( w )
        #else:
        #    print u"OK. '{}' indexed by word2vec model.".format( w )
    
    return result
