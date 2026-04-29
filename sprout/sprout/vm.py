"""Stack-based virtual machine for the Sprout language."""

from __future__ import annotations
from typing import Any, Optional, Callable
from .bytecode import Op, CodeObject, Instruction


class SproutError(Exception):
    """Runtime error raised during execution."""
    def __init__(self, message: str, line: int = 0):
        super().__init__(message)
        self.line = line


class SproutReturn(Exception):
    """Control flow exception for return statements."""
    def __init__(self, value: Any):
        self.value = value


class SproutBreak(Exception):
    pass


class SproutContinue(Exception):
    pass


class SproutFunction:
    """A first-class function value."""
    def __init__(self, code: CodeObject, defaults: list[Any], closure_env: "Environment"):
        self.code = code
        self.defaults = defaults
        self.closure_env = closure_env

    def __repr__(self) -> str:
        return f"<fn {self.code.name}>"


class SproutIterator:
    """Wraps a Python iterator for the FOR_ITER opcode."""
    def __init__(self, iterable: Any):
        if isinstance(iterable, (list, str, dict)):
            self._iter = iter(iterable)
        elif isinstance(iterable, SproutRange):
            self._iter = iter(iterable)
        else:
            raise SproutError(f"Value of type '{sprout_type(iterable)}' is not iterable")

    def __iter__(self):
        return self._iter

    def __next__(self):
        return next(self._iter)


class SproutRange:
    def __init__(self, *args: int):
        if len(args) == 1:
            self.start, self.stop, self.step = 0, int(args[0]), 1
        elif len(args) == 2:
            self.start, self.stop, self.step = int(args[0]), int(args[1]), 1
        elif len(args) == 3:
            self.start, self.stop, self.step = int(args[0]), int(args[1]), int(args[2])
        else:
            raise SproutError("range() takes 1-3 arguments")

    def __iter__(self):
        return iter(range(self.start, self.stop, self.step))

    def __repr__(self):
        return f"range({self.start}, {self.stop}, {self.step})"


def sprout_type(val: Any) -> str:
    if val is None:
        return "nil"
    if isinstance(val, bool):
        return "bool"
    if isinstance(val, int):
        return "int"
    if isinstance(val, float):
        return "float"
    if isinstance(val, str):
        return "string"
    if isinstance(val, list):
        return "array"
    if isinstance(val, dict):
        return "dict"
    if isinstance(val, SproutFunction):
        return "function"
    if isinstance(val, SproutRange):
        return "range"
    return "object"


def sprout_repr(val: Any) -> str:
    if val is None:
        return "nil"
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, list):
        return "[" + ", ".join(sprout_repr(v) for v in val) + "]"
    if isinstance(val, dict):
        pairs = ", ".join(f"{sprout_repr(k)}: {sprout_repr(v)}" for k, v in val.items())
        return "{" + pairs + "}"
    return str(val)


class Environment:
    """Variable environment (frame-local variables)."""
    def __init__(self, parent: Optional["Environment"] = None):
        self.vars: dict[str, Any] = {}
        self.parent = parent

    def define(self, name: str, value: Any) -> None:
        self.vars[name] = value

    def set(self, name: str, value: Any) -> None:
        if name in self.vars:
            self.vars[name] = value
        elif self.parent:
            self.parent.set(name, value)
        else:
            # New global
            self.vars[name] = value

    def get(self, name: str) -> Any:
        if name in self.vars:
            return self.vars[name]
        if self.parent:
            return self.parent.get(name)
        raise SproutError(f"Undefined variable '{name}'")

    def has(self, name: str) -> bool:
        if name in self.vars:
            return True
        if self.parent:
            return self.parent.has(name)
        return False


class Frame:
    """Execution frame for one function call."""
    def __init__(self, code: CodeObject, env: Environment):
        self.code = code
        self.env = env  # local environment
        self.ip = 0     # instruction pointer
        self.stack: list[Any] = []

    def push(self, val: Any) -> None:
        self.stack.append(val)

    def pop(self) -> Any:
        return self.stack.pop()

    def peek(self, offset: int = 0) -> Any:
        return self.stack[-(1 + offset)]


