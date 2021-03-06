#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Filter lemmas in source files. Remain only words which are presented in RusVectores dictionary.
# Remain sentences only with 5 words or more.
# Remain texts with 10 or more lines of sentences, which words are presented in RusVectores
# Remain only sentences with serveral variants generated by lemmatizer (with pipe '|').

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

#from synonyms_data import word_syn # small local synonyms
#from synset_synonyms import word_syn
#from synset_antonyms import word_syn
#from synset_hyponyms import word_syn
#from synset_hypernyms import word_syn

import configus
model = keyedvectors.KeyedVectors.load_word2vec_format(configus.MODEL_PATH, binary=True)


# script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
#abs_dir_path       = "/data/all/projects/git/wcorpus.addon/src.addon/sentences/sentences2_lemmas" 
#abs_dir_path_write = "/data/all/projects/git/wcorpus.addon/src.addon/sentences/sentences3_rusvectores_filtered"

abs_dir_path       = "/data/all/projects/git/wcorpus.addon/src.addon/sentences.short/sentences2_lemmas.short" 
abs_dir_path_write = "/data/all/projects/git/wcorpus.addon/src.addon/sentences.short/sentences3_rusvectores_filtered.short"

#abs_dir_path       = os.path.join(script_dir, read_path )
#abs_dir_path_write = os.path.join(script_dir, write_path)
onlyfiles = [f for f in listdir(abs_dir_path) if isfile(join(abs_dir_path, f))]

i = 0
for filename in onlyfiles:
    # filename = '10102.txt'
    i += 1
    file_path       = os.path.join(abs_dir_path,       filename)
    file_path_write = os.path.join(abs_dir_path_write, filename)
    print u"{0}. {1}".format(i, file_path);
    print u" . {0}".format( file_path_write );

    output_lines = []
    lines = [line.rstrip('\n') for line in open(file_path)]
    remark_line = ""
    for source_text in lines:
        source_text = source_text.decode('utf-8')
        if len(source_text) > 0:
            if "#" == source_text[:1]:          # REM, line starts from "#",
                remark_line = source_text
                continue                        # get next line

        # print source_text

        result_words = []

        # split text to words[]: брать|берет, начать|начало, слободской|слободский
        words_with_pipe = re.split("[, ]", source_text)
        words_with_pipe = filter(None, words_with_pipe) # remove empty elements
        # print "Words (with pipe) in sentence: " + u', '.join(words_with_pipe)

        for w in words_with_pipe:
            a = ''
            if '|' in w:
                words = re.split("[|]", w)
                # print "Piped words: " + u', '.join(words)
                words = lib.filter_vocab_words.filterVocabWords( words, model.vocab )
                a = u'|'.join(words)
            else:
                if w in model.vocab:
                    a = w
            result_words.append( a )

        result_words = filter(None, result_words) # remove empty elements
        if len(result_words) > 4:
            result_line = u', '.join(result_words)
            if '|' in result_line:                  # remain only sentences with serveral variants generated by lemmatizer (with pipe '|')
                output_lines.append( remark_line )  
                remark_line = ""
                output_lines.append( result_line )
                #print u"Filtered result: {0}".format(result_line)

    if len(output_lines) > 9:
        result_text = u'\n'.join(output_lines)
        file_out = open(file_path_write, 'w')
        file_out.write( result_text.encode('utf-8') )
        file_out.close()


    # sys.exit("\nLet's stop and think.")
