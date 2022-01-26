import time

from Game import *
from players.Simple_ISMCTS import Simple_ISMCTS
import csv
import json


def main(save_scores=False):
    ss = SpadesGameState(Player.north)
    score_track = []
    while ss.GetMoves():
        print(ss)
        if save_scores:
            if len(ss.playerHands[Player.north]) == 13 and len(ss.playerHands[Player.east]) == 13 and len(
                    ss.playerHands[Player.south]) == 13 and len(ss.playerHands[Player.west]) == 13:
                score_track.append([ss.NSscore[0], ss.NSscore[1], ss.EWscore[0], ss.EWscore[1],
                                    ss.bets[Player.north], ss.bets[Player.east], ss.bets[Player.south],
                                    ss.bets[Player.west]])

        if ss.playerToMove == Player.north:
            st = time.time()
            # m = ParaISMCTS_driver(rootstate=ss, total_iter=5000, verbose=0, numWorkers=5)

            pl = Simple_ISMCTS(rootState = ss, player = ss.playerToMove, max_iter = 100)
            m = pl.search()
            # print(pl.MAST)
            # print(pl.MAST_n)
#            print(np.divide(pl.MAST, pl.MAST_n))
            print('Time taken = {} seconds'.format(time.time() - st))

        else:
            pl = Simple_ISMCTS(rootState = ss, player = ss.playerToMove, max_iter = 5)
            m = pl.search()

        print("Best Move: " + str(m) + "\n")
        ss.DoMove(m)

    score_track.append([ss.NSscore[0], ss.NSscore[1], ss.EWscore[0], ss.EWscore[1],
                        ss.bets[Player.north], ss.bets[Player.east], ss.bets[Player.south], ss.bets[Player.west]])
    if save_scores:
        with open('scores/score.csv', mode='w', newline='') as f:
            score_writer = csv.writer(f, delimiter=',')
            for line in score_track:
                score_writer.writerow(line)
    print(str(ss.NSscore) + str(ss.EWscore))


def main2(ngames):
    score_track = {"NS": 0, "EW": 0, "Scores": [[], []], "Margin": []}
    for i in range(ngames):
        ss = SpadesGameState(Player.north)
        ss.SCORE_LIMIT = 400
        #ss.EXPLORATION = .5
        while ss.GetMoves():
            # print(ss)
            if ss.playerToMove == Player.north or ss.playerToMove == Player.south:
                pl = Simple_ISMCTS(rootState = ss, player = ss.playerToMove, max_iter = 100)
                #m = ISMCTS(rootstate=ss, itermax=1000, verbose=2)
                m = pl.search()
            else:
                # m = ISMCTS(rootstate=ss, itermax=5, verbose=0)
                #m = random.choice(ss.GetMoves())
                pl = Simple_ISMCTS(rootState = ss, player = ss.playerToMove, max_iter = 100)
                m = pl.search()

            # print("Best Move: " + str(m) + "\n")
            ss.DoMove(m)
        if ss.NSscore[0] > ss.EWscore[0]:
            score_track["NS"] += 1
        else:
            score_track["EW"] += 1
        score_track["Margin"].append(ss.NSscore[0] - ss.EWscore[0])
        score_track["Scores"][0].append(ss.NSscore[0])
        score_track["Scores"][1].append(ss.EWscore[0])
        print(str(ss.NSscore) + str(ss.EWscore))

    with open("scores/main2_output.json", 'w') as f:
        json.dump(score_track, f)

    print(score_track)


if __name__ == "__main__":
    #random.seed(123)
    #main(save_scores=False)
    main()
