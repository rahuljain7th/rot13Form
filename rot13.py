import webapp2
import jinja2
import logging
import os

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))
class Handler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        logging.info('In the Handler Class')
        self.response.out.write(*a,**kw)
        
    def render_str(self,template,**params):
        t = jinja_env.get_template(template)
        return t.render(params)
    
    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))


class MainPage(Handler):
    def get(self):
        logging.info("Directory Path is : %s", os.path.dirname(__file__))
        #self.response.headers['Content-Type'] = 'text/plain'
        self.render('index.html')

class Rot13Handler(Handler):
    def post(self):
        logging.info("Inside the Post Method of Rot13Handler")
        rotinput = self.request.get("rot13input")
        rotoutput=rot13converter(rotinput)
        self.render('index.html',output=rotoutput)


def rot13converter(input):
    alphabets=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    inputarr=list(input)
    outputarr=[]
    for count,input in enumerate(inputarr):
        if input.isalpha():
            index = alphabets.index(input.upper())
            logging.debug("Index %s",index)
            index = index + 13
            if index > 25:
                index=index-26
                logging.debug("Manipulated Index %s",index)
            output=alphabets[index]
            if input.islower():
                output=output.lower()
            outputarr.append(output)            
        else:
            outputarr.append(input)

    return ''.join(outputarr)
        
    
app = webapp2.WSGIApplication([
('/', MainPage),('/rot13',Rot13Handler),
], debug=True)

