from Game import *
from Types.types import *
from players.Simple_ISMCTS import Simple_ISMCTS

import numpy as np


class MAST_ISMCTS(Simple_ISMCTS):

    def __init__(self, rootState, player, max_iter=100, verbose=0, exploration=.7, tau = 1):
        super().__init__(rootState, player, max_iter=max_iter, verbose=verbose, exploration=exploration)
        self.MAST = np.zeros(52)
        self.MAST_n = np.zeros(52)
        self.tau = tau

    def makeProbs(self, moves, tau=1):
        # MAST_this_time = self.MAST[moves]
        pluck_wins = []
        pluck_n = []
        for m in moves:
            pluck_wins.append(self.MAST[m.__hash__()])
            pluck_n.append(self.MAST_n[m.__hash__()])
        pluck_wins = np.array(pluck_wins)
        pluck_n = np.array(pluck_n)
        # MAST_avg = self.MAST / self.MAST_n
        MAST_avg = pluck_wins / pluck_n

        MAST_avg = np.nan_to_num(MAST_avg)
        probs = np.exp(MAST_avg / tau) / np.sum(np.exp(MAST_avg / tau))

        probs[np.random.randint(0, len(moves))] += 1 - np.sum(probs)

        return probs

    def playout(self, state):
        while state.GetMoves():
            if len(state.playerHands[Player.north]) + len(state.playerHands[Player.east]) + len(
                    state.playerHands[Player.south]) + len(state.playerHands[Player.west]) == 1:
                state.DoMove(random.choice(state.GetMoves()))
                break
            probs = self.makeProbs(state.GetMoves(), tau = self.tau)
            probs = probs.flatten()
            m = np.random.choice(state.GetMoves(), p=probs)
            state.DoMove(m)

        return state

    def backpropagate(self, node, state):
        while node is not None:
            node.Update(state)
            if node.move is not None:
                self.MAST[node.move.__hash__()] += state.GetResult(node.playerJustMoved)
                self.MAST_n[node.move.__hash__()] += 1
            node = node.parentNode
