from pathlib import Path

from services.parser import read_text_file


def test_read_text_file(tmp_path):

    test_file = tmp_path / "sample.txt"

    test_file.write_text(
        "Python developer with machine learning experience.",
        encoding="utf-8"
    )

    result = read_text_file(str(test_file))

    assert isinstance(result, str)
    assert "Python" in result
    assert "machine learning" in result


def test_file_not_found():

    fake_file = "this_file_does_not_exist.txt"

    try:
        read_text_file(fake_file)
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        assert True