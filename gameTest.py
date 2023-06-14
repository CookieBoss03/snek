from game import SnekGame

class Test():
    def testGame(self):
        game = SnekGame(8)
        game.addPlayer(0, (5,4))
        
        while(True):
            choice = input("Enter command: (t = tick) (empty = stop)")
            if choice == "t":
                game.tick()
            elif choice == "":
                break;

if __name__ == "__main__":
    test = Test()
    test.testGame()