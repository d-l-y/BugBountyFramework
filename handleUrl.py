from furl import furl
import hashlib

class HandleUrl():
    
    def __init__(self,url):
         self.url = url
         self.f=furl(url)
         self.args = self.f.args
         self.params = sorted(self.f.args.keys())
         self.values = self.f.args.values()
         self.domain = self.f.host

    def dbParams(self):
        return "||".join(self.params)


    def emptyValues(self):
        for param in self.params:
            del self.args[param]
            self.args[param] = ''
        return self.f.url

print hashlib.md5(HandleUrl('http://www.google.com/?c=FSF&zome=test&a=dff&p=jhd&aome2=test2').emptyValues()).hexdigest()
print hashlib.md5(HandleUrl('http://www.google.com/?zome=test&aome2=tet2&c=FSF&a=dff&p=hd').emptyValues()).hexdigest()
print hashlib.md5(HandleUrl('http://www.google.com/?a=dff&c=FF&zome=test&p=jh&aome2=test2').emptyValues()).hexdigest()
print hashlib.md5(HandleUrl('http://www.google.com/?a=dff&c=FSF&zome=t&p=jhd&aome2=tes2').emptyValues()).hexdigest()
print hashlib.md5(HandleUrl('http://www.google.com/?ab=dff&c=FSF&zome=t&p=jhd&aome2=tes2').emptyValues()).hexdigest()

