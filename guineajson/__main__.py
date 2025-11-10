from . import ver
import sys

def main():
    valid_args = {"--version": 1, "--license": 5, "--model": 3, "--version+model": 4, "--full-version": 0}

    if len(sys.argv) == 1: print(("-" * len(f"GuineaJSON {ver()}")) + f"\nGuineaJSON {ver()}\n" + f"{'| GitHub: Dominik-Salawa |':^{len(f"GuineaJSON {ver()}")}}\n" + ("-" * len(f"GuineaJSON {ver()}")))
    else:
        for arg in sys.argv[1:]:
            if not arg in valid_args:
                print(f"I'm here, but arguement [{arg}] is invalid. Use either \"python -m guineajson\" or an available arguement like \"python -m guineajson [--version/--license/--model/--version+model/--full-version]\".")
                return
        for arg in sys.argv[1:]:
            print(ver(valid_args[arg]))

if __name__ == "__main__": main()