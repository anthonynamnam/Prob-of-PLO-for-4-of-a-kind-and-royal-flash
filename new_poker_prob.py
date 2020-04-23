import random

def convertIndexToCard(number):
    cardTypeStr = ''
    cardType = number // 13
    cardNumber = number % 13
    if cardType == 0:
        cardTypeStr = "Spades"
    elif cardType == 1:
        cardTypeStr = "Hearts"
    elif cardType == 2:
        cardTypeStr = "Clubs"
    elif cardType == 3:
        cardTypeStr = "Diamonds"
    return (cardTypeStr, cardNumber+1)

def convertCardToIndex(cardTypeStr,cardNumber):
    cardType = 0
    if cardTypeStr == "Spades":
        cardType = 0
    elif cardTypeStr == "Hearts":
        cardType = 1
    elif cardTypeStr == "Clubs":
        cardType = 2
    elif cardTypeStr == "Diamonds":
        cardType = 3
    number = cardType * 13 + cardNumber - 1
    return number

def checkIfWin(gameset):
    royalFlushCount = 0
    fourOFAKindCount = 0
    fourCount=[]
    for player in gameset.playerList:
        poolCardIndex = []
        handCardIndex = []
        playerID = player.ID
        for x in gameset.publicCard:
            poolCardIndex.append(convertCardToIndex(*x))
        for y in player.cards:
            handCardIndex.append(convertCardToIndex(*y))
        
        poolCardIndexCombination = [[0,1,2],[0,1,3],[0,1,4],[1,2,3],[1,2,4],[2,3,4]]
        handCardIndexCombination = [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]
        # Testing
##        poolCardIndex=[1,13,27,5,38]
##        handCardIndex=[14,6,2,40]
        # Testing
        tempHand = []
        for x in poolCardIndexCombination:
            for y in handCardIndexCombination:
                tempHand = []
                for i in x:
                    tempHand.append(poolCardIndex[i])
                for j in y:
                    tempHand.append(handCardIndex[j])
                a = RoyalFlash(tempHand)
                b,ind = FourOfAKind(tempHand)
                if a or b:
                    if a:
                        royalFlushCount = royalFlushCount + 1
                    if b:
                        if ind not in fourCount:
                            fourOFAKindCount = fourOFAKindCount + 1
                            fourCount.append(ind)
##                    print(poolCardIndex)
##                    print(handCardIndex)
##                    print(x)
##                    print(y)
##                    print('Player ID:',playerID,'-- temp Hand',tempHand,'===> Royal Flush:',a)
##                    print('Player ID:',playerID,'-- temp Hand',tempHand,'===> Four of a Kind:',b)
##    print('Royal Flush Count:', royalFlushCount)
##    print('Four oF a Kind Count:', fourOFAKindCount)
    return (royalFlushCount,fourOFAKindCount)
            
    

