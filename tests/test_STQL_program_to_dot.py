import pydot
import pytest

from language.language_utils import STQL_program_to_dot


def dot_from_string(s: str) -> pydot.Dot:
    graphs = pydot.graph_from_dot_data(s)
    return graphs[0]


testdata = [
    (
        "/* simple comment */",
        dot_from_string(
            """
            digraph "STQL program" {
                1 [label="Rule[prog]"];
                2 [label="Rule[comment]"];
                1 -> 2;
                3 [label="/*"];
                2 -> 3;
                4 [label="simple"];
                2 -> 4;
                5 [label="comment"];
                2 -> 5;
                6 [label="*/"];
                2 -> 6;
            }
        """
        ),
    ),
    (
        "print 1;",
        dot_from_string(
            """
            digraph "STQL program" {
                1 [label="Rule[prog]"];
                2 [label="Rule[print_stmt]"];
                1 -> 2;
                3 [label="print"];
                2 -> 3;
                4 [label="Rule[expr]"];
                2 -> 4;
                5 [label="Rule[const]"];
                4 -> 5;
                6 [label="1"];
                5 -> 6;
                7 [label=";"];
                1 -> 7;
            }
        """
        ),
    ),
    (
        "number := 1;",
        dot_from_string(
            """
            digraph "STQL program" {
                1 [label="Rule[prog]"];
                2 [label="Rule[bind]"];
                1 -> 2;
                3 [label="number"];
                2 -> 3;
                4 [label=":="];
                2 -> 4;
                5 [label="Rule[expr]"];
                2 -> 5;
                6 [label="Rule[const]"];
                5 -> 6;
                7 [label="1"];
                6 -> 7;
                8 [label=";"];
                1 -> 8;
            }
        """
        ),
    ),
    (
        'string := "str";',
        dot_from_string(
            """
            digraph "STQL program" {
                1 [label="Rule[prog]"];
                2 [label="Rule[bind]"];
                1 -> 2;
                3 [label="string"];
                2 -> 3;
                4 [label=":="];
                2 -> 4;
                5 [label="Rule[expr]"];
                2 -> 5;
                6 [label="Rule[const]"];
                5 -> 6;
                7 [label="str"];
                6 -> 7;
                8 [label=";"];
                1 -> 8;
            }
        """
        ),
    ),
    (
        "l := lambda (a) of a fo;",
        dot_from_string(
            """
            digraph "STQL program" {
                1 [label="Rule[prog]"];
                2 [label="Rule[bind]"];
                1 -> 2;
                3 [label="l"];
                2 -> 3;
                4 [label=":="];
                2 -> 4;
                5 [label="Rule[expr]"];
                2 -> 5;
                6 [label="Rule[lambda_expr]"];
                5 -> 6;
                7 [label="lambda"];
                6 -> 7;
                8 [label="("];
                6 -> 8;
                9 [label="Rule[args]"];
                6 -> 9;
                10 [label="a"];
                9 -> 10;
                11 [label=")"];
                6 -> 11;
                12 [label="of"];
                6 -> 12;
                13 [label="Rule[expr]"];
                6 -> 13;
                14 [label="a"];
                13 -> 14;
                15 [label="fo"];
                6 -> 15;
                16 [label=";"];
                1 -> 16;
            }
        """
        ),
    ),
    (
        "l := lambda ([a, b]) of a fo;",
        dot_from_string(
            """
            digraph "STQL program" {
                1 [label="Rule[prog]"];
                2 [label="Rule[bind]"];
                1 -> 2;
                3 [label="l"];
                2 -> 3;
                4 [label=":="];
                2 -> 4;
                5 [label="Rule[expr]"];
                2 -> 5;
                6 [label="Rule[lambda_expr]"];
                5 -> 6;
                7 [label="lambda"];
                6 -> 7;
                8 [label="("];
                6 -> 8;
                9 [label="Rule[args]"];
                6 -> 9;
                10 [label="["];
                9 -> 10;
                11 [label="Rule[args]"];
                9 -> 11;
                12 [label="a"];
                11 -> 12;
                13 [label=","];
                9 -> 13;
                14 [label="Rule[args]"];
                9 -> 14;
                15 [label="b"];
                14 -> 15;
                16 [label="]"];
                9 -> 16;
                17 [label=")"];
                6 -> 17;
                18 [label="of"];
                6 -> 18;
                19 [label="Rule[expr]"];
                6 -> 19;
                20 [label="a"];
                19 -> 20;
                21 [label="fo"];
                6 -> 21;
                22 [label=";"];
                1 -> 22;
            }
        """
        ),
    ),
    (
        "nodes := set_start (graph, [0, 1, 2]);",
        dot_from_string(
            """
            digraph "STQL program" {
                1 [label="Rule[prog]"];
                2 [label="Rule[bind]"];
                1 -> 2;
                3 [label="nodes"];
                2 -> 3;
                4 [label=":="];
                2 -> 4;
                5 [label="Rule[expr]"];
                2 -> 5;
                6 [label="Rule[two_args_builtin]"];
                5 -> 6;
                7 [label="set_start"];
                6 -> 7;
                8 [label="("];
                5 -> 8;
                9 [label="Rule[expr]"];
                5 -> 9;
                10 [label="graph"];
                9 -> 10;
                11 [label=","];
                5 -> 11;
                12 [label="Rule[expr]"];
                5 -> 12;
                13 [label="Rule[list_expr]"];
                12 -> 13;
                14 [label="["];
                13 -> 14;
                15 [label="Rule[expr]"];
                13 -> 15;
                16 [label="Rule[const]"];
                15 -> 16;
                17 [label="0"];
                16 -> 17;
                18 [label=","];
                13 -> 18;
                19 [label="Rule[expr]"];
                13 -> 19;
                20 [label="Rule[const]"];
                19 -> 20;
                21 [label="1"];
                20 -> 21;
                22 [label=","];
                13 -> 22;
                23 [label="Rule[expr]"];
                13 -> 23;
                24 [label="Rule[const]"];
                23 -> 24;
                25 [label="2"];
                24 -> 25;
                26 [label="]"];
                13 -> 26;
                27 [label=")"];
                5 -> 27;
                28 [label=";"];
                1 -> 28;
            }
        """
        ),
    ),
    (
        "nodes := get_start (graph);",
        dot_from_string(
            """
            digraph "STQL program" {
                1 [label="Rule[prog]"];
                2 [label="Rule[bind]"];
                1 -> 2;
                3 [label="nodes"];
                2 -> 3;
                4 [label=":="];
                2 -> 4;
                5 [label="Rule[expr]"];
                2 -> 5;
                6 [label="Rule[one_args_builtin]"];
                5 -> 6;
                7 [label="get_start"];
                6 -> 7;
                8 [label="("];
                5 -> 8;
                9 [label="Rule[expr]"];
                5 -> 9;
                10 [label="graph"];
                9 -> 10;
                11 [label=")"];
                5 -> 11;
                12 [label=";"];
                1 -> 12;
            }
        """
        ),
    ),
    (
        "nodes := filter nodes with lambda (a) of a in graph fo;",
        dot_from_string(
            """
            digraph "STQL program" {
                1 [label="Rule[prog]"];
                2 [label="Rule[bind]"];
                1 -> 2;
                3 [label="nodes"];
                2 -> 3;
                4 [label=":="];
                2 -> 4;
                5 [label="Rule[expr]"];
                2 -> 5;
                6 [label="Rule[with_builtin]"];
                5 -> 6;
                7 [label="filter"];
                6 -> 7;
                8 [label="Rule[expr]"];
                5 -> 8;
                9 [label="nodes"];
                8 -> 9;
                10 [label="with"];
                5 -> 10;
                11 [label="Rule[expr]"];
                5 -> 11;
                12 [label="Rule[lambda_expr]"];
                11 -> 12;
                13 [label="lambda"];
                12 -> 13;
                14 [label="("];
                12 -> 14;
                15 [label="Rule[args]"];
                12 -> 15;
                16 [label="a"];
                15 -> 16;
                17 [label=")"];
                12 -> 17;
                18 [label="of"];
                12 -> 18;
                19 [label="Rule[expr]"];
                12 -> 19;
                20 [label="Rule[logic]"];
                19 -> 20;
                21 [label="Rule[logic_atom]"];
                20 -> 21;
                22 [label="a"];
                21 -> 22;
                23 [label="in"];
                21 -> 23;
                24 [label="Rule[expr]"];
                21 -> 24;
                25 [label="graph"];
                24 -> 25;
                26 [label="fo"];
                12 -> 26;
                27 [label=";"];
                1 -> 27;
            }
        """
        ),
    ),
    (
        'reg := regex "a*";',
        dot_from_string(
            """
            digraph "STQL program" {
                1 [label="Rule[prog]"];
                2 [label="Rule[bind]"];
                1 -> 2;
                3 [label="reg"];
                2 -> 3;
                4 [label=":="];
                2 -> 4;
                5 [label="Rule[expr]"];
                2 -> 5;
                6 [label="Rule[string_arg_builtin]"];
                5 -> 6;
                7 [label="regex"];
                6 -> 7;
                8 [label="a*"];
                5 -> 8;
                9 [label=";"];
                1 -> 9;
            }
        """
        ),
    ),
    (
        "lang := intersect a and b;",
        dot_from_string(
            """
            digraph "STQL program" {
                1 [label="Rule[prog]"];
                2 [label="Rule[bind]"];
                1 -> 2;
                3 [label="lang"];
                2 -> 3;
                4 [label=":="];
                2 -> 4;
                5 [label="Rule[expr]"];
                2 -> 5;
                6 [label="Rule[two_args_language_builtin]"];
                5 -> 6;
                7 [label="intersect"];
                6 -> 7;
                8 [label="Rule[expr]"];
                5 -> 8;
                9 [label="a"];
                8 -> 9;
                10 [label="and"];
                5 -> 10;
                11 [label="Rule[expr]"];
                5 -> 11;
                12 [label="b"];
                11 -> 12;
                13 [label=";"];
                1 -> 13;
            }
        """
        ),
    ),
    (
        "lang := [1, 2];",
        dot_from_string(
            """
            digraph "STQL program" {
                1 [label="Rule[prog]"];
                2 [label="Rule[bind]"];
                1 -> 2;
                3 [label="lang"];
                2 -> 3;
                4 [label=":="];
                2 -> 4;
                5 [label="Rule[expr]"];
                2 -> 5;
                6 [label="Rule[list_expr]"];
                5 -> 6;
                7 [label="["];
                6 -> 7;
                8 [label="Rule[expr]"];
                6 -> 8;
                9 [label="Rule[const]"];
                8 -> 9;
                10 [label="1"];
                9 -> 10;
                11 [label=","];
                6 -> 11;
                12 [label="Rule[expr]"];
                6 -> 12;
                13 [label="Rule[const]"];
                12 -> 13;
                14 [label="2"];
                13 -> 14;
                15 [label="]"];
                6 -> 15;
                16 [label=";"];
                1 -> 16;
            }
        """
        ),
    ),
    (
        "logic := a in graph;",
        dot_from_string(
            """
            digraph "STQL program" {
                1 [label="Rule[prog]"];
                2 [label="Rule[bind]"];
                1 -> 2;
                3 [label="logic"];
                2 -> 3;
                4 [label=":="];
                2 -> 4;
                5 [label="Rule[expr]"];
                2 -> 5;
                6 [label="Rule[logic]"];
                5 -> 6;
                7 [label="Rule[logic_atom]"];
                6 -> 7;
                8 [label="a"];
                7 -> 8;
                9 [label="in"];
                7 -> 9;
                10 [label="Rule[expr]"];
                7 -> 10;
                11 [label="graph"];
                10 -> 11;
                12 [label=";"];
                1 -> 12;
            }
        """
        ),
    ),
    (
        "logic := a in graph and b in graph;",
        dot_from_string(
            """
            digraph "STQL program" {
                1 [label="Rule[prog]"];
                2 [label="Rule[bind]"];
                1 -> 2;
                3 [label="logic"];
                2 -> 3;
                4 [label=":="];
                2 -> 4;
                5 [label="Rule[expr]"];
                2 -> 5;
                6 [label="Rule[logic]"];
                5 -> 6;
                7 [label="Rule[logic_atom]"];
                6 -> 7;
                8 [label="a"];
                7 -> 8;
                9 [label="in"];
                7 -> 9;
                10 [label="Rule[expr]"];
                7 -> 10;
                11 [label="graph"];
                10 -> 11;
                12 [label="and"];
                6 -> 12;
                13 [label="Rule[logic]"];
                6 -> 13;
                14 [label="Rule[logic_atom]"];
                13 -> 14;
                15 [label="b"];
                14 -> 15;
                16 [label="in"];
                14 -> 16;
                17 [label="Rule[expr]"];
                14 -> 17;
                18 [label="graph"];
                17 -> 18;
                19 [label=";"];
                1 -> 19;
            }
        """
        ),
    ),
]


