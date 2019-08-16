from benchmarkstt.output import Base, factory
import pytest


def test_base():
    with pytest.raises(NotImplementedError):
        Base().result(None)


@pytest.mark.parametrize('kind,expected', [
    [
        'restructuredtext',
        '''title
=====

result

somethingelse
=============

0.420000

'''
    ],
    [
        'markdown',
        '''# title

result

# somethingelse

0.420000

'''
    ],
    [
        'json',
        '[\n\t{"title": "title", "result": "result"},\n\t{"title": "somethingelse", "result": 0.42}\n]\n'
    ],
])
def test_core(kind, expected, capsys):
    data = [
        ['title', 'result'],
        ['somethingelse', 0.420]
    ]
    with factory.create(kind) as cls:
        for title, result in data:
            cls.title(title)
            cls.result(result)

    captured = capsys.readouterr()
    assert expected == captured.out


@pytest.mark.parametrize('cls', ['json'])
def test_already_open(cls):
    with pytest.raises(ValueError) as exc:
        with factory.create(cls) as instance:
            with instance as test:
                raise NotImplementedError("Shouldnt get here")
    assert 'Already open' in str(exc)
