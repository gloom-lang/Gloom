from pprint import pprint as print

from enum import Enum

class Token(Enum):
    LPAREN = "("
    RPAREN = ")"
    PLUS = "+"
    MINUS = "-"
    TIMES = "*"
    DIV = "/"
    COMMA = ","
    HASH = "#"
    PERIOD = "."
    OBJECT = "object"
    NAMED_PARAMETER = "named_param"
    NUMBER = "number"
    STRING = "string"
    BOOLEAN = "boolean"
    BINARY_MESSAGE = "binary_message"
    NAMED_MESSAGE = "named_message"
    UNARY_MESSAGE = "unary_message"


class Lexer:

    def __init__(self):
        self.program = ""
        self.position = 0
        self.buffer = ""
        self.tokens = []
        self.maybe_token_type = None


    def reset(self):
        self.program = ""
        self.buffer = ""
        self.tokens = []
        self.maybe_token_type = None


    def dump_buffer(self):
        self.tokens.append(
            (self.maybe_token_type, self.buffer)
        )
        self.maybe_token_type = None
        self.buffer = ""


    def eat(self):
        self.buffer += self.current_character
        self.advance()


    @property
    def current_character(self):
        return self.program[self.position]
    

    def peek(self):
        try:
            self.position += 1
            char = self.current_character
        except IndexError:
            char = None
        self.retract()
        return char
    

    def is_eof(self):
        try:
            self.current_character
            return False
        except IndexError:
            return True
        

    def is_paren(self):
        return self.current_character in "()"
    

    def is_space(self):
        return self.is_eof() or self.current_character.isspace()
    

    def is_param(self):
        return not self.is_eof() and self.current_character.isidentifier()
    

    def is_numeric(self):
        if self.current_character == ".":
            next_character = self.peek()
            return False if next_character is None else next_character.isnumeric()
        return self.current_character.isnumeric()
    
    def is_number(self):
        return not self.is_eof() and self.is_numeric()
    

    def is_string_end(self, start_quote):
        return self.is_eof() or self.current_character == start_quote

    def advance(self):
        self.position += 1


    def retract(self):
        self.position -= 1


    def handle_lparen(self):
        self.maybe_token_type = Token.LPAREN
        self.buffer += self.current_character
        self.dump_buffer()


    def handle_rparen(self):
        self.maybe_token_type = Token.RPAREN
        self.buffer += self.current_character
        self.dump_buffer()


    def handle_plus(self):
        self.maybe_token_type = Token.PLUS
        self.buffer += self.current_character
        self.dump_buffer()


    def handle_minus(self):
        self.maybe_token_type = Token.MINUS
        self.buffer += self.current_character
        self.dump_buffer()


    def handle_comma(self):
        self.maybe_token_type = Token.COMMA
        self.buffer += self.current_character
        self.dump_buffer()


    def handle_period(self):
        self.maybe_token_type = Token.PERIOD
        self.buffer += self.current_character
        self.dump_buffer()


    def handle_hash(self):
        self.maybe_token_type = Token.HASH
        self.buffer += self.current_character
        self.dump_buffer()


    def handle_times(self):
        self.maybe_token_type = Token.TIMES
        self.buffer += self.current_character
        self.dump_buffer()


    def handle_div(self):
        self.maybe_token_type = Token.DIV
        self.buffer += self.current_character
        self.dump_buffer()


    def handle_named_parameter(self):
        self.maybe_token_type = Token.NAMED_PARAMETER
        self.advance()
        while self.is_param():
            self.eat()
        self.dump_buffer()
        self.retract()


    def handle_object(self):
        self.maybe_token_type = Token.OBJECT
        while self.is_param():
            self.eat()
        self.dump_buffer()
        self.retract()


    def handle_number(self):
        self.maybe_token_type = Token.NUMBER
        while self.is_number():
            self.eat()
        self.dump_buffer()
        self.retract()


    def handle_binary(self):
        self.maybe_token_type = Token.BINARY_MESSAGE
        self.buffer += self.current_character
        self.dump_buffer()


    def handle_string(self):
        self.maybe_token_type = Token.STRING
        end_quote = self.current_character
        self.advance()
        while not self.is_string_end(end_quote):
            self.eat()
        self.dump_buffer()
        # We don't retract here -- current character is string_end,
        # and next we'll advance and be out of the string


    def check_true(self):
        end_index = self.current_position + 4            
        maybe_true = self.program[self.current_position:end_index]
        return maybe_true == "true"
    

    def check_false(self):
        end_index = self.current_position + 5      
        maybe_false = self.program[self.current_position:end_index]
        return maybe_false == "false"
    

    def handle_true(self):
        self.buffer = "true"
        self.dump_buffer()
        self.advance()
        self.advance()
        self.advance()
        self.advance()


    def handle_false(self):
        self.buffer = "false"
        self.dump_buffer()
        self.advance()
        self.advance()
        self.advance()
        self.advance()
        self.advance()      
    

    def handle_boolean(self, bool_value):
        self.maybe_token_type = Token.BOOLEAN
        if bool_value == "true":
            self.handle_true()
        else:
            self.handle_false()



    def lex(self, program):
        self.program = program
        while not self.is_eof():
            match self.current_character:
                case "(":
                    self.handle_lparen()
                case ")":
                    self.handle_rparen()
                case "#":
                    self.handle_hash()
                case "+" | "-" | "," | "/" | "%" | "*":
                    self.handle_binary()
                case ".":
                    self.handle_period()
                case ":":
                    self.handle_named_parameter()
                case "'" | '"':
                    self.handle_string()
                case c if c.isspace():
                    pass
                case c if c.isnumeric():
                    self.handle_number()
                case c if c == "t" or c == "f":
                    if self.check_true():
                        self.handle_boolean("true")
                    elif self.check_false():
                        self.handle_boolean("false")
                    self.handle_object()
                case c:
                    self.handle_object()
            self.advance()
        return self.tokens
    


