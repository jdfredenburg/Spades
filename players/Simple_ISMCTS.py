from Game import *
from Types.types import *


class Simple_ISMCTS:

    def __init__(self, rootState, player, max_iter=100, verbose=0, exploration=.7):
        self.max_iterations = max_iter
        self.EXPLORATION = exploration
        self.verbose = verbose
        self.rootstate = rootState
        self.rootnode = Node()
        self.player = player

    def search(self):
        for i in range(self.max_iterations):
            node = self.rootnode

            state = self.rootstate.CloneAndRandomize(self.player)

            while state.GetMoves() != [] and node.GetUntriedMoves(state.GetMoves()) == []:
                node = node.SelectChild(state.GetMoves(), self.EXPLORATION)
                state.DoMove(node.move)

            untriedMoves = node.GetUntriedMoves(state.GetMoves())
            if untriedMoves:
                m = random.choice(untriedMoves)
                player = state.playerToMove
                state.DoMove(m)
                node = node.AddChild(m, player)

            # Playout
            state = self.playout(state)

            # Backpropagate
            self.backpropagate(node, state)

        # Output some information about the tree - can be omitted
        if self.verbose == 2:
            print(self.rootnode.TreeToString(0))
        elif self.verbose == 1:
            print(self.rootnode.ChildrenToString())

        return max(self.rootnode.childNodes, key=lambda c: c.visits).move  # return the move that was most visited

    def playout(self, state):
        while state.GetMoves():
            if len(state.playerHands[Player.north]) + len(state.playerHands[Player.east]) + len(
                    state.playerHands[Player.south]) + len(state.playerHands[Player.west]) == 1:
                state.DoMove(random.choice(state.GetMoves()))
                break
            state.DoMove(random.choice(state.GetMoves()))

        return state

    def backpropagate(self, node, state):
        while node is not None:
            node.Update(state)
            node = node.parentNode
