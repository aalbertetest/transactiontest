"""Bytecode instruction set for the Sprout VM."""

from enum import IntEnum, auto
from dataclasses import dataclass, field
from typing import Any


class Op(IntEnum):
    # Stack manipulation
    LOAD_CONST = auto()    # LOAD_CONST <const_idx>
    LOAD_VAR = auto()      # LOAD_VAR <name_idx>
    STORE_VAR = auto()     # STORE_VAR <name_idx>
    DEFINE_VAR = auto()    # DEFINE_VAR <name_idx>
    LOAD_GLOBAL = auto()   # LOAD_GLOBAL <name_idx>
    STORE_GLOBAL = auto()  # STORE_GLOBAL <name_idx>

    # Arithmetic
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()
    POW = auto()
    NEG = auto()

    # Comparison
    EQ = auto()
    NEQ = auto()
    LT = auto()
    LTE = auto()
    GT = auto()
    GTE = auto()

    # Logical
    NOT = auto()
    AND = auto()   # short-circuit: if TOS is false, jump
    OR = auto()    # short-circuit: if TOS is true, jump

    # Control flow
    JUMP = auto()           # JUMP <offset>
    JUMP_IF_FALSE = auto()  # JUMP_IF_FALSE <offset> (pops TOS)
    JUMP_IF_TRUE = auto()   # JUMP_IF_TRUE <offset>  (pops TOS)
    JUMP_IF_FALSE_PEEK = auto()  # short-circuit: peek TOS, jump if false (don't pop)
    JUMP_IF_TRUE_PEEK = auto()   # short-circuit: peek TOS, jump if true (don't pop)

    # Functions
    MAKE_FUNCTION = auto()  # MAKE_FUNCTION <code_idx> <num_defaults>
    CALL = auto()           # CALL <num_args>
    RETURN = auto()

    # Collections
    BUILD_ARRAY = auto()    # BUILD_ARRAY <n>
    BUILD_DICT = auto()     # BUILD_DICT <n pairs>
    GET_ITEM = auto()       # TOS1[TOS]
    SET_ITEM = auto()       # TOS2[TOS1] = TOS  (pops all three)
    GET_ATTR = auto()       # GET_ATTR <name_idx>

    # Iteration
    GET_ITER = auto()
    FOR_ITER = auto()       # FOR_ITER <jump_past_loop>  push next or jump

    # Misc
    POP = auto()
    DUP = auto()
    PRINT = auto()   # legacy shortcut kept for simplicity
    NOP = auto()
    HALT = auto()

    # Loop control markers (resolved by compiler, not executed)
    BREAK_PLACEHOLDER = auto()
    CONTINUE_PLACEHOLDER = auto()


@dataclass
class Instruction:
    op: Op
    arg: int = 0
    line: int = 0

    def __repr__(self) -> str:
        return f"{self.op.name}({self.arg})"


@dataclass
class CodeObject:
    """Compiled code for a function or module."""
    name: str
    params: list[str]
    num_defaults: int
    instructions: list[Instruction] = field(default_factory=list)
    constants: list[Any] = field(default_factory=list)
    names: list[str] = field(default_factory=list)   # variable/attribute names
    nested: list["CodeObject"] = field(default_factory=list)

    def add_const(self, value: Any) -> int:
        """Add constant, reusing existing if possible."""
        for i, c in enumerate(self.constants):
            if c == value and type(c) == type(value):
                return i
        self.constants.append(value)
        return len(self.constants) - 1

    def add_name(self, name: str) -> int:
        if name not in self.names:
            self.names.append(name)
        return self.names.index(name)

    def emit(self, op: Op, arg: int = 0, line: int = 0) -> int:
        idx = len(self.instructions)
        self.instructions.append(Instruction(op, arg, line))
        return idx

    def patch(self, idx: int, arg: int) -> None:
        self.instructions[idx].arg = arg

    def current_offset(self) -> int:
        return len(self.instructions)

    def disassemble(self) -> str:
        lines = [f"<CodeObject '{self.name}'>"]
        lines.append(f"  params:    {self.params}")
        lines.append(f"  constants: {self.constants}")
        lines.append(f"  names:     {self.names}")
        lines.append("  code:")
        for i, instr in enumerate(self.instructions):
            extra = ""
            if instr.op in (Op.LOAD_CONST,):
                val = self.constants[instr.arg] if instr.arg < len(self.constants) else "?"
                extra = f"  ; {val!r}"
            elif instr.op in (Op.LOAD_VAR, Op.STORE_VAR, Op.DEFINE_VAR,
                               Op.LOAD_GLOBAL, Op.STORE_GLOBAL, Op.GET_ATTR):
                name = self.names[instr.arg] if instr.arg < len(self.names) else "?"
                extra = f"  ; '{name}'"
            elif instr.op == Op.MAKE_FUNCTION:
                nested = self.nested[instr.arg] if instr.arg < len(self.nested) else "?"
                extra = f"  ; <fn '{getattr(nested, 'name', '?')}'>"
            lines.append(f"    {i:04d}  {instr.op.name:<24} {instr.arg:>6}{extra}")
        for nested in self.nested:
            lines.append("")
            lines.append(nested.disassemble())
        return "\n".join(lines)
