import csv
import numpy as np
import pandas as pd
import re
import cmudict
import random
import pronouncing
# import markovify

class LyricsData:

	def __init__(self, fileName = "lyrics.csv"):
		self.removePunct = re.compile(":|\[|\(|chorus|verse")
		self.actualFile = pd.read_csv(fileName, encoding="ISO-8859-1", engine='python')
		self.cleanedLyrics = list()

		self.rhymingDict = cmudict.dict()
		self.keysInDict = sorted(self.rhymingDict)
		self.markovString = ""

		# print(self.actualFile["lyrics"][0])

	def cleanLyrics(self):
		for song in self.actualFile["lyrics"]:
			for line in song.split('\n'):
				if (not self.removePunct.search(line)) and (len(line) < 80) and (len(line) > 20):
					line = line.lower().strip("!@#$%^&*()_+-={}[];:\,.<>/\?")
					self.cleanedLyrics.append(line)

	def exportLyrics(self):
		out = csv.writer(open("cleanedLyrics.csv","w"), delimiter=',')
		out.writerow(self.cleanedLyrics)

	def getLyrics(self):
		# print("inside")
		testFile = pd.read_csv("cleanedLyrics.csv", engine='python', header=None)
		# print(testFile)

	def countUniqueWords(self):
		countDict = {}
		i = 0
		for lines in self.cleanedLyrics:
			for word in lines.split():
				if word in countDict:
					countDict[word] += 1
				else:
					countDict[word] = 1
					i += 1

		self.wordCount = [(j,countDict[j]) for j in countDict]
		self.wordCount.sort(key=lambda x: x[1])
		self.wordList = list(countDict.keys())
		self.numUniqueWords = i
		# print("Num of words: %d\n" % i)

	def numberOfSharedPhones(self, inputWord, randomWord):
		if len(self.rhymingDict[inputWord]) == 0 or len(self.rhymingDict[randomWord]) == 0:
			return 0

		inputWordPhones = self.rhymingDict[inputWord]
		randomWordPhones = self.rhymingDict[randomWord]

		currGreatestMatches = 0
		for inputPhones in inputWordPhones:
			for currInputPhone in reversed(inputPhones):
				k=0
				currPhoneFound = False
				for randomPhones in randomWordPhones:
					if(currPhoneFound):
						break

					for currRandomPhone in reversed(randomPhones):
						if currInputPhone == currRandomPhone:
							# print("%s %s %s %s " % (currInputPhone, currRandomPhone, inputPhones, randomPhones))
							randomPhones.remove(currRandomPhone)
							k+=1
							currPhoneFound = True
							
				if k > currGreatestMatches:
					currGreatestMatches = k
		print("%s %d" % (randomWord, currGreatestMatches))
		# print("Num of matching phones: %d" % (k))
		return currGreatestMatches


	def findRhymingWord(self, inputWord):
		currList = {}
		maxWords = self.numUniqueWords
		randomNums = [(random.randrange(0, maxWords)) for i in range(0, maxWords)]

		mostSharedPhones = 0
		wordWithMostSharedPhones = ""
		for i in range(0,maxWords):
			currWord = self.wordList[randomNums[i]]

			if self.numberOfSharedPhones(inputWord, currWord) >= mostSharedPhones:
				# print("Word with most: %s %d" % (currWord, mostSharedPhones))
				wordWithMostSharedPhones = currWord
				mostSharedPhones = self.numberOfSharedPhones(inputWord, currWord)

		print("Most shared phones: %d for word: %s" % (mostSharedPhones, wordWithMostSharedPhones))
		print("%s %s" % (wordWithMostSharedPhones,self.rhymingDict[wordWithMostSharedPhones]))
		print("%s %s" % (inputWord, self.rhymingDict[inputWord]))
		print("num shared: %d" % self.numberOfSharedPhones(inputWord, wordWithMostSharedPhones))

	def markovModel():
		print()


	# def rhyme(inp, level):
	# 	entries = nltk.corpus.cmudict.entries()
	# 	syllables = [(word, syl) for word, syl in entries if word == inp]
	# 	rhymes = []
	# 	for (word, syllable) in syllables:
	# 		rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
	# 	return set(rhymes)

	# def tryCMUDict(self, inputWord=""):
		# print(self.rhymingDict["benjamin"][0])
		# print(len(self.keysInDict))



				
rapLyrics = LyricsData()
rapLyrics.cleanLyrics()
rapLyrics.countUniqueWords()
# print(pronouncing.rhymes("hello"))
# rapLyrics.findRhymingWord()
