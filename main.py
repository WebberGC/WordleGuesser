def readfile(filename):
    file = open(filename, "r")
    words = []
    for word in file.readlines():
        words.append(word[:-1])
    file.close()
    return words

def doubleLetterCheck(words):
    noDoubles = []
    # Checks word for double letters and if word has 5 unique letters, it adds the word to a separate list
    for word in words:
        letters = []
        for letter in word:
            if letter not in letters:
                letters.append(letter)
        if len(letters) == 5:
            noDoubles.append(word)
    return noDoubles


def guessPositioning(words, bestWords, letterIndex, finalWord):
    guessedWord = input("What was your word? ")

    # asks how many letters are green and then saves those letters into final word
    correctPosition = int(input("How many letters were green? "))
    for number in range(1, correctPosition + 1):
        letterPosition = int(input("What position is the letter (1-5)? "))
        letterIndex.remove(letterPosition)
        finalWord[letterPosition - 1] = guessedWord[letterPosition - 1]

    # asks how many letters are yellow and saves those letters into lettersInWord
    correctLetter = int(input("How many letters were yellow? "))
    for number in range(1, correctLetter + 1):
        letterPosition = int(input("What position is the letter (1-5)? "))
        letterIndex.remove(letterPosition)
        lettersInWord.append(guessedWord[letterPosition - 1])

    # deletes all words with incorrect letters
    for word in words:
        letterCount = 0
        for index in letterIndex:
            letter = guessedWord[index - 1]
            if letter not in word:
                letterCount += 1
            if letterCount == len(letterIndex):
                bestWords.append(word)

    words = bestWords
    bestWords = []

    # removes incorrect letters from bestLetters
    for index in letterIndex:
        letter = guessedWord[index - 1]
        bestLetters.remove(letter)

    # Checks all words which have the same letter placing as final words and then those words become the best words list
    letterCount = 0
    for letter in finalWord:
        if letter.isalpha():
            for word in words:
                if word[letterCount] == letter:
                    bestWords.append(word)
        letterCount += 1

    words = bestWords
    bestWords = []

    # Checks all words which have the same letters as the final word and then those words become the best words list
    for word in words:
        letterCount = 0
        for letter in lettersInWord:
            if letter in word:
                letterCount += 1
            if letterCount == len(lettersInWord):
                bestWords.append(word)
    words = bestWords
    bestWords = []

    for word in words:
        wordTotal = 0
        for letter in word:
            wordTotal += bestLetters.index(letter)
        if wordTotal < 17:
            bestWords.append(word)

    print("The best words are:")
    print(bestWords)
    print()
    bestWords = []

    return words, bestWords, letterIndex, finalWord


words = readfile("Words")

# letters ranked in order of how common they are in the words
bestLetters = ["e", "a", "r", "o", "t", "i", "l", "s", "n", "u", "c", "y", "h", "d", "p", "g", "m", "b", "f", "k", "w",
               "v", "x", "z", "q", "j"]
finalWord = ["", "", "", "", ""]
lettersInWord = []
letterIndex = [1, 2, 3, 4, 5]
removedLetters = []
bestWords = []

words, bestWords, letterIndex, finalWord = guessPositioning(words, bestWords, letterIndex, finalWord)
words, bestWords, letterIndex, finalWord = guessPositioning(words, bestWords, letterIndex, finalWord)

# for word in noDoubles:
#    wordTotal = 0
#    for letter in word:
#        wordTotal += bestLetters.index(letter)
#    if wordTotal < 15:
#        bestWords.append(word)
