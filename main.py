import sys, urllib, re, requests, time

def is_valid_url(url):

    pattern = r"^((http|https):\/\/)?(www\.)?([\w\-\.]+)+$"
    obj = re.match(pattern, url)
        
    return obj

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


def extractDirectories(url, line, links, output):

    code = 429
    while code == 429:
                        
        code = requests.get(url + line.rstrip('\n')).status_code
        if code == 404:

            print('Directory/File does not exist: ' + line.rstrip('\n'))

        elif code // 100 == 2 or code == 403:

            print('Directory/File does exist: ' + line.rstrip('\n') + " " + str(code)) 

            if code != 403:
                
                extractLinks(master + line.rstrip('\n'), links)   

            output.write(url + line.rstrip('\n') + "\t" + str(code) + "\n" )
            output.flush()         

        elif code == 429:

            print("Waiting")
            time.sleep(5)

def extractSubdomains(line, output, links):
    
    code = 429
    while code == 429:
            
        link = sur_master + line.rstrip('\n') + "." + sub_master
        
        try:
            
            code = requests.get(link).status_code

        except:

            code = 404

        if code == 404:

            print('Subdomain does not exist: ' + line.rstrip('\n'))

        elif code // 100 == 2 or code == 403:

            print('Subdomain does exist: ' + line.rstrip('\n') + " " + str(code)) 

            if code != 403:
                
                extractLinks(link, links)

            output.write(link + "\t" + str(code) + "\n" )
            output.flush()
            

        if code == 429:

            print("Waiting")
            time.sleep(5)

def cleanUrls(master):

    if not master.startswith("http"):

            if not master.startswith("www."):

                master = "https://www." + master

            else: 

                master = "https://" + master
    else:

            if not re.sub("https?:\/\/", "", master).startswith("www."):

                flag = False
                if master.find("https") != -1:

                    flag = True

                master = ("https" if flag else "http") + "://www." + re.sub(r"https?://", "", master)


            
    components = master.split("//")
    master = master.split("//")[0] + "//" + master.split("//")[1] + "/"

    sur_master = components[0] + "//"
    sub_master = re.sub("www\.", "", components[1])

    return (master, sub_master, sur_master)

if(len(sys.argv) >= 2):

    master = sys.argv[1]

    if is_valid_url(master):

        (master, sub_master, sur_master) = cleanUrls(master)

        with open("./subdomains_output.bat", 'w') as domains_output:

            with open("./dirs_files_output.bat", 'w') as dirs_output:
                    
                with open("./links.bat", 'w') as links_output:

                    extractLinks(master, links_output)


                    with open("./dirs_dictionary.bat", "r") as dirs:

                        for line in dirs.readlines()[0:15]:
                                    
                            extractDirectories(line, dirs_output, links_output)

                    with open("./subdomains_dictionary.bat", "r") as dirs:

                        for line in dirs.readlines()[0:15]:
                                    
                            extractSubdomains(line, domains_output, links_output)



                        

    else:

        print("Invalid URL")           

                    

else:

    print("Missing Parameters")
       

       
            