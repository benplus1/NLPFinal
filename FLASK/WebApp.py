from flask import Flask, request, render_template
import re
import pronouncing
import random
import numpy as np

app = Flask(__name__)
normprobs = np.loadtxt("normprobs.txt", delimiter=',', ndmin=2)
print(normprobs[0][0])
print(normprobs[0])
print(np.amax(normprobs[0]))
wordList = []
with open("file.txt", "r") as output:
    for line in output:
        wordList.append(line)

print(wordList[0])


def findRhymingWord(inputWord):
    rhymingWords = pronouncing.rhymes(inputWord)
    maxWords = min(5, len(rhymingWords))
    if (maxWords == 0):
        return "orange"
    randomNum = (random.randrange(0, maxWords))
    return rhymingWords[randomNum]

@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    text = re.sub(r'[^a-zA-Z0-9_\'\s]', '', text.lower())
    arr = text.split()
    finalWord = arr[len(arr)-1]
    print(arr)
    print(finalWord)
    finalWord = findRhymingWord(finalWord)
    print(finalWord)
    currWord = finalWord
    returnThis = finalWord
    for i in range(1, len(arr)):
        print("in loop\n")
        currIndex = normprobs.index(currWord) if currWord in normprobs else None
        #currIndex = normprobs.index(currWord)
        if (currIndex == None) :
            currIndex = random.randint(1,25734)
        print(normprobs[currIndex])
        max = np.argmax(normprobs[currIndex])
        nextword = wordList[max]
        currWord = nextword
        returnThis = nextword + returnThis

    return returnThis