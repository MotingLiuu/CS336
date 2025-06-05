import pytest

def f():
    raise ExceptionGroup(
            'Group message',
            [
                RuntimeError(),
            ],
    )

def g():
    raise Exception

def test_exception():
    with pytest.raises(Exception) as excinfo:
        g()
    assert isinstance(excinfo.value, Exception)

def test_exception_in_group():
    with pytest.raises(ExceptionGroup) as excinfo:
        f()
    assert excinfo.group_contains(RuntimeError)
    assert not excinfo.group_contains(TypeError)

