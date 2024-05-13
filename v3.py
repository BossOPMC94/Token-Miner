import os
import random
import hashlib
import string

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_gui():
    clear_terminal()
    print("--------------- PortKVM Token Miner v3 Beta ---------------")
    print("1 > Start mining Tokens")
    print("2 > Print last token mined")
    print("3 > Get an address")
    print("4 > Mine a specific number of tokens")
    print("5 > List addresses")
    print("6 > Get an existing address")
    print("7 > Exit")
    print("-----------------------------------------------------------")

def print_mining_log(logs, last_printed_index):
    print("--------------- Mining Tokens ---------------")
    for i in range(last_printed_index + 1, len(logs)):
        print(f"{logs[i][0]} Token(s) mined | Token: {logs[i][1]}")
    return len(logs) - 1

def generate_address(name, last_token_number, last_token_id):
    rand_num = random.randint(0, 9999999999999999)  # Generate a random number
    address_info = f"{name}{last_token_number}{last_token_id}{rand_num}"
    address_hash = hashlib.sha256(address_info.encode()).hexdigest()  # Hash the information using SHA256
    return address_hash

def generate_token(length=16):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def encrypt_token(token):
    hasher = hashlib.sha256() # this is kinda like bitcoin, Bitcoin uses SHA256d and this uses something like it - Katy
    hasher.update(token.encode())
    return hasher.hexdigest()

def get_last_mined_token(filename):
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
            if not lines:  # Check for empty file
                return 0, ""
            last_line = lines[-1]
            try:
                number, token = last_line.split("|")
                return int(number), token.strip()  # Strip whitespace from token
            except ValueError:
                return 0, ""
    except FileNotFoundError:
        try:
            with open(filename, "x") as file:  # Use 'x' mode for exclusive creation
                file.write("0 | 0\n")  # Write default line only on first creation
        except OSError:
            print("Error: Could not create file 'tokens.txt'. Check write permissions.")
        return 0, ""

def mine_tokens(logs, num_tokens=None):
    try:
        last_number, _ = get_last_mined_token("tokens.txt")
        if last_number is None:
            last_number = 0
        else:
            last_number += 1

        last_printed_index = -1

        if num_tokens is None:
            while True:
                token = generate_token()
                encrypted_token = encrypt_token(token)
                logs.append((last_number, encrypted_token))

                if len(logs) > last_printed_index + 8:
                    last_printed_index = print_mining_log(logs, last_printed_index)

                if (last_number + 1) % 8 == 0:
                    clear_terminal()

                with open("tokens.txt", "a") as file:
                    file.write(f"{last_number} | {encrypted_token}\n")  # Write to file

                last_number += 21269
        else:
            for _ in range(num_tokens):
                token = generate_token()
                encrypted_token = encrypt_token(token)
                logs.append((last_number, encrypted_token))

                if len(logs) > last_printed_index + 8:
                    last_printed_index = print_mining_log(logs, last_printed_index)

                if (last_number + 1) % 8 == 0:
                    clear_terminal()

                with open("tokens.txt", "a") as file:
                    file.write(f"{last_number} | {encrypted_token}\n")  # Write to file

                last_number += 21269
    except KeyboardInterrupt:
        print("\nStopped Mining (Ctrl+C pressed).")
    except Exception as e:
        print(f"An error occurred: {e}")

def print_last_mined_token(filename="tokens.txt"):
    last_number, last_token = get_last_mined_token(filename)
    if last_number is not None:
        print(f"Last Mined Token: {last_number} | Token id: {last_token}")
    else:
        print("No tokens mined yet.")

def get_address():
    name = input("Enter a name for address (Will be encrypted) > ")
    last_number, last_token_id = get_last_mined_token("tokens.txt")
    address = generate_address(name, last_number, last_token_id)
    with open("address.txt", "w") as file:
        file.write(address)
    print(f"Address generated and saved to 'address.txt': {address}")

def list_addresses():
    try:
        with open("address.txt", "r") as file:
            addresses = file.readlines()
            if not addresses:
                print("No addresses found.")
            else:
                print("--------------- PortKVM Token Miner v3 Beta ---------------")
                for i, address in enumerate(addresses, start=1):
                    print(f"{i} > Address {i} | Address: {address.strip()}")
                if len(addresses) > 5:
                    print("[2] Go to previous page")
                    print("[1] Go to next page")
                print("-----------------------------------------------------------")
    except FileNotFoundError:
        print("No addresses found.")

def mine_specific_tokens(num_tokens):
    logs = []
    mine_tokens(logs, num_tokens)

def get_existing_address():
    address = input("Enter your address > ")
    try:
        with open("address.txt", "a") as file:
            file.write(address.strip() + "\n")
        print("Address added successfully!")
    except FileNotFoundError:
        print("Error: No address file found. Please generate a new address first.")

def main():
    logs = []

    try:
        while True:
            print_gui()
            choice = input("> ")

            if choice == "1":
                mine_tokens(logs)
            elif choice == "2":
                print_last_mined_token()
            elif choice == "3":
                get_address()
            elif choice == "4":
                num_tokens = int(input("Enter number of tokens to mine > "))
                mine_specific_tokens(num_tokens)
            elif choice == "5":
                list_addresses()
                input("Press Enter to return to the main menu > ")
            elif choice == "6":
                get_existing_address()
            elif choice == "7":
                print("Exiting...")
                break
            else:
                print("Invalid option, Please enter a valid option.")
    except KeyboardInterrupt:
        print("\nExited (Ctrl+C pressed).")

if __name__ == "__main__":
    main()
