"""Command-line entry point: `python -m sprout [file]`."""

import sys
import os
import argparse

from .interpreter import SproutInterpreter
from .repl import start_repl
from .lexer import LexerError
from .parser import ParseError
from .semantic import SemanticError
from .compiler import CompileError
from .vm import SproutError


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="sprout",
        description="Sprout programming language interpreter",
    )
    parser.add_argument("file", nargs="?", help="Sprout source file to run (.sp)")
    parser.add_argument("-c", "--code", help="Execute a Sprout code string")
    parser.add_argument("--dis", action="store_true",
                        help="Disassemble bytecode instead of running")
    parser.add_argument("--ast", action="store_true",
                        help="Print parsed AST and exit")
    args = parser.parse_args()

    if args.file is None and args.code is None:
        start_repl()
        return

    source = args.code
    filename = "<cmd>"

    if args.file:
        filename = args.file
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                source = f.read()
        except FileNotFoundError:
            print(f"sprout: file not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        except OSError as e:
            print(f"sprout: {e}", file=sys.stderr)
            sys.exit(1)

    if args.ast:
        from .lexer import Lexer
        from .parser import Parser
        import ast as _ast
        try:
            tokens = Lexer(source).tokenize()
            tree = Parser(tokens).parse()
            import pprint
            pprint.pprint(tree)
        except (LexerError, ParseError) as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        return

    interp = SproutInterpreter()

    if args.dis:
        try:
            print(interp.disassemble(source, filename))
        except (LexerError, ParseError, SemanticError, CompileError) as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        return

    try:
        interp.run_source(source, filename)
    except (LexerError, ParseError, SemanticError, CompileError, SproutError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