class EverythingNode:

    def __init__(self):
        pass


class MessageSendNode:

    def __init__(self, receiver, arguments):
        self.receiver = receiver
        self.arguments = arguments


    def __repr__(self):
        return f"""MessageSendNode(
            receiver={self.receiver}, 
            arguments={self.arguments}
        )
                    """
    

    def evaluate(self, environment):
        if isinstance(self.receiver, MessageSendNode):
            self.receiver = self.receiver.evaluate(environment)

        message_payload = {}
        for argument in self.arguments:
            message_payload[argument.selector] = argument.evaluate(environment)

        value = self.receiver.send(message_payload, environment)
        return value


    

class MessageArgumentNode:

    def __init__(self, selector, value):
        self.selector = selector
        self.value = value


    def __repr__(self):
        return f"""Argument({self.selector}, {self.value})"""
    

    def evaluate(self, environment):
        if isinstance(self.value, MessageSendNode):
            self.value.evaluate(environment)
        if isinstance(self.value, list):
            return []
        return self.value.evaluate(environment)
        



class ObjectNode:

    def __init__(self, value, kind):
        self.value = value
        self.kind = kind
        self.properties = {}


    def evaluate(self, environment):
        return self if self.kind != 'object' else self.properties.get(self.value, 0)


    def send(self, payload, environment):
        if payload.get('print'):
            print(self.value)
        elif (m := payload.get("+")):
            self.value += m.value
        elif (m := payload.get("*")):
            self.value *= m.value
        elif (varname := payload.get("set")):
            value = payload.get("to")
            self.properties[varname] = value
 
        return self


    def __repr__(self):
        return f"Object({self.value}, {self.kind})"


