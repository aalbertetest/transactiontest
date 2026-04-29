"""Interactive REPL for the Sprout language."""

from __future__ import annotations
import sys
import os
import traceback
from io import StringIO
from typing import Optional

from .lexer import Lexer, LexerError
from .parser import Parser, ParseError
from .semantic import SemanticAnalyzer, SemanticError
from .compiler import Compiler, CompileError
from .vm import VM, SproutError, sprout_repr
from .bytecode import CodeObject

BANNER = """\
  ____                       _
 / ___| _ __  _ __ ___  _   _| |_
 \\___ \\| '_ \\| '__/ _ \\| | | | __|
  ___) | |_) | | | (_) | |_| | |_
 |____/| .__/|_|  \\___/ \\__,_|\\__|
       |_|

  Sprout v0.1.0 — type 'exit' or Ctrl-D to quit
  type '.help' for commands, '.dis' to disassemble last input
"""

HELP_TEXT = """
REPL Commands:
  .help      Show this help message
  .exit      Quit the REPL
  .dis       Disassemble last compiled code
  .clear     Clear the accumulated block buffer
  .reset     Reset the VM (clear all variables)
  exit       Alias for .exit (also works as a function call: exit())
"""


def _is_complete(source: str) -> bool:
    """
    Heuristic to decide whether the user's input is a complete statement.
    Counts unmatched { braces. If the source has open braces, it's incomplete.
    """
    depth = 0
    in_string = False
    string_char = ""
    i = 0
    while i < len(source):
        ch = source[i]
        if in_string:
            if ch == "\\" and i + 1 < len(source):
                i += 2
                continue
            if ch == string_char:
                in_string = False
        elif ch in ('"', "'"):
            in_string = True
            string_char = ch
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        i += 1
    return depth <= 0


class REPL:
    def __init__(self):
        self._vm = VM(stdout_write=sys.stdout.write)
        self._buffer: list[str] = []
        self._last_code: Optional[CodeObject] = None
        self._history: list[str] = []

        # Enable readline if available
        try:
            import readline
            history_file = os.path.expanduser("~/.sprout_history")
            try:
                readline.read_history_file(history_file)
            except FileNotFoundError:
                pass
            import atexit
            atexit.register(readline.write_history_file, history_file)
        except ImportError:
            pass

    def run(self) -> None:
        print(BANNER)
        while True:
            try:
                prompt = ">>> " if not self._buffer else "... "
                try:
                    line = input(prompt)
                except EOFError:
                    print("\nBye!")
                    break

                # Handle REPL meta-commands
                stripped = line.strip()
                if stripped in ("exit", ".exit", "quit", ".quit"):
                    print("Bye!")
                    break
                if stripped == ".help":
                    print(HELP_TEXT)
                    continue
                if stripped == ".clear":
                    self._buffer.clear()
                    print("Buffer cleared.")
                    continue
                if stripped == ".reset":
                    self._vm = VM(stdout_write=sys.stdout.write)
                    self._buffer.clear()
                    print("VM reset.")
                    continue
                if stripped == ".dis":
                    if self._last_code:
                        print(self._last_code.disassemble())
                    else:
                        print("No code compiled yet.")
                    continue

                self._buffer.append(line)
                source = "\n".join(self._buffer)

                if not _is_complete(source):
                    continue  # Wait for more input

                if source.strip() == "":
                    self._buffer.clear()
                    continue

                self._execute_source(source)
                self._buffer.clear()

            except KeyboardInterrupt:
                self._buffer.clear()
                print("\n(interrupted — buffer cleared)")

    def _execute_source(self, source: str) -> None:
        try:
            tokens = Lexer(source).tokenize()
            ast = Parser(tokens).parse()
            SemanticAnalyzer().analyze(ast)
            compiler = Compiler()
            code = compiler.compile(ast)
            self._last_code = code

            # Wrap in a temporary module frame but share the global env
            from .bytecode import Op
            from .vm import Frame, Environment

            env = Environment(parent=self._vm._global_env)
            frame = Frame(code, env)
            self._vm._call_stack.append(frame)
            try:
                result = self._vm._execute(frame)
            finally:
                self._vm._call_stack.pop()

            # Promote globals defined in this run to the global env
            for name, val in env.vars.items():
                self._vm._global_env.define(name, val)

            if result is not None:
                print(sprout_repr(result))

        except (LexerError, ParseError, SemanticError, CompileError, SproutError) as e:
            print(f"\x1b[31mError: {e}\x1b[0m")
        except Exception as e:
            print(f"\x1b[31mInternal error: {e}\x1b[0m")
            if os.environ.get("SPROUT_DEBUG"):
                traceback.print_exc()


def start_repl() -> None:
    REPL().run()
