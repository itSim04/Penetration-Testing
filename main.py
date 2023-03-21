import sys, urllib

master = sys.argv[1]

req = urllib.request.Request(master)
webUrl = urllib.request.urlopen(req)
print(webUrl)
                                    
                                    
