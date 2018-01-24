#!/usr/bin/env python
# -*- coding: utf-8 -*-

# for each word from Russian Wiktionary, which have synonyms and which is presented in RusVectores

# 1. Get the word w (vector v)
# 2. Word w -> vector v -> vector -v -> word -w.
# 3. Find a word which has vector nearest to the vector -v (vector v of word w)
#       -> v_near_negative = model.most_similar (top_n = 1,  similar words, distance from -w <= Epsilon)
# 4. result = sim( v, v_near_negative )

import logging
import sys
import os
import operator

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim.models import Word2Vec, keyedvectors
import numpy as np

from scipy import spatial # Cosine similarity calculation

sys.path.append(os.path.abspath('../')) # add parent folder, access to 'lib'
import lib.filter_vocab_words
import lib.string_util
import lib.synset
import lib.average_vector
import lib.epsilon_neighborhood

import configus
model = keyedvectors.KeyedVectors.load_word2vec_format(configus.MODEL_PATH, binary=True)


print "__________________Read data from SYNSETS________________"
sys.path.append(os.path.abspath('../data/word_syn')) # add folder with synsets, access to 'synset_synonyms.py'
from synset_synonyms import word_syn

#for w in word_syn:
#    # word_syn[w]   # word's synonyms
#    synonyms_string = lib.string_util.joinUtf8( ", ", word_syn[w] )
#    print u" synonym( {} ) = ( {} )".format( w, synonyms_string )
#    break

#lib.filter_vocab_words.filterSynsets( synsets, model.vocab ) # filter synsets, remove words absented in RusVectores

# ruscorpora
# 0.3 too noisy... try 0.45

#news
#eps_plus = 0.35
#eps_minus = 0.12

i = 0

#word_epsilons = dict() # dictionary of WordSim's objects

print u"source_word (v), nearest_word (nearest to -v)"
print u"v near sim(-v, near) sim(v, near)" # .format( source_word, negative_nearest_word, sim, result )
#print u"{} {} {} {}".format( source_word, negative_nearest_word, sim, result )

#for word in model.vocab:
for word in word_syn:
    if word.lower() not in model.vocab:
        continue    # word is absent in RusVectores 
    i += 1
    dist = lib.epsilon_neighborhood.getDistanceToNearestNegative( word.lower(), model, np, word_syn )
    
    # do not store words with 0.0 distance (it is special return value - failed)
    #print u" word={}, dist (v, -v)={}, abs dist={}".format( word, dist, abs(dist) )
    
    #if abs(dist) > 0.000001:
    #    print
    #    print u" word={}, dist (v, -v)={}".format( word, dist )
    #    word_epsilons[ word ] = dist
    
    #sys.exit("\nLet's stop and think.")
    
    #break;
    #if i > 30:
    #    break


#sorted_words_by_eps = sorted(word_epsilons.items(), key=operator.itemgetter(1))

#print 
#print "Similarity from positive to negative set sim( eps(w), eps(-w) ) -----------"
#for _word_sim in sorted_words_by_eps:
    
#   print u" word={}, dist (v, -v)={}".format( _word_sim[0], _word_sim[1] )
    #print u" word={}".format( _word_sim )
    #print u" word={}, dist (v, -v)={}".format( _word_sim, sorted_words_by_eps [_word_sim] )