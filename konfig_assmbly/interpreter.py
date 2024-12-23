import sys
import csv

def interpret(input_file, output_file, memory_range):
    memory = [0] * 1024  # Предположим, что память имеет размер 1024 байта
    accumulator = 0

    with open(input_file, 'rb') as f:
        while True:
            cmd_byte = f.read(1)
            if not cmd_byte:
                break
            cmd = int.from_bytes(cmd_byte, 'big')
            operand = int.from_bytes(f.read(4), 'big')

            if cmd == 0xEF:  # LOAD_CONST
                accumulator = operand
            elif cmd == 0x2E:  # READ_MEM
                accumulator = memory[operand]
            elif cmd == 0xF4:  # WRITE_MEM
                memory[operand] = accumulator
            elif cmd == 0x2A:  # BIN_OP_NE
                accumulator = 1 if accumulator != memory[operand] else 0

    start, end = memory_range
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Address", "Value"])
        for addr in range(start, end + 1):
            writer.writerow([addr, memory[addr]])

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python interpreter.py <input_file> <output_file> <memory_range>")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    memory_range = tuple(map(int, sys.argv[3].split('-')))
    interpret(input_file, output_file, memory_range)
