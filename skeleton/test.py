def precedence(operator):
    precedence_map = {'+': 1, '-': 1, '*': 2, '/': 2}
    return precedence_map.get(operator, 0)

def infix_to_postfix(expression):
    stack = []
    postfix = []
    operators = set(['+', '-', '*', '/', '(', ')'])

    for char in expression:
        if char.isdigit() or char.isalpha():
            postfix.append(char)
        elif char in operators:
            if char == '(':
                stack.append(char)
            elif char == ')':
                while stack and stack[-1] != '(':
                    postfix.append(stack.pop())
                stack.pop()  # Удаляем открывающую скобку из стека
            else:
                while (stack and precedence(stack[-1]) >= precedence(char)):
                    postfix.append(stack.pop())
                stack.append(char)

    while stack:
        postfix.append(stack.pop())

    return ''.join(postfix)

# Пример использования
expression = "(2-1)*(x+3*d)/2-z"
postfix_expression = infix_to_postfix(expression)
print("Выражение в ОПН:", postfix_expression)

