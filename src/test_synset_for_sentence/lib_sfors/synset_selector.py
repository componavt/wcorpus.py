#!/usr/bin/python
# synset_selectory.py

from __future__ import division # https://stackoverflow.com/a/21317109/1173350

# (Algorithm 1) Select synset for the sentence using average similarity (model.n_similarity)
def selectSynsetForSentenceByAverageSimilarity( sent, sentences, synsets, model ):
    """
    Select synset for the sentence using average similarity.
        (1) sent is current sentence
        (2) for each synset
        (3)     calculate dist( lemmas of sentence, synonyms of synset)
        (4) select the most similar synset to sentence lemmas (where "dist" is Cosine similarity)
    
    Parameters
    ----------
    sent : current sentence index in the multi-array sentences[][]
    model : object (Word2Vec model).
        
    Returns
    -------
    updates the argument 'sentences' (list of objects)
    """
    positive_answer = 0 # 1 if an answer of expert is the same
    negative_answer = 0 # 1 in other case

    lemma = sentences[sent]['lemma']
    if len(sentences[sent]['lemmas']) > 0 :
        max_d = 0
        max_i = 0
#        print "LEMMA LIST:", ', '.join(sentences[sent]['lemmas'])
#        print "EXPERT ANSWER:", ', '.join(synsets[lemma][sentences[sent]['synset_exp']])
        for synset_id in synsets[lemma]:
            if len(synsets[lemma][synset_id]) > 0 :
                d = abs(model.n_similarity(sentences[sent]['lemmas'], synsets[lemma][synset_id]))
#                print d, ':', ', '.join(synsets[lemma][synset_id])
                if d > max_d:
                    max_d = d
                    max_i = synset_id
#            else :
#                print synset_id, 'synset is empty'

        if (max_i == 0): # there is no best synset (e.g. lemmas list of sentence is empty)
            sentences[sent]['synset_alg1'] = '-'
            sentences[sent]['alg1_right'] = '-'
        else:
            sentences[sent]['synset_alg1'] = max_i
            if sentences[sent]['synset_exp'] == max_i:
                sentences[sent]['alg1_right'] = 1
                positive_answer = 1
            else: 
                sentences[sent]['alg1_right'] = 0
                negative_answer = 1
#        print sentences[sent]['alg1_right'];
#    else:
#        print 'Lemma list empty'
#    print "best synset id=", str(max_i)+',', " with maximum similarity d=", str(max_d)
    
    return positive_answer, negative_answer


# Epsilon: 0.5, right answers: 588, wrong answers: 693
# Epsilon: 0.5, right answers: 596, wrong answers: 685

# (Algorithm 2) Select synset for the sentence using average similarity (model.n_similarity)
def selectSynsetForSentenceByAlienDegree( sent, sentences, synsets, model, eps):
    """
    Select synset for the sentence calculating ratio of different words 
    to the number of similar words in a sentence and synset.
        (1) sent is current sentence
        (2) for each synset
        (3)     calculate number of similar( lemmas of sentence, synonyms of synset) > eps
        (4) select the synset with the minimum alien degree.
    
    Parameters
    ----------
    sent : current sentence index in the multi-array sentences[][]
    model : object (Word2Vec model).
        
    Returns
    -------
    updates the artument sentences (list of objects)
    """
    positive_answer = 0 # 1 if an answer of expert is the same
    negative_answer = 0 # 1 in other case

#    print "\n\nSENTENCE:", sent
    lemma = sentences[sent]['lemma']
    
    if 0 == len(sentences[sent]['lemmas']) :
#        print 'Lemma list empty'
        return positive_answer, negative_answer

    alien_degree_min = 1000     # number of words (pairs from sentence and synset) which are far from each other
    alien_degree_synset = 0     # synset id? What synset? 
#    print "LEMMA LIST:", ', '.join(sentences[sent]['lemmas'])
#    print "EXPERT ANSWER:", ', '.join(synsets[lemma][sentences[sent]['synset_exp']])
    for synset_id in synsets[lemma]:
        near_set = set()        # unique close elements from sentence and synset
        alien_degree = '';
        
        if 0 == len(synsets[lemma][synset_id]) :
