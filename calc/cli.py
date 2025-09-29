import builtins
from typing import Callable, Dict, Tuple, Optional
from . import operations as ops

Operation = Callable[[float, float], float]

OPERATIONS: Dict[str, Tuple[Operation, str]] = {
    "add": (ops.add, "add X Y     → X + Y"),
    "sub": (ops.sub, "sub X Y     → X - Y"),
    "mul": (ops.mul, "mul X Y     → X * Y"),
    "div": (ops.div, "div X Y     → X / Y"),
}

HELP_TEXT = """Commands:
  add X Y     → X + Y
  sub X Y     → X - Y
  mul X Y     → X * Y
  div X Y     → X / Y
  help        → show this help
  exit|quit|q → leave the calculator
"""

def _format_number(x: float) -> str:
    return str(int(x)) if x.is_integer() else str(x)

def parse_line(line: str) -> Tuple[str, Optional[Tuple[float, float]]]:
    tokens = line.strip().split()
    if not tokens:
        return "__empty__", None

    cmd = tokens[0].lower()

    if cmd in {"exit", "quit", "q"}:
        if len(tokens) != 1:
            return "__error__", (f"'{cmd}' takes no arguments",)  # type: ignore
        return "exit", None

    if cmd == "help":
        if len(tokens) != 1:
            return "__error__", ("'help' takes no arguments",)  # type: ignore
        return "help", None

    if cmd in OPERATIONS:
        if len(tokens) != 3:
            return "__error__", ("expected two numbers, e.g. 'add 2 3'",)  # type: ignore
        try:
            a = float(tokens[1]); b = float(tokens[2])
        except ValueError:
            return "__error__", ("numbers must be numeric (int or float)",)  # type: ignore
        return cmd, (a, b)

    return "__error__", (f"unknown command '{cmd}'. Type 'help' for options.",)  # type: ignore

def process_line(line: str):
    cmd, payload = parse_line(line)

    if cmd == "__empty__":
        return False, None
    if cmd == "__error__":
        return False, f"Error: {payload[0]}"  # type: ignore

    if cmd == "help":
        return False, HELP_TEXT.rstrip("\n")
    if cmd == "exit":
        return True, "Bye!"

    func, _ = OPERATIONS[cmd]
    a, b = payload  # type: ignore
    try:
        res = func(a, b)
        return False, _format_number(res)
    except ZeroDivisionError as e:
        return False, f"Error: {str(e)}"

def repl(input_fn=None, print_fn=None) -> None:
    """
    Interactive loop. Late-binds builtins so tests can inject input/print.
    """
    if input_fn is None:
        input_fn = builtins.input # pragma: no cover
    if print_fn is None:
        print_fn = builtins.print

    print_fn("Simple Calculator. Type 'help' for commands.") 

    while True:
        try:
            line = input_fn("calc> ")
        except EOFError:
            print_fn("\nBye!")
            break

        should_exit, out = process_line(line)
        if out:
            print_fn(out)
        if should_exit:
            break
