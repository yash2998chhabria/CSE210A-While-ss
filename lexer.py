class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(type=self.type, value=repr(self.value))

    def __repr__(self):
        return self.__str__()


class Tokenizer:
    def __init__(self, user_input):
        self.state = {}
        self.user_input = user_input
        self.pos = 0
        self.current_char = self.user_input[self.pos]

    def syntax_error(self):
        raise Exception('Invalid input !')

    def next(self):
        self.pos += 1

        if self.pos > len(self.user_input)-1:
            self.current_char = None
        else:
            self.current_char = self.user_input[self.pos]

    def num(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result = result + self.current_char
            self.next()
        return int(result)

    def arr(self):
        result = ''
        self.next()
        while self.current_char is not None and self.current_char != ']':
            result += self.current_char
            self.next()
        self.next()
        result = [int(t) for t in result.split(',')]
        return result

    def assign(self):
        result = ''
        while self.current_char is not None and self.current_char in (':', '='):
            result = result + self.current_char
            self.next()
        if result == ':=':
            return 'assign'
        else:
            self.syntax_error()

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.next()
            if self.current_char.isdigit():
                return Token('INT', self.num())
            if self.current_char == '[':
                return Token('ARR', self.arr())
            if self.current_char == '+':
                self.next()
                return Token('PLUS', '+')
            if self.current_char == '-':
                self.next()
                return Token('MINUS', '-')
            if self.current_char == '*':
                self.next()
                return Token('MUL', '*')
            if self.current_char == ';':
                self.next()
                return Token('SEMI', ';')
            if self.current_char == '=':
                self.next()
                return Token('EQUALS', '=')
            if self.current_char == '<':
                self.next()
                return Token('SMALLER', '<')
            if self.current_char == '¬':
                self.next()
                return Token('NOT', '¬')
            if self.current_char == '∧':
                self.next()
                return Token('AND', '∧')
            if self.current_char == '∨':
                self.next()
                return Token('OR', '∨')
            if self.current_char == '{':
                self.next()
                return Token('LEFT_BRACES', '{')
            if self.current_char == '}':
                self.next()
                return Token('RIGHT_BRACES', '}')
            if self.current_char == '(':
                self.next()
                return Token('LEFT_PARENTHESIS', '(')
            if self.current_char == ')':
                self.next()
                return Token('RIGHT_PARENTHESIS', ')')
            if self.current_char == ':':
                return Token('ASSIGN', self.assign())
            if self.current_char.isalpha():
                result = ''
                while self.current_char is not None and (self.current_char.isalpha() or self.current_char.isdigit()):
                    result = result+self.current_char
                    self.next()
                if result == 'while':
                    return Token('WHILE', 'while')
                elif result == 'skip':
                    return Token('SKIP', 'skip')
                elif result == 'do':
                    return Token('DO', 'do')
                elif result == 'if':
                    return Token('IF', 'if')
                elif result == 'else':
                    return Token('ELSE', 'else')
                elif result == 'then':
                    return Token('THEN', 'then')
                elif result == 'true':
                    return Token('BOOL', True)
                elif result == 'false':
                    return Token('BOOL', False)
                else:
                    return Token('VAR', result)
            self.syntax_error()
        return Token('EOF', None)
