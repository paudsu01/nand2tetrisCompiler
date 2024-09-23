from __future__ import annotations
from typing import List

from jack_token import Token
from exceptions import OutOfTokens

import re

class Scanner:

    def __init__(self, fileName: str):
        
        self.__current_token_index = 0

        with open(fileName, 'r') as infile:
            all_lines = infile.readlines()

        # remove comments and strip whitespaces 
        cleaned_lines = self.__clean_jack_file(all_lines)
        print(cleaned_lines)
        self.__tokens = self.__tokenize(cleaned_lines)

    def __tokenize(self, cleaned_lines: List[str])->List[str]:

        all_tokens = []
        empty_pattern = re.compile(r'\s')

        for line in cleaned_lines:

            current_token = ''
            current_index = 0

            while current_index < len(line):

                char = line[current_index]

                if char in Token.symbols or empty_pattern.match(char):

                    if current_token != '': all_tokens.append(current_token)
                    if char in Token.symbols: all_tokens.append(char)

                    current_token = ''
                    current_index += 1

                else:
                    current_token += char
                    current_index += 1

        return all_tokens

    def __clean_jack_file(self, lines: List[str]) -> List[str]:

        comment_pattern = re.compile(r'(.*)(//.*)?')
        filtered_lines = []
        for line in lines:
            if comment_pattern.match(line.strip()):
                necessary_tokens = comment_pattern.match(line.strip()).group(1)
                if necessary_tokens != '': filtered_lines.append(necessary_tokens)

        return filtered_lines

    def current_token(self) -> Token:
        return self.__tokens[self.__current_token_index]

    def advance(self) -> None:
        if self.has_more_tokens():
            self.__current_token_index += 1
        else:
            raise OutOfTokens("Out of tokens")

    def has_more_tokens(self) -> bool:
        return self.__current_token_index < len(self.__tokens) -1

