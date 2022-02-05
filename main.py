def readfile(filename):
    file = open(filename, "r")
    words = []
    for word in file.readlines():
        words = addToList(word[:-1], words)
    file.close()
    return words


def addToList(word, list):
    for item in list:
        if word == item:
            return list
    list.append(word)
    return list


def doubleLetterCheck(words):
    noDoubles = []
    # Checks word for double letters and if word has 5 unique letters, it adds the word to a separate list
    for word in words:
        letters = []
        for letter in word:
            if letter not in letters:
                letters = addToList(letter, letters)
        if len(letters) == 5:
            noDoubles = addToList(word, noDoubles)
    return noDoubles


def guessPositioning(words, bestWords, letterIndex, finalWord):
    global lettersInWord
    guessedWord = input("What was your word? ")

    while len(guessedWord) != 5 or guessedWord not in words:
        guessedWord = input("That is not a valid guess. What was your word? ")

    # asks how many letters are green and then saves those letters into final word
    correctPosition = input("Which position letters were green (1-5)? (0 for none) ")
    while "6" in correctPosition or "7" in correctPosition or "8" in correctPosition or "9" in correctPosition:
        correctPosition = input("Invalid number. Which position letters were green (1-5)? (0 for none) ")
    if correctPosition != "0":
        for number in correctPosition:
            number = int(number)
            letterIndex.remove(number)
            finalWord[number - 1] = guessedWord[number - 1]

    # asks how many letters are yellow and saves those letters into lettersInWord
    correctLetter = input("Which position letters were yellow (1-5)? (0 for none) ")
    while "6" in correctPosition or "7" in correctPosition or "8" in correctPosition or "9" in correctPosition:
        correctPosition = input("Invalid number. Which position letters were yellow (1-5)? (0 for none) ")
    if correctLetter != "0":
        for number in correctLetter:
            number = int(number)
            letterIndex.remove(number)
            lettersInWord = addToList([guessedWord[number - 1], number], lettersInWord)

    # deletes all words with incorrect letters
    for word in words:
        letterCount = 0
        for index in letterIndex:
            letter = guessedWord[index - 1]
            if letter not in word:
                letterCount += 1
            if letterCount == len(letterIndex):
                bestWords = addToList(word, bestWords)

    words = bestWords
    bestWords = []

    # removes incorrect letters from bestLetters
    for index in letterIndex:
        letter = guessedWord[index - 1]
        if letter in bestLetters:
            bestLetters.remove(letter)

    # Checks all words which have the same letter placing as final words and then those words become the best words list
    for word in words:
        letterCount = 0
        letterPlace = 0
        for letter in finalWord:
            if letter.isalpha():
                if word[letterPlace] == letter:
                    letterCount += 1
            else:
                letterCount += 1
            letterPlace += 1
        if letterCount == 5:
            bestWords = addToList(word, bestWords)

    words = bestWords
    bestWords = []

    # Checks all words which have the same letters as the final word and then those words become the best words list
    if len(lettersInWord) > 0:
        for word in words:
            letterCount = 0
            for letter in lettersInWord:
                if letter[0] not in word:
                    continue
                if letter[0] != word[letter[1]-1]:
                    letterCount += 1
                if letterCount == len(lettersInWord):
                    bestWords = addToList(word, bestWords)

        words = bestWords
        bestWords = []

    # Puts the best words to guess in a list
    for word in words:
        wordTotal = 0
        for letter in word:
            wordTotal += bestLetters.index(letter)
        if wordTotal < 50:
            bestWords = addToList(word, bestWords)

    # Shows the best words to guess
    print("The best words are:")
    print(bestWords)
    print()
    bestWords = []

    letterIndex = [1, 2, 3, 4, 5]

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
words, bestWords, letterIndex, finalWord = guessPositioning(words, bestWords, letterIndex, finalWord)
words, bestWords, letterIndex, finalWord = guessPositioning(words, bestWords, letterIndex, finalWord)
words, bestWords, letterIndex, finalWord = guessPositioning(words, bestWords, letterIndex, finalWord)
words, bestWords, letterIndex, finalWord = guessPositioning(words, bestWords, letterIndex, finalWord)
