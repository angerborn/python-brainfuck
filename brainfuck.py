#! /usr/bin/env python3

import sys

class Interpreter():
    MAX_DATA_SIZE = 50000

    def __init__(self):
        pass

    def __prepare__(self):
        self.ptr = 0
        self.instruction_pointer = 0
        self.bracket_cache = {}
        self.data = [0] * self.MAX_DATA_SIZE

    def run(self, program):
        self.program = program
        self.__prepare__()
        self.__init_bracket_cache()
        while self.instruction_pointer < len(program):
            self.__execute_instruction_at_pointer()
            self.instruction_pointer += 1

    def __execute_instruction_at_pointer(self):
        instruction = self.program[self.instruction_pointer]
        if instruction == ">":
            self.__increment_pointer()
        elif instruction == "<":
            self.__decrement_pointer()
        elif instruction == "+":
            self.__increment()
        elif instruction == "-":
            self.__decrement()
        elif instruction == ".":
            self.__putchar()
        elif instruction == ",":
            self.__readchar()
        elif instruction == "[":
            self.__bracket()
        elif instruction == "]":
            self.__end_bracket()

    def __increment_pointer(self):
        self.ptr += 1
        if self.ptr >= len(self.data):
            raise Exception("Data pointer pointing at value outside of data array: {0} > {1}".format(self.ptr, self.MAX_DATA_SIZE-1))

    def __decrement_pointer(self):
        self.ptr -= 1
        if self.ptr < 0:
            raise Exception("Data pointer pointing at value outside of data array: {0} < 0".format(self.ptr))

    def __increment(self):
        self.data[self.ptr] += 1

    def __decrement(self):
        self.data[self.ptr] -= 1

    def __putchar(self):
        sys.stdout.write(chr(self.data[self.ptr]))
        sys.stdout.flush()

    def __readchar(self):
        self.data[self.ptr] = ord(sys.stdin.read(1))

    def __bracket(self):
        if self.data[self.ptr] == 0:
            self.__go_to_matching_bracket()

    def __end_bracket(self):
        if self.data[self.ptr] != 0:
            self.__go_to_matching_bracket()

    def __find_matching_bracket(self, bracket_position):
        return self.bracket_cache[bracket_position]

    def __go_to_matching_bracket(self):
        self.instruction_pointer = self.__find_matching_bracket(self.instruction_pointer)

    def __init_bracket_cache(self):
        stack = []
        for i, o in enumerate(self.program):
            if o == "[":
                stack.append(i)
            elif o == "]":
                index = stack.pop()
                self.bracket_cache[i] = index
                self.bracket_cache[index] = i
        if not len(stack) == 0:
            raise Exception("Bracket counts doesn't match, there's {0} more [ than ].".format(len(stack)))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="A simple brainfuck interpreter")
    parser.add_argument("file", nargs="?", help="file to run, if a file is not given it will run on stdin")
    args = parser.parse_args()

    if args.file:
        program = open(args.file, "r").read()
    else:
        program = sys.stdin.read()
    interpreter = Interpreter()
    interpreter.run(program)
