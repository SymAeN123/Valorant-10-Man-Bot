import pickle5 as pickle

def loadData():
    with open('leaderboardData.bin', 'rb') as f:
        data = pickle.load(f)
        return data

class Leaderboard:

    def __init__(self):
        self.data = {}

    def printData(self):
        print(self.data)

    def save(self):
        with open('leaderboardData.bin', 'wb') as f:
            pickle.dump(self, f)

    def update(self, win, loss, guildID):
        if ((guildID in self.data) == False):
            self.data[guildID] = {}
        for player in win:
            if (player in self.data[guildID]):
                self.data[guildID][player][0] = self.data[guildID][player][0] + 1
                self.data[guildID][player][1] = self.data[guildID][player][1] + 1
            else:
                self.data[guildID][player] = [1, 1]
        for player in loss:
            if (player in self.data[guildID]):
                self.data[guildID][player][0] = self.data[guildID][player][0] + 1
            else:
                self.data[guildID][player] = [1, 0]
    
    def getArray(self, guildID):
        if ((guildID in self.data) == False):
            return []
        lDict = self.data[guildID]
        lArray = []
        for member in lDict:
            entry = [member, lDict[member][0], lDict[member][1]]
            lArray.append(entry)
        
        lArray.sort(key=lambda x: x[2], reverse=True)
        lArray.sort(key=lambda x: x[1], reverse=True)

        ret = [[lArray[0]]]

        max = 10
        if len(lArray) < 10:
            max = len(lArray)

        cBuffer = lArray[0][1]
        wBuffer = lArray[0][2]
        i = 1
        index = 0
        while i < max:
            if lArray[i][1] == cBuffer and lArray[i][2] == wBuffer:
                ret[index].append(lArray[i])
                i += 1
            else:
                ret.append([lArray[i]])
                i += 1
                index += 1

        return ret

if __name__ == "__main__":
    emptyLeaderboard = Leaderboard()
    with open('leaderboardData.bin', 'wb') as f:
        pickle.dump(emptyLeaderboard, f)
