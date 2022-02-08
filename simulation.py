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


def guessPositioning(wordAnswer, words, letterIndex, finalWord):
    global lettersInWord
    global letterValues
    global correctPosition
    global statsList

    answer = wordAnswer

    # Puts the best words to guess in a list
    letterValues, valuesList = calculateLetterValue(alphabet, words)
    newWordList = []
    for word in words:
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

    bestWords = []

    guessedWord = str(newWordList[0][0])

    print("You selected:", guessedWord)
    # asks how many letters are green and then saves those letters into final word

    correctPosition = "0"
    answerCount = 0
    for letter in answer:
        if letter == guessedWord[answerCount]:
            if "0" in correctPosition:
                correctPosition = ""
            correctPosition = correctPosition + str(answerCount + 1)
        answerCount += 1


    if correctPosition == "12345":
        turnsIndex = turns - 1
        statsList[turnsIndex] += 1

        return words, bestWords, letterIndex, finalWord

    if correctPosition != "0":
        for number in correctPosition:
            number = int(number)
            letterIndex.remove(number)
            finalWord[number - 1] = guessedWord[number - 1]

    # asks how many letters are yellow and saves those letters into lettersInWord
    correctLetter = "0"
    answerCount = 0
    for letter in guessedWord:
        if answerCount + 1 not in letterIndex:
            answerCount += 1
            continue
        if letter in answer:
            if correctLetter == "0":
                correctLetter = ""
            correctLetter = correctLetter + str(answerCount + 1)
        answerCount += 1

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

    letterIndex = [1, 2, 3, 4, 5]

    return words, bestWords, letterIndex, finalWord


# letters ranked in order of how common they are in the words
bestLetters = ["e", "a", "r", "o", "t", "i", "l", "s", "n", "u", "c", "y", "h", "d", "p", "g", "m", "b", "f", "k", "w",
               "v", "x", "z", "q", "j"]
lettersInWord = []
removedLetters = []
statsList = [0, 0, 0, 0, 0, 0, 0]


alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
            "v", "w", "x", "y", "z"]
letterValues = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
program = True
correctPosition = ""

simulationList = readfile("Words")


for wordAnswer in simulationList:
    print("\nAnswer is:", wordAnswer, "\n")
    turns = 1
    words = readfile("Words")
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
    removeYellow = [words, finalWord, letterIndex, bestWords]

    while correctPosition != "12345" and turns < 6:
        words, bestWords, letterIndex, finalWord = guessPositioning(wordAnswer, words, letterIndex, finalWord)
        turns += 1
    if turns == 7:
        statsList[6] += 1

    print()
    print("1 turn : ", statsList[0])
    print("2 turns: ", statsList[1])
    print("3 turns: ", statsList[2])
    print("4 turns: ", statsList[3])
    print("5 turns: ", statsList[4])
    print("6 turns: ", statsList[5])
    print("Failed : ", statsList[6])
    wins = statsList[0] + statsList[1] + statsList[2] + statsList[3] + statsList[4] + statsList[5]
    games = wins + statsList[6]
    average = (((1*statsList[0]) + (2*statsList[1]) + (3*statsList[2]) + (4*statsList[3]) + (5*statsList[4]) +
               (6*statsList[5])) / wins)
    print("Average:", round(average, 2))
    print("Win percentage:", round((wins/games)*100))
    print()

print(statsList)