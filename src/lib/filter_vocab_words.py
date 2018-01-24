#!/usr/bin/python

# Filters words, skip words which are absent in the vocabulary 'vocab' (RusVectores).
def filterVocabWords( word_list, vocab ):
    "Skip words which are absent in the model vocabulary"
    
    # result filtered list
    result = []
    
    #print u"First word in the vocabulary: '{}'".format(vocab[0])

    for w in word_list:
        if w.lower() in vocab:
            result.append(w)
            
        #if w.decode('utf8') not in vocab:
        #if w.lower() not in vocab:
        #    word_list.remove( w )
            #print u"My KeyError: '{}' does not indexed by word2vec model.".format( w )
        #else:
        #    print u"OK. '{}' indexed by word2vec model.".format( w )
    
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


# Filters synsets, removes words absented in RusVectores.
# Result returned in the synsents argument.
def filterSynsets( synsets, vocab ):
    "Remove synonyms absented in the model vocabulary"

    for lemma in synsets:
        for synset_id in synsets[lemma]:
            filtered_list = filterVocabWords( synsets[lemma][synset_id], vocab )
            if len(filtered_list) < 2:
                print u"\n{}".format( lemma )
                print 'OLD LIST:', ', '.join(synsets[lemma][synset_id])
                print 'DELETED:', ', '.join(diff(synsets[lemma][synset_id],filtered_list))
                print 'NEW SYNSET:', ', '.join(filtered_list)
            synsets[lemma][synset_id] = filtered_list
