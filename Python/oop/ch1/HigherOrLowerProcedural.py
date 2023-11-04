import random
SUIT_TUPLE = ('Spades', 'Hearts', 'Clubs', 'Diamonds')
RANK_TUPLE = ('Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King')
NCADS = 8

def getCard(deckListIn):
    thisCard= deckListIn.pop()
    return thisCard

def shuffle(deckListIn):
    deckListOut = deckListIn.copy()
    random.shuffle(deckListOut)
    return deckListOut

print('Welcom to higher or lower')
print('you have to choose whether the next card to be shown will be higher or lower than the current card')
print('Getting it right adds point; get it wrong and you lose 15 points')
print('You have 50 points to start')
print()

startingDeckList = []

for suit in SUIT_TUPLE:
    for thisValue, rank in enumerate(RANK_TUPLE):
        cardDict = {'rank': rank, 'suit': suit, 'value': thisValue + 1}
        startingDeckList.append(cardDict)


score = 50

while True:
    print()
    gameDeckList = shuffle(startingDeckList)
    currentCardDict = getCard(gameDeckList)
    currentCardRank = currentCardDict['rank']
    currentCardValue = currentCardDict['value']
    currentCardSuit = currentCardDict['suit']
    print('Starting card is :', currentCardRank + ' of' + currentCardSuit)
    print()


    for cardNumber in range(0, NCADS):
        answer = input('Will the next card be higher or lower than the' + currentCardRank + ' of' + currentCardSuit + '? (enter h or 1) : ')
        answer = answer.casefold()
        nextCardDict = getCard(gameDeckList)
        nextCardRank = nextCardDict['rank']
        nextCardSuit = nextCardDict['suit']
        nextCardValue = nextCardDict['value']
        print('Next card is:', nextCardRank + ' of' + nextCardSuit)

        if answer == 'h':
            if nextCardValue > currentCardValue:
                print('you got it right, it was higher')

            else:
                print('Sorry, it was not higher')
        elif answer == '1':
            if nextCardValue < currentCardValue:
                socre = score + 20
                print('you got it right, it was lower')

            else:
                score = score - 15
                print('Sorry, it was not lower')
            print('Your score is :', score)
            print()
            currentCardRank = nextCardRank
            currentCardValue = nextCardValue

    goAgain = input('To play again, press ENTER, or "q" to quit: ')
    if goAgain == 'q':
        break

print('OK bye')