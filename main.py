import sys, urllib, re

master = sys.argv[1]

req = urllib.request.Request(master)
webUrl = urllib.request.urlopen(req)
print(webUrl)
                                    
link_pattern = r'href="[^#\"]{2,}?"'

refs = re.findall(link_pattern, webUrl.read().decode())
print(refs)

cleaning_pattern = r'".*"'
result = []
    
for ref in refs:

    line = re.findall(cleaning_pattern, ref)[0][1:-1]
    result.append(line)
