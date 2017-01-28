from puzzle import Puzzle


class MNPuzzle(Puzzle):
    """
    An nxm puzzle, like the 15-puzzle, which may be solved, unsolved,
    or even unsolvable.
    """

    def __init__(self, from_grid, to_grid):
        """
        MNPuzzle in state from_grid, working towards
        state to_grid

        @param MNPuzzle self: this MNPuzzle
        @param tuple[tuple[str]] from_grid: current configuration
        @param tuple[tuple[str]] to_grid: solution configuration
        @rtype: None
        """
        # represent grid symbols with letters or numerals
        # represent the empty space with a "*"
        assert len(from_grid) > 0
        assert all([len(r) == len(from_grid[0]) for r in from_grid])
        assert all([len(r) == len(to_grid[0]) for r in to_grid])
        self.n, self.m = len(from_grid), len(from_grid[0])
        self.from_grid, self.to_grid = from_grid, to_grid

    def __eq__(self, other):
        """
        Return whether MNPuzzle self is equivalent to other.

        @type self: MNPuzzle
        @type other: MNPuzzle
        """
        return type(self) == type(other) and (self.from_grid, self.to_grid, self.n, self.m) == (other.from_grid,
                                                                                                other.to_grid, other.n,
                                                                                                other.m)

    def __str__(self):
        """
        Return a string representation of self

        @type self: MNPuzzle
        @rtype: str

        >>> m1 = MNPuzzle((("2","3","5"),("1", "4", "8"),("*", "7", "6")), (("1","2","3"),("4", "5", "6"),("7", "8", "*")))
        >>> print(m1)
        235
        148
        *76
        """
        return "\n".join(["".join(lines) for lines in self.from_grid])

    # TODO
    # implement __eq__ and __str__  check!
    # __repr__ is up to you

    def extensions(self):
        """
        Return a list of extensions for MNPuzzle self.

        @type self: MNPuzzle
        @rtype: list[MNPuzzle]

        >>> start_puzzle = (("1", "3"), ("2", "*"))
        >>> target_puzzle = (("1", "2"), ("3", "*"))
        >>> m2 = MNPuzzle(start_puzzle, target_puzzle)
        >>> list1 = m2.extensions()
        >>> list2 = [MNPuzzle((("1", "*"), ("2", "3")),target_puzzle), MNPuzzle((("1", "3"), ("*", "2")), target_puzzle)]
        >>> all([items in list2 for items in list1])
        True
        >>> all([items in list1 for items in list2])
        True
        """
        return_list = []
        for line in range(len(self.from_grid)):
            for chars in range(len(self.from_grid[line])):
                if self.from_grid[line][chars] == "*":
                    if chars <= self.m - 2:  # if * can be swapped with the item at it's right
                        list_line = list(self.from_grid[line])
                        list_line[chars] = list_line[chars + 1]
                        list_line[chars + 1] = "*"
                        first_half = list(self.from_grid[:line])
                        second_half = list(self.from_grid[line + 1:])
                        first_half.append(tuple(list_line))
                        new_tuple = tuple(first_half + second_half)
                        return_list.append(MNPuzzle(new_tuple, self.to_grid))
                    if chars >= 1:  # if * can be swapped with item at it's left
                        list_line = list(self.from_grid[line])
                        list_line[chars] = list_line[chars - 1]
                        list_line[chars - 1] = "*"
                        first_half = list(self.from_grid[:line])
                        second_half = list(self.from_grid[line + 1:])
                        first_half.append(tuple(list_line))
                        new_tuple = tuple(first_half + second_half)
                        return_list.append(MNPuzzle(new_tuple, self.to_grid))
                    if line >= 1:  # if * can be swapped with item at it's top
                        list_line_top = list(self.from_grid[line - 1])
                        list_line_current = list(self.from_grid[line])
                        list_line_current[chars] = list_line_top[chars]
                        list_line_top[chars] = "*"
                        first_half = list(self.from_grid[:line - 1])
                        second_half = list(self.from_grid[line + 1:])
                        first_half.append(tuple(list_line_top))
                        first_half.append(tuple(list_line_current))
                        new_tuple = tuple(first_half + second_half)
                        return_list.append(MNPuzzle(new_tuple, self.to_grid))
                    if line <= self.n - 2:  # if * can be swapped with item at it's bottom
                        list_line_bottom = list(self.from_grid[line + 1])
                        list_line_current = list(self.from_grid[line])
                        list_line_current[chars] = list_line_bottom[chars]
                        list_line_bottom[chars] = "*"
                        first_half = list(self.from_grid[:line])
                        second_half = list(self.from_grid[line + 2:])
                        first_half.append(tuple(list_line_current))
                        first_half.append(tuple(list_line_bottom))
                        new_tuple = tuple(first_half + second_half)
                        return_list.append(MNPuzzle(new_tuple, self.to_grid))
        return return_list
    # TODO
    # breadth search, tuple
    # override extensions
    # legal extensions are configurations that can be reached by swapping one
    # symbol to the left, right, above, or below "*" with "*"
    def is_solved(self):
        """
        Return whether MNPuzzle self is solved

        @type self: MNPuzzle
        @rtype: bool

        >>> start_puzzle = (("1", "2"), ("3", "*"))
        >>> end_puzzle = (("1", "2"), ("3", "*"))
        >>> m3 = MNPuzzle(start_puzzle, end_puzzle)
        >>> m3.is_solved()
        True
        >>> start_puzzle2 = (("2", "1"), ("3", "*"))
        >>> m4 = MNPuzzle(start_puzzle2, end_puzzle)
        >>> m4.is_solved()
        False
        """
        return all([self.from_grid[lines] == self.to_grid[lines] for lines in range(len(self.from_grid))])
    # TODO
    # override is_solved
    # a configuration is solved when from_grid is the same as to_grid


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    target_grid = (("1", "2", "3"), ("4", "5", "*"))
    start_grid = (("*", "2", "3"), ("1", "4", "5"))
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    start = time()
    solution = breadth_first_solve(MNPuzzle(start_grid, target_grid))
    end = time()
    print("BFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
    start = time()
    solution = depth_first_solve((MNPuzzle(start_grid, target_grid)))
    end = time()
    print("DFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
