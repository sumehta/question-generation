#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 14:04:55 2017

@author: sneha
"""
import os
import re
import subprocess
from os.path import dirname


class QuestionGenerator(object):
	"""
	Define a class that generates questions given an input text file
	or a db connection. Currently supported db connection is mongodb.
	"""
	def __init__(self, input_file=None, mongod_collection=None):
		"""
		Arguments:

			input_file: A text file containing input statements
			to be converted to questions. One statement per line.

			mongod_collection: The reference to the mongodb
			 collection object from which to retrieve the statements from.
		"""
		if input_file:
			self.input_file=input_file
			print("Reading from file")

		if mongod_collection:
			self.mongod_collection=mongod_collection
			print("Reading from mongodb")

		os.chdir(os.path.join(os.path.dirname(__file__), 'QuestionGeneration'))

	def _get_raw_output(self, input_sentence):
		"""
		Invokes the QuestionGenerator Java class to generate questions given a declarative statement.
		Runs the command "java -Xmx1200m -cp question-generation.jar \
						edu/cmu/ark/QuestionAsker --verbose --model models/linear-regression-ranker-reg500.ser.gz \
						--prefer-wh --max-length 30 --downweight-pro"
		Arguments:
			input_sentence: The declarative statement to be converted to a question. Should be in bytes.

		Returns:
			The relatively free-form output consisting of question followed by its answer followed by the
			score for that question.

		"""
		# This commands requires the question_generation package.
		# command = "java -Xmx1200m -cp question-generation.jar \ edu/cmu/ark/QuestionAsker --verbose --model models/linear-regression-ranker-reg500.ser.gz --prefer-wh --max-length 30 --downweight-pro"

		p = subprocess.Popen(['bash', 'run.sh'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
		output = p.communicate(input=input_sentence)[0]
		return output.decode()

	def generate_question(self, sentence, question_types=['Wh', 'Are', 'How', 'Do']):
		"""
		An utility method that generates a question for a single sentence
		Arguments:
			sentence: The sentence for which to generate question
			question_types: The types of questions to be generated. Options include,
			`Wh`, `Are`

		Returns:
			A list of lists of length of `question_types`
			Each list contains questions of the corresponding type.
		"""
		output = self._get_raw_output(bytearray(sentence, 'utf-8'))

		results = []

		try:
			q_a_pairs = output.split('\n')[3:]
		except:
			exit('No viable questions generated! Please try a different sentence.')

		for ty in question_types:
			for q_a in q_a_pairs:
				if re.match(r"{}\w+|\W\?".format(ty), q_a):
					results.append({'Q': q_a.split('\t')[0], 'A': q_a.split('\t')[1]})
		return results


	def generate_sentence_question_pairs(self):
		"""
		Generator that yields the sentence along with the generated question for that sentence

		Returns:
			Yields a dictionary containing the `id` same as the id of the sentence from the collection,
			`text` the sentence and `questions` a list of `Wh` type questions.
		"""
		# Mongodb collection should have data in the format {`id`: <id> , `text`, <text>}
		pattern = re.compile(r"(Wh[^.?!]*)\\?")

		if self.mongod_collection:
			print("Reading data from the collection")
			for obj in self.mongod_collection.find():
				output = self._get_raw_output(bytearray(obj['text'], 'utf-8'))
				result = pattern.findall(output)
				yield {'id': obj['id'], 'text': obj['text'], 'questions': result}
