"""
Test program what convert tokens to commands in stack
"""


def _term(stack, tokens):
    t1 = tokens.pop(0)
    op = tokens.pop(0)
    t2 = tokens.pop(0)

    _expression(stack, tokens)
    stack.append(t1)
    stack.append(op)


def _factor(stack, tokens):
    t1 = tokens.pop(0)
    op = tokens.pop(0)
    t2 = tokens.pop(0)

    if t1 == "(":
        _expression(stack, tokens)
    else:
        stack.append(t1)
        stack.append(t2)
    stack.append(op)


def _expression(stack, tokens):
    while tokens:
        token = tokens[0]

        print("stack:", stack)
        print("token:", token)
        print("tokens:", tokens)
        input()


        if token == "(":
            tokens.pop(0)
            _expression(stack, tokens)
        elif token.isalpha() or token.isnumeric():
            if not len(tokens) > 1:
                return
            op = tokens[1]
            if op in ["*", "/"]:
                _factor(stack, tokens)
            if op in ["+", "-"]:
                print("dfa")
                _term(stack, tokens)
        elif token == ")":
            tokens.pop(0)
            return


def to_rpn(expr):
    stack = []
    
    for ch in ["+", "-", "*", "/", "(", ")"]:
        expr = expr.replace(ch, f" {ch} ")
    tokens = expr.split()
    tokens = list(filter(lambda x: x != "", tokens))

    _expression(stack, tokens)

    return stack 


print(to_rpn("1 + 2 + 3 + 4 + ((((3))))"))
print(to_rpn("(2-1)*(x+3*d)/2-z"))
