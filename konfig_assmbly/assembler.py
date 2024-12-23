import sys
import csv

def assemble(input_file, output_file, log_file):
    commands = []
    try:
        with open(input_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) != 2:
                    print(f"Invalid line: {line.strip()}")
                    continue
                command = parts[0]
                operand = int(parts[1])
                if command == "LOAD_CONST":
                    commands.append((0xEF, operand))
                elif command == "READ_MEM":
                    commands.append((0x2E, operand))
                elif command == "WRITE_MEM":
                    commands.append((0xF4, operand))
                elif command == "BIN_OP_NE":
                    commands.append((0x2A, operand))
                else:
                    print(f"Unknown command: {command}")

        with open(output_file, 'wb') as f:
            for cmd, operand in commands:
                f.write(cmd.to_bytes(1, 'big'))
                f.write(operand.to_bytes(4, 'big'))

        with open(log_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Command", "Operand"])
            for cmd, operand in commands:
                writer.writerow([f"0x{cmd:02X}", f"0x{operand:04X}"])

    except FileNotFoundError:
        print(f"File not found: {input_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python assembler.py <input_file> <output_file> <log_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = sys.argv[3]
    assemble(input_file, output_file, log_file)
