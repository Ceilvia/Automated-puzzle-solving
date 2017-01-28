"""
Some functions for working with puzzles
"""
from puzzle import Puzzle
from collections import deque
# set higher recursion limit
# which is needed in PuzzleNode.__str__
# you may uncomment the next lines on a unix system such as CDF
# import resource
# resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
import sys
sys.setrecursionlimit(10**6)


# implement depth_first_solve
# do NOT change the type contract
# you are welcome to create any helper functions
# you like
def depth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child containing an extension of the puzzle
    in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode
    """
    # define create_depth_path so I can have a set seen in my parameter to keep track of Puzzles that I already seen.
    def create_depth_path(start, seen=set()):
        """
        Return a path with no duplication of PuzzleNode from PuzzleNode(puzzle) to a PuzzleNode containing
        a solution, with each child containing an extension of the puzzle
        in its parent.  Return None if this is not possible.

        @type start: Puzzle
        @type seen: set
        @rtype: PuzzleNode
        """
        seen.add(str(start))   # use string instead of Puzzle because string is hashable
        if start.fail_fast():  # If the puzzle failed
            return None
        if start.is_solved():  # If the puzzle is solved
            return start
        if start is None:      # If the puzzle is None, which I don't think will happen but just in case.
            return None
        else:
            for node in start.extensions():
                if str(node) not in seen:  # check whether or not I have seen this Puzzle
                    solution = create_depth_path(node, seen)
                    if solution:           # If there is a solution returned
                        return create_puzzlenode(start, solution)  # call helper function
    return create_depth_path(puzzle)


def create_puzzlenode(puzzle, item):
    """
    Return a PuzzleNode with self.puzzle as puzzle, and has 1 children which is either PuzzleNode with self.puzzle as
    item or PuzzleNode item, depending on the input, and also set the parent of PuzzleNode item as the returned
    PuzzleNode.

    @type puzzle: Puzzle
    @type item: PuzzleNode | Puzzle
    @rtype: PuzzleNode
    """
    if not isinstance(item, PuzzleNode):
        item = PuzzleNode(item)
    parent_node = PuzzleNode(puzzle, [item])
    item.parent = parent_node
    return parent_node


# implement breadth_first_solve
# do NOT change the type contract
# you are welcome to create any helper functions
# you like
# Hint: you may find a queue useful, that's why
# we imported deque
def breadth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child PuzzleNode containing an extension
    of the puzzle in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode
    """
    # create a puzzle node
    # create queue

    def create_breadth_path(start, seen=set()):
        """
        Return a path with no duplicate from PuzzleNode(puzzle) to a PuzzleNode containing
        a solution, with each child PuzzleNode containing an extension
        of the puzzle in its parent.  Return None if this is not possible.
        @type start: Puzzle
        @type seen: set
        @rtype: PuzzleNode
        """
        q = deque()
        start = PuzzleNode(start)
        start.parent = start
        q.append(start)
        while not len(q) == 0:
            next_puzzle = q.popleft()               # pop the first item in q
            if str(next_puzzle.puzzle) not in seen:        # make sure we never seen this PuzzleNode before
                seen.add(str(next_puzzle.puzzle))
                if next_puzzle.puzzle.is_solved():  # If puzzle is solved
                    return return_path(next_puzzle)
                else:
                    for child in next_puzzle.puzzle.extensions():
                        child = PuzzleNode(child)
                        child.parent = next_puzzle
                        next_puzzle.children.append(child)
                        q.append(child)             # put child in q

    def return_path(leaf):
        """
        Return PuzzleNode that has one children that has one children that has one children... eventually reaches the leaf.

        @type leaf: PuzzleNode
        @rtype: PuzzleNode
        """
        if leaf.puzzle == puzzle:  # if we are back to the root of the tree
            return leaf
        else:                      # if we are not at the root yet
            new_node = PuzzleNode(leaf.parent.puzzle, [leaf], leaf.parent.parent)
            # create a new PuzzleNode that only has 1 children
            leaf.parent = new_node
            return return_path(new_node)

    return create_breadth_path(puzzle)


# Class PuzzleNode helps build trees of PuzzleNodes that have
# an arbitrary number of children, and a parent.
class PuzzleNode:
    """
    A Puzzle configuration that refers to other configurations that it
    can be extended to.
    """

    def __init__(self, puzzle=None, children=None, parent=None):
        """
        Create a new puzzle node self with configuration puzzle.

        @type self: PuzzleNode
        @type puzzle: Puzzle | None
        @type children: list[PuzzleNode]
        @type parent: PuzzleNode | None
        @rtype: None
        """
        self.puzzle, self.parent = puzzle, parent
        if children is None:
            self.children = []
        else:
            self.children = children[:]

    def __eq__(self, other):
        """
        Return whether Puzzle self is equivalent to other

        @type self: PuzzleNode
        @type other: PuzzleNode | Any
        @rtype: bool

        >>> from word_ladder_puzzle import WordLadderPuzzle
        >>> pn1 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "no", "oo"}))
        >>> pn2 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "oo", "no"}))
        >>> pn3 = PuzzleNode(WordLadderPuzzle("no", "on", {"on", "no", "oo"}))
        >>> pn1.__eq__(pn2)
        True
        >>> pn1.__eq__(pn3)
        False
        """
        return (type(self) == type(other) and
                self.puzzle == other.puzzle and
                all([x in self.children for x in other.children]) and
                all([x in other.children for x in self.children]))

    def __str__(self):
        """
        Return a human-readable string representing PuzzleNode self.

        # doctest not feasible.
        """
        return "{}\n\n{}".format(self.puzzle,
                                 "\n".join([str(x) for x in self.children]))
