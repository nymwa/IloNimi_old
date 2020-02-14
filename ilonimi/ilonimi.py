import sys
import re
import numpy as np
from collections import Counter

class IloNimi:
	instance = None
	def __new__(cls):
		if cls.instance is None:
			cls.instance = super().__new__(cls)
			punctuations = '!"#\$%&\'\(\)\*\+,-\.:;<=>\?@\[\\\\\]\^_`{\|}~“„'
			cls.tag_list = '[PAD] [UNK] [CLS] [SEP] [MASK]'.split(' ')
			cls.punct_list = '! " # $ % & \' ( ) * , - . / : ; < = > ? @ [ \\ ] ^ _ ` { | } ~'.split(' ')
			cls.word_list = 'a akesi ala alasa ale ali anpa ante anu apeja awen e en esun ijo ike ilo insa jaki jan jelo jo kala kalama kama kan kasi ken kepeken kijetesantakalu kili kin kipisi kiwen ko kon kule kulupu kute la lape laso lawa leko len lete li lili linja lipu loje lon luka lukin lupa ma majuna mama mani meli mi mije moku moli monsi monsuta mu mun musi mute namako nanpa nasa nasin nena ni nimi noka o oko olin ona open pakala pake pali palisa pan pana pata pi pilin pimeja pini pipi poka poki pona pu sama seli selo seme sewi sijelo sike sin sina sinpin sitelen sona soweli suli suno supa suwi tan taso tawa telo tenpo toki tomo tu unpa uta utala walo wan waso wawa weka wile'.split(' ')
			cls.vocab_list = cls.tag_list + cls.punct_list + cls.word_list
			cls.vocab_set = set(cls.vocab_list)
			cls.left_punct_pattern  = re.compile(r'(?<=[^\s])([{}])'.format(punctuations, punctuations))
			cls.right_punct_pattern = re.compile(r'([{}])(?=[^\s])'.format(punctuations, punctuations))
			cls.space_pattern = re.compile(r'\s+')
			cls.proper_pattern = re.compile(r'^([AIUEO]|[KSNPML][aiueo]|[TJ][aueo]|W[aie])n?(([ksnpml]?[aiueo]|[tj][aueo]|w[aie])n?)*$')
		return cls.instance

	def is_proper(self, x):
		return self.proper_pattern.match(x)

	def split_punct(self, x):
		x = self.left_punct_pattern.sub(' \\1', x)
		x = self.right_punct_pattern.sub('\\1 ', x)
		return x

	def tag(self, x):
		if x in self.tag_list:
			return 'tag'
		elif x in self.punct_list:
			return 'punct'
		elif x in self.vocab_list:
			return 'word'
		elif self.is_proper(x):
			return 'proper'
		elif x.isdecimal():
			return 'number'
		else:
			return 'unk'

	def __call__(self, x):
		x = x.strip()
		x = self.split_punct(x)
		x = self.space_pattern.sub(x, ' ')
		x = x.split(' ')
		print('S {}'.format(' '.join(x)))
		for w in x:
			print('W {}\t{}'.format(w, self.tag(w)))
		print('EOS\n')

	def convert_unk(self, x):
		x = [w if w in self.vocab_set or self.is_proper(w) or w.isdecimal() else '[UNK]' for w in x]
		return x

