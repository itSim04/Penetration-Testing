import sys, urllib, re

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