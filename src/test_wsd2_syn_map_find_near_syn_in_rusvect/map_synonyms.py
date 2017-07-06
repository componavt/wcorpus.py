#!/usr/bin/env python
# -*- coding: utf-8 -*-

# if duration > duration_limit_sec seconds, then calculations for the line of text is interrupted.

duration_limit_sec = 4

import logging
import sys

import os
from os import listdir
from os.path import isfile, join

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim.models import word2vec, keyedvectors
import numpy as np
import re
import itertools

sys.path.append(os.path.abspath('../')) # add parent folder, access to 'lib'
import lib.filter_vocab_words
import lib.string_util
#import lib.synset
import lib.average_vector

#from data.word_syn.synonyms_data import word_syn # small local synonyms
#from data.word_syn.synset_synonyms import word_syn
from data.word_syn.synset_antonyms import word_syn
#from data.word_syn.synset_hyponyms import word_syn
#from data.word_syn.synset_hypernyms import word_syn

import configus
model = keyedvectors.KeyedVectors.load_word2vec_format(configus.MODEL_PATH, binary=True)

import time

#source_text = u'ОН ПЛОТНЫЙ ЗАСТЕГНУТЬ СВОЙ ЛЁГКИЙ ПИДЖАЧОК ВЕТЕР ПРОНИЗЫВАТЬ ЕГО НАСКВОЗЬ'
source_text = u'пасть|пал|палый, битва|батон, престол, племянник, оно, котор, могущество'
#source_text = u'УЖЕ НЕСКОЛЬКО ЛЕТ ГОСТЕПРИИМНЫЙ ТЮРЬМА НА ОСТРОВ СЛУЖИТЬ ОН ЗИМНИЙ КВАРТИРА'

read_path  = "/data/all/projects/git/wcorpus.addon/src.addon/sentences/sentences3_rusvectores_filtered"

onlyfiles = [f for f in listdir(read_path) if isfile(join(read_path, f))]

i = 0
for filename in onlyfiles:
    # filename = '10102.txt'
    i += 1
    file_path       = os.path.join(read_path, filename)
    print u"{0}. {1}".format(i, file_path);

    lines = [line.rstrip('\n') for line in open(file_path)]
    for source_text in lines:
        source_text = source_text.decode('utf-8')
        # print "Text = " + source_text
        sys.stdout.write('+') # every new line of text is a "+"
        sys.stdout.flush()

        # split text to words[]
        delim = ' \n\t,.!?:;';  # see http://stackoverflow.com/a/790600/1173350
        sentence_words = re.split("[" + delim + "]", source_text.lower())
        sentence_words = filter(None, sentence_words)           # remove empty strings
        #print "Words in sentence: " + u', '.join(sentence_words)

        # first rebirth: let's remain only first variant of lemmatizer :( other variants dissolved
        # пасть|пал|палый -> пасть, (remain only first word now)
        sw = []
        for w in sentence_words:
            if '|' in w:
                piped_words = re.split("[|]", w)
                # sw.extend (piped_words)
                sw.append (piped_words [0] )                   # remain only first lemmatizer's word now
                #print "Piped words: " + u', '.join( piped_words )
                #print "Piped words [0]: " + piped_words[0]
            else:
                sw.append (w)
        sentence_words = sw
        # print "Words in new sentence (without|pipes) : " + u', '.join(sentence_words)

        # let's filter out words without vectors, that is remain only words, which are presented in RusVectores dictionary
        words = lib.filter_vocab_words.filterVocabWords( sentence_words, model.vocab )
        #print "Words in RusVectores: " + u', '.join(words)


        # replace several words in sentence by synonyms from word_syn (replace w_remove by w_add), try all combinations of synonyms
        start_time = time.time()
        duration = 0
        generated_sentences_counter = 0
        for target_word in words:
            sentences_list = list()

            # print "target word: " + target_word

            # sentence without target word
            sentence_minus_target = words[:]
            sentence_minus_target.remove( target_word )
            ## print "Words in sentence without target word: " + u', '.join(sentence_minus_target)

            # calculate sentence average vector
            average_sentence = lib.average_vector.getAverageVectorForWords( sentence_minus_target, model, np )
            # print "sentence average_vector: {}".format( average_sentence )

            # get list of synonyms of words from sentence, invert subset of map word_syn
            synonyms_to_word = dict()
            for w in sentence_minus_target:
                # print u'Next word w: {}'.format( w )
                if w in word_syn:
                    # print u"    word_syn[w] = {}".format( word_syn[w] )
                    for syn in word_syn[w] :
                        # print u'        syn: {}'.format( syn )
                        if syn in model.vocab:
                            synonyms_to_word[ syn ] = w

            # print "Synonyms of words in sentence: " #+ u', '.join(synonyms_to_word)
            #for syn, w in synonyms_to_word.items():
            #    print u"    synonym <- word   '{}' <- '{}'".format( syn, w)

            # all combinations of synonyms of words in sentence without the target word, 
            # every combination of synonyms will replace words in sentence
            i = 0
            synonyms = list(synonyms_to_word.keys())
            #print "Synonyms of words in sentence: " + u', '.join(synonyms)

            for L in range(0, len(synonyms)+1):

                for subset in itertools.combinations(synonyms, L):
                    # print u'{0} {1}'.format(i, ', '.join(subset))

                    sentence = sentence_minus_target[:] # copy words from sentence_minus_target
                
                    # replace subset in sentence_minus_target by synonyms from our dictionary (word_syn)
                    for syn in subset:
                        w_remove = synonyms_to_word[ syn ]  # w_remove does exists in word_syn, since all keys of synonyms_to_word are presented in model.vocab 
                        # print u'    word remove ({0}), synonym add ({1})'.format(w_remove, syn)
                        while w_remove in sentence: 
                            sentence.remove( w_remove )
                            sentence.append( syn )

                    # check that this is new sentence, skip repetitions
                    new_sentence = True

                    ss = set(sentence)
                    for phrase in sentences_list:
                        if phrase == ss:
                            new_sentence = False
                            break
                    if new_sentence:
                        sentences_list.append( ss ) 
                        i += 1
                        # print u'{0} {1}'.format(i, ', '.join(sentence)) # with synonyms instead of words

                duration = time.time() - start_time
                if duration > duration_limit_sec:
                    #print "Break, break, break, break, break, break ....."
                    break

            if duration > 20:
                sys.stdout.write('-'), # every interruption of calculation is "-"
                sys.stdout.flush()
                #print "2222222222222222222 break, break, break, break, break ....."
                break
                #print("--- %s seconds ---" % (duration))

            generated_sentences_counter += len(sentences_list)

            i = 0
            for words_with_syn in sentences_list:

                # calculate sentence with synonyms without target word average vector
                average_sentence_with_syn_wotarget = lib.average_vector.getAverageVectorForWords( words_with_syn, model, np )

                vect_target_syn = model[ target_word ] - average_sentence + average_sentence_with_syn_wotarget
                # print "vect_target_syn: {}".format( vect_target_syn )

                arr_target_synonyms = model.similar_by_vector(vect_target_syn, topn=1, restrict_vocab=None)

                # print results
                # print "Calculated target synonyms: " + u', '.join(arr_target_synonyms)
                i += 1
                target_synonym = arr_target_synonyms[0][0]
                # print u"target word={0}, target synonym '{1}'".format(target_word, target_synonym) 
                if target_synonym != target_word:
                    print "target word: " + target_word
                    print "Synonyms of words in sentence: " + u', '.join(synonyms)
                    print "Words in sentence without target word: " + u', '.join(sentence_minus_target)
                    print u"{0} {1}  target word:'{2}', synonym found:'{3}', similarity={4}".format(i, ', '.join(words_with_syn), target_word, target_synonym, arr_target_synonyms[0][1]) 
                # print u'{0} {1}'.format(arr_target_synonyms[0][0], arr_target_synonyms[0][1])

                # sys.exit("\nLet's stop and think.")
                
            # print u'{0} sentences were generated by synonyms substitutions.'.format(generated_sentences_counter)

    sys.exit("\nLet's stop and think.")



