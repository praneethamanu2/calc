def test_main_run(monkeypatch):
    import main
    called = []
    # Patch the 'repl' symbol inside main to avoid interactive I/O
    monkeypatch.setattr(main, "repl", lambda: called.append(True))
    main.run()
    assert called == [True]
