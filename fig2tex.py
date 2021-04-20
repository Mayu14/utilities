#!/usr/bin/python3

import argparse
from pathlib import Path

import yaml


def get_cmd_args():
    parser = argparse.ArgumentParser("make tex source from some figure and YAML file")
    parser.add_argument('-y', '--filename_YAML', help='full or relative path of YAML setting file', required=True)
    parser.add_argument('-f', '--filename_FIG', help='such as <filename_FIG_base>001.png', required=True)
    parser.add_argument('-n', '--number_of_fig', type=int, help='number of figure (assume start with 001~)',
                        required=True)
    parser.add_argument('-w', '--width', default='130', help='width of figure')
    parser.add_argument('-c', '--captions_tag', default='captions', help='caption key of the yaml')
    return parser.parse_args()


def get_captions(fname_yaml, captions_tag='captions'):
    fname_yaml = Path(fname_yaml)
    if not fname_yaml.exists():
        raise FileNotFoundError(f"{fname_yaml} is not exist")

    with open(fname_yaml) as f:
        yml = yaml.safe_load(f)

    if not captions_tag in yml:
        raise KeyError(f"no key {captions_tag} in yaml file")

    return yml[captions_tag]


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
    get_captions(setting.filename_YAML, setting.captions_tag)

if __name__ == '__main__':
    main()