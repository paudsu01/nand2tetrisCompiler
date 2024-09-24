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
        self.__tokens = self.__tokenize(cleaned_lines)

    def __tokenize(self, cleaned_lines: List[str])->List[str]:

        all_tokens = []
        empty_pattern = re.compile(r'\s')

        for line in cleaned_lines:

            current_token = ''
            current_index = 0
            string_processing = False

            while current_index < len(line):

                char = line[current_index]

                if char == '"':

                    if string_processing:
                        all_tokens.append(Token(current_token + '"'))
                        current_token = ''
                    else:
                        current_token += char

                    string_processing = False if string_processing else True

                elif (char in Token.symbols or empty_pattern.match(char)) and not string_processing:

                    if current_token != '': all_tokens.append(Token(current_token))
                    if char in Token.symbols: all_tokens.append(Token(char))

                    current_token = ''

                else:
                    current_token += char

                current_index += 1

        return all_tokens

    def __clean_jack_file(self, lines: List[str]) -> List[str]:

        comment_pattern = re.compile(r'^(.*?)((/\*\*?|//).*)?$')
        asterisk_comment_pattern = re.compile(r'/\*\*?.*')

        filtered_lines = []
        line_index = 0

        while line_index < len(lines):

            line = lines[line_index]
            if comment_pattern.match(line.strip()):
                necessary_tokens = comment_pattern.match(line.strip()).group(1)
                if necessary_tokens != '': filtered_lines.append(necessary_tokens)

            if asterisk_comment_pattern.search(line.strip()):
                while not lines[line_index].strip().endswith('*/'):
                    line_index += 1

            line_index += 1

        return filtered_lines

    def current_token(self) -> Token:
        return self.__tokens[self.__current_token_index]

    def next_token(self) -> Token:
        if self.has_more_tokens(): return self.__tokens[self.__current_token_index+1]
        else: raise OutOfTokens("Out of tokens")

    def advance(self) -> None:
        if self.has_more_tokens():
            self.__current_token_index += 1
        else:
            raise OutOfTokens("Out of tokens")

    def has_more_tokens(self) -> bool:
        return self.__current_token_index < len(self.__tokens) -1

