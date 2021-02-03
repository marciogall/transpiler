import copy


class IndentLexer:
    """
    A second lexing stage that interprets WHITESPACE
    Manages Off-Side Rule for indentation
    """

    def __init__(self, lexer):
        self.indents = [0]  # indentation stack
        self.tokens = []  # token queue
        self.lexer = lexer
        self.linenumber = 1

    def input(self, *args, **kwds):
        self.lexer.input(*args, **kwds)

    # Iterator interface
    def __iter__(self):
        return self

    def next(self):
        t = self.token()
        if t is None:
            raise StopIteration
        return t

    __next__ = next

    def token(self):
        # empty our buffer first
        if self.tokens:
            return self.tokens.pop(0)

        # loop until we find a valid token
        while 1:
            # grab the next from first stage
            token = self.lexer.token()

            # we only care about whitespace
            if not token or token.type != 'WHITESPACE':
                return token

            self.linenumber += 1

            # check for new indent/dedent
            whitespace = token.value[1:]  # strip \n
            change = self._calc_indent(whitespace)
            if change:
                break

        # indentation change
        if change == 1:
            token.type = 'INDENT'
            return token

        # dedenting one or more times
        assert change < 0
        change += 1
        token.type = 'DEDENT'

        # buffer any additional DEDENTs
        while change:
            self.tokens.append(copy.copy(token))
            change += 1

        return token

    def _calc_indent(self, whitespace):
        "returns a number representing indents added or removed"
        n = len(whitespace)  # number of spaces
        indents = self.indents  # stack of space numbers
        if n > indents[-1]:
            indents.append(n)
            return 1

        # we are at the same level
        if n == indents[-1]:
            return 0

        # dedent one or more times
        i = 0
        while n < indents[-1]:
            indents.pop()
            if n > indents[-1]:
                raise SyntaxError("wrong indentation level")
            i -= 1
        return i

    def error(self):
        print("Grammar error at line {}".format(self.linenumber))
