from cmath import exp
from collections import namedtuple
from unittest import expectedFailure
from pprint import pprint


Task = namedtuple('Task', ['summary', 'owner', 'done', 'id'])
Task.__new__.__defaults__ = (None, None, False, None)

def test_defaults():
    t1 = Task()
    t2 = Task(None, None, False, None)
    assert t1 == t2


def test_member_access():
    t = Task('buy milk', 'brian')
    assert t.summary == 'buy milk'
    assert t.owner == 'brian'
    assert (t.done, t.id) == (False, None)

def test_asdict():
    t_task = Task('finish book', 'brian', False)
    t_dict = t_task._asdict()
    pprint(dict(t_dict))
    expected = {'summary':'finish book', 'owner':'brian', 'done': False, 'id': None}
    assert t_dict == expected