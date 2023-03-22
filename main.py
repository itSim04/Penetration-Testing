import sys, urllib, re, requests, time

master = sys.argv[1]

def extractLinks(url, links):

    req = urllib.request.Request(url)
    webUrl = urllib.request.urlopen(req)

    links_pattern = r'href="[^#\"]{2,}?"'

    refs = re.findall(links_pattern, webUrl.read().decode())

    cleaning_pattern = r'".*"'
        
    links.write(url + ":\n\n")

    for ref in refs:

        line = re.findall(cleaning_pattern, ref)[0][1:-1]
        links.write("\t" + line + "\n")
        links.flush()

    links.write("\n\n")

with open("./links.bat", 'w') as links_output:

    extractLinks(master, links_output)

    with open("./dirs_files_output.bat", 'w') as dirs_output:

        with open("./dirs_dictionary.bat", "r") as dirs:
            
            for line in dirs.readlines()[0:15]:
                                                                    
                code = 429

        while code == 429:
                
            code = requests.get(master + line.rstrip('\n')).status_code
            if code == 404:

                print('Directory/File does not exist: ' + line.rstrip('\n'))

            elif code // 100 == 2 or code == 403:

                print('Directory/File does exist: ' + line.rstrip('\n') + " " + str(code))    

                dirs_output.write(master + line.rstrip('\n') + "\t" + str(code) + "\n" )
                dirs_output.flush()         

            if code == 429:

                print("Waiting")
                time.sleep(5)

       

       
            