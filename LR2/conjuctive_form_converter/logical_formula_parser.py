from enum import Enum
from dataclasses import dataclass
from itertools import product


class UnrecognisableToken(Exception):
    pass


class ImpossibleSolve(Exception):
    pass


class TokenType(Enum):
    VARIABLE = 0
    LEFT_BRACKET = 1
    RIGHT_BRACKET = 2
    INVERSION = 3
    CONJUCTION = 4
    DISJUNCTION = 5
    IMPLICATION = 6
    EQUIVALENCE = 7
    TRUE = 8
    FALSE = 9


@dataclass
class Token:
    token_type: TokenType
    value: str
    order: int


@dataclass
class FullLogicalInterpretation:
    logical_interpretation: dict
    formula_value: int


class LogicalFormulaParser:
    one_sym_tokens: dict = {'(': TokenType.LEFT_BRACKET, ')': TokenType.RIGHT_BRACKET, '!': TokenType.INVERSION,
                            '¬': TokenType.INVERSION, '&': TokenType.CONJUCTION, '∧': TokenType.CONJUCTION,
                            '∨': TokenType.DISJUNCTION, '⇒': TokenType.IMPLICATION, '→': TokenType.IMPLICATION,
                            '↔': TokenType.EQUIVALENCE, '⇔': TokenType.EQUIVALENCE, '≡': TokenType.EQUIVALENCE,
                            '~': TokenType.EQUIVALENCE}
    token_orders: dict = {TokenType.VARIABLE: -1, TokenType.LEFT_BRACKET: -1, TokenType.RIGHT_BRACKET: -1,
                          TokenType.INVERSION: 0, TokenType.CONJUCTION: 1, TokenType.DISJUNCTION: 2,
                          TokenType.IMPLICATION: 3, TokenType.EQUIVALENCE: 4}

    def __init__(self, raw_formula: str):
        self.token_list: list[Token] = []
        self.raw_formula: str = raw_formula
        self.variables: list[str] = list()
        self.operation_stack: list[Token] = []
        self.value_stack: list[int] = []

    def __replace_special_syms(self):
        self.raw_formula = self.raw_formula.replace('->', '→')
        self.raw_formula = self.raw_formula.replace('=>', '→')
        self.raw_formula = self.raw_formula.replace('<->', '↔')
        self.raw_formula = self.raw_formula.replace('<=>', '↔')
        self.raw_formula = self.raw_formula.replace('^', '∧')
        self.raw_formula = self.raw_formula.replace('+', '∨')
        self.raw_formula = self.raw_formula.replace('*', '∧')

    def __divide_into_tokens(self):
        self.__replace_special_syms()
        raw_token: str = ''
        for sym in self.raw_formula:
            if sym.isdigit() and len(raw_token) == 0:
                raise UnrecognisableToken('Numbers can go only after letters')
            elif sym.isalpha() or sym.isdigit():
                raw_token += sym
            elif sym.isspace():
                continue
            elif self.one_sym_tokens.get(sym, None):
                self.token_list.append(Token(TokenType.VARIABLE, raw_token, self.token_orders[TokenType.VARIABLE]))
                self.variables.append(raw_token)
                raw_token = ''
                new_token_type = self.one_sym_tokens[sym]
                self.token_list.append(Token(new_token_type, sym, self.token_orders[new_token_type]))
            else:
                raise UnrecognisableToken('Forbidden symbol. Logical formula contains only:\n'
                                          '1. Letters\n'
                                          '2. Spaces\n'
                                          '3. Numbers after letters\n'
                                          '4. Logical operations symbols')

    def __solve_operation(self):
        if self.operation_stack[len(self.operation_stack) - 1].token_type == TokenType.INVERSION:
            self.value_stack.append(~self.value_stack.pop())
            self.operation_stack.pop()
            return
        first_value: int = self.value_stack.pop()
        second_value: int = self.value_stack.pop()
        if self.operation_stack[len(self.operation_stack) - 1].token_type == TokenType.CONJUCTION:
            self.value_stack.append(first_value & second_value)
        elif self.operation_stack[len(self.operation_stack) - 1].token_type == TokenType.DISJUNCTION:
            self.value_stack.append(first_value | second_value)
        self.operation_stack.pop()

    def __solve_for_interpretation(self, logical_interpretation: dict):
        for token in self.token_list:
            if token.token_type == TokenType.VARIABLE:
                self.value_stack.append(logical_interpretation[token.value])
            elif token.token_type == TokenType.LEFT_BRACKET:
                self.operation_stack.append(token)
            elif token.token_type in (TokenType.INVERSION, TokenType.CONJUCTION, TokenType.DISJUNCTION,
                                      TokenType.IMPLICATION, TokenType.EQUIVALENCE):
                if len(self.operation_stack) == 0 or self.operation_stack[len(self.operation_stack) - 1].token_type == \
                        TokenType.LEFT_BRACKET:
                    self.operation_stack.append(token)
                else:
                    if token.order > self.operation_stack[len(self.operation_stack) - 1].order:
                        self.operation_stack.append(token)
                    else:
                        while not token.order > self.operation_stack[len(self.operation_stack) - 1].order:
                            self.__solve_operation()
            elif token.token_type == TokenType.RIGHT_BRACKET:
                while not self.operation_stack[len(self.operation_stack) - 1].token_type == TokenType.LEFT_BRACKET:
                    self.__solve_operation()
                self.operation_stack.pop()
        while len(self.operation_stack) != 0:
            self.__solve_operation()
        return FullLogicalInterpretation(logical_interpretation, self.value_stack.pop())

    def solve_formula(self):
        self.__divide_into_tokens()
        possible_var_combs = list(product([0, 1], repeat=len(self.variables)))
        raw_truth_table: list[FullLogicalInterpretation] = list()
        for combo in possible_var_combs:
            logical_interpretation = dict(zip(self.variables, combo))
            raw_truth_table.append(self.__solve_for_interpretation(logical_interpretation))
        return raw_truth_table
