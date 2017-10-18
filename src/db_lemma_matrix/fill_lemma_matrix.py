#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Fill wcorpus database table 'lemma_matrix' by data from RusVectores.
# Input: 
#   lemma_matrix.lemma1, 
#   lemma_matrix.lemma2
# Output: 
#   lemma_matrix.sim_ruscorpora, 
#   lemma_matrix.sim_news
# Calculate:
#   sim_ruscorpora = model.n_similarity( lemma1, lemma2 )

import logging
import sys
import os
import MySQLdb

db = MySQLdb.connect(host="localhost",
                     user="wcorpus",
                     passwd="secret",
                     db="wcorpus")

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim.models import word2vec, keyedvectors
import numpy as np
#import re

sys.path.append(os.path.abspath('../')) # add parent folder, access to 'lib'
import lib.filter_vocab_words
import lib.string_util
#import lib.synset
#import lib.average_vector

import configus
model = keyedvectors.KeyedVectors.load_word2vec_format(configus.MODEL_PATH, binary=True)

# Universal part of speech in table wcorpus.pos
pos_universal_to_id = {}

cursor  = db.cursor(MySQLdb.cursors.DictCursor)
cursor2 = db.cursor(MySQLdb.cursors.DictCursor)

# fill pos_universal_to_id
cursor.execute("SELECT * FROM pos WHERE universal IS NOT NULL;")
result_set = cursor.fetchall()
for row in result_set:
    pos_universal_to_id [row['id']] = row['universal']
    #print " {0} : {1}".format( row['id'], row['universal'] )

#print "Database: id : universal"#pos_universal_to_id[1] = 'NOUN'
#for x in pos_universal_to_id:
#    print "{0} : {1}".format( x, pos_universal_to_id[x] )

# SELECT * from lemma_matrix LIMIT 13;
#    lemma1=434, lemma2=58321
# SELECT lemma, pos_id FROM lemmas WHERE id=434;
# SELECT lemma, pos_id FROM lemmas WHERE id=58321;


cursor.execute("SELECT lemma1, lemma2, sim_ruscorpora, sim_news FROM lemma_matrix WHERE sim_ruscorpora IS NULL LIMIT 13;")
result_set = cursor.fetchall()

for row in result_set:
    # row['lemma1'], row['lemma2'], row['sim_ruscorpora'], row['sim_news']
    lemma1_id = row['lemma1']
    lemma2_id = row['lemma2']
    print "Two lemmas id ({0}, {1}), sim_ruscorpora={2}, sim_news={3}".format( lemma1_id, lemma2_id, row['sim_ruscorpora'], row['sim_news'] )

    # SELECT lemma, pos_id FROM lemmas WHERE id IN (434, 58321);
    lemmas_count = cursor2.execute("SELECT lemma, pos_id FROM lemmas WHERE id IN (%s,%s);" % (lemma1_id, lemma2_id) )
    if lemmas_count == 2:
        result_2lemmas = cursor2.fetchall()
        lemma1  = result_2lemmas[0]['lemma']
        lemma2  = result_2lemmas[1]['lemma']
        pos1_id = result_2lemmas[0]['pos_id']
        pos2_id = result_2lemmas[1]['pos_id']
        print u"lemma1,pos1_universal=({0},{1})".format( lemma1, pos1_id )
    #else:
    #    asdf


#for (lemma1, lemma2, sim_ruscorpora, sim_news) in cursor:
#    print "lemma 1 and 2 ({0}, {1}), sim_ruscorpora={2}, sim_news={3}".format( lemma1, lemma2, sim_ruscorpora, sim_news )





cursor.close()
cursor2.close()
db.close()

#words = [u'сосредоточиваться', u'барон', u'ляляляки', u'sssfff']
words = [u'слово_NOUN', u'дело_NOUN', u'ляляляки', u'sssfff']
# todo words = [u'сосредоточиваться', u'барон_NOUN', u'ляляляки', u'sssfff']   # todo: to use _Part_of_speech tags
lemma1 = words[0]
lemma2 = words[1]
print # (word)
#v_word = model[ word ]
#print (v_word)

# let's filter out words without vectors, that is remain only words, which are presented in RusVectores dictionary
words_in_dict = lib.filter_vocab_words.filterVocabWords( words, model.vocab )
#print lib.string_util.joinUtf8( ", ", words_in_dict )
#print u"list of words in RusVectores dictionary: {0}".format( u', '.join(words_in_dict) )

if ( lemma1 in model.vocab and 
     lemma2 in model.vocab     ):
    # calculate similarity
    print u"Words in RusVectores dict: {0}, {1}".format( lemma1, lemma2 )

    sim = model.wv.similarity(lemma1, lemma2)
    print "sim = {:8.7f}".format(sim)
else:
    if lemma1 not in model.vocab:
        print u"!Word '{0}' not in RusVectores dict.".format( lemma1 )
    if lemma2 not in model.vocab:
        print u"!Word '{0}' not in RusVectores dict.".format( lemma2 )

sys.exit("\nLet's stop and think.")



print "\bMax similarity = {:5.3f}".format(sim_max) + ", best synonym: " + best_synonym

# let's scan all words in RusVectores dictionary to find better synonym. Does it exist?
for w_add in model.vocab:

    words_with_syn = [w_add if w == w_remove else w for w in words_in_dict]
    
    sim = model.n_similarity(words_in_dict, words_with_syn)
    if sim > 0.943: # sim_max:
        print "sim = {:5.3f}".format(sim) + ", better synonym: " + w_add
