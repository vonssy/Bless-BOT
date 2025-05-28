import random, string
from colorama import *

def main():
    count = int(input(f"{Fore.GREEN + Style.BRIGHT}Count? -> {Style.RESET_ALL}"))

    filename = "hardware_ids.txt"

    with open(filename, "a") as f:
        for i in range(count):
            hardware_id = ''.join(random.choices(string.hexdigits.lower(), k=64))
            print(
                f"{Fore.CYAN + Style.BRIGHT}Hardware Id {i+1}{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {hardware_id} {Style.RESET_ALL}"
            )
            f.write(hardware_id + "\n")

    print(f"{Fore.GREEN + Style.BRIGHT}{count} Hardware Ids successfully saved in {filename}.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()