#            print synset_id, 'Synset is empty'
            continue

        for sent_lemma in sentences[sent]['lemmas']:
            for syns_lemma in synsets[lemma][synset_id]:
                d = model.n_similarity([sent_lemma], [syns_lemma])
                if d > eps:
                    near_set.add(sent_lemma)
                    near_set.add(syns_lemma)
#                    print u"+ d=sim(sent_lemma, syns_lemma) | {}=sim({}, {})".format( d, sent_lemma, syns_lemma)
#                else:
#                    print u"- d=sim(sent_lemma, syns_lemma) | {}=sim({}, {})".format( d, sent_lemma, syns_lemma)
        all_set = set(sentences[sent]['lemmas']).union(set(synsets[lemma][synset_id]))
        far_set = all_set.difference(near_set)
        alien_degree =  len(far_set) / (1 + len(near_set))   
#        print alien_degree, ':', ', '.join(synsets[lemma][synset_id])
        if alien_degree < alien_degree_min:
            alien_degree_min = alien_degree
            alien_degree_synset = synset_id
#        print "all_set:", ', '.join(all_set)
#        print "near_set:", ', '.join(near_set)
#        print "far_set:", ', '.join(far_set)
#        print "alien_degree:", str(alien_degree)
            
    if (alien_degree_min == 1000):
        sentences[sent]['synset_alg2'] = '-'
        sentences[sent]['alg2_right'] = '-'
    else:
        sentences[sent]['synset_alg2'] = alien_degree_synset
        if sentences[sent]['synset_exp'] == alien_degree_synset:
            sentences[sent]['alg2_right'] = 1
            positive_answer = 1
        else: 
            if sentences[sent]['alg2_right'] == '':
                sentences[sent]['alg2_right'] = 0
            negative_answer = 1
#    print sentences[sent]['alg2_right']

    return positive_answer, negative_answer

# (Algorithm 3, modified 1) Select synset for the sentence using average similarity (model.n_similarity)
def selectSynsetForSentenceByAverageSimilarityModified( sent, sentences, lemma_synsets, model, eps ):
    """
    Select synset for the sentence using average similarity.
        (1) sent is current sentence
        (2) filter words of sentences and synonyms of synset,
        (3)     remain only similar words: similarity( lemma of sentence, synonym of synset) > eps
        (4) select the most similar synset to sentence lemmas (where "dist" is Cosine similarity)
    
    Parameters
    ----------
    sent : current sentence index in the multi-array sentences[][]
    model : object (Word2Vec model).
        
    Returns
    -------
    updates the argument sentences (list of objects)
    """
    positive_answer = 0 # 1 if an answer of expert is the same
    negative_answer = 0 # 1 in other case

    if 0 == len(sentences[sent]['lemmas']) :
        return positive_answer, negative_answer

    max_sim = 0
    best_synset = '' # id of synset which is most similar to sentence
    for synset_id in lemma_synsets:
        S_k = set()     # words of sentence which are similar to some synonyms
        Cand_k = set()  # synonyms of synset which are similar to some words of sentence
        for sent_lemma in sentences[sent]['lemmas']:    # for each word from sentence
            for syns_lemma in lemma_synsets[synset_id]:  # for each synonym from synset
                d = model.n_similarity([sent_lemma], [syns_lemma])
                if d > eps:
                    S_k.add(sent_lemma)
                    Cand_k.add(syns_lemma)
        if len(S_k) > 0 and len(Cand_k) > 0:
            sim_k = model.n_similarity(list(S_k), list(Cand_k))
            if sim_k > max_sim:
                max_sim = sim_k
                best_synset = synset_id
    sentences[sent]['synset_alg3'] = best_synset
    if sentences[sent]['synset_exp'] == sentences[sent]['synset_alg3']:
        sentences[sent]['alg3_right'] = 1
        positive_answer = 1
    else:
        if sentences[sent]['alg3_right'] == '':
            sentences[sent]['alg3_right'] = 0
        negative_answer = 1

    return positive_answer, negative_answer # return 0, 1 or 1, 0

