#!/usr/bin/python3

import argparse
from pathlib import Path

import yaml


def get_cmd_args():
    parser = argparse.ArgumentParser("make tex source from some figure and YAML file")
    parser.add_argument('-y', '--filename_YAML', help='full or relative path of YAML setting file', required=True)
    parser.add_argument('-f', '--filename_FIG', help='such as <filename_FIG_base>001.png', required=True)
    parser.add_argument('-e', '--fig_extension', help='png, jpg, eps, ...', required=True)
    parser.add_argument('-n', '--number_of_fig', type=int, help='number of figure (assume start with 001~)',
                        required=True)
    parser.add_argument('-z', '--number_of_zero', type=int, help='1~9 -> 1, 01~99 -> 2, 001~999 -> 3',
                        required=True)
    parser.add_argument('-o', '--output', help='output filename', default='main.tex')
    parser.add_argument('-w', '--width', default='130', help='width of figure')
    parser.add_argument('-c', '--captions_tag', default='captions', help='caption key of the yaml')
    parser.add_argument('-t', '--title', default=None, help='document title')
    parser.add_argument('-a', '--author', default=None, help='document author')
    return parser.parse_args()


def get_captions(fname_yaml, fig_number, captions_tag='captions'):
    fname_yaml = Path(fname_yaml)
    if not fname_yaml.exists():
        raise FileNotFoundError(f"{fname_yaml} is not exist")

    with open(fname_yaml) as f:
        yml = yaml.safe_load(f)

    if not captions_tag in yml:
        raise KeyError(f"no key {captions_tag} in yaml file")

    if len(yml[captions_tag]) != fig_number:
        raise SyntaxError("The row number of YAML and user specify figure number are conflicted.")

    return yml[captions_tag]


def get_latex_source(setting, captions):
    def set_preambles_and_packages(title=None, author=None):
        return f"""
        \\documentclass[12pt, a4paper]{{article}}
        \\usepackage{{amsmath}}
        \\usepackage[whole]{{bxcjkjatype}}
        \\usepackage[utf8]{{inputenc}}
        \\usepackage[T1]{{fontenc}}
        \\font\\f=cmr10
        \\pdffontexpand\\f 30 20 10 autoexpand
        \\pdfadjustspacing=2
        \\usepackage{{graphicx}}
        \\graphicspath{{{{../src/}}}}
        \\captionsetup{{compatibility=false}}
        \\title{{{title}}}
        \\author{{{author}}}
        """[:-1]

    def get_figure_core(fig_name, caption, width):
        return f"""
            \\begin{{figure}}
            \\begin{{center}}
            \\includegraphics[width={width}truemm]{{{fig_name}}}
            \\end{{center}}
            \\caption{{{caption}}}
            \\end{{figure}}
            """[:-1]

    def get_figure_source(fig_name_core, number_of_zfill, fig_format, captions, width=130):
        fig_block = ""
        for i, caption in enumerate(captions):
            fig_name = f"{fig_name_core}{str(i+1).zfill(number_of_zfill)}.{fig_format.replace('.', '')}"
            fig_block += get_figure_core(fig_name, caption, width)
        return fig_block

    title = setting.title
    author = setting.author
    fig_name_core = setting.filename_FIG
    number_of_zfill = setting.number_of_zero
    fig_format = setting.fig_extension
    width = setting.width
    maketitle = ""

    if (title is not None) or (author is not None):
        maketitle = "\maketitle"

    return f"""
    {set_preambles_and_packages(title=title, author=author)}
    \\begin{{document}}
    {maketitle}
    {get_figure_source(fig_name_core, number_of_zfill, fig_format, captions, width)}
    \\end{{document}}
    """[1:-1]


def main():
    setting = get_cmd_args()
    captions = get_captions(setting.filename_YAML, setting.number_of_fig, setting.captions_tag)
    source = get_latex_source(setting, captions)

    with open(setting.output, "w") as f:
        f.write(source)

if __name__ == '__main__':
    main()