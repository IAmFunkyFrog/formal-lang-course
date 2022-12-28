import pydot
from antlr4 import (
    InputStream,
    CommonTokenStream,
    ParseTreeWalker,
    ParseTreeListener,
    TerminalNode,
    ParserRuleContext,
)

from language.dist.STQLLexer import STQLLexer
from language.dist.STQLParser import STQLParser


def get_parser(prog: str) -> STQLParser:
    return STQLParser(CommonTokenStream(STQLLexer(InputStream(prog))))


class STQLProgramToDotConverter(ParseTreeListener):
    def __init__(self):
        self._dot = pydot.Dot("STQL program")
        self._stack = []
        self._id = 1

    @classmethod
    def convert(cls, prog: str) -> pydot.Dot:
        if not is_STQL_program(prog):
            raise ValueError("Given program is not in STQL language")
        converter = STQLProgramToDotConverter()
        parser = get_parser(prog)
        walker = ParseTreeWalker()
        walker.walk(converter, parser.prog())
        return converter._dot

    def visitTerminal(self, node: TerminalNode):
        label = str(node).strip('"')
        label = f'"{label}"'
        new_node = pydot.Node(self._id, label=label)
        self._dot.add_node(new_node)
        self._try_connect_with_parent(new_node)
        self._id += 1

    def enterEveryRule(self, ctx: ParserRuleContext):
        new_node = pydot.Node(
            self._id, label=f"Rule[{STQLParser.ruleNames[ctx.getRuleIndex()]}]"
        )
        self._dot.add_node(new_node)
        self._try_connect_with_parent(new_node)
        self._stack.append(new_node)
        self._id += 1

    def exitEveryRule(self, ctx: ParserRuleContext):
        self._stack.pop()

    def _try_connect_with_parent(self, new_node):
        if len(self._stack) > 0:
            parent = self._stack[-1]
            self._dot.add_edge(pydot.Edge(parent.get_name(), new_node.get_name()))


def is_STQL_program(prog: str) -> bool:
    parser = get_parser(prog)
    parser.removeErrorListeners()
    parser.prog()
    return parser.getNumberOfSyntaxErrors() == 0


def STQL_program_to_dot(prog: str) -> pydot.Dot:
    return STQLProgramToDotConverter.convert(prog)


def write_STQL_program_to_file_as_dot(prog: str, path: str):
    dot = STQL_program_to_dot(prog)
    dot.write(path)
