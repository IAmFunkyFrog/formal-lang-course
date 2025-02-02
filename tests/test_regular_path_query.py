import pytest
from pyformlang.regular_expression import Regex

from project.regular_path_query import regular_path_query
from test_utils import create_graph

testdata = [
    (
        regular_path_query(
            Regex("a*"), create_graph(nodes=[0, 1], edges=[(0, "a", 1)])
        ),
        {(0, 1)},
    ),
    (
        regular_path_query(
            Regex("a.b"),
            create_graph(nodes=[0, 1, 2], edges=[(0, "a", 1), (1, "b", 2)]),
        ),
        {(0, 2)},
    ),
    (
        regular_path_query(
            Regex("a*"), create_graph(nodes=[0, 1, 2], edges=[(0, "a", 1), (1, "a", 2)])
        ),
        {(0, 1), (1, 2), (0, 2)},
    ),
    (
        regular_path_query(
            Regex("(a.b)|c"),
            create_graph(
                nodes=[0, 1, 2], edges=[(0, "c", 0), (0, "a", 1), (1, "b", 2)]
            ),
        ),
        {(0, 2), (0, 0)},
    ),
    (
        regular_path_query(
            Regex("c*.a.b"),
            create_graph(
                nodes=[0, 1, 2], edges=[(0, "c", 0), (0, "a", 1), (1, "b", 2)]
            ),
        ),
        {(0, 2)},
    ),
]


@pytest.mark.parametrize("actual,expected", testdata)
def test_regular_path_query(
    actual: set[tuple[any, any]], expected: set[tuple[any, any]]
):
    assert (
        len(actual.difference(expected)) == 0 and len(expected.difference(actual)) == 0
    )
