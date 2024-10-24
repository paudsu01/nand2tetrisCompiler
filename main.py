from __future__ import annotations

import argparse
import re
import os
from parser import Parser
from scanner import Scanner
from symbol_table import SymbolTable

def generate_vm_file(full_path: str, outFileName: str) -> None:

    myParser = Parser(Scanner(full_path), outFileName, full_path)
    myParser.compileClass()
    SymbolTable.reset_class_table()

def main(full_path: str)-> None:
    match = jack_file_pattern.match(full_path)
    if match:
        generate_vm_file(full_path, match.group(2))

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('fileOrDirectory')

    args = arg_parser.parse_args()
    jack_file_pattern = re.compile(r'^(.*?)([^/]+)\.jack$')

    file_or_dir = args.fileOrDirectory
    if jack_file_pattern.match(file_or_dir):
        # Handle only one jack file
        main(file_or_dir)

    else:
        # assume it is a directory and handle all the jack files in the directory
        try:
            main_path = os.path.join(os.getcwd(), file_or_dir)
            all_files = os.listdir(main_path)
        except FileNotFoundError:

            raise FileNotFoundError(
                    "No such directory exists!: Provide a valid directory with .jack files to compile or a single .jack file"
                    )
        for file in all_files:
            file_path = os.path.join(main_path, file)
            main(file_path)


