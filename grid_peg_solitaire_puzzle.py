from puzzle import Puzzle
import copy


class GridPegSolitairePuzzle(Puzzle):
    """
    Snapshot of peg solitaire on a rectangular grid. May be solved,
    unsolved, or even unsolvable.
    """

    def __init__(self, marker, marker_set):
        """
        Create a new GridPegSolitairePuzzle self with
        marker indicating pegs, spaces, and unused
        and marker_set indicating allowed markers.

        @type marker: list[list[str]]
        @type marker_set: set[str]
                          "#" for unused, "*" for peg, "." for empty
        """
        assert isinstance(marker, list)
        assert len(marker) > 0
        assert all([len(x) == len(marker[0]) for x in marker[1:]])
        assert all([all(x in marker_set for x in row) for row in marker])
        assert all([x == "*" or x == "." or x == "#" for x in marker_set])
        self._marker, self._marker_set = marker, marker_set

    def __eq__(self, other):
        """
        Return whether GridPegSolitairePuzzle self is equivalent ot other

        @type self: GridPegSolitairePuzzle
        @type other: GridPegSolitairePuzzle | Any
        @rtype: bool

        >>> grid1 = [["#", "*", "*", "*", "#"]]
        >>> grid1.append(["*", "*", ".", "*", "*"])
        >>> grid1.append(["*", "*", "*", "*", "*"])
        >>> grid1.append(["*", "*", ".", "*", "*"])
        >>> grid1.append(["#", "*", "*", "*", "#"])
        >>> grid2 = [["#", "*", "*", "*", "#"]]
        >>> grid2.append(["*", "*", ".", "*", "*"])
        >>> grid2.append(["*", "*", "*", "*", "*"])
        >>> grid2.append(["*", "*", ".", "*", "*"])
        >>> grid2.append(["#", "*", "*", "*", "#"])
        >>> g1 = GridPegSolitairePuzzle(grid1, {"*", ".", "#"})
        >>> g2 = GridPegSolitairePuzzle(grid2, {"#", ".", "*"})
        >>> g1 == g2
        True
        >>> grid2[0][0] = "*"
        >>> g3 = GridPegSolitairePuzzle(grid2, {"*",".","#"})
        >>> g1 == g3
        False
        """
        return type(self) == type(other) and self._marker == other._marker and self._marker_set == other._marker_set

    def __str__(self):
        """
        Return a human readable string representation of GridPegSolitairePuzzle self

        @type self: GridPegSolitairePuzzle
        @rtype: str

        >>> grid1 = [["#", "*", "*", "*", "#"]]
        >>> grid1.append(["*", "*", ".", "*", "*"])
        >>> grid1.append(["*", "*", "*", "*", "*"])
        >>> grid1.append(["*", "*", ".", "*", "*"])
        >>> grid1.append(["#", "*", "*", "*", "#"])
        >>> puzzle1 = GridPegSolitairePuzzle(grid1, {"*", ".", "#"})
        >>> print(puzzle1)
        #***#
        **.**
        *****
        **.**
        #***#
        """
        return "\n".join(["".join(item) for item in self._marker])


    # TODO
    # implement __eq__, __str__ methods
    # __repr__ is up to you
    def extensions(self):
        """
        Return list of legal extensions of GridPegSolitairePuzzle self.

        @type self: GridPegSolitairePuzzle
        @rtype: list[GridPegSolitairePuzzle]

        >>> grid1 = [["#", ".", ".", ".", "#"]]
        >>> grid1.append([".", ".", ".", ".", "."])
        >>> grid1.append(["*", "*", ".", ".", "."])
        >>> grid1.append([".", ".", ".", ".", "."])
        >>> grid1.append(["#", ".", ".", ".", "#"])
        >>> g1 = GridPegSolitairePuzzle(grid1, {"*", ".", "#"})
        >>> newlist = list(g1.extensions())
        >>> grid1[2][0] = "."
        >>> grid1[2][1] = "."
        >>> grid1[2][2] = "*"
        >>> g2 = GridPegSolitairePuzzle(grid1, {"*", ".", "#"})
        >>> len(g1._marker) == len(g2._marker)
        True
        >>> all([s in g1._marker for s in g2._marker])
        True
        >>> all([s in g2._marker for s in g1._marker])
        True
        """
        # convenient names
        marker, marker_set = self._marker, self._marker_set
        new_list = []
        if self.is_solved():
            return [_ for _ in []]
        else:
            for row in range(len(marker)):
                for item in range(len(marker[row])):
                    if marker[row][item] == ".":
                        if item >= 2 and marker[row][item - 1] == "*" and marker[row][item - 2] == "*":
                            new_marker = copy.deepcopy(self._marker)
                            new_marker[row][item] = "*"
                            new_marker[row][item - 1] = "."
                            new_marker[row][item - 2] = "."
                            new_list.append(GridPegSolitairePuzzle(new_marker,self._marker_set))
                        if item <= len(marker[row]) - 3 and marker[row][item + 1] == "*" and \
                           marker[row][item + 2] == "*":
                            new_marker = copy.deepcopy(self._marker)
                            new_marker[row][item] = "*"
                            new_marker[row][item + 1] = "."
                            new_marker[row][item + 2] = "."
                            new_list.append(GridPegSolitairePuzzle(new_marker,self._marker_set))
                        if row >= 2 and marker[row - 1][item] == "*" and marker[row - 2][item] == "*":
                            new_marker = copy.deepcopy(self._marker)
                            new_marker[row][item] = "*"
                            new_marker[row - 1][item] = "."
                            new_marker[row - 2][item] = "."
                            new_list.append(GridPegSolitairePuzzle(new_marker,self._marker_set))
                        if row <= len(marker) - 3 and marker[row + 1][item] == "*" and marker[row + 2][item] == "*":
                            new_marker = copy.deepcopy(self._marker)
                            new_marker[row][item] = "*"
                            new_marker[row + 1][item] = "."
                            new_marker[row + 2][item] = "."
                            new_list.append(GridPegSolitairePuzzle(new_marker,self._marker_set))
                    else:
                        pass
            return new_list

    # TODO
    # override extensions
    # legal extensions consist of all configurations that can be reached by
    # making a single jump from this configuration
    def is_solved(self):
        """
        Return whether GridPegSolitairePuzzle self is solved

        @type self: GridPegSolitairePuzzle
        @rtype: bool

        >>> grid1 = [["#", ".", ".", ".", "#"]]
        >>> grid1.append([".", ".", ".", ".", "."])
        >>> grid1.append([".", ".", ".", "*", "."])
        >>> grid1.append([".", ".", ".", ".", "."])
        >>> grid1.append(["#", ".", ".", ".", "#"])
        >>> g1 = GridPegSolitairePuzzle(grid1, {"*", ".", "#"})
        >>> g1.is_solved()
        True
        """
        gather = []
        for row in self._marker:
            gather += row
        return gather.count("*") == 1
    # TODO
    # override is_solved
    # A configuration is solved when there is exactly one "*" left


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    from puzzle_tools import depth_first_solve

    grid = [["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", ".", "*", "*"],
            ["*", "*", "*", "*", "*"]]
    gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
    import time

    start = time.time()
    solution = depth_first_solve(gpsp)
    end = time.time()
    print("Solved 5x5 peg solitaire in {} seconds.".format(end - start))
    print("Using depth-first: \n{}".format(solution))
