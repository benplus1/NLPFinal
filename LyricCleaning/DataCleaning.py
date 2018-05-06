import csv
import numpy as np
import pandas as pd
import re
import cmudict
import random
import pronouncing
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize


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
					#line = line.lower().strip("!@#$%^&*()_+-={}[];:\,.<>/\?")
					line = re.sub(r'[^a-zA-Z0-9_\'\ ]', '', line.lower())
					self.cleanedLyrics.append(line)

	def exportLyrics(self):
		out = csv.writer(open("cleanedLyrics2.csv","w", encoding='utf-8'), delimiter=',')
		out.writerow(self.cleanedLyrics)

	def getLyrics(self):
		# print("inside")
		testFile = pd.read_csv("cleanedLyrics2.csv", engine='python', header=None)
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

		for key in list(countDict):
			if countDict[key] < 11:
				del countDict[key]
				i -= 1

		self.wordCountDictionary = [(j,countDict[j]) for j in countDict]
		self.wordCountDictionary.sort(key=lambda x: x[1], reverse=True)
		self.occurenceDictionary = countDict
		j = 0
		self.trainingDict = []
		for x in self.wordCountDictionary:
			if x[1] <= 30:
				self.trainingDict.append(x[0])
		# print("Num of 1s: %d" % j)
		# print("len of list: %d" % len(self.wordCountDictionary))
		# print(self.wordCountDictionary)
		# self.wordCountDictionary = countDict
		self.wordList = list(countDict.keys())
		with open("file.txt", "w") as output:
			for word in countDict.keys():
				output.write(word + "\n")
		self.numUniqueWords = i
		# print("Num of words: %d\n" % i)

	def plotUniqueWords(self, orientation="v"):

		if orientation == "h":
			values = reversed([x[1] for x in self.wordCountDictionary[:40]])
			keys = reversed([str(x[0]) for x in self.wordCountDictionary[:40]])
			plt.barh(range(40), list(values))
			plt.yticks(range(40), list(keys))
			plt.show()
		else:
			values = ([x[1] for x in self.wordCountDictionary[:40]])
			keys = ([str(x[0]) for x in self.wordCountDictionary[:40]])
			plt.bar(range(40), list(values))
			plt.xticks(range(40), list(keys))
			plt.show()


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


	def findRhymingWord1(self, inputWord):
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

	def findRhymingWord(self, inputWord):
		rhymingWords = pronouncing.rhymes(inputWord)
		maxWords = min(5, len(rhymingWords))
		if(maxWords == 0):
			return "hello"
		randomNum = (random.randrange(0,maxWords))
		return rhymingWords[randomNum]

	# def tryCMUDict(self, inputWord=""):
		# print(self.rhymingDict["benjamin"][0])
		# print(len(self.keysInDict))


class HMM:
	def __init__(self, rapLyrics, fileName="cleanedLyrics2.csv"):
		self.probs = np.array((rapLyrics.numUniqueWords, rapLyrics.numUniqueWords))
		self.words = rapLyrics.wordsList
		f = open(fileName, "r+")
		for line in f:
			arr = line.split()
			for i in range(1, len(arr)):
				indexCurr = self.words.index(arr[i]) if arr[i] in self.words else None
				indexPrev = self.words.index(arr[i-1]) if arr[i-1] in self.words else None
				if (indexCurr!=None and indexPrev!= None):
					self.probs[indexCurr, indexPrev] += 1
		self.normprobs = normalize(self.probs, axis=1, norm='l1')
		self.totalindexes = self.normprobs.size

	def exportHMM(self):
		np.savetxt('normprobs.txt', self.normprobs, fmt='%1.3f')
		np.savetxt('probs.txt', self.probs, fmt='%1.3f')


rapLyrics = LyricsData()
rapLyrics.cleanLyrics()
rapLyrics.countUniqueWords()
rapLyrics.plotUniqueWords(orientation='v')
hmm = HMM(rapLyrics)
print(hmm.totalindexes)
print("Done")