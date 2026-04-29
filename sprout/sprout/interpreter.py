"""High-level interpreter pipeline: source → tokens → AST → bytecode → execution."""

from __future__ import annotations
from typing import Any, Callable, Optional
from io import StringIO

from .lexer import Lexer, LexerError
from .parser import Parser, ParseError
from .semantic import SemanticAnalyzer, SemanticError
from .compiler import Compiler, CompileError
from .vm import VM, SproutError
from .bytecode import CodeObject


class SproutInterpreter:
    """Combines all pipeline stages into a single convenience object."""

    def __init__(self, stdout_write: Optional[Callable[[str], None]] = None):
        self.vm = VM(stdout_write=stdout_write)
        self._compiler = Compiler()

    def run_source(self, source: str, filename: str = "<input>") -> Any:
        """Lex, parse, analyse, compile and run *source*. Returns the last value."""
        code = self.compile(source, filename)
        return self.vm.run(code)

    def compile(self, source: str, filename: str = "<input>") -> CodeObject:
        """Return compiled CodeObject without executing."""
        tokens = Lexer(source).tokenize()
        ast = Parser(tokens).parse()
        SemanticAnalyzer().analyze(ast)
        compiler = Compiler()
        return compiler.compile(ast)

    def disassemble(self, source: str, filename: str = "<input>") -> str:
        co = self.compile(source, filename)
        return co.disassemble()

    def run_file(self, path: str) -> Any:
        with open(path, "r", encoding="utf-8") as f:
            source = f.read()
        return self.run_source(source, filename=path)


def run_string(source: str) -> str:
    """Helper for tests: run Sprout source and capture stdout as a string."""
    buf = StringIO()
    interp = SproutInterpreter(stdout_write=buf.write)
    interp.run_source(source)
    return buf.getvalue()