def RoyalFlash(fiveCard):
    mincard = min(fiveCard)
    cardType = [mincard // 13]
    for i in range(len(fiveCard)):
        newcardType = fiveCard[i] // 13
        if newcardType not in cardType:
            return False
        fiveCard[i] = fiveCard[i] % 13
    
    mincard = min(fiveCard)
    if mincard == 0:
        if not (sum(fiveCard) == 10 or sum(fiveCard)+8 == 50):
            return False
    elif mincard <= 8 and mincard > 0:
        for card in fiveCard:
            if card-mincard >= 5:
                return False
    return True

def FourOfAKind(fiveCard):
    for i in range(len(fiveCard)):
        fiveCard[i] = fiveCard[i] % 13
    for j in range(13):
        if fiveCard.count(j) == 4:
            return (True,j)
    return (False,-1)






class Game:
    
    def __init__(self,numOfPlayer = 6,maxNumOfCard = 4):
        self.maxCardPerPlayer = maxNumOfCard
        self.publicCard = []
        self.numOfPlayer = numOfPlayer
        self.playerList = []
        self.poker = []
        self.flop = False
        self.flip = False
        self.river = False
        self.skip = False

    def startGame(self):
        self.poker = Poker()
        for i in range(self.numOfPlayer):
            player = Player(self.getNumberOfPlayer()+1,MAXCARD = self.maxCardPerPlayer)
            self.playerList.append(player)
        self.distributeCards()
            
    def distributeCards(self):
        for i in range(self.maxCardPerPlayer):
            for player in self.playerList:
                index = (i*self.getNumberOfPlayer())+player.ID-1
                thiscard = self.poker.cards[index]
                self.poker.here[index] = False
                player.cards.append(thiscard)

    def nextRound(self):
        if not(self.flop and self.flip and self.river):
            if not self.flop:
                self.openCard(3)
                self.flop = True
            elif self.flop and not self.flip:
                self.openCard(1)
                self.flip = True
            elif self.flop and self.flip and not self.river:
                self.openCard(1)
                self.river = True
        else:
            print('The game is ended!')
        

    def openCard(self,openHowMany = 1):
        self.skip = False
        openedNum = 0
        for i in range(self.poker.maxNumOfCard):
            if not (openedNum < openHowMany):
                break
            if self.poker.here[i]:
                if not self.skip:
                    self.skip = True
                    self.poker.here[i] = False
                else:
                    if openedNum < openHowMany:
                        self.publicCard.append(self.poker.cards[i])
                        self.poker.here[i] = False
                        openedNum = openedNum + 1
           
    def print(self):
        self.printPoker()
        print('')
        self.printNumOfPlayer()
        print('')
        self.printPublicCard()
        print('')
        self.printPlayer()
        
    def printPoker(self):
        self.poker.print()
    
    def printPlayer(self):
        for player in self.playerList:
            player.print()
            print('')
            
    def printPublicCard(self):
        print('Public Card =>',self.publicCard)

    def printNumOfPlayer(self):
        print('Number of player :',self.getNumberOfPlayer())

    def getNumberOfPlayer(self):
        return len(self.playerList)

    

class Poker:
    def __init__(self,MAXCARD = 52):
        self.maxNumOfCard = MAXCARD
        self.cards = []
        self.here = [False]*self.maxNumOfCard
        self.mix()

    def mix(self):
        self.cards = []
        while len(self.cards) != (self.maxNumOfCard):
            randnum = random.randint(0,(self.maxNumOfCard-1))
            if not (self.here[randnum]):
                self.cards.append(convertIndexToCard(randnum))
                self.here[randnum] = True

    def reset(self):
        self.cards = []
        self.here = [False]*self.maxNumOfCard
        self.mix()         

    def print(self):
        print('POKER SET =>',self.cards)

    

class Player:

    def __init__(self,UID,MAXCARD = 4):
        self.maxcard = MAXCARD
        self.cards = []
        self.ID = UID
        

    def print(self):
        self.printID()
        self.printCards()

    def printID(self):
        print('Player ID :', self.ID)

    def printCards(self):
        print('Player Cards =>', self.cards)


##################################################

hour = 1
time = hour * 3600
dp = 4

for numppl in range(2,7):
    numPlayer = numppl
    TestSize = 500
    GameSize = int(time/(numppl*30))
    RoyalFlushDistribution = []
    FourKindDistribution = []
    if numppl == 2:
        print('Experiment Size:',TestSize)
        print('Playing Duration:',hour,'hours\n')
    for _ in range(TestSize):
        
        # play 100 games every time
        gamesize = GameSize
        totalFourOFAKindCount = 0
        totalRoyalFlushCount = 0

        for roundNum in range (gamesize):
            gameset = Game(numPlayer)
            gameset.startGame()
            while not(gameset.flop and gameset.flip and gameset.river):
                gameset.nextRound()
        ##        gameset.printPublicCard()
        ##        print('')
        ##    print('\n===== The game is ended =======\n')
        ##    gameset.print()
        ##    print('Round:',roundNum+1)
            x,y = checkIfWin(gameset)
            totalFourOFAKindCount = totalFourOFAKindCount + y
            totalRoyalFlushCount = totalRoyalFlushCount + x
            #print('====================')
    ##    print('totalFourOFAKindCount =', int(totalFourOFAKindCount))
    ##    print('Probability of FourOFAKindCount =', round(totalFourOFAKindCount/gamesize,dp))
    ##    print('totalRoyalFlushCount =', int(totalRoyalFlushCount))
    ##    print('Probability of FlushCount =', round(totalRoyalFlushCount/gamesize,dp))
        FourKindDistribution.append(round(totalFourOFAKindCount/gamesize,dp))
        RoyalFlushDistribution.append(round(totalRoyalFlushCount/gamesize,dp))

    print('Mean of getting Royal Flush in',GameSize,'games (' + str(numPlayer) + ' players):', round(sum(RoyalFlushDistribution)/len(RoyalFlushDistribution),dp))
    print('Mean of getting Four of a Kind in',GameSize,'games (' + str(numPlayer) + ' players):',round(sum(FourKindDistribution)/len(FourKindDistribution),dp))
    print('')




      
