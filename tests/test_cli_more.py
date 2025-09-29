from calc.cli import repl

def test_repl_blank_then_exit(capsys):
    # Exercises the REPL path where process_line returns (False, None)
    inputs = iter(["", "exit"])
    repl(input_fn=lambda _: next(inputs))
    out = capsys.readouterr().out
    assert "Simple Calculator" in out
    assert "Bye!" in out

def test_repl_quit_alias(capsys):
    # Also covers the 'q' alias for exit
    inputs = iter(["q"])
    repl(input_fn=lambda _: next(inputs))
    out = capsys.readouterr().out
    assert "Bye!" in out