# make sync dfc to compare trees
def deep_compare(a_graph: pydot.Dot, b_graph: pydot.Dot) -> bool:
    start_a = a_graph.get_node("1")
    start_b = b_graph.get_node("1")

    edges_a = a_graph.get_edge_list()
    edges_b = b_graph.get_edge_list()

    if len(start_a) != len(start_b) or len(start_a) != 1:
        return False

    query = [(start_a[0], start_b[0])]

    def strip_label(lab: str):
        return lab.strip('"')

    while len(query) > 0:
        a, b = query.pop()
        if strip_label(a.get("label")) != strip_label(b.get("label")):
            return False

        neighbours_a = []
        for e_a in filter(lambda e: e.get_source() == a.get_name(), edges_a):
            nodes = a_graph.get_node(e_a.get_destination())
            if len(nodes) != 1:
                return False
            neighbours_a.append(nodes[0])

        neighbours_b = []
        for e_b in filter(lambda e: e.get_source() == b.get_name(), edges_b):
            nodes = b_graph.get_node(e_b.get_destination())
            if len(nodes) != 1:
                return False
            neighbours_b.append(nodes[0])

        if len(neighbours_a) != len(neighbours_b):
            return False

        for p in zip(neighbours_a, neighbours_b):
            query.append(p)

    return True


def compare_programs(actual: pydot.Dot, expected: pydot.Dot) -> bool:
    return deep_compare(actual, expected)


@pytest.mark.parametrize("program,expected", testdata)
def test_STQL_program_to_dot(program: str, expected: pydot.Dot):
    actual = STQL_program_to_dot(program)
    assert compare_programs(actual, expected)
