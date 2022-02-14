import copy


(INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, ID, ASSIGN, SEMI, EOF, 
EQUAL, LESSTHAN, GREATERTHAN, AND, OR, NOT, IF, THEN, ELSE , LBRACE, RBRACE,
WHILE, DO, TRUE, FALSE, SKIP) = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', 'ID', 'ASSIGN','SEMI', 'EOF',
    'EQUAL', 'LESSTHAN', 'GREATERTHAN', 'AND', 'OR', 'NOT','if','then','else', '{', '}',
    'while', 'do', 'true', 'false', 'skip'
)


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


RESERVED_KEYWORDS = {
    'if': Token('if','if'),
    'then': Token('then','then'),
    'else': Token('else','else'),
    'while': Token('while','while'),
    'do': Token('do','do'),
    'true': Token('true',True),
    'false': Token('false',False),
    'skip': Token('skip','skip')
}


class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "4 + 2 * 3 - 6 / 2"
        self.text = text
        self.state = {}
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def _id(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isalpha():
                return self._id()

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == ':' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(ASSIGN, ':=')

            if self.current_char == ';':
                self.advance()
                return Token(SEMI, ';')

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == '=':
                self.advance()
                return Token(EQUAL, '=')

            if self.current_char == '<':
                self.advance()
                return Token(LESSTHAN, '<')

            if self.current_char == '>':
                self.advance()
                return Token(GREATERTHAN, '>')

            if self.current_char == '∧':
                self.advance()
                return Token(AND, '∧')

            if self.current_char == '∨':
                self.advance()
                return Token(OR, '∨')

            if self.current_char == '¬':
                self.advance()
                return Token(NOT, '¬')

            if self.current_char == '{':
                self.advance()
                return Token(LBRACE, '{')

            if self.current_char == '}':
                self.advance()
                return Token(RBRACE, '}')

            self.error()

        return Token(EOF, None)


###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################

class AST(object):
    pass


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.op = token.type
        self.value = token.value


class Compound(AST):
    def __init__(self):
        self.children = []


class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Var(AST):
    def __init__(self, token):
        self.op = token.type
        self.value = token.value


class Bool(AST):
    def __init__(self, token):
        self.value = token.value
        self.op = token.type


class Semi(AST):
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op


class Not(AST):
    def __init__(self, node):
        self.op = 'NOT'
        self.ap = node


class BoolOp(AST):
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op

class Skip(AST):
    def __init__(self, token):
        self.value = token.value
        self.op = token.type



class NoOp(AST):
    pass

class If(AST):
    def __init__(self, condition, if_true, if_false):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false
        self.op = 'if'

class While(AST):
    def __init__(self, condition, while_true, while_false):
        self.condition = condition
        self.while_true = while_true
        self.while_false = while_false
        self.op = 'while'



########## NEW PARSER ##############

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.state = lexer.state
        self.current_token = lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def factor(self):
        token = self.current_token
        if token.type == MINUS:
            self.current_token = self.lexer.get_next_token()
            token = self.current_token
            token.value = -token.value
            node = Num(token)
        elif token.type == INTEGER:
            node = Num(token)
        elif token.type == ID:
            node = Var(token)
        elif token.type == NOT:
            self.current_token = self.lexer.get_next_token()
            if self.current_token.type == LPAREN:
                self.current_token = self.lexer.get_next_token()
                node = self.boolean_expression()
            elif self.current_token.type == TRUE or self.current_token.type == FALSE:
                node = Bool(token)
            else:
                self.error()
            node = Not(node)
        elif token.type == TRUE or token.type == FALSE:
            node = Bool(token)
        elif token.type == LPAREN:
            self.current_token = self.lexer.get_next_token()
            node = self.boolean_expression()
        elif token.type == RPAREN:
            self.current_token = self.lexer.get_next_token()
        elif token.type == LBRACE:
            self.current_token = self.lexer.get_next_token()
            node = self.statement_expression()
        elif token.type == RBRACE:
            self.current_token = self.lexer.get_next_token()
        elif token.type == SKIP:
            node = Skip(token)
        elif token.type == WHILE:
            self.current_token = self.lexer.get_next_token()
            condition = self.boolean_expression()
            while_false = Skip(Token('skip', 'skip'))
            if self.current_token.type == DO:
                self.current_token = self.lexer.get_next_token()
                if self.current_token == LBRACE:
                    while_true = self.statement_expression()
                else:
                    while_true = self.statement_term()

            return While(condition, while_true, while_false)
        elif token.type == IF:
            self.current_token = self.lexer.get_next_token()
            condition = self.boolean_expression()
            if self.current_token.type == THEN:
                self.current_token = self.lexer.get_next_token()
                if_true = self.statement_expression()
            if self.current_token.type == ELSE:
                self.current_token = self.lexer.get_next_token()
                if_false = self.statement_expression()
            return If(condition, if_true, if_false)
        else:
            self.syntax_error()
        self.current_token = self.lexer.get_next_token()
        return node

    def arith_term(self):
        node = self.factor()
        while self.current_token.type == MUL:
            type_name = self.current_token.type
            self.current_token = self.lexer.get_next_token()
            node = BinOp(left=node, right=self.factor(), op=type_name)
        return node

    def arith_expression(self):
        node = self.arith_term()
        while self.current_token.type in (PLUS, MINUS):
            type_name = self.current_token.type
            self.current_token = self.lexer.get_next_token()
            node = BinOp(left=node, right=self.arith_term(), op=type_name)
        return node

    def arith_parse(self):
        return self.arith_expression()

    def boolean_term(self):
        node = self.arith_expression()
        if self.current_token.type in (EQUAL, LESSTHAN):
            type_name = self.current_token.type
            self.current_token = self.lexer.get_next_token()
            node = BoolOp(left=node, right=self.arith_expression(), op=type_name)
        return node

    def boolean_expression(self):
        node = self.boolean_term()
        while self.current_token.type in (AND, OR):
            type_name = self.current_token.type
            self.current_token = self.lexer.get_next_token()
            node = BinOp(left=node, right=self.boolean_term(), op=type_name)
        return node

    def boolean_parse(self):
        return self.boolean_expression()

    def statement_term(self):
        node = self.boolean_expression()
        if self.current_token.type == ASSIGN:
            type_name = self.current_token.type
            self.current_token = self.lexer.get_next_token()
            node = Assign(left=node, right=self.boolean_expression(), op=type_name)
        return node

    def statement_expression(self):
        node = self.statement_term()
        while self.current_token.type == SEMI:
            type_name = self.current_token.type
            self.current_token = self.lexer.get_next_token()
            node = Semi(left=node, right=self.statement_term(), op=type_name)
        return node

    def statement_parse(self):
        return self.statement_expression()



###############################################################################
#                                                                             #
#  INTERPRETER                                                                #
#                                                                             #
###############################################################################

def dictionary(var, value):
    return dict( [ tuple( [var, value] ) ] )


def to_print(node):
    if node.op in (INTEGER, ID, SKIP):
        return node.value
    elif node.op in (TRUE,FALSE):
        return str(node.value).lower()
    elif node.op in (PLUS, MINUS, MUL, EQUAL, LESSTHAN, AND, OR):
        return ''.join(['(', str(to_print(node.left)), definitions(node.op), str(to_print(node.right)), ')'])
    elif node.op in NOT:
        return ''.join([definitions(node.op), str(to_print(node.ap))])
    elif node.op in ASSIGN:
        return ' '.join([str(to_print(node.left)), definitions(node.op), str(to_print(node.right))])
    elif node.op in SEMI:
        return ' '.join([''.join([str(to_print(node.left)), definitions(node.op)]), str(to_print(node.right))])
    elif node.op in WHILE:
        return ' '.join(['while', str(to_print(node.condition)), 'do', '{', str(to_print(node.while_true)), '}'])
    elif node.op in IF:
        return ' '.join(['if', str(to_print(node.condition)), 'then', '{', str(to_print(node.if_true)), '}', 'else', '{', str(to_print(node.if_false)), '}'])
    else:
        raise Exception('You have a syntax error . . ')


class SubString:
    def __init__(self, string):
        self.string = string

    def __sub__(self, other):
        return self.string.replace(other.string, '', 1)


def eval(ast, state, variables, immediate_state, print_ss, first_step):
    state = state
    node = ast
    variables = variables
    immediate_state = immediate_state
    print_ss = print_ss
    first_step = first_step
    if node.op in (INTEGER, TRUE, FALSE):
        return node.value
    elif node.op == ID:
        if node.value in state:
            return state[node.value]
        else:
            state.update(dictionary(node.value, 0))
            return 0
    elif node.op == SKIP:
        state = state
        temp_variable = set(variables)
        temp_state = copy.deepcopy(state)
        temp_state = dict((var, temp_state[var]) for var in temp_variable)
        immediate_state.append(temp_state)
        temp_step = SubString(str(to_print(node)))
        print_ss.append([SubString(SubString(first_step) - temp_step) - SubString('; ')])
        SubString(SubString(first_step) - temp_step) - SubString('; ') #what the fuck does this do?
    elif node.op == SEMI:
        eval(node.left, state, variables, immediate_state, print_ss, first_step)
        temp_variable = set(variables)
        temp_state = copy.deepcopy(state)
        temp_state = dict((var, temp_state[var]) for var in temp_variable)
        immediate_state.append(temp_state)
        temp_step = SubString(str(to_print(node.left)))
        print_ss.append([str(SubString(SubString(first_step) - temp_step) - SubString('; '))])
        first_step = SubString(SubString(first_step) - temp_step) - SubString('; ')
        eval(node.right, state, variables, immediate_state, print_ss, first_step)
    elif node.op == ASSIGN:
        var = node.left.value
        variables.append(var)
        if var in state:
            state[var] = eval(node.right, state, variables, immediate_state, print_ss, first_step)
        else:
            state.update(dictionary(var, eval(node.right, state, variables, immediate_state, print_ss, first_step)))
        temp_variable = set(variables)
        temp_state = copy.deepcopy(state)
        temp_state = dict((var, temp_state[var]) for var in temp_variable)
        immediate_state.append(temp_state)
        temp_step = SubString(str(to_print(node)))
        print_ss.append(['skip; ' + str(SubString(SubString(first_step) - temp_step) - SubString('; '))])
        SubString(SubString(first_step) - temp_step) - SubString('; ')

    elif node.op == PLUS:
        return eval(node.left, state, variables, immediate_state, print_ss, first_step) + eval(node.right, state, variables, immediate_state, print_ss, first_step)
    elif node.op == MINUS:
        return eval(node.left, state, variables, immediate_state, print_ss, first_step) - eval(node.right, state, variables, immediate_state, print_ss, first_step)
    elif node.op == MUL:
        return eval(node.left, state, variables, immediate_state, print_ss, first_step) * eval(node.right, state, variables, immediate_state, print_ss, first_step)
    elif node.op == NOT:
        return not eval(node.ap, state, variables, immediate_state, print_ss, first_step)
    elif node.op == EQUAL:
        return eval(node.left, state, variables, immediate_state, print_ss, first_step) == eval(node.right, state, variables, immediate_state, print_ss, first_step)
    elif node.op == LESSTHAN:
        return eval(node.left, state, variables, immediate_state, print_ss, first_step) < eval(node.right, state, variables, immediate_state, print_ss, first_step)
    elif node.op == AND:
        return eval(node.left, state, variables, immediate_state, print_ss, first_step) and eval(node.right, state, variables, immediate_state, print_ss, first_step)
    elif node.op == OR:
        return eval(node.left, state, variables, immediate_state, print_ss, first_step) or eval(node.right, state, variables, immediate_state, print_ss, first_step)
    elif node.op == WHILE:
        condition = node.condition
        while_true = node.while_true
        node.while_false
        break_while = 0
        while eval(condition, state, variables, immediate_state, print_ss, first_step):
            break_while += 1
            if break_while >= 10000:
                break
            temp_variable = set(variables)
            temp_state = copy.deepcopy(state)
            temp_state = dict((var, temp_state[var]) for var in temp_variable)
            immediate_state.append(temp_state)
            first_step = first_step.replace(to_print(node), str(to_print(node.while_true) + '; ' + to_print(node)))
            print_ss.append([first_step])
            eval(while_true, state, variables, immediate_state, print_ss, first_step)
            temp_variable = set(variables)
            temp_state = copy.deepcopy(state)
            temp_state = dict((var, temp_state[var]) for var in temp_variable)
            immediate_state.append(temp_state)
            temp_step = SubString(str(to_print(node.while_true)))
            print_ss.append([SubString(SubString(first_step) - temp_step) - SubString('; ')])
            first_step = SubString(SubString(first_step) - temp_step) - SubString('; ')
        temp_variable = set(variables)
        temp_state = copy.deepcopy(state)
        temp_state = dict((var, temp_state[var]) for var in temp_variable)
        immediate_state.append(temp_state)
        temp_step = SubString(to_print(node))
        print_ss.append(['skip; ' + (SubString(SubString(first_step) - temp_step) - SubString('; '))])
        SubString(SubString(first_step) - temp_step) - SubString('; ')
    elif node.op == IF:
        condition = node.condition
        if_true = node.if_true
        if_false = node.if_false
        if eval(condition, state, variables, immediate_state, print_ss, first_step):
            temp_variable = set(variables)
            temp_state = copy.deepcopy(state)
            temp_state = dict((var, temp_state[var]) for var in temp_variable)
            immediate_state.append(temp_state)
            temp_step = SubString(str(to_print(node)))
            print_ss.append([str(to_print(node.if_true)) + (SubString(first_step) - temp_step)])
            first_step = str(to_print(node.if_true)) + (SubString(first_step) - temp_step)
            eval(if_true, state, variables, immediate_state, print_ss, first_step)
        else:
            temp_variable = set(variables)
            temp_state = copy.deepcopy(state)
            temp_state = dict((var, temp_state[var]) for var in temp_variable)
            immediate_state.append(temp_state)
            temp_step = SubString(str(to_print(node)))
            print_ss.append([str(to_print(node.if_false)) + (SubString(first_step) - temp_step)])
            first_step = str(to_print(node.if_false)) + (SubString(first_step) - temp_step)
            eval(if_false, state, variables, immediate_state, print_ss, first_step)
    else:
        raise Exception('Something went wrong!')


class Interpreter:
    def __init__(self, parser):
        self.state = parser.state
        self.ast = parser.statement_parse()
        self.variables = []
        self.immediate_state = []
        self.print_ss = []
        self.first_step = to_print(self.ast)

    def visit(self):
        return eval(self.ast, self.state, self.variables, self.immediate_state, self.print_ss, self.first_step)


def definitions(operand):
    cases = {
        'PLUS': '+',
        'MINUS': '-',
        'MUL': '*',
        'EQUAL': '=',
        'LESSTHAN': '<',
        'AND': '∨',
        'OR': '∧',
        'ASSIGN': ':=',
        'SEMI': ';',
        'NOT': '¬',
    }
    return cases.get(operand, 'You made a mistake!')



def main():
    contents = []
    line = input()
    line = line.strip()
    line = ' '.join(line.split())
    contents.append(line)
    user_input = ' '.join(contents)
    user_input = ' '.join(user_input.split())
    lexer = Lexer(user_input)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.visit()
    steps = interpreter.print_ss
    steps = [item for sublist in steps for item in sublist]
    states = interpreter.immediate_state
    if user_input[0:5] == 'skip;' or user_input[0:6] == 'skip ;':
        del steps[0]
        del states[0]
    steps[-1] = 'skip'
    if len(states) > 10000:
        states = states[0:10000]
        steps = steps[0:10000]
    if len(states) == 1 and states[0] == {} and user_input[0:4] == 'skip':
        print('')
    else:
        for i in range(len(states)):
            output_string = []
            for key in sorted(states[i]):
                output_string.append(' '.join([key, '→', str(states[i][key])]))
            state_string = ''.join(['{', ', '.join(output_string), '}'])
            step_string = ' '.join(['⇒', steps[i]])
            print(step_string, state_string, sep=', ')


if __name__ == '__main__':
    main()