class Parser:

    def __init__(self, tokens=None):
        if tokens is None:
            tokens = []
        self.tokens = tokens
        self.ast = None
        self.position = 0
        self.target = None
        self.buffer = []


    def parse(self, program_string):
        lexer = Lexer()
        self.tokens = lexer.lex(program_string)
        return self.parse_program()


    def eof(self):
        try:
            self.current_token
            return False
        except IndexError:
            return True
        

    def advance(self):
        self.position += 1


    def retreat(self):
        self.position -= 1
        

    @property
    def current_token(self):
        return self.tokens[self.position]
    

    @property
    def current_tokentype(self):
        return self.current_token[0]
    

    @property
    def current_tokenvalue(self):
        return self.current_token[1]

    
    def consume(self, kind):
        if self.current_tokentype == kind:
            self.advance()
        else:
            raise SyntaxError(f'weird, I expected {kind}, but got {self.current_tokentype} instead')


    def peek(self, kinds):
        if not isinstance(kinds, list):
            kinds = [kinds]
        self.advance()
        if self.eof():
            self.retreat()
            return False
        is_of_kind = self.current_tokentype in kinds
        self.retreat()
        return is_of_kind

    

    def is_lparen(self):
        return self.current_tokentype == Token.LPAREN
    

    def is_rparen(self):
        return self.current_tokentype == Token.RPAREN
    

    def is_period(self):
        return self.current_tokentype == Token.PERIOD
    

    def is_message_parameter(self):
        return self.current_tokentype in (
            Token.BINARY_MESSAGE,
            Token.NAMED_PARAMETER
        )


    def parse_program(self):
        return self.parse_statements()


    def parse_statements(self):
        statements = []
        while not self.eof():
            statements.append(
                self.parse_statement()
            )
        return statements
    

    def prepend_everything_token(self):
        self.tokens.insert(
            self.position, (Token.OBJECT, "Everything")
        )



    def parse_statement(self):
        if self.is_message_parameter():
            self.prepend_everything_token()
        value = self.parse_message_send()
        self.consume(Token.PERIOD)
        return value


    def parse_message_send(self):
        return MessageSendNode(
            self.parse_receiver(), 
            self.parse_arguments()
        )
    

    def parse_receiver(self):
        try:
            self.consume(Token.LPAREN)
            receiver = self.parse_message_send()
            self.consume(Token.RPAREN)
            return receiver
        except SyntaxError:
            return self.parse_value()


    def parse_unary_argument(self):
        value = MessageArgumentNode(
            self.current_tokenvalue,
            []
        )
        self.advance()
        return value


    def parse_named_argument(self):
        value = MessageArgumentNode(
            self.current_tokenvalue,
            self.parse_value()
        )
        self.advance()
        return value


    def parse_unary_or_named_argument(self):
        values = [
            Token.LPAREN,
            Token.STRING,
            Token.NUMBER,
            Token.BOOLEAN,
            Token.OBJECT,
            Token.HASH
        ]
        if not self.peek(values):
            value = self.parse_unary_argument()
        else:
            value = self.parse_binary_argument()
        return value
    

    def parse_binary_argument(self):
        return MessageArgumentNode(
            self.parse_operator(),
            self.parse_value()
        )


    def parse_operator(self):
        value = self.current_tokenvalue
        self.advance()
        return value


    def parse_arguments(self):
        arguments = []
        while not self.eof() and not self.is_period() and not self.is_rparen():
            match self.current_tokentype:
                case Token.NAMED_PARAMETER:
                    arguments.append(
                        self.parse_unary_or_named_argument()
                    )
                case Token.BINARY_MESSAGE:
                    arguments.append(
                        self.parse_binary_argument()
                    )
        return arguments
        

    def parse_number(self):
        value = ObjectNode(
            float(self.current_tokenvalue),
            "number"
        )
        self.advance()
        return value
    

    def parse_string(self):
        value = ObjectNode(
             self.current_tokenvalue,
            "string"
        )
        self.advance()
        return value

    
    def parse_array(self):
        self.consume(Token.HASH)
        self.consume(Token.LPAREN)
        value = ObjectNode(
            [],
            "array"
        )
        while not (self.eof() or self.is_rparen()):
            value.value.append(
                self.parse_value()
            )
        self.consume(Token.RPAREN)
        return value

    
    def parse_boolean(self):
        value = ObjectNode(
            self.current_tokenvalue == "true",
            "boolean"
        )
        self.advance()
        return value
    

    def parse_object(self):
        value = ObjectNode(
            self.current_tokenvalue,
            "object"
        )
        self.advance()
        return value
    
        

    def parse_value(self):
        match self.current_tokentype:
            # parse literal
            case Token.NUMBER:
                return self.parse_number()
            case Token.STRING:
                return self.parse_string()
            case Token.HASH:
                return self.parse_array()
            case Token.BOOLEAN:
                return self.parse_boolean()

            # parse name
            case Token.OBJECT:
                return self.parse_object()
            
            # parse message send
            case Token.LPAREN:
                self.consume(Token.LPAREN)
                value = self.parse_message_send()
                self.consume(Token.RPAREN)
                return value
            case _:
                raise Exception(
                    f"hmmm i was expecting something nicer like a number | string | hash | boolean | object but got {self.current_token} instead ;//"
                )
        
    


if __name__ == '__main__':
    program = """
    :listen.
    ((1 + 2) * 3) :print.
    :set x :to 5.
    :set y :to x :at 6.0.
    y :print.

    :set x :to #(1 2 3 #(4.0 5)).
    :set y :to (x :at 2).
    y :print.

    1 :times 5.
    """
    l = Lexer()
    tokens = l.lex(program)
    p = Parser(tokens)
    ast = p.parse_program()
    print(ast, indent=2)
