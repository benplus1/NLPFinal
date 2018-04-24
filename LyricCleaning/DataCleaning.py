import csv
import numpy as np
import pandas as pd
import re


class lyricsData:

	def __init__(self, fileName = "lyrics.csv"):
		self.removePunct = re.compile(":|\[|\(|chorus|verse")
		self.punct = re.compile(u"[^\w'’\.\?!\n]+")
		self.actualFile = pd.read_csv(fileName, encoding="ISO-8859-1", engine='python')
		self.cleanedLyrics = list()
		# print(self.actualFile["lyrics"][0])

	def cleanLyrics(self):
		for song in self.actualFile["lyrics"]:
			for line in song.split('\n'):
				if (not self.removePunct.search(line)) and (len(line) < 80) and (len(line) > 20):
					line = line.lower()
					line = self.punct.sub(' ', line)

					# print(line)
					self.cleanedLyrics.append(line+"\n")

	def exportLyrics(self):
		out = csv.writer(open("cleanedLyrics.csv","w"), delimiter=',')
		out.writerow(self.cleanedLyrics)

	def getLyrics(self):
		print("inside")
		testFile = pd.read_csv("cleanedLyrics.csv", engine='python', header=None)
		print(testFile)


				
rapLyrics = lyricsData()
rapLyrics.cleanLyrics()
rapLyrics.exportLyrics()
# rapLyrics.getLyrics()
# print(rapLyrics.actualFile["lyrics"][0])
