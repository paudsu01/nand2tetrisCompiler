from __future__ import annotations
from exceptions import JACKFileNeeded

import argparse
import re
from parser import Parser
from scanner import Scanner

def generate_xml_file(fileName: str) -> None:
    myParser = Parser(Scanner(f'{fileName}.jack'))
    with open(f'{fileName}.xml', 'w') as out:
        out.write(myParser.compileClass())

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('file.jack', nargs='+')
    args = arg_parser.parse_args()

    jack_file_pattern = re.compile(r'(.*)\.jack')
    for file in (vars(args)['file.jack']):
        match = jack_file_pattern.match(file)
        if match:
            generate_xml_file(match.group(1))
        else:
            raise JACKFileNeeded(".jack file should be provided")

    
