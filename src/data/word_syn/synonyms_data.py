#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Dictionary[word] := [array of synonyms]
word = u'плотный'
synonyms = [ u'густой',
                u'светонепроницаемый', 
                u'частый', u'сплошной',
                u'толстый', u'массивный',
                u'крепкий', u'сбитый', u'упитанный', u'полный',
                u'обильный', u'сытный']

word_syn = {word : synonyms}

word_syn[u'-де']=[u'грит',u'гыт',u'де',u'дескать',u'дискать',u'мол',u'молвил',u'стало быть']
word_syn[u'-ей']=[u'-е-',u'-ше-',u'ее|-ее-]]']
word_syn[u'-енциj']=[u'-анциj']

word_syn [u'ветер'] = [ 
                u'дуновение']

word_syn [u'пронизывать'] = [ 
                u'нанизывать', u'низать',
                u'продевать',
                u'продырявливать', u'протыкать', u'пронзать',
                u'проникать', u'пропитывать']



# our synonyms --------------------------------------------------------------
word_syn [u'застегнуть'] = [ 
                u'запахнуть', u'одеться'] # u'закрыться' absent in RusVectores 
word_syn [u'пиджачок'] = [ 
                u'пиджак', u'одежда', u'сюртук']
word_syn [u'насквозь'] = [ 
                u'сквозь', u'навылет']
# ----------------------------------------------------------- eo our synonyms



word_syn [u'несколько'] = [ 
                u'немного',
                u'слегка']

word_syn [u'служить'] = [ 
                u'работать',
                u'подчиняться', u'работать', u'помогать', u'угождать', u'содействовать',
                u'прислуживать', u'повиноваться',
                u'использоваться', u'являться', u'предназначаться'
                ]
