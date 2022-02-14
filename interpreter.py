import copy


def dictionary(var, value):
    return dict( [ tuple( [var, value] ) ] )


def to_print(node):
    if node.op in ('INT', 'ARR', 'VAR', 'SKIP'):
        return node.value
    elif node.op in 'BOOL':
        return str(node.value).lower()
    elif node.op in ('PLUS', 'MINUS', 'MUL', 'EQUALS', 'SMALLER', 'AND', 'OR'):
        return ''.join(['(', str(to_print(node.left)), definitions(node.op), str(to_print(node.right)), ')'])
    elif node.op in 'NOT':
        return ''.join([definitions(node.op), str(to_print(node.ap))])
    elif node.op in 'ASSIGN':
        return ' '.join([str(to_print(node.left)), definitions(node.op), str(to_print(node.right))])
    elif node.op in 'SEMI':
        return ' '.join([''.join([str(to_print(node.left)), definitions(node.op)]), str(to_print(node.right))])
    elif node.op in 'WHILE':
        return ' '.join(['while', str(to_print(node.condition)), 'do', '{', str(to_print(node.while_true)), '}'])
    elif node.op in 'IF':
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
    if node.op in ('INT', 'ARR', 'BOOL'):
        return node.value
    elif node.op == 'VAR':
        if node.value in state:
            return state[node.value]
        else:
            state.update(dictionary(node.value, 0))
            return 0
    elif node.op == 'SKIP':
        state = state
        temp_variable = set(variables)
        temp_state = copy.deepcopy(state)
        temp_state = dict((var, temp_state[var]) for var in temp_variable)
        immediate_state.append(temp_state)
        temp_step = SubString(str(to_print(node)))
        print_ss.append([SubString(SubString(first_step) - temp_step) - SubString('; ')])
        SubString(SubString(first_step) - temp_step) - SubString('; ') #what the fuck does this do?
    elif node.op == 'SEMI':
        eval(node.left, state, variables, immediate_state, print_ss, first_step)
        temp_variable = set(variables)
        temp_state = copy.deepcopy(state)
        temp_state = dict((var, temp_state[var]) for var in temp_variable)
        immediate_state.append(temp_state)
        temp_step = SubString(str(to_print(node.left)))
        print_ss.append([str(SubString(SubString(first_step) - temp_step) - SubString('; '))])
        first_step = SubString(SubString(first_step) - temp_step) - SubString('; ')
        eval(node.right, state, variables, immediate_state, print_ss, first_step)
    elif node.op == 'ASSIGN':
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

    elif node.op == 'PLUS':
        return eval(node.left, state, variables, immediate_state, print_ss, first_step) + eval(node.right, state, variables, immediate_state, print_ss, first_step)
    elif node.op == 'MINUS':
        return eval(node.left, state, variables, immediate_state, print_ss, first_step) - eval(node.right, state, variables, immediate_state, print_ss, first_step)
    elif node.op == 'MUL':
        return eval(node.left, state, variables, immediate_state, print_ss, first_step) * eval(node.right, state, variables, immediate_state, print_ss, first_step)
    elif node.op == 'NOT':
        return not eval(node.ap, state, variables, immediate_state, print_ss, first_step)
    elif node.op == 'EQUALS':
        return eval(node.left, state, variables, immediate_state, print_ss, first_step) == eval(node.right, state, variables, immediate_state, print_ss, first_step)
    elif node.op == 'SMALLER':
        return eval(node.left, state, variables, immediate_state, print_ss, first_step) < eval(node.right, state, variables, immediate_state, print_ss, first_step)
    elif node.op == 'AND':
        return eval(node.left, state, variables, immediate_state, print_ss, first_step) and eval(node.right, state, variables, immediate_state, print_ss, first_step)
    elif node.op == 'OR':
        return eval(node.left, state, variables, immediate_state, print_ss, first_step) or eval(node.right, state, variables, immediate_state, print_ss, first_step)
    elif node.op == 'WHILE':
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
    elif node.op == 'IF':
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
        'EQUALS': '=',
        'SMALLER': '<',
        'AND': '∨',
        'OR': '∧',
        'ASSIGN': ':=',
        'SEMI': ';',
        'NOT': '¬',
    }
    return cases.get(operand, 'You made a mistake!')
