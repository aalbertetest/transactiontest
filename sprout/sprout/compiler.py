"""Bytecode compiler for the Sprout language.

Walks the AST and emits CodeObject bytecode.
"""

from __future__ import annotations
from typing import Optional
from .ast_nodes import (
    Node, Program, Block, VarDecl, Assign, IfStmt, WhileStmt, ForStmt,
    FunctionDef, ReturnStmt, BreakStmt, ContinueStmt, ExprStmt, ImportStmt,
    BinaryOp, UnaryOp, LogicalOp, Identifier, IntLiteral, FloatLiteral,
    StringLiteral, BoolLiteral, NilLiteral, ArrayLiteral, DictLiteral,
    Subscript, Attribute, Call, FunctionExpr,
)
from .bytecode import Op, CodeObject, Instruction


class CompileError(Exception):
    def __init__(self, message: str, line: int = 0, col: int = 0):
        super().__init__(f"CompileError at {line}:{col}: {message}")
        self.line = line
        self.col = col


class _LoopContext:
    """Tracks break/continue patch points for one loop."""
    def __init__(self):
        self.break_patches: list[int] = []
        self.continue_patches: list[int] = []


class Compiler:
    def __init__(self):
        self._code_stack: list[CodeObject] = []
        self._loop_stack: list[_LoopContext] = []
        # Track which names are local (defined with 'let' in current scope)
        self._local_stack: list[set[str]] = []

    # ── Helpers ────────────────────────────────────────────────────────────

    @property
    def _code(self) -> CodeObject:
        return self._code_stack[-1]

    @property
    def _locals(self) -> set[str]:
        return self._local_stack[-1]

    def _emit(self, op: Op, arg: int = 0, line: int = 0) -> int:
        return self._code.emit(op, arg, line)

    def _patch(self, idx: int, arg: int) -> None:
        self._code.patch(idx, arg)

    def _current_offset(self) -> int:
        return self._code.current_offset()

    def _push_code(self, name: str, params: list[str], num_defaults: int) -> CodeObject:
        co = CodeObject(name=name, params=params, num_defaults=num_defaults)
        self._code_stack.append(co)
        self._local_stack.append(set(params))
        return co

    def _pop_code(self) -> CodeObject:
        self._local_stack.pop()
        return self._code_stack.pop()

    def _is_global_scope(self) -> bool:
        return len(self._code_stack) == 1

    def _load_name(self, name: str, line: int) -> None:
        if not self._is_global_scope() and name in self._locals:
            idx = self._code.add_name(name)
            self._emit(Op.LOAD_VAR, idx, line)
        else:
            idx = self._code.add_name(name)
            self._emit(Op.LOAD_GLOBAL, idx, line)

    def _store_name(self, name: str, line: int, define: bool = False) -> None:
        if not self._is_global_scope() and (define or name in self._locals):
            if define:
                self._locals.add(name)
            idx = self._code.add_name(name)
            self._emit(Op.DEFINE_VAR if define else Op.STORE_VAR, idx, line)
        else:
            idx = self._code.add_name(name)
            self._emit(Op.STORE_GLOBAL, idx, line)

    # ── Entry point ────────────────────────────────────────────────────────

    def compile(self, node: Program) -> CodeObject:
        self._push_code("<module>", [], 0)
        self._compile_node(node)
        self._emit(Op.HALT)
        return self._pop_code()

    # ── Dispatch ───────────────────────────────────────────────────────────

    def _compile_node(self, node: Node) -> None:
        method = f"_compile_{type(node).__name__}"
        compiler = getattr(self, method, None)
        if compiler is None:
            raise CompileError(f"No compiler for {type(node).__name__}", getattr(node, "line", 0))
        compiler(node)

    # ── Statements ─────────────────────────────────────────────────────────

    def _compile_Program(self, node: Program) -> None:
        for stmt in node.statements:
            self._compile_node(stmt)

    def _compile_Block(self, node: Block) -> None:
        for stmt in node.statements:
            self._compile_node(stmt)

    def _compile_ExprStmt(self, node: ExprStmt) -> None:
        self._compile_node(node.expr)
        self._emit(Op.POP, 0, node.line)

    def _compile_VarDecl(self, node: VarDecl) -> None:
        if node.value is not None:
            self._compile_node(node.value)
        else:
            idx = self._code.add_const(None)
            self._emit(Op.LOAD_CONST, idx, node.line)
        # DUP so ExprStmt's POP is balanced (VarDecl is never wrapped in ExprStmt,
        # but keeping the stack clean: VarDecl is a statement, no POP needed).
        # VarDecl is always a standalone statement, not inside ExprStmt, so we
        # simply store without leaving anything on the stack.
        self._store_name(node.name, node.line, define=True)
        # VarDecl does NOT push a result; it is handled as a statement, not expr.

    def _compile_Assign(self, node: Assign) -> None:
        if node.op != "=":
            # Compound assignment: load current, compute, store
            self._compile_node(node.target)
            self._compile_node(node.value)
            op_map = {"+=": Op.ADD, "-=": Op.SUB, "*=": Op.MUL, "/=": Op.DIV}
            self._emit(op_map[node.op], 0, node.line)
        else:
            self._compile_node(node.value)

        # DUP so that after storing the value stays on the stack for ExprStmt's POP
        self._emit(Op.DUP, 0, node.line)

        target = node.target
        if isinstance(target, Identifier):
            self._store_name(target.name, node.line)
        elif isinstance(target, Subscript):
            # Stack (bottom→top): dup_val, obj, index → SET_ITEM pops obj+index+val
            # We need: value already on stack (from DUP), then obj, then index
            self._compile_node(target.obj)
            self._compile_node(target.index)
            self._emit(Op.SET_ITEM, 0, node.line)
        elif isinstance(target, Attribute):
            self._compile_node(target.obj)
            name_idx = self._code.add_name(target.name)
            self._emit(Op.GET_ATTR, name_idx, node.line)
        else:
            raise CompileError("Invalid assignment target", node.line, node.col)

    def _compile_IfStmt(self, node: IfStmt) -> None:
        end_patches: list[int] = []

        # Main condition
        self._compile_node(node.condition)
        false_jump = self._emit(Op.JUMP_IF_FALSE, 0, node.line)
        self._compile_node(node.then_branch)
        end_patches.append(self._emit(Op.JUMP, 0, node.line))
        self._patch(false_jump, self._current_offset())

        # elif branches
        for cond, body in node.elif_branches:
            self._compile_node(cond)
            false_jump = self._emit(Op.JUMP_IF_FALSE, 0, node.line)
            self._compile_node(body)
            end_patches.append(self._emit(Op.JUMP, 0, node.line))
            self._patch(false_jump, self._current_offset())

        # else
        if node.else_branch:
            self._compile_node(node.else_branch)

        end = self._current_offset()
        for p in end_patches:
            self._patch(p, end)

    def _compile_WhileStmt(self, node: WhileStmt) -> None:
        ctx = _LoopContext()
        self._loop_stack.append(ctx)

        loop_start = self._current_offset()
        self._compile_node(node.condition)
        exit_jump = self._emit(Op.JUMP_IF_FALSE, 0, node.line)

        self._compile_node(node.body)

        # continue target: re-evaluate condition
        continue_target = loop_start
        self._emit(Op.JUMP, loop_start, node.line)
        loop_end = self._current_offset()
        self._patch(exit_jump, loop_end)

        self._loop_stack.pop()
        for bp in ctx.break_patches:
            self._patch(bp, loop_end)
        for cp in ctx.continue_patches:
            self._patch(cp, continue_target)

    def _compile_ForStmt(self, node: ForStmt) -> None:
        ctx = _LoopContext()
        self._loop_stack.append(ctx)

        # Build iterator from iterable
        self._compile_node(node.iterable)
        self._emit(Op.GET_ITER, 0, node.line)

        loop_start = self._current_offset()
        # FOR_ITER: push next value or jump past loop
        for_iter_instr = self._emit(Op.FOR_ITER, 0, node.line)

        # Store loop variable
        self._store_name(node.var, node.line, define=True)

        # Body
        self._compile_node(node.body)

        # Jump back
        continue_target = loop_start
        self._emit(Op.JUMP, loop_start, node.line)
        loop_end = self._current_offset()
        self._patch(for_iter_instr, loop_end)

        self._loop_stack.pop()
        for bp in ctx.break_patches:
            self._patch(bp, loop_end)
        for cp in ctx.continue_patches:
            self._patch(cp, continue_target)

    def _compile_FunctionDef(self, node: FunctionDef) -> None:
        self._compile_function(node.name, node.params, node.defaults, node.body, node.line)
        # Store the function in the current scope
        self._store_name(node.name, node.line, define=True)

    def _compile_FunctionExpr(self, node: FunctionExpr) -> None:
        self._compile_function("<lambda>", node.params, node.defaults, node.body, node.line)

    def _compile_function(
        self,
        name: str,
        params: list[str],
        defaults: list,
        body: Block,
        line: int,
    ) -> None:
        num_defaults = sum(1 for d in defaults if d is not None)

        # Compile default values in the enclosing scope
        for d in defaults:
            if d is not None:
                self._compile_node(d)

        fn_co = self._push_code(name, params, num_defaults)
        self._compile_node(body)
        # Implicit return nil
        nil_idx = self._code.add_const(None)
        self._emit(Op.LOAD_CONST, nil_idx)
        self._emit(Op.RETURN)
        fn_co = self._pop_code()

        # Register nested code object and emit MAKE_FUNCTION
        nested_idx = len(self._code.nested)
        self._code.nested.append(fn_co)
        self._emit(Op.MAKE_FUNCTION, nested_idx, line)

    def _compile_ReturnStmt(self, node: ReturnStmt) -> None:
        if node.value:
            self._compile_node(node.value)
        else:
            nil_idx = self._code.add_const(None)
            self._emit(Op.LOAD_CONST, nil_idx, node.line)
        self._emit(Op.RETURN, 0, node.line)

    def _compile_BreakStmt(self, node: BreakStmt) -> None:
        if not self._loop_stack:
            raise CompileError("'break' outside loop", node.line, node.col)
        bp = self._emit(Op.JUMP, 0, node.line)
        self._loop_stack[-1].break_patches.append(bp)

    def _compile_ContinueStmt(self, node: ContinueStmt) -> None:
        if not self._loop_stack:
            raise CompileError("'continue' outside loop", node.line, node.col)
        cp = self._emit(Op.JUMP, 0, node.line)
        self._loop_stack[-1].continue_patches.append(cp)

    def _compile_ImportStmt(self, node: ImportStmt) -> None:
        # Call __import__(module_name) and store result as module name
        import_idx = self._code.add_name("__import__")
        self._emit(Op.LOAD_GLOBAL, import_idx, node.line)  # callee first
        idx = self._code.add_const(node.module)
        self._emit(Op.LOAD_CONST, idx, node.line)           # then arg
        self._emit(Op.CALL, 1, node.line)
        self._store_name(node.module, node.line, define=True)

    # ── Expressions ────────────────────────────────────────────────────────

    def _compile_IntLiteral(self, node: IntLiteral) -> None:
        idx = self._code.add_const(node.value)
        self._emit(Op.LOAD_CONST, idx, node.line)

    def _compile_FloatLiteral(self, node: FloatLiteral) -> None:
        idx = self._code.add_const(node.value)
        self._emit(Op.LOAD_CONST, idx, node.line)

    def _compile_StringLiteral(self, node: StringLiteral) -> None:
        idx = self._code.add_const(node.value)
        self._emit(Op.LOAD_CONST, idx, node.line)

    def _compile_BoolLiteral(self, node: BoolLiteral) -> None:
        idx = self._code.add_const(node.value)
        self._emit(Op.LOAD_CONST, idx, node.line)

    def _compile_NilLiteral(self, node: NilLiteral) -> None:
        idx = self._code.add_const(None)
        self._emit(Op.LOAD_CONST, idx, node.line)

    def _compile_Identifier(self, node: Identifier) -> None:
        self._load_name(node.name, node.line)

    def _compile_BinaryOp(self, node: BinaryOp) -> None:
        op_map = {
            "+": Op.ADD, "-": Op.SUB, "*": Op.MUL, "/": Op.DIV,
            "%": Op.MOD, "**": Op.POW,
            "==": Op.EQ, "!=": Op.NEQ,
            "<": Op.LT, "<=": Op.LTE, ">": Op.GT, ">=": Op.GTE,
        }
        self._compile_node(node.left)
        self._compile_node(node.right)
        self._emit(op_map[node.op], 0, node.line)

    def _compile_UnaryOp(self, node: UnaryOp) -> None:
        self._compile_node(node.operand)
        if node.op == "-":
            self._emit(Op.NEG, 0, node.line)
        elif node.op == "not":
            self._emit(Op.NOT, 0, node.line)

    def _compile_LogicalOp(self, node: LogicalOp) -> None:
        self._compile_node(node.left)
        if node.op == "and":
            # Short-circuit: if left is false, jump to end (leave false on stack)
            peek_jump = self._emit(Op.JUMP_IF_FALSE_PEEK, 0, node.line)
            self._emit(Op.POP)
            self._compile_node(node.right)
            self._patch(peek_jump, self._current_offset())
        else:  # or
            # Short-circuit: if left is true, jump to end (leave true on stack)
            peek_jump = self._emit(Op.JUMP_IF_TRUE_PEEK, 0, node.line)
            self._emit(Op.POP)
            self._compile_node(node.right)
            self._patch(peek_jump, self._current_offset())

    def _compile_Call(self, node: Call) -> None:
        self._compile_node(node.callee)
        for arg in node.args:
            self._compile_node(arg)
        self._emit(Op.CALL, len(node.args), node.line)

    def _compile_ArrayLiteral(self, node: ArrayLiteral) -> None:
        for elem in node.elements:
            self._compile_node(elem)
        self._emit(Op.BUILD_ARRAY, len(node.elements), node.line)

    def _compile_DictLiteral(self, node: DictLiteral) -> None:
        for k, v in node.pairs:
            self._compile_node(k)
            self._compile_node(v)
        self._emit(Op.BUILD_DICT, len(node.pairs), node.line)

    def _compile_Subscript(self, node: Subscript) -> None:
        self._compile_node(node.obj)
        self._compile_node(node.index)
        self._emit(Op.GET_ITEM, 0, node.line)

    def _compile_Attribute(self, node: Attribute) -> None:
        self._compile_node(node.obj)
        name_idx = self._code.add_name(node.name)
        self._emit(Op.GET_ATTR, name_idx, node.line)
