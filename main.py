from __future__ import annotations
from exceptions import JACKFileNeeded

import argparse
import re
from parser import Parser
from scanner import Scanner
from symbol_table import SymbolTable

def generate_xml_file(file, outFileName: str) -> None:
    myParser = Parser(Scanner(file))
    with open(f'{outFileName}.xml', 'w') as out:
        out.write(myParser.compileClass())
    SymbolTable.reset_class_table()

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('file.jack', nargs='+')
    args = arg_parser.parse_args()

    jack_file_pattern = re.compile(r'^(.*?)([^/]+)\.jack$')
    for file in (vars(args)['file.jack']):
        match = jack_file_pattern.match(file)
        if match:
            generate_xml_file(file, match.group(2))
        else:
            raise JACKFileNeeded(".jack file should be provided")

    
