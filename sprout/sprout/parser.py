"""Recursive descent parser for the Sprout language."""

from typing import Optional
from .tokens import Token, TokenType
from .ast_nodes import (
    Program, Block, VarDecl, Assign, IfStmt, WhileStmt, ForStmt,
    FunctionDef, ReturnStmt, BreakStmt, ContinueStmt, ExprStmt, ImportStmt,
    BinaryOp, UnaryOp, LogicalOp, Identifier, IntLiteral, FloatLiteral,
    StringLiteral, BoolLiteral, NilLiteral, ArrayLiteral, DictLiteral,
    Subscript, Attribute, Call, FunctionExpr, Node,
)


class ParseError(Exception):
    def __init__(self, message: str, line: int, col: int):
        super().__init__(f"ParseError at {line}:{col}: {message}")
        self.line = line
        self.col = col


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = [t for t in tokens if t.type != TokenType.NEWLINE]
        self.pos = 0

    # ── Helpers ────────────────────────────────────────────────────────────

    def _peek(self, offset: int = 0) -> Token:
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1]  # EOF

    def _current(self) -> Token:
        return self._peek(0)

    def _advance(self) -> Token:
        tok = self.tokens[self.pos]
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return tok

    def _check(self, *types: TokenType) -> bool:
        return self._current().type in types

    def _match(self, *types: TokenType) -> Optional[Token]:
        if self._check(*types):
            return self._advance()
        return None

    def _expect(self, ttype: TokenType, msg: str = "") -> Token:
        if self._check(ttype):
            return self._advance()
        tok = self._current()
        raise ParseError(
            msg or f"Expected {ttype.name}, got {tok.type.name} ({tok.value!r})",
            tok.line, tok.col,
        )

    def _at_end(self) -> bool:
        return self._current().type == TokenType.EOF

    # ── Entry point ────────────────────────────────────────────────────────

    def parse(self) -> Program:
        stmts: list[Node] = []
        while not self._at_end():
            stmts.append(self._parse_statement())
        return Program(1, 1, stmts)

    # ── Statements ─────────────────────────────────────────────────────────

    def _parse_statement(self) -> Node:
        tok = self._current()

        if tok.type == TokenType.LET:
            return self._parse_var_decl()
        if tok.type == TokenType.FN:
            return self._parse_function_def()
        if tok.type == TokenType.IF:
            return self._parse_if()
        if tok.type == TokenType.WHILE:
            return self._parse_while()
        if tok.type == TokenType.FOR:
            return self._parse_for()
        if tok.type == TokenType.RETURN:
            return self._parse_return()
        if tok.type == TokenType.BREAK:
            self._advance()
            self._match(TokenType.SEMICOLON)
            return BreakStmt(tok.line, tok.col)
        if tok.type == TokenType.CONTINUE:
            self._advance()
            self._match(TokenType.SEMICOLON)
            return ContinueStmt(tok.line, tok.col)
        if tok.type == TokenType.IMPORT:
            return self._parse_import()

        return self._parse_expr_stmt()

    def _parse_var_decl(self) -> VarDecl:
        tok = self._expect(TokenType.LET)
        name_tok = self._expect(TokenType.IDENTIFIER, "Expected variable name after 'let'")
        value: Optional[Node] = None
        if self._match(TokenType.ASSIGN):
            value = self._parse_expr()
        self._match(TokenType.SEMICOLON)
        return VarDecl(tok.line, tok.col, name_tok.value, value)

    def _parse_function_def(self) -> FunctionDef:
        tok = self._expect(TokenType.FN)
        name_tok = self._expect(TokenType.IDENTIFIER, "Expected function name after 'fn'")
        params, defaults = self._parse_params()
        body = self._parse_block()
        return FunctionDef(tok.line, tok.col, name_tok.value, params, defaults, body)

    def _parse_params(self) -> tuple[list[str], list[Optional[Node]]]:
        self._expect(TokenType.LPAREN, "Expected '(' in function definition")
        params: list[str] = []
        defaults: list[Optional[Node]] = []
        while not self._check(TokenType.RPAREN) and not self._at_end():
            p = self._expect(TokenType.IDENTIFIER, "Expected parameter name")
            params.append(p.value)
            if self._match(TokenType.ASSIGN):
                defaults.append(self._parse_expr())
            else:
                defaults.append(None)
            if not self._match(TokenType.COMMA):
                break
        self._expect(TokenType.RPAREN, "Expected ')' after parameters")
        return params, defaults

    def _parse_block(self) -> Block:
        tok = self._expect(TokenType.LBRACE, "Expected '{'")
        stmts: list[Node] = []
        while not self._check(TokenType.RBRACE) and not self._at_end():
            stmts.append(self._parse_statement())
        self._expect(TokenType.RBRACE, "Expected '}'")
        return Block(tok.line, tok.col, stmts)

    def _parse_if(self) -> IfStmt:
        tok = self._expect(TokenType.IF)
        condition = self._parse_expr()
        then_branch = self._parse_block()
        elif_branches: list[tuple[Node, Block]] = []
        else_branch: Optional[Block] = None
        while self._check(TokenType.ELSE):
            self._advance()
            if self._check(TokenType.IF):
                self._advance()
                elif_cond = self._parse_expr()
                elif_body = self._parse_block()
                elif_branches.append((elif_cond, elif_body))
            else:
                else_branch = self._parse_block()
                break
        return IfStmt(tok.line, tok.col, condition, then_branch, elif_branches, else_branch)

    def _parse_while(self) -> WhileStmt:
        tok = self._expect(TokenType.WHILE)
        condition = self._parse_expr()
        body = self._parse_block()
        return WhileStmt(tok.line, tok.col, condition, body)

    def _parse_for(self) -> ForStmt:
        tok = self._expect(TokenType.FOR)
        var_tok = self._expect(TokenType.IDENTIFIER, "Expected loop variable")
        self._expect(TokenType.IN, "Expected 'in' after loop variable")
        iterable = self._parse_expr()
        body = self._parse_block()
        return ForStmt(tok.line, tok.col, var_tok.value, iterable, body)

    def _parse_return(self) -> ReturnStmt:
        tok = self._expect(TokenType.RETURN)
        value: Optional[Node] = None
        if (not self._check(TokenType.SEMICOLON) and
                not self._check(TokenType.RBRACE) and
                not self._at_end()):
            value = self._parse_expr()
        self._match(TokenType.SEMICOLON)
        return ReturnStmt(tok.line, tok.col, value)

    def _parse_import(self) -> ImportStmt:
        tok = self._expect(TokenType.IMPORT)
        name_tok = self._expect(TokenType.IDENTIFIER, "Expected module name")
        self._match(TokenType.SEMICOLON)
        return ImportStmt(tok.line, tok.col, name_tok.value)

    def _parse_expr_stmt(self) -> Node:
        expr = self._parse_expr()
        self._match(TokenType.SEMICOLON)
        return ExprStmt(expr.line, expr.col, expr)

    # ── Expressions ────────────────────────────────────────────────────────

    def _parse_expr(self) -> Node:
        return self._parse_assignment()

    def _parse_assignment(self) -> Node:
        expr = self._parse_or()
        assign_ops = {
            TokenType.ASSIGN: "=",
            TokenType.PLUS_ASSIGN: "+=",
            TokenType.MINUS_ASSIGN: "-=",
            TokenType.STAR_ASSIGN: "*=",
            TokenType.SLASH_ASSIGN: "/=",
        }
        if self._current().type in assign_ops:
            op_tok = self._advance()
            op = assign_ops[op_tok.type]
            value = self._parse_assignment()
            if not isinstance(expr, (Identifier, Subscript, Attribute)):
                raise ParseError("Invalid assignment target", op_tok.line, op_tok.col)
            return Assign(op_tok.line, op_tok.col, expr, op, value)
        return expr

    def _parse_or(self) -> Node:
        left = self._parse_and()
        while self._check(TokenType.OR):
            tok = self._advance()
            right = self._parse_and()
            left = LogicalOp(tok.line, tok.col, "or", left, right)
        return left

    def _parse_and(self) -> Node:
        left = self._parse_not()
        while self._check(TokenType.AND):
            tok = self._advance()
            right = self._parse_not()
            left = LogicalOp(tok.line, tok.col, "and", left, right)
        return left

    def _parse_not(self) -> Node:
        if self._check(TokenType.NOT):
            tok = self._advance()
            operand = self._parse_not()
            return UnaryOp(tok.line, tok.col, "not", operand)
        return self._parse_comparison()

    def _parse_comparison(self) -> Node:
        left = self._parse_additive()
        cmp_ops = {
            TokenType.EQ: "==", TokenType.NEQ: "!=",
            TokenType.LT: "<", TokenType.LTE: "<=",
            TokenType.GT: ">", TokenType.GTE: ">=",
        }
        while self._current().type in cmp_ops:
            tok = self._advance()
            right = self._parse_additive()
            left = BinaryOp(tok.line, tok.col, cmp_ops[tok.type], left, right)
        return left

    def _parse_additive(self) -> Node:
        left = self._parse_multiplicative()
        while self._check(TokenType.PLUS, TokenType.MINUS):
            tok = self._advance()
            right = self._parse_multiplicative()
            left = BinaryOp(tok.line, tok.col, tok.value, left, right)
        return left

    def _parse_multiplicative(self) -> Node:
        left = self._parse_unary()
        while self._check(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            tok = self._advance()
            right = self._parse_unary()
            left = BinaryOp(tok.line, tok.col, tok.value, left, right)
        return left

    def _parse_unary(self) -> Node:
        if self._check(TokenType.MINUS):
            tok = self._advance()
            operand = self._parse_unary()
            return UnaryOp(tok.line, tok.col, "-", operand)
        if self._check(TokenType.PLUS):
            self._advance()
            return self._parse_unary()
        return self._parse_power()

    def _parse_power(self) -> Node:
        base = self._parse_postfix()
        if self._check(TokenType.POWER):
            tok = self._advance()
            exp = self._parse_unary()  # right-associative
            return BinaryOp(tok.line, tok.col, "**", base, exp)
        return base

    def _parse_postfix(self) -> Node:
        expr = self._parse_primary()
        while True:
            if self._check(TokenType.LPAREN):
                tok = self._current()
                self._advance()
                args = []
                while not self._check(TokenType.RPAREN) and not self._at_end():
                    args.append(self._parse_expr())
                    if not self._match(TokenType.COMMA):
                        break
                self._expect(TokenType.RPAREN, "Expected ')' after arguments")
                expr = Call(tok.line, tok.col, expr, args)
            elif self._check(TokenType.LBRACKET):
                tok = self._advance()
                index = self._parse_expr()
                self._expect(TokenType.RBRACKET, "Expected ']' after index")
                expr = Subscript(tok.line, tok.col, expr, index)
            elif self._check(TokenType.DOT):
                tok = self._advance()
                attr = self._expect(TokenType.IDENTIFIER, "Expected attribute name after '.'")
                expr = Attribute(tok.line, tok.col, expr, attr.value)
            else:
                break
        return expr

    def _parse_primary(self) -> Node:
        tok = self._current()

        if tok.type == TokenType.INTEGER:
            self._advance()
            return IntLiteral(tok.line, tok.col, tok.value)

        if tok.type == TokenType.FLOAT:
            self._advance()
            return FloatLiteral(tok.line, tok.col, tok.value)

        if tok.type == TokenType.STRING:
            self._advance()
            return StringLiteral(tok.line, tok.col, tok.value)

        if tok.type == TokenType.TRUE:
            self._advance()
            return BoolLiteral(tok.line, tok.col, True)

        if tok.type == TokenType.FALSE:
            self._advance()
            return BoolLiteral(tok.line, tok.col, False)

        if tok.type == TokenType.NIL:
            self._advance()
            return NilLiteral(tok.line, tok.col)

        if tok.type == TokenType.IDENTIFIER:
            self._advance()
            return Identifier(tok.line, tok.col, tok.value)

        if tok.type == TokenType.LPAREN:
            self._advance()
            expr = self._parse_expr()
            self._expect(TokenType.RPAREN, "Expected ')' after expression")
            return expr

        if tok.type == TokenType.LBRACKET:
            return self._parse_array_literal()

        if tok.type == TokenType.LBRACE:
            return self._parse_dict_literal()

        if tok.type == TokenType.FN:
            return self._parse_function_expr()

        raise ParseError(
            f"Unexpected token {tok.type.name} ({tok.value!r})",
            tok.line, tok.col,
        )

    def _parse_array_literal(self) -> ArrayLiteral:
        tok = self._expect(TokenType.LBRACKET)
        elements: list[Node] = []
        while not self._check(TokenType.RBRACKET) and not self._at_end():
            elements.append(self._parse_expr())
            if not self._match(TokenType.COMMA):
                break
        self._expect(TokenType.RBRACKET, "Expected ']'")
        return ArrayLiteral(tok.line, tok.col, elements)

    def _parse_dict_literal(self) -> DictLiteral:
        tok = self._expect(TokenType.LBRACE)
        pairs: list[tuple[Node, Node]] = []
        while not self._check(TokenType.RBRACE) and not self._at_end():
            key = self._parse_expr()
            self._expect(TokenType.COLON, "Expected ':' in dict literal")
            value = self._parse_expr()
            pairs.append((key, value))
            if not self._match(TokenType.COMMA):
                break
        self._expect(TokenType.RBRACE, "Expected '}'")
        return DictLiteral(tok.line, tok.col, pairs)

    def _parse_function_expr(self) -> FunctionExpr:
        tok = self._expect(TokenType.FN)
        params, defaults = self._parse_params()
        body = self._parse_block()
        return FunctionExpr(tok.line, tok.col, params, defaults, body)
