from functools import reduce
from io import open  # Python2 compatibility

from django_compat_patcher.registry import get_all_fixers


def make_table(grid):
    """
    Borrowed from http://stackoverflow.com/a/12539081/5088990
    :param grid: List of lists
    :return:
    """

    def _table_div(num_cols, col_width, header_flag):
        if header_flag == 1:
            return num_cols * ('+' + (col_width) * '=') + '+\n'
        else:
            return num_cols * ('+' + (col_width) * '-') + '+\n'

    def _normalize_cell(string, length):
        return string + ((length - len(string)) * ' ')

    cell_width = 2 + max(reduce(lambda x, y: x + y, [[len(item) for item in row] for row in grid], []))
    num_cols = len(grid[0])
    rst = _table_div(num_cols, cell_width, 0)
    header_flag = 1
    for row in grid:
        rst = rst + '| ' + '| '.join([_normalize_cell(x, cell_width - 1) for x in row]) + '|\n'
        rst = rst + _table_div(num_cols, cell_width, header_flag)
        header_flag = 0
    return rst


def detuplify(input_tuple):
    """
    Coerces the version tuple (if not None), to a version string.
    Ex. (1, 7, 0) becomes "1.7.0".
    """
    if input_tuple is None:
        return ""
    assert isinstance(input_tuple, tuple)
    string = ".".join(str(number) for number in input_tuple)
    return string


def _create_fixer_list(all_fixers, grid):
    """
    Creates a list for the fixers table.
    Each fixer creates a list of its name, its min version and its max version if it exists.
    Ex: ["fix_deletion_http_request_HttpRequest_raw_post_data", "1.6", ""]
    """
    for fixer in all_fixers:
        grid.append([
            fixer["fixer_callable"].__name__,
            detuplify(fixer["fixer_applied_from_django"]),
            detuplify(fixer['fixer_applied_upto_django'])
        ])


def _create_headers(grid):
    table_headers = ['Fixer name', "Min version", "Max version"]
    grid.append(table_headers)


def generate_readme():
    all_fixers = get_all_fixers()
    grid = []

    with open('README.rst', mode="w", encoding="utf-8") as readme_final:

        with open("README.in", mode="r", encoding='utf-8') as readme_manual:
            readme_manual_content = readme_manual.read()
        _create_headers(grid)
        _create_fixer_list(all_fixers, grid)

        readme_final.write('.. sectnum::\n\n')
        readme_final.write(readme_manual_content)
        readme_final.write('\n\nTable of fixers\n===============\n\n')
        readme_final.write('There are currently {} working fixers.\n\n'.format(len(all_fixers)))
        readme_final.write(make_table(grid))


if __name__ == '__main__':
    generate_readme()
