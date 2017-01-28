from puzzle import Puzzle


class WordLadderPuzzle(Puzzle):
    """
    A word-ladder puzzle that may be solved, unsolved, or even unsolvable.
    """

    def __init__(self, from_word, to_word, ws):
        """
        Create a new word-ladder puzzle with the aim of stepping
        from from_word to to_word using words in ws, changing one
        character at each step.

        @type from_word: str
        @type to_word: str
        @type ws: set[str]
        @rtype: None
        """
        (self._from_word, self._to_word, self._word_set) = (from_word,
                                                            to_word, ws)
        # set of characters to use for 1-character changes
        self._chars = "abcdefghijklmnopqrstuvwxyz"

    def __eq__(self, other):
        """
        Return True if self is equal to other

        @type self: WordLadderPuzzle
        @type other: WordLadderPuzzle
        @rtype: bool

        >>> word_set = {"bill", "bell", "tell"}
        >>> w1 = WordLadderPuzzle("bill", "tell", word_set)
        >>> word_set2 = {"bell", "bill", "tell"}
        >>> w2 = WordLadderPuzzle("bill", "tell", word_set2)
        >>> w1 == w2
        True
        >>> w3 = WordLadderPuzzle("bell", "tell", word_set)
        >>> w1 == w3
        False
        """
        return type(self) == type(other) and (self._from_word, self._to_word, self._word_set) == (other._from_word,
                                                                                                  other._to_word,
                                                                                                  other._word_set)

    def __str__(self):
        """
        Return a string representation of WordLadderPuzzle self.

        @type self: WordLadderPuzzle
        @rtype: str
        >>> word_set = {"bill", "bell", "tell"}
        >>> w1 = WordLadderPuzzle("bill", "tell", word_set)
        >>> str(w1)
        'bill -> tell'
        """
        return "{} -> {}".format(self._from_word, self._to_word)
        # TODO
        # implement __eq__ and __str__
        # __repr__ is up to you
    def extensions(self):
        """
        Return list of legal extensions of WordLadderPuzzle self.

        @type self: WordLadderPuzzle
        @rtype: list[WordLadderPuzzle]
        >>> word_set = {"seal", "bell", "tell", "belle", "tall"}
        >>> w1 = WordLadderPuzzle("bell", "tall", word_set)
        >>> ex = w1.extensions()
        >>> w2 = WordLadderPuzzle("tell", "tall", word_set)
        >>> ex[0] = w2
        """
        return_list = []
        for word in self._word_set:
            if len(word) == len(self._from_word):
                counter = 0
                for char in range(len(self._from_word)):
                    if self._from_word[char] != word[char]:
                        counter += 1
                if counter == 1:
                    return_list.append(WordLadderPuzzle(word, self._to_word, self._word_set))
        return return_list

    def is_solved(self):
        """
        Return True iff WordLadderPuzzle self is solved.

        @type self: WordLadderPuzzle
        @rtype: bool

        >>> word_set = {"bill", "bell", "tell"}
        >>> w1 = WordLadderPuzzle("tell", "tell", word_set)
        >>> w1.is_solved()
        True
        """
        return self._from_word == self._to_word and self._from_word in self._word_set
        # TODO
        # override extensions
        # legal extensions are WordPadderPuzzles that have a from_word that can
        # be reached from this one by changing a single letter to one of those
        # in self._chars

        # TODO
        # override is_solved
        # this WordLadderPuzzle is solved when _from_word is the same as
        # _to_word


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    with open("words", "r") as words:
        word_set = set(words.read().split())
    w = WordLadderPuzzle("same", "cost", word_set)
    start = time()
    sol = breadth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using breadth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
    start = time()
    sol = depth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using depth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))




