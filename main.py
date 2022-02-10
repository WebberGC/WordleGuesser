# function which reads the file and adds all words in the file to a list
def readfile(filename):
    file = open(filename, "r")
    words = []
    for word in file.readlines():
        words = addToList(word[:-1], words)
    file.close()
    return words


# function which adds items to a list
def addToList(word, list):
    for item in list:
        if word == item:
            return list
    list.append(word)
    return list


# function which calculates letter value
def calculateLetterValue(letters, words):
    letterCount = 0  # Counts the placing of each letter, A = 1, B = 2 etc
    values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    firstValues = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    secondValues = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    thirdValues = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fourthValues = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fifthValues = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    valuesList = [firstValues, secondValues, thirdValues, fourthValues, fifthValues]

    # If that letter is in the current word, the placing of that letter in the above list will increase it's value by 1
    for letter in letters:
        for word in words:
            if letter in word:
                values[letterCount] += 1
                for position in range(5):
                    if letter == word[position]:
                        valuesList[position][letterCount] += 1
        letterCount += 1
    return values, valuesList


# Checks word for double letters and if word has 5 unique letters, the function returns True
def doubleLetterCheck(word):
    letters = []
    if len(word) == 1:
        return False
    for letter in word:
        if letter not in letters:
            letters = addToList(letter, letters)
    if len(letters) == len(word):
        return False
    return True


def guessPositioning(words, bestWords, letterIndex, finalWord):
    global lettersInWord
    global letterValues
    global correctPosition
    global allowedGuesses

    # Puts the best words to guess in a list
    letterValues, valuesList = calculateLetterValue(alphabet, words)
    newWordList = []
    if len(allowedGuesses) < 10 or turns >= 3:
        allowedGuesses = words
    for word in allowedGuesses:
        currValue = 0
        for letter in word:
            placing = alphabet.index(letter)
            letterPlacing = word.index(letter)
            currValue += letterValues[placing]
            currValue += valuesList[letterPlacing][placing]
        if doubleLetterCheck(word) is True:
            currValue = int(currValue / 2)
        newWordList.append([word, currValue])
        newWordList.sort(key=lambda x: x[1], reverse=True)

    # Shows the best words to guess
    print("\nThe best words are:")
    rangeNumber = min(len(newWordList), 5)
    for number in range(0, rangeNumber):
        print(str(number + 1) + ".", newWordList[number][0], "-", newWordList[number][1], "points")
    print()
    bestWords = []

    guessedWord = input("What was your word? \n")

    if guessedWord.isnumeric():
        guessedWord = int(guessedWord)
        guessedWord = str(newWordList[guessedWord-1][0])
    else:
        guessedWord.islower()

    guessedWord = str(guessedWord)
    while guessedWord not in words and guessedWord.isnumeric():
        guessedWord = input("That is not a valid guess. What was your word? \n")

        if guessedWord.isnumeric():
            guessedWord = int(guessedWord)
            guessedWord = newWordList[guessedWord - 1]
        else:
            guessedWord.islower()

    print("\nYou selected:", guessedWord)
    # asks how many letters are green and then saves those letters into final word
    correctPosition = input("\nWhich position letters were green (1-5)? (0 for none) ")
    while "6" in correctPosition or "7" in correctPosition or "8" in correctPosition or "9" in correctPosition or \
            doubleLetterCheck(correctPosition) is True or (len(correctPosition) > 1 and "0" in correctPosition) or \
            correctPosition.isalpha():
        correctPosition = input("Invalid number. Which position letters were green (1-5)? (0 for none) ")

    if correctPosition == "12345":
        return words, bestWords, letterIndex, finalWord

    if correctPosition != "0":
        for number in correctPosition:
            number = int(number)
            letterIndex.remove(number)
            finalWord[number - 1] = guessedWord[number - 1]

    # asks how many letters are yellow and saves those letters into lettersInWord
    correctLetter = input("Which position letters were yellow (1-5)? (0 for none) ")
    while "6" in correctPosition or "7" in correctPosition or "8" in correctPosition or "9" in correctPosition or \
            doubleLetterCheck(correctLetter) is True or (len(correctLetter) > 1 and "0" in correctLetter) or \
            correctPosition.isalpha():
        correctLetter = input("Invalid number. Which position letters were yellow (1-5)? (0 for none) ")
    if correctLetter != "0":
        for number in correctLetter:
            number = int(number)
            letterIndex.remove(number)
            lettersInWord = addToList([guessedWord[number - 1], number], lettersInWord)

    # deletes all words with incorrect letters
    for word in allowedGuesses:
        letterCount = 0

        for index in letterIndex:
            letter = guessedWord[index - 1]
            if letter not in word:
                letterCount += 1
            if letterCount == len(letterIndex):
                bestWords = addToList(word, bestWords)

    if len(letterIndex) > 1:
        allowedGuesses = bestWords

    bestWords = []

    for word in words:
        letterCount = 0

        for index in letterIndex:
            letter = guessedWord[index - 1]
            if letter not in word:
                letterCount += 1
            if letterCount == len(letterIndex):
                bestWords = addToList(word, bestWords)

    if len(letterIndex) > 1:
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

    for word in allowedGuesses:
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

    allowedGuesses = bestWords
    bestWords = []

    # Checks all words which have the same letters as the final word and then those words become the best words list
    if len(lettersInWord) > 0:
        for word in words:
            letterCount = 0
            for letter in lettersInWord:
                if letter[0] not in word:
                    continue
                if letter[0] != word[letter[1] - 1]:
                    letterCount += 1
                if letterCount == len(lettersInWord):
                    bestWords = addToList(word, bestWords)

        words = bestWords
        bestWords = []

        for word in allowedGuesses:
            letterCount = 0
            for letter in lettersInWord:
                if letter[0] not in word:
                    continue
                if letter[0] != word[letter[1] - 1]:
                    letterCount += 1
                if letterCount == len(lettersInWord):
                    bestWords = addToList(word, bestWords)

        allowedGuesses = bestWords
        bestWords = []

    letterIndex = [1, 2, 3, 4, 5]

    return words, bestWords, letterIndex, finalWord


# letters ranked in order of how common they are in the words
bestLetters = ["e", "a", "r", "o", "t", "i", "l", "s", "n", "u", "c", "y", "h", "d", "p", "g", "m", "b", "f", "k", "w",
               "v", "x", "z", "q", "j"]
finalWord = ["", "", "", "", ""]
lettersInWord = []
letterIndex = [1, 2, 3, 4, 5]
removedLetters = []
bestWords = []

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
            "v", "w", "x", "y", "z"]
letterValues = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
program = True
correctPosition = ""

while program is True:
    turns = 1
    words = readfile("Words")
    allowedGuesses = readfile("AllowedGuesses")
    finalWord = ["", "", "", "", ""]
    lettersInWord = []
    letterIndex = [1, 2, 3, 4, 5]
    removedLetters = []
    bestWords = []

    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
                "v", "w", "x", "y", "z"]
    letterValues = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    program = True
    correctPosition = ""

    while correctPosition != "12345" and turns < 6:
        words, bestWords, letterIndex, finalWord = guessPositioning(words, bestWords, letterIndex, finalWord)
        turns += 1
    playAgain = input("Do you wish to play again? Y/N ").lower()
    if playAgain == "n":
        print("\nThanks for playing!")
        program = False
