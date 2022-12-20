import prettytable
from prettytable import PrettyTable


def print_table(header: list[str], rows: list[list[any]]) -> str:
    """
    Utility function to print python results as table
    """
    table = PrettyTable()
    table.set_style(prettytable.MARKDOWN)
    table.field_names = header
    for row in rows:
        table.add_row(row)
    table.max_width = 200
    return str(table)


def concat_as_time_result(n1: float, n2: float) -> str:
    if n2 < 0:
        return "timeout exceed"
    return "%.2f +- %.2f" % (n1, n2)


def regex_to_markdown(s: str) -> str:
    return s.replace("|", "\|")
