"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
SP = 7   # <-- stack pointer


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = False
        self.reg[7] = 0xF4

    def load(self):
        """Load a program into memory."""

        address = 0

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    try:
                        line = line.strip()
                        line = line.split('#', 1)[0]
                        line = int(line, 2)
                        self.ram[address] = line
                        address += 1
                    except ValueError:
                        pass
        except FileNotFoundError:
            print(f"Couldn't find file {sys.argv[1]}")
            sys.exit(1)
        except IndexError:
            print("Usage: ls8.py filename")
            sys.exit(1)
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def ram_read(self, index):
        return self.ram[index]

    def ram_write(self, index, value):
        self.ram[index] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.running = True
        while self.running:
            ir = self.pc
            instruction = self.ram[ir]

            if instruction == HLT:
                self.running = False
            elif instruction == PRN:
                to_prn = self.ram[self.pc + 1]
                print(self.reg[to_prn])
                self.pc += 2
            elif instruction == LDI:
                op_a = self.ram[self.pc + 1]
                op_b = self.ram[self.pc + 2]
                self.reg[op_a] = op_b
                self.pc += 3
            elif instruction == MUL:
                op_a = self.ram[self.pc + 1]
                op_b = self.ram[self.pc + 2]
                self.reg[op_a] *= self.reg[op_b]
                self.pc += 3
            elif instruction == PUSH:
                self.reg[SP] -= 1
                stack_address = self.reg[SP]
                reg_num = self.ram_read(self.pc + 1)
                reg_num_val = self.reg[reg_num]
                self.ram_write(stack_address, reg_num_val)
                self.pc += 2
            elif instruction == POP:
                stack_val = self.ram_read(self.reg[SP])
                reg_num = self.ram_read(self.pc + 1)
                self.reg[reg_num] = stack_val
                self.reg[SP] += 1
                self.pc += 2
