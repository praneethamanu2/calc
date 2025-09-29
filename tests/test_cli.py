from calc.cli import parse_line, process_line, repl, HELP_TEXT

def test_parse_line_valid():
    assert parse_line("add 2 3") == ("add", (2.0, 3.0))
    assert parse_line("DIV 10 2") == ("div", (10.0, 2.0))
    assert parse_line("help") == ("help", None)
    assert parse_line("exit") == ("exit", None)

def test_parse_line_errors():
    assert process_line("") == (False, None)
    assert process_line("add 1") == (False, "Error: expected two numbers, e.g. 'add 2 3'")
    assert process_line("add one 2") == (False, "Error: numbers must be numeric (int or float)")
    assert process_line("quit now") == (False, "Error: 'quit' takes no arguments")
    assert process_line("help now") == (False, "Error: 'help' takes no arguments")
    assert process_line("foo 1 2")[1].startswith("Error: unknown command")

def test_process_line_ok_and_zero_division():
    assert process_line("add 1 2") == (False, "3")
    assert process_line("sub 5 2") == (False, "3")
    assert process_line("mul 2 2") == (False, "4")
    assert process_line("div 3 2") == (False, "1.5")
    assert process_line("div 1 0") == (False, "Error: division by zero")

def test_help():
    should_exit, out = process_line("help")
    assert should_exit is False
    assert "add X Y" in out
    assert out.strip() == HELP_TEXT.strip()

def test_repl_flow(capsys):
    # Inject an input function: add → help → exit
    inputs = iter(["add 2 3", "help", "exit"])
    repl(input_fn=lambda _: next(inputs))
    printed = capsys.readouterr().out
    assert "Simple Calculator" in printed
    assert "\n5\n" in printed
    assert "Commands:" in printed
    assert "Bye!" in printed

def test_repl_eof(capsys):
    # Simulate Ctrl-D immediately
    def _eof(_): raise EOFError
    repl(input_fn=_eof)
    out = capsys.readouterr().out
    assert "Simple Calculator" in out
    assert "Bye!" in out
