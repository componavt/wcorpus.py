#!/usr/bin/env python
# -*- coding: utf-8 -*-
sentences = {
	u'Он знал бездну источников, где мог почерпнуть, разумеется заработком.': {
		'lemmas': [u'ОН', u'ЗНАТЬ', u'БЕЗДНА', u'ИСТОЧНИК', u'ГДЕ', u'МОЧЬ', u'ПОЧЕРПНУТЬ', u'РАЗУМЕТЬСЯ', u'ЗАРАБОТОК'],
		'lemma': u'БЕЗДНА',
		'synset_exp': 8,
		'synset_alg1': '',
		'synset_alg2': ''
	},
	u'Он бросал на него злобные взгляды, стараясь, впрочем, чтобы тот их не заметил, и нетерпеливо ожидал своей очереди, когда досадный оборванец уйдет.': {
		'lemmas': [u'ОН', u'БРОСАТЬ', u'НА', u'ОНО', u'ЗЛОБНЫЙ', u'ВЗГЛЯД', u'СТАРАТЬСЯ', u'ВПРОЧЕМ', u'ЧТОБЫ', u'ТОТ', u'ОНИ', u'ИХ', u'НЕ', u'ЗАМЕТИТЬ', u'НЕТЕРПЕЛИВО', u'НЕТЕРПЕЛИВЫЙ', u'ОЖИДАТЬ', u'СВОЙ', u'ОЧЕРЕДЬ', u'КОГДА', u'ДОСАДНЫЙ', u'ОБОРВАНЕЦ'],
		'lemma': u'БРОСАТЬ',
		'synset_exp': 30,
		'synset_alg1': '',
		'synset_alg2': ''
	},
	u'Другая же дама, очень полная и багровокрасная, с пятнами, видная женщина, и что-то уж очень пышно одетая, с брошкой на груди, величиной в чайное блюдечко, стояла в сторонке и чего-то ждала.': {
		'lemmas': [u'ДРУГОЙ', u'ЖЕ', u'ДАМА', u'ОЧЕНЬ', u'ПОЛНЫЙ', u'БАГРОВОКРАСНАЯ', u'БАГРОВОКРАСНЫЙ', u'ПЯТНО', u'ВИДНЫЙ', u'ЖЕНЩИНА', u'ЧТО-ТО', u'УЖ', u'ПЫШНЫЙ', u'ПЫШНО', u'ОДЕТЫЙ', u'ОДЕТЬ', u'БРОШКА', u'НА', u'ГРУДЬ', u'ВЕЛИЧИНА', u'ЧАЙНЫЙ', u'БЛЮДЕЧКО', u'СТОЯЛЫЙ', u'СТОЯТЬ', u'СТОРОНКА', u'ЧЕГО-ТО', u'ЖДАТЬ'],
		'lemma': u'ВИДНЫЙ',
		'synset_exp': 24,
		'synset_alg1': '',
		'synset_alg2': ''
	},
	u'Донесу, матушка…  Старуха завязала блины в узелок и дала сыночку.': {
		'lemmas': [u'ДОНЕСТИ', u'МАТУШКА', u'СТАРУХА', u'ЗАВЯЗАТЬ', u'БЛИН', u'УЗЕЛОК', u'ДАТЬ', u'СЫНОЧЕК'],
		'lemma': u'ДОНЕСТИ',
		'synset_exp': 16,
		'synset_alg1': '',
		'synset_alg2': ''
	},
	u'Она теперь, уже несколько дней, просто в каком-то жару и составила целый проект о том, что впоследствии ты можешь быть товарищем и даже компаньоном Петра Петровича по его тяжебным занятиям, тем более что ты сам на юридическом факультете.': {
		'lemmas': [u'ОНА', u'ТЕПЕРЬ', u'УЖ', u'УЖЕ', u'УЗКИЙ', u'НЕСКОЛЬКО', u'ДЕНЬ', u'ПРОСТО', u'ПРОСТОЙ', u'КАКОЙ-ТО', u'ЖАРА', u'ЖАР', u'СОСТАВИТЬ', u'ЦЕЛЫЙ', u'ПРОЕКТ', u'ТОМ', u'ТОМА', u'ТОТ', u'ЧТО', u'ВПОСЛЕДСТВИИ', u'ТЫ', u'МОЧЬ', u'БЫТЬ', u'ТОВАРИЩ', u'ДАЖЕ', u'КОМПАНЬОН', u'ПЕТР', u'ПЕТРА', u'ПО', u'ОН', u'ЕГО', u'ОНО', u'ТЯЖЕБНЫЙ', u'ЗАНЯТИЕ', u'ТЕМ', u'ТЕМА', u'БОЛЕЕ', u'МНОГО', u'САМ', u'НА', u'ЮРИДИЧЕСКИЙ', u'ФАКУЛЬТЕТ'],
		'lemma': u'ЗАНЯТИЕ',
		'synset_exp': 12,
		'synset_alg1': '',
		'synset_alg2': ''
	},
	u'Это он почувствовал при одном виде Игната и лошадей; но когда он надел привезенный ему тулуп, сел, закутавшись, в сани и поехал, раздумывая о предстоящих распоряжениях в деревне и поглядывая на пристяжную, бывшую верховою, донскую, надорванную, но лихую лошадь, он совершенно иначе стал понимать то, что с ним случилось.': {
		'lemmas': [u'ЭТОТ', u'ЭТО', u'ОН', u'ПОЧУВСТВОВАТЬ', u'ПРИ', u'ПЕРЕТЬ', u'ПРЯ', u'ОДИН', u'ВИД', u'ИГНАТ', u'ЛОШАДЬ', u'НО', u'КОГДА', u'НАДЕЛ', u'НАДЕТЬ', u'ПРИВЕЗЕННЫЙ', u'ПРИВЕЗИТЬ', u'ОНО', u'ТУЛУП', u'СЕСТЬ', u'ЗАКУТАТЬСЯ', u'САНИ', u'САНЯ', u'ПОЕХАТЬ', u'РАЗДУМЫВАТЬ', u'ПРЕДСТОЯЩИЙ', u'ПРЕДСТОЯТЬ', u'РАСПОРЯЖЕНИЕ', u'ДЕРЕВНЯ', u'ПОГЛЯДЫВАТЬ', u'НА', u'ПРИСТЯЖНОЙ', u'ПРИСТЯЖНАЯ', u'БЫТЬ', u'БЫВШИЙ', u'ВЕРХОВЫЙ', u'ВЕРХОВОЙ', u'ДОНСКИЙ', u'ДОНСКОЙ', u'НАДОРВАТЬ', u'ЛИХОЙ', u'СОВЕРШЕННО', u'СОВЕРШЕННЫЙ', u'ИНАЧЕ', u'СТАТЬ', u'ПОНИМАТЬ', u'ТОТ', u'ТО', u'ЧТО', u'ОНИ', u'СЛУЧИТЬСЯ'],
		'lemma': u'ЛИХОЙ',
		'synset_exp': 14,
		'synset_alg1': '',
		'synset_alg2': ''
	},
	u'Вы далеко ль отсюда их нашли?': {
		'lemmas': [u'ВЫ', u'ДАЛЁКИЙ', u'ДАЛЕКО', u'ЛЬ', u'ОТСЮДА', u'ОНИ', u'ИХ', u'НАЙТИ', u'НАСЛАТЬ'],
		'lemma': u'ОТСЮДА',
		'synset_exp': 25,
		'synset_alg1': '',
		'synset_alg2': ''
	},
	u'Да потому что слишком уж все удачно сошлось… и сплелось… точно как на театре.': {
		'lemmas': [u'ДА', u'ПОТОМУ', u'ЧТО', u'СЛИШКОМ', u'УЖ', u'ВЕСЬ', u'ВСЕ', u'УДАЧНО', u'УДАЧНЫЙ', u'СОЙТИСЬ', u'СПЛЕСТИСЬ', u'ТОЧНО', u'ТОЧНЫЙ', u'КАК', u'НА', u'ТЕАТР'],
		'lemma': u'УДАЧНО',
		'synset_exp': 28,
		'synset_alg1': '',
		'synset_alg2': ''
	}
}