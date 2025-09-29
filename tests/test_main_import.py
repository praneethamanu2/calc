def test_main_import():
    import main
    assert callable(main.run)
