# Penetration Testing - Ethical Hacking

## Introduction

This code is a Python program that extracts `links`, `directories`, and `subdomains` of a given URL using brute force techniques. It can also crack login informations.

## Libraries Used
The program makes use of several Python libraries:

- `urllib`: Used to extract the source of a URL
- `re`: Used to perform several regex operation
- `requests`: Used to check if directories and subdomains exist using GET requests. Also used to perform Login POST requests.
- `time`: Used to wait
- `string`: Used to build the legal characters of a password
- `itertools`: Used to generate password

## Extracting Links
The program starts by validating a given URL through the terminal using a regular expression, which checks if the URL is of the correct format. If the URL is valid, the program proceeds to extract all links present in the given URL by scraping the URL's HTML code. It then cleans and writes the extracted links to a file.

## Checking Directories
The program can also check if a given directory of a URL exists or not. It does so by sending a request to the URL and retrieving the status code of the response. If the status code indicates that the directory exists, the program extracts all links present in the directory and writes them to a file. If the directory is not found, the program prints a message indicating the same. If too many requests were sent, the program waits for 5 seconds and then retries the request. If an optional `-d` parameter is given, the program will exclusively perform this action

## Checking Subdomains
The program also checks if a given subdomain of a URL exists or not. It does so by assembling the URL and sending a request to it. If the status code indicates that the subdomain exists, the program extracts all links present in the subdomain and writes them to a file. If the subdomain is not found, the program prints a message indicating the same. If too many requests were sent, the program waits for 5 seconds and then retries the request. If an optional `-s` parameter is given, the program will exclusively perform this action

## Brute Force Attacks
The program has an extra function that performs brute force attacks on a given URL to find the password of a specified username. The function generates all possible combinations of passwords with the specified length and attempts to log in to the given URL using these passwords and the specified username. If the correct password is found, it is printed to the console. This will only be performed if `-b` is passed to the file.

## Challenges

1. Due to a big number of requests the code at some point started signaling a lot of success as I was only checking for 404. Turns out, when too many requests are sent, a 429 error is produced, which does not mean that the subdomain/directory does not exist. I fixed this by repeating the search after some time if 429 is encountered.

2. https URLs were returning a 403 error code when attempting to scrape them. Turns out the library used was commonly associated with 'hacks' which triggered some defenses. I fixed this by assigning the urllib requests to a known agent (Mozzilla)

3. The search was taking a lot of time. I attempted to fix this using multi-threading, but I noticed that the improvement was barely noticeable. I decided to scrap this idea and switched to another VPN which made things much faster