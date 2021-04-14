from Game import *


def main():
    ss = SpadesGameState(Player.north)

    while ss.GetMoves():
        print(ss)

        if ss.playerToMove == Player.north:
            m = ISMCTS(rootstate=ss, itermax=100, verbose=False)
        else:
            m = ISMCTS(rootstate=ss, itermax=5, verbose=False)

        print("Best Move: " + str(m) + "\n")
        ss.DoMove(m)

    print(str(ss.NSscore) + str(ss.EWscore))


if __name__ == "__main__":
    random.seed(123)
    main()
