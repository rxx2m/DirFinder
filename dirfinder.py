#!/usr/bin/python3

import requests
import time
import re

# ANSI escape sequences for text formatting
GREEN = '\u001b[32m'
YELLOW = '\u001b[33m'
RED = '\u001b[31m'
BLUE = '\u001b[34m'
PINK = '\u001b[35m'
PURPLE = '\u001b[36m'
BOLD = '\u001b[1m'
ORANGE = '\u001b[38;5;208m'
RESET = '\u001b[0m'

print(ORANGE + "**********************************************")
print("*                                            *")
print("*          Welcome to Dir Finder!            *")
print("*                By : Rxx2m                  *")
print("**********************************************" + RESET)
print("")
print("")


def check_server(url):
    try:
        response = requests.head(url, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False


def check_url(url):
    try:
        response = requests.head(url)
        return response.status_code
    except requests.exceptions.RequestException as e:
        return str(e)


def validate_url(url):
    pattern = re.compile(r'^https?://')

    if not pattern.match(url):
        url = 'http://' + url

    return url


while True:
    target_url = input(RED + BOLD + "[***] Enter URL: " + RESET)
    if target_url.lower() == 'q':
        break

    target_url = validate_url(target_url)

    if not check_server(target_url):
        print(RED + BOLD + "[!!!!] Server is not accessible." + RESET)
        continue

    file_name = input(RED + BOLD + "[***] Enter File Directory: " + RESET)
    if file_name.lower() == 'q':
        break

    try:
        with open(file_name, "r") as file:

            lines = file.readlines()
            total_count = len(lines)
            count = 0

            # Print initial count
            print(PURPLE + BOLD + f"Progress: {count}/{total_count}"+ RESET, end="")

            for line in lines:
                word = line.strip()
                if not word:
                    continue
                full_url = target_url.rstrip('/') + '/' + word
                status_code = check_url(full_url)
                count += 1

                # Update count after each iteration
                print(PURPLE + BOLD + f"\rProgress: {count}/{total_count}"+ RESET, end="")

                if status_code is not None:
                    if isinstance(status_code, int):
                        if status_code == 200:
                            print(GREEN + BOLD + f"\n[+] (Status: {status_code}) Found: " + full_url + RESET)
                        elif 300 <= status_code <= 308:
                            print(BLUE + f"\n[-] (Status: {status_code}) Redirects: " + full_url + RESET)
                        elif status_code == 401:
                            print(RED + f"\n[-] (Status: {status_code}) Authorization Required: " + full_url + RESET)
                        elif status_code == 403:
                            print(YELLOW + f"\n[-] (Status: {status_code}) Forbidden: " + full_url + RESET)
                        elif status_code == 503:
                            print(PINK + f"\n[-] (Status: {status_code}) Service Unavailable: " + full_url + RESET)
                        # Remove the following lines to exclude 404 status code
                        elif status_code == 404:
                            continue
                        else:
                            print(YELLOW + f"\n[-] (Status: {status_code}) Unknown: " + full_url + RESET)
                    else:
                        print(RED + "\n[!!!!] Connection error: " + status_code + RESET)

            print("\n")  # Add a new line after the loop ends

    except FileNotFoundError:
        print(RED + BOLD + "[#-#] File not found." + RESET)
