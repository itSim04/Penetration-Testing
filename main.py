import sys, urllib, re

master = sys.argv[1]

req = urllib.request.Request(master)
webUrl = urllib.request.urlopen(req)
print(webUrl)
                                    
link_pattern = r'href="[^#\"]{2,}?"'

refs = re.findall(link_pattern, webUrl.read().decode())
print(refs)