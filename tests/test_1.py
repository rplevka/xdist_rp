from time import sleep
import pytest

def func(x):
    return x + 1

def test_answer():
    for i in range(1):
        print('sleeping {0}'.format(i))
        sleep(1)
    assert func(3) == 5


def test_answer_2():
    for i in range(1):
        print('sleeping {0}'.format(i))
        sleep(1)
    assert func(3) == 4

class TestWhatever(object):
    def test_answer_3(self):
        for i in range(1):
            print('sleeping {0}'.format(i))
            sleep(1)
        assert func(3) == 4


    def test_answer_4(self):
        for i in range(1):
            print('sleeping {0}'.format(i))
            sleep(1)
        assert func(3) == 4
