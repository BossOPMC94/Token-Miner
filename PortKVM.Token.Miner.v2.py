import os
import random
import string
import hashlib
from time import sleep

print("$$$$$$$\                       $$\     $$\   $$\ $$\    $$\ $$\      $$\       $$$$$$$$\        $$\                                 $$\      $$\ $$\                               ")
print("$$  __$$\                      $$ |    $$ | $$  |$$ |   $$ |$$$\    $$$ |      \__$$  __|       $$ |                                $$$\    $$$ |\__|                              ")
print("$$ |  $$ | $$$$$$\   $$$$$$\ $$$$$$\   $$ |$$  / $$ |   $$ |$$$$\  $$$$ |         $$ | $$$$$$\  $$ |  $$\  $$$$$$\  $$$$$$$\        $$$$\  $$$$ |$$\ $$$$$$$\   $$$$$$\   $$$$$$\  ")
print("$$$$$$$  |$$  __$$\ $$  __$$\\_$$  _|  $$$$$  /  \$$\  $$  |$$\$$\$$ $$ |         $$ |$$  __$$\ $$ | $$  |$$  __$$\ $$  __$$\       $$\$$\$$ $$ |$$ |$$  __$$\ $$  __$$\ $$  __$$\ ")
print("$$  ____/ $$ /  $$ |$$ |  \__| $$ |    $$  $$<    \$$\$$  / $$ \$$$  $$ |         $$ |$$ /  $$ |$$$$$$  / $$$$$$$$ |$$ |  $$ |      $$ \$$$  $$ |$$ |$$ |  $$ |$$$$$$$$ |$$ |  \__|")
print("$$ |      $$ |  $$ |$$ |       $$ |$$\ $$ |\$$\    \$$$  /  $$ |\$  /$$ |         $$ |$$ |  $$ |$$  _$$<  $$   ____|$$ |  $$ |      $$ |\$  /$$ |$$ |$$ |  $$ |$$   ____|$$ |      ")
print("$$ |      \$$$$$$  |$$ |       \$$$$  |$$ | \$$\    \$  /   $$ | \_/ $$ |         $$ |\$$$$$$  |$$ | \$$\ \$$$$$$$\ $$ |  $$ |      $$ | \_/ $$ |$$ |$$ |  $$ |\$$$$$$$\ $$ |      ")
print("\__|       \______/ \__|        \____/ \__|  \__|    \_/    \__|     \__|         \__| \______/ \__|  \__| \_______|\__|  \__|      \__|     \__|\__|\__|  \__| \_______|\__|       Stable v2")
print("---------------------------------------------------------------------------- Made By PortKVM with love ----------------------------------------------------------------------------")
print("")
print("Checking for up to date version")
sleep(1.7)
print("Sucess: Up to date")
print("Waiting for system runner")
sleep(0.9)
print("Runner Started")
sleep(0.7)

def generate_token(length=16):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def encrypt_token(token):
    hasher = hashlib.sha256()
    hasher.update(token.encode())
    return hasher.hexdigest()


def get_last_mined_number(filename):
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1]
                return int(last_line.split("|")[0])
    except (FileNotFoundError, ValueError):
        return 0  # Start from 1 if no valid data is found


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


def mine_tokens(filename="tokens.txt", loop_forever=True):
    with open(filename, "a") as file:
        last_number = get_last_mined_number(filename)
        number = last_number + 1

        try:
            while loop_forever:
                token = generate_token()
                encrypted_token = encrypt_token(token)

                print(f"Mined {number} token(s) (token id: {encrypted_token})")
                file.write(f"{number} | {encrypted_token}\n")  # Write to file

                number += 1
        except KeyboardInterrupt:
            print("\nStopped Mining (Ctrl+C pressed).")

if __name__ == "__main__":
    last_number, last_token = get_last_mined_token("tokens.txt")
    if last_number is not None:
        print(f"Runner: Last Mined Token: {last_number} | Token id: {last_token} (Ctrl c right now if you were starting this for just the last token)")
        sleep(2.6)

    mine_tokens()
