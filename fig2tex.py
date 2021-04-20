#!/usr/bin/python3

import argparse

def get_cmd_args():
    parser = argparse.ArgumentParser("make tex source from some figure and YAML file")
    parser.add_argument('-y', '--filename_YAML', help='full or relative path of YAML setting file', required=True)
    parser.add_argument('-f', '--filename_FIG', help='such as <filename_FIG_base>001.png', required=True)
    parser.add_argument('-n', '--number_of_fig', type=int, help='number of figure (assume start with 001~)',
                        required=True)
    parser.add_argument('-w', '--width', default='130', help='width of figure')
    return parser.parse_args()


def get_figure_source(fig_name, caption, width=130):
    return f"""\\begin{{figure}}
\\begin{{center}}
\\includegraphics[width={width}truemm]{fig_name}
\\end{{center}}
\\caption{caption}
\\end{{figure}}
"""

def main():
    setting = get_cmd_args()


if __name__ == '__main__':
    main()