class VM:
    """Stack-based Sprout virtual machine."""

    def __init__(self, stdout_write: Optional[Callable[[str], None]] = None):
        self._stdout = stdout_write or (lambda s: print(s, end=""))
        self._global_env = Environment()
        self._call_stack: list[Frame] = []
        self._setup_builtins()

    def _setup_builtins(self) -> None:
        env = self._global_env

        def _print(*args):
            self._stdout(" ".join(sprout_repr(a) for a in args))
            return None

        def _println(*args):
            self._stdout(" ".join(sprout_repr(a) for a in args) + "\n")
            return None

        def _input(prompt=""):
            if prompt:
                self._stdout(prompt)
            return input()

        def _len(v):
            if isinstance(v, (list, str, dict)):
                return len(v)
            if isinstance(v, SproutRange):
                return len(range(v.start, v.stop, v.step))
            raise SproutError(f"len() not supported for type '{sprout_type(v)}'")

        def _type(v):
            return sprout_type(v)

        def _str(v):
            return sprout_repr(v)

        def _int(v):
            if isinstance(v, bool):
                return int(v)
            if isinstance(v, (int, float, str)):
                try:
                    return int(v)
                except ValueError:
                    raise SproutError(f"Cannot convert '{v}' to int")
            raise SproutError(f"Cannot convert type '{sprout_type(v)}' to int")

        def _float(v):
            if isinstance(v, (int, float, str)):
                try:
                    return float(v)
                except ValueError:
                    raise SproutError(f"Cannot convert '{v}' to float")
            raise SproutError(f"Cannot convert type '{sprout_type(v)}' to float")

        def _bool(v):
            return _sprout_truthy(v)

        def _range(*args):
            return SproutRange(*args)

        def _append(arr, val):
            if not isinstance(arr, list):
                raise SproutError("append() requires an array")
            arr.append(val)
            return arr

        def _pop(arr, idx=None):
            if not isinstance(arr, list):
                raise SproutError("pop() requires an array")
            if idx is None:
                return arr.pop()
            return arr.pop(int(idx))

        def _keys(d):
            if not isinstance(d, dict):
                raise SproutError("keys() requires a dict")
            return list(d.keys())

        def _values(d):
            if not isinstance(d, dict):
                raise SproutError("values() requires a dict")
            return list(d.values())

        def _has(d, key):
            if isinstance(d, dict):
                return key in d
            raise SproutError("has() requires a dict")

        import math

        def _sqrt(v): return math.sqrt(float(v))
        def _abs(v): return abs(v)
        def _floor(v): return int(math.floor(float(v)))
        def _ceil(v): return int(math.ceil(float(v)))
        def _min(*args):
            if len(args) == 1 and isinstance(args[0], list):
                return min(args[0])
            return min(args)
        def _max(*args):
            if len(args) == 1 and isinstance(args[0], list):
                return max(args[0])
            return max(args)
        def _round(v, n=0): return round(float(v), int(n))

        def _split(s, sep=None):
            if not isinstance(s, str):
                raise SproutError("split() requires a string")
            return s.split(sep)

        def _join(arr, sep=""):
            if not isinstance(arr, list):
                raise SproutError("join() requires an array")
            return sep.join(str(x) for x in arr)

        def _trim(s):
            if not isinstance(s, str):
                raise SproutError("trim() requires a string")
            return s.strip()

        def _upper(s):
            if not isinstance(s, str):
                raise SproutError("upper() requires a string")
            return s.upper()

        def _lower(s):
            if not isinstance(s, str):
                raise SproutError("lower() requires a string")
            return s.lower()

        def _starts_with(s, prefix):
            if not isinstance(s, str):
                raise SproutError("starts_with() requires a string")
            return s.startswith(prefix)

        def _ends_with(s, suffix):
            if not isinstance(s, str):
                raise SproutError("ends_with() requires a string")
            return s.endswith(suffix)

        def _contains(s, sub):
            if isinstance(s, str):
                return sub in s
            if isinstance(s, list):
                return sub in s
            if isinstance(s, dict):
                return sub in s
            raise SproutError("contains() requires a string, array, or dict")

        def _replace(s, old, new):
            if not isinstance(s, str):
                raise SproutError("replace() requires a string")
            return s.replace(old, new)

        def _format(template, *args):
            if not isinstance(template, str):
                raise SproutError("format() requires a string template")
            try:
                return template.format(*[sprout_repr(a) for a in args])
            except (IndexError, KeyError) as e:
                raise SproutError(f"format() error: {e}")

        def _exit(code=0):
            import sys
            sys.exit(int(code))

        def _assert(condition, msg="Assertion failed"):
            if not _sprout_truthy(condition):
                raise SproutError(str(msg))
            return None

        def _make_import(vm_ref):
            def _import(module_name):
                # Built-in module simulation
                modules = {
                    "math": {
                        "pi": math.pi,
                        "e": math.e,
                        "sqrt": lambda x: math.sqrt(float(x)),
                        "sin": lambda x: math.sin(float(x)),
                        "cos": lambda x: math.cos(float(x)),
                        "tan": lambda x: math.tan(float(x)),
                        "log": lambda x: math.log(float(x)),
                        "log2": lambda x: math.log2(float(x)),
                        "log10": lambda x: math.log10(float(x)),
                        "floor": lambda x: int(math.floor(float(x))),
                        "ceil": lambda x: int(math.ceil(float(x))),
                        "abs": lambda x: abs(x),
                        "pow": lambda x, y: x ** y,
                    },
                    "string": {
                        "upper": _upper,
                        "lower": _lower,
                        "trim": _trim,
                        "split": _split,
                        "join": _join,
                        "replace": _replace,
                        "contains": _contains,
                        "starts_with": _starts_with,
                        "ends_with": _ends_with,
                        "format": _format,
                    },
                }
                if module_name not in modules:
                    raise SproutError(f"Unknown module '{module_name}'")
                return modules[module_name]
            return _import

        # Register builtins
        builtins = {
            "print": _print,
            "println": _println,
            "input": _input,
            "len": _len,
            "type": _type,
            "str": _str,
            "int": _int,
            "float": _float,
            "bool": _bool,
            "range": _range,
            "append": _append,
            "pop": _pop,
            "keys": _keys,
            "values": _values,
            "has": _has,
            "sqrt": _sqrt,
            "abs": _abs,
            "floor": _floor,
            "ceil": _ceil,
            "min": _min,
            "max": _max,
            "round": _round,
            "split": _split,
            "join": _join,
            "trim": _trim,
            "upper": _upper,
            "lower": _lower,
            "starts_with": _starts_with,
            "ends_with": _ends_with,
            "contains": _contains,
            "replace": _replace,
            "format": _format,
            "exit": _exit,
            "assert": _assert,
            "__import__": _make_import(self),
        }
        for name, fn in builtins.items():
            env.define(name, fn)

    def run(self, code: CodeObject) -> Any:
        """Execute a top-level CodeObject."""
        env = Environment(parent=self._global_env)
        frame = Frame(code, env)
        self._call_stack.append(frame)
        try:
            result = self._execute(frame)
        finally:
            self._call_stack.pop()
        return result

    def _execute(self, frame: Frame) -> Any:
        code = frame.code
        instructions = code.instructions

        while frame.ip < len(instructions):
            instr = instructions[frame.ip]
            frame.ip += 1
            op = instr.op
            arg = instr.arg

            try:
                if op == Op.LOAD_CONST:
                    frame.push(code.constants[arg])

                elif op == Op.LOAD_VAR:
                    name = code.names[arg]
                    frame.push(frame.env.get(name))

                elif op == Op.STORE_VAR:
                    name = code.names[arg]
                    frame.env.set(name, frame.pop())

                elif op == Op.DEFINE_VAR:
                    name = code.names[arg]
                    frame.env.define(name, frame.pop())

                elif op == Op.LOAD_GLOBAL:
                    name = code.names[arg]
                    # Search frame env first (captures local function scope)
                    if frame.env.has(name):
                        frame.push(frame.env.get(name))
                    else:
                        frame.push(self._global_env.get(name))

                elif op == Op.STORE_GLOBAL:
                    name = code.names[arg]
                    val = frame.pop()
                    if frame.env.has(name):
                        frame.env.set(name, val)
                    else:
                        self._global_env.set(name, val)

                elif op == Op.ADD:
                    b, a = frame.pop(), frame.pop()
                    if isinstance(a, str) and isinstance(b, str):
                        frame.push(a + b)
                    elif isinstance(a, list) and isinstance(b, list):
                        frame.push(a + b)
                    elif isinstance(a, (int, float)) and isinstance(b, (int, float)):
                        frame.push(a + b)
                    else:
                        raise SproutError(
                            f"Unsupported operand types for '+': '{sprout_type(a)}' and '{sprout_type(b)}'",
                            instr.line,
                        )

                elif op == Op.SUB:
                    b, a = frame.pop(), frame.pop()
                    frame.push(a - b)

                elif op == Op.MUL:
                    b, a = frame.pop(), frame.pop()
                    if isinstance(a, str) and isinstance(b, int):
                        frame.push(a * b)
                    elif isinstance(a, int) and isinstance(b, str):
                        frame.push(b * a)
                    elif isinstance(a, list) and isinstance(b, int):
                        frame.push(a * b)
                    else:
                        frame.push(a * b)

                elif op == Op.DIV:
                    b, a = frame.pop(), frame.pop()
                    if b == 0:
                        raise SproutError("Division by zero", instr.line)
                    if isinstance(a, int) and isinstance(b, int):
                        # Integer floor division (Python-style)
                        frame.push(a // b)
                    else:
                        frame.push(a / b)

                elif op == Op.MOD:
                    b, a = frame.pop(), frame.pop()
                    if b == 0:
                        raise SproutError("Modulo by zero", instr.line)
                    frame.push(a % b)

                elif op == Op.POW:
                    b, a = frame.pop(), frame.pop()
                    frame.push(a ** b)

                elif op == Op.NEG:
                    frame.push(-frame.pop())

                elif op == Op.EQ:
                    b, a = frame.pop(), frame.pop()
                    frame.push(a == b)

                elif op == Op.NEQ:
                    b, a = frame.pop(), frame.pop()
                    frame.push(a != b)

                elif op == Op.LT:
                    b, a = frame.pop(), frame.pop()
                    frame.push(a < b)

                elif op == Op.LTE:
                    b, a = frame.pop(), frame.pop()
                    frame.push(a <= b)

                elif op == Op.GT:
                    b, a = frame.pop(), frame.pop()
                    frame.push(a > b)

                elif op == Op.GTE:
                    b, a = frame.pop(), frame.pop()
                    frame.push(a >= b)

                elif op == Op.NOT:
                    frame.push(not _sprout_truthy(frame.pop()))

                elif op == Op.JUMP:
                    frame.ip = arg

                elif op == Op.JUMP_IF_FALSE:
                    val = frame.pop()
                    if not _sprout_truthy(val):
                        frame.ip = arg

                elif op == Op.JUMP_IF_TRUE:
                    val = frame.pop()
                    if _sprout_truthy(val):
                        frame.ip = arg

                elif op == Op.JUMP_IF_FALSE_PEEK:
                    if not _sprout_truthy(frame.peek()):
                        frame.ip = arg

                elif op == Op.JUMP_IF_TRUE_PEEK:
                    if _sprout_truthy(frame.peek()):
                        frame.ip = arg

                elif op == Op.MAKE_FUNCTION:
                    fn_code = code.nested[arg]
                    # Pop defaults (they were pushed before MAKE_FUNCTION)
                    defaults = []
                    for _ in range(fn_code.num_defaults):
                        defaults.insert(0, frame.pop())
                    fn = SproutFunction(fn_code, defaults, frame.env)
                    frame.push(fn)

                elif op == Op.CALL:
                    num_args = arg
                    args = [frame.pop() for _ in range(num_args)]
                    args.reverse()
                    callee = frame.pop()
                    result = self._call(callee, args, instr.line)
                    frame.push(result)

                elif op == Op.RETURN:
                    return frame.pop()

                elif op == Op.GET_ITER:
                    val = frame.pop()
                    frame.push(SproutIterator(val))

                elif op == Op.FOR_ITER:
                    it = frame.peek()
                    try:
                        val = next(it)
                        frame.push(val)
                    except StopIteration:
                        frame.pop()  # pop the iterator
                        frame.ip = arg

                elif op == Op.BUILD_ARRAY:
                    elems = [frame.pop() for _ in range(arg)]
                    elems.reverse()
                    frame.push(elems)

                elif op == Op.BUILD_DICT:
                    pairs: dict = {}
                    items = [frame.pop() for _ in range(arg * 2)]
                    items.reverse()
                    for i in range(0, len(items), 2):
                        pairs[items[i]] = items[i + 1]
                    frame.push(pairs)

                elif op == Op.GET_ITEM:
                    index = frame.pop()
                    obj = frame.pop()
                    if isinstance(obj, list):
                        if not isinstance(index, int):
                            raise SproutError(f"Array index must be int, got '{sprout_type(index)}'")
                        if index < 0 or index >= len(obj):
                            raise SproutError(f"Index {index} out of bounds (length {len(obj)})")
                        frame.push(obj[index])
                    elif isinstance(obj, str):
                        if not isinstance(index, int):
                            raise SproutError("String index must be int")
                        if index < 0 or index >= len(obj):
                            raise SproutError(f"Index {index} out of bounds")
                        frame.push(obj[index])
                    elif isinstance(obj, dict):
                        if index not in obj:
                            raise SproutError(f"Key {sprout_repr(index)!r} not found in dict")
                        frame.push(obj[index])
                    else:
                        raise SproutError(f"Type '{sprout_type(obj)}' is not subscriptable")

                elif op == Op.SET_ITEM:
                    index = frame.pop()
                    obj = frame.pop()
                    value = frame.pop()
                    if isinstance(obj, list):
                        if not isinstance(index, int):
                            raise SproutError("Array index must be int")
                        if index < 0 or index >= len(obj):
                            raise SproutError(f"Index {index} out of bounds")
                        obj[index] = value
                    elif isinstance(obj, dict):
                        obj[index] = value
                    else:
                        raise SproutError(f"Type '{sprout_type(obj)}' does not support item assignment")

                elif op == Op.GET_ATTR:
                    name = code.names[arg]
                    obj = frame.pop()
                    if isinstance(obj, dict):
                        if name not in obj:
                            raise SproutError(f"Dict has no key '{name}'")
                        frame.push(obj[name])
                    elif isinstance(obj, SproutFunction):
                        raise SproutError(f"Function has no attribute '{name}'")
                    else:
                        raise SproutError(f"Type '{sprout_type(obj)}' has no attribute '{name}'")

                elif op == Op.POP:
                    if frame.stack:
                        frame.pop()

                elif op == Op.DUP:
                    frame.push(frame.peek())

                elif op == Op.NOP:
                    pass

                elif op == Op.HALT:
                    return None

                else:
                    raise SproutError(f"Unknown opcode {op}", instr.line)

            except SproutError:
                raise
            except SproutReturn as ret:
                return ret.value
            except Exception as e:
                raise SproutError(str(e), instr.line) from e

        return None

    def _call(self, callee: Any, args: list[Any], line: int) -> Any:
        if callable(callee) and not isinstance(callee, SproutFunction):
            # Python built-in
            try:
                return callee(*args)
            except SproutError:
                raise
            except Exception as e:
                raise SproutError(str(e), line) from e

        if isinstance(callee, SproutFunction):
            fn = callee
            params = fn.code.params
            num_required = len(params) - fn.code.num_defaults

            if len(args) < num_required:
                raise SproutError(
                    f"Function '{fn.code.name}' requires at least {num_required} argument(s), "
                    f"got {len(args)}",
                    line,
                )
            if len(args) > len(params):
                raise SproutError(
                    f"Function '{fn.code.name}' takes at most {len(params)} argument(s), "
                    f"got {len(args)}",
                    line,
                )

            # Build local environment with closure as parent
            local_env = Environment(parent=fn.closure_env)

            # Bind args (with defaults for missing)
            for i, param in enumerate(params):
                if i < len(args):
                    local_env.define(param, args[i])
                else:
                    default_idx = i - num_required
                    local_env.define(param, fn.defaults[default_idx])

            call_frame = Frame(fn.code, local_env)
            self._call_stack.append(call_frame)
            try:
                result = self._execute(call_frame)
            except SproutReturn as ret:
                result = ret.value
            finally:
                self._call_stack.pop()
            return result

        raise SproutError(
            f"Value of type '{sprout_type(callee)}' is not callable", line
        )


def _sprout_truthy(val: Any) -> bool:
    if val is None:
        return False
    if isinstance(val, bool):
        return val
    if isinstance(val, int):
        return val != 0
    if isinstance(val, float):
        return val != 0.0
    if isinstance(val, str):
        return len(val) > 0
    if isinstance(val, list):
        return len(val) > 0
    if isinstance(val, dict):
        return len(val) > 0
    return True
