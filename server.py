#Silas Wrights web server for 2750 course UOG
from http.server import HTTPServer, BaseHTTPRequestHandler
import Physics
import phylib
import math
import string
import os
import glob
from urllib.parse import urlparse
from urllib.parse import urlunparse
#import cgi
import json
#import pickle
# handler subclass with methods for both GET and POST requests
class MyHandler( BaseHTTPRequestHandler ):
    def do_GET(self):
        #print("hello world")
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path )
        copy = parsed
        copyString = urlunparse(copy)
        #split the string since we dont know the table number
        split = copyString.split("-")

        # check if the web-pages matches the list
        if parsed.path in [ '/shot.html' ]:
            #print("yayyy")
            # retreive the HTML file
            fp = open( '.'+self.path )
            content = fp.read()

            # generate the headers
            self.send_response( 200 ) # OK
            self.send_header( "Content-type", "text/html" )
            self.send_header( "Content-length", len( content ) )
            self.end_headers()

            # send it to the broswer
            self.wfile.write( bytes( content, "utf-8" ) )
            fp.close()

        elif parsed.path in [ '/poolgame' ]:
            #print("yayyy")
            # retreive the HTML file
            fp = open( './a4.html' )
            content = fp.read()

            # generate the headers
            self.send_response( 200 ) # OK
            self.send_header( "Content-type", "text/html" )
            self.send_header( "Content-length", len( content ) )
            self.end_headers()

            # send it to the broswer
            self.wfile.write( bytes( content, "utf-8" ) )
            fp.close()
            
        
        elif split[0] in '/table' and '.svg' in split[1]:
            # retreive the svg file
            try:
                fp = open( '.'+self.path, 'rb' )
                content = fp.read()

                self.send_response( 200 ); # OK
                self.send_header( "Content-type", "image/svg+xml" )
                self.send_header( "Content-length", len( content ) )
                self.end_headers()

                self.wfile.write( content )
                fp.close()
            except:
                # generate 404 for GET requests that aren't the files above
                self.send_response( 404 )
                self.end_headers()
                self.wfile.write( bytes( "404: %s not found silly error #1" % self.path, "utf-8" ) )
        else:
            # generate 404 for GET requests that aren't the files above
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: %s not found silly error #2" % self.path, "utf-8" ) )


    def do_POST(self):
        # hanle post request
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path )

        if parsed.path in [ '/display.html' ]:#not needed or supported

            # get data send as Multipart FormData (MIME format)
            #form = cgi.FieldStorage( fp=self.rfile,
            #                         headers=self.headers,
            #                         environ = { 'REQUEST_METHOD': 'POST',
            #                                     'CONTENT_TYPE': 
            #                                       self.headers['Content-Type'],
            #                                   } 
            #                       )
            #get form data
            sbPos = Physics.Coordinate(form['sb_x'],form['sb_y'])
            rbPos = Physics.Coordinate(form['rb_x'],form['rb_y'])
            rbVel = Physics.Coordinate(form['rb_dx']+0.0,form['rb_dy']+0.0)#!!!
            stillBall = Physics.StillBall(self,phylib.PHYLIB_STILL_BALL,form['sb_number'],sbPos,None,None,0,0)
            rollingBall = Physics.RollingBall(self,phylib.PHYLIB_ROLLING_BALL,form['rb_number'],rbPos,rbVel,None,0,0)
            
            #calculate speed
            x2 = rbVel.x * rbVel.x
            y2 = rbVel.y * rbVel.y
            speed = math.sqrt(x2+y2)

            #if either speed is greater than our constant for still balls then compute acceleration as negitive velocity divided by speed multiplied to our drag constant
            if speed>Physics.VEL_EPSILON:
                rollingBall.obj.rolling_ball.acc = Physics.Coordinate(-(rollingBall.obj.rolling_ball.vel.x)/ speed*Physics.DRAG,-(rollingBall.obj.rolling_ball.vel.y)/ speed*Physics.DRAG)
            
            #delete all svg files
            os.chdir(".")#look in current dir
            svgFiles = glob.glob('*svg')#put all svg files in a list
            for svgFile in svgFiles:
                os.remove(svgFile)

            #construct table
            table = Physics.Table()
            table += stillBall
            table += rollingBall

            #save all svg files
            i = 0
            newSvgFiles = ["table-"+i+".svg"]
            # open file for write
            fp = open( "table-"+i+".svg", 'wb' )
            # write svg function string to file in local dir
            fp.write( table.svg() )
            #close file
            fp.close()
            while(table != None):
                #call segment function
                table = table.segment()
                #add to list of filenames
                newSvgFiles = ["table-"+i+".svg"]
                # open file for write
                fp = open( "table-"+i+".svg", 'wb' )
                # write svg function string to file in local dir
                fp.write( table.svg() )
                #close file
                fp.close()
                #increment i
                i += 1
            
            #save html with svg files
            myHTML = """<!--HTML code for 2750 A2 assignment-->
<html>
    <head>
        <title>Silas' A2 Assignment for 2750</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        
        <style>
            .nav{
                display: flex;
                background-color: black;
            }
            
            .nav a{
                color: white;
                padding: 14px 20px;
                text-decoration: none;
                text-align: center;
            }
            
            .nav a:hover{
                background-color: gray;
                color: black;
            }
            .p_text{
                font-family: serif;
                text-align: center;
                font-size: 150%;
            }
            .h_text{
                font-family: serif;
                text-align: center;
                font-size: 300%;
            }
        </style>
    
    </head>
    <body style="background-color: lightsteelblue">
        <div class="nav">
            <h4 class="nav_title" >Silas' A2</h4>
            <a href ="shoot.html">Back</a>
        </div>
        
        <div>
            <h1 class="h_text">Initial Balls</h1>
            <p class="p_text">Still ball pos x """+stillBall.obj.still_ball.pos.x+"""</p>
            <p class="p_text">Still ball pos y """+stillBall.obj.still_ball.pos.y+"""</p>
            <p class="p_text">Rolling ball pos x """+rollingBall.obj.rolling_ball.pos.x+"""</p>
            <p class="p_text">Rolling ball pos y """+rollingBall.obj.rolling_ball.pos.y+"""</p>
            <p class="p_text">Rolling ball vel x """+rollingBall.obj.rolling_ball.vel.x+"""</p>
            <p class="p_text">Rolling ball vel y """+rollingBall.obj.rolling_ball.vel.y+"""</p>

         """
            for file in newSvgFiles:
                myHTML += """<img src=\""""+file+"""\" alt="svg file">"""
            
            myHTML +="""
        </div>
    </body>
</html>"""

            #send html file to client
            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" )
            self.send_header( "Content-length", len( myHTML ) )
            self.end_headers()

            # send it to the browser
            self.wfile.write( bytes( myHTML, "utf-8" ) )
            fp.close()

        elif parsed.path in [ '/poolgame' ]:
            # retreive the HTML file
            fp = open( './a4.html')
            content = fp.read()

            # generate the headers
            self.send_response( 200 ) # OK
            self.send_header( "Content-type", "text/html" )
            self.send_header( "Content-length", len( content ) )
            self.end_headers()

            # send it to the broswer
            self.wfile.write( bytes( content, "utf-8" ) )
            fp.close()

    
        #for a4 we need more post requests one for both functions
        elif(parsed.path in '/start.html'):
            #get length of post
            contentLen = int(self.headers['Content-Length'])
            #read post data
            post = self.rfile.read(contentLen)
            #parse data
            data = json.loads(post.decode('utf-8'))

            #get parameters
            gameName = data.get('param1')
            player1Name = data.get('param2')
            player2Name = data.get('param3')
            #call python function to start game
            myTuple = Physics.startGame(gameName,player1Name,player2Name)
            #extract variables returned by python function
            #svg = myTuple[0]
            #game = myTuple[1]
            #table = myTuple[2]

            #gameSerialized = {'gameName':game.gameName,'player1Name':game.player1Name,'player2Name':game.player2Name}
            #tableSerialized = {'objs':table.object,'time':table.time}

            #resultTuple = (svg,tableSerialized)

            #resultTuple = (myTuple[0],pickle.dumps(myTuple[1]),pickle.dumps(myTuple[2]))

            #send 200 ok
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'result': myTuple}).encode('utf-8'))
            #self.wfile.write(resultTuple)

        elif(parsed.path in '/shoot.html'):
            #get length of post
            contentLen = int(self.headers['Content-Length'])
            #read post data
            post = self.rfile.read(contentLen)
            #parse data
            data = json.loads(post.decode('utf-8'))

            #get parameters
            player1Name = data.get('param1')
            table = data.get('param2')
            gameName = data.get('param3')
            playerName = data.get('param4')
            xVel = data.get('param5')
            yVel = data.get('param6')

            #game = Physics.Game(gameDict['gameName'],gameDict['player1Name'],gameDict['player2Name'])#will have new db which is a flaw but not fatal
            #table = Physics.Table()
            #table.object = tableDict['objs']
            #table.time = tableDict['time']

            #call python function to start game
            myTuple = Physics.shot(player1Name,table,gameName,playerName,xVel,yVel)
            #extract variables returned by python function
            #svg = myTuple[0]
            #anotherTurn = myTuple[1]
            #winner = myTuple[2]
            #table = myTuple[3]

            #tableSerialized = {'objs':table.object,'time':table.time}

            #resultTuple = (svg,anotherTurn,winner,tableSerialized)

            #send 200 ok
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'result': myTuple}).encode('utf-8'))

        
        else:
            # generate 404 for POST requests that aren't the file above
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: %s not found silly error #3" % self.path, "utf-8" ) )



if __name__ == '__main__':
    httpd = HTTPServer(('localhost',57810), MyHandler)
    print(f'Starting server on port {57810}...')
    httpd.serve_forever()
