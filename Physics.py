import sqlite3
import math
import os
import phylib;
import time

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />"""
FOOTER = """</svg>\n"""
################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH
SIM_RATE = phylib.PHYLIB_SIM_RATE
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON
DRAG = phylib.PHYLIB_DRAG
MAX_TIME = phylib.PHYLIB_MAX_TIME
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS

FRAME_INTERVAL = 0.01
# add more here

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;

    def svg(self,number,pos,x,y):
        xStr = str(pos.x)
        yStr = str(pos.y)
        rad = str(BALL_RADIUS)
        svgString = """ <circle cx=\""""+xStr+"""\" cy=\""""+yStr+"""\" r=\""""+rad+"""\" fill=\""""+BALL_COLOURS[number]+"""\" />\n"""
        return svgString

##################################Silas' classes
class RollingBall( phylib.phylib_object ):
    """
    Python ROLLINGBALL class.
    """

    def __init__( self, number, pos, vel, acc):
        """
        Constructor function. Requires ball number and position (x,y) and vel and acc vectors as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a RollingBall class
        self.__class__ = RollingBall;

    def svg(self,number, pos,x,y):
        xStr = str(pos.x)
        yStr = str(pos.y)
        rad = str(BALL_RADIUS)
        svgString = """ <circle cx=\""""+xStr+"""\" cy=\""""+yStr+"""\" r=\""""+rad+"""\" fill=\""""+BALL_COLOURS[number]+"""\" />\n"""
        return svgString


###############################
##################################
class Hole( phylib.phylib_object ):
    """
    Python hole class.
    """

    def __init__( self, pos):
        """
        Constructor function. Requires position as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE, 
                                       pos, None,None,
                                       0.0, 0.0);
      
        # this converts the phylib_object into a hole class
        self.__class__ = Hole;

    def svg(self,number, pos,x,y):
        xStr = str(pos.x)
        yStr = str(pos.y)
        rad = str(BALL_RADIUS)
        svgString = """ <circle cx=\""""+xStr+"""\" cy=\""""+yStr+"""\" r=\""""+rad+"""\" fill="black" />\n"""
        return svgString


##################################
class HCushion( phylib.phylib_object ):
    """
    Python HCUSHION class.
    """

    def __init__( self, y):
        """
        Constructor function. Requires y value as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCUSHION, 
                                       None,None,None,
                                       0.0,y);
      
        # this converts the phylib_object into a hole class
        self.__class__ = HCushion;

    def svg(self,number,pos,x,y):
        yString = str(y)
        svgString = """ <rect width="1400" height="25" x="-25" y=\""""+ yString +"""\" fill="darkgreen" />\n"""
        return svgString


##################################
class VCushion( phylib.phylib_object ):
    """
    Python VCUSHION class.
    """

    def __init__( self, x):
        """
        Constructor function. Requires x value as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_VCUSHION, 
                                       None,None,None,
                                       x,0.0);
      
        # this converts the phylib_object into a hole class
        self.__class__ = VCushion;
    # add an svg method here

    def svg(self,number,pos,x,y):
        xString = str(x)
        svgString = """ <rect width="25" height="2750" x=\""""+xString+"""\" y="-25" fill="darkgreen" />\n"""
        return svgString

class Database():
    def __init__(self,reset = False):
        if reset:
            if os.path.exists("phylib.db"):
                os.remove("phylib.db")#if reset is true remove phylib.db
        self.conn = sqlite3.connect("phylib.db")#connect to database
        self.cursor = self.conn.cursor()

    def createDB(self):
        #create tables
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Ball(BALLID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, BALLNO INTEGER NOT NULL, XPOS FLOAT NOT NULL, YPOS FLOAT NOT NULL, XVEL FLOAT, YVEL FLOAT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS TTable(TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, TIME FLOAT NOT NULL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS BallTable(BALLID INTEGER NOT NULL, TABLEID INTEGER NOT NULL, FOREIGN KEY (BALLID) REFERENCES Ball(BALLID),FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Game(GAMEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, GAMENAME VARCHAR(64) NOT NULL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Player(PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,GAMEID INTEGER NOT NULL, PLAYERNAME VARCHAR(64) NOT NULL,FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Shot(SHOTID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,PLAYERID INTEGER NOT NULL, GAMEID INTEGER NOT NULL,FOREIGN KEY (PLAYERID) REFERENCES Player(PLAYERID),FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS TableShot(TABLEID INTEGER NOT NULL,SHOTID INTEGER NOT NULL,FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID),FOREIGN KEY (SHOTID) REFERENCES Shot(SHOTID))")
            
        self.conn.commit()

    def readTable(self,tableID):
        sql_query = '''SELECT * FROM Ball, BallTable WHERE (Ball.BALLID = BallTable.BALLID and BallTable.TABLEID = (tableID+1))'''
        time = 'SELECT TIME FROM TTable WHERE (TTable.TABLEID = (tableID +1))'

        if rows is None:
            return None

        table = Table()


        for row in sql_query:
            ballID,ballNO,xPos,yPos,xVel,yPos,time = row

            if xVel == 0 or yVel == 0:
                ball = StillBall(ballNo, Coordinate(xPos, yPos))
            else:
                #calculate speed
                x2 = xVel * xVel
                y2 = yVel * yVel
                speed = math.sqrt(x2+y2)

                #compute acceleration as negitive velocity divided by speed multiplied to our drag constant
                acc = Coordinate(-(xVel)/ speed*DRAG,-(yVel)/ speed*DRAG)
                
                ball = RollingBall(ballNo, Coordinate(xPos, yPos), Coordinate(xVel, yVel), acc)

            table += ball

        self.conn.commit()
        return table

    def writeTable(self,table):
        rollingBalls = []
        stillBalls = []
        for obj in table:
            if obj is not None:
                if obj.type == phylib.PHYLIB_STILL_BALL: 
                    stillBalls.append(obj)
                elif obj.type == phylib.PHYLIB_ROLLING_BALL:
                    rollingBalls.append(obj)
         
        for ball in stillBalls:
            self.cursor.execute('''INSERT INTO Ball(BALLNO,XPOS,YPOS,XVEL,YVEL) VALUES (?,?,?,?,?)''',(ball.obj.still_ball.number,ball.obj.still_ball.pos.x,ball.obj.still_ball.pos.y,0,0))

        for ball in rollingBalls:
            self.cursor.execute('''INSERT INTO Ball(BALLNO,XPOS,YPOS,XVEL,YVEL) VALUES (?,?,?,?,?)''',(ball.obj.rolling_ball.number,ball.obj.rolling_ball.pos.x,ball.obj.rolling_ball.pos.y,ball.obj.rolling_ball.vel.x,ball.obj.rolling_ball.vel.y))

        self.cursor.execute('''SELECT TABLEID FROM TTable''')
        tableID = self.cursor.fetchone()

        self.conn.commit()
        #self.cursor.close()
        
        return tableID

    def close(self):
        self.conn.commit()
        self.conn.close()

class Game():
    def __init__(self, gameID,gameName, player1Name, player2Name):
        if (gameID is not None and gameName is None and player1Name is None and player2Name is None):
            #if one of two execeptable cases
            gameID += 1

            db = Database()
            db.cursor.execute('''SELECT Game.GAMENAME,Player.PLAYERNAME FROM Game, Player WHERE (Game.GAMEID = Player.GAMEID) ORDER BY Player.PLAYERID''')
            names = db.cursor.fetchall()

            self.gameName = names[0][0]
            self.player1Name = names[0][1]
            self.player2Names = names[1][1]

            db.conn.commit()

            
        elif (gameID is None and gameName is not None and player1Name is not None and player2Name is not None):
            #if one of two execeptable cases
            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name

            db = Database()
            db.cursor.execute('''INSERT INTO Game(GAMENAME) VALUES(?)''',(gameName,))
            db.cursor.execute('''SELECT Game.GAMEID FROM Game WHERE (Game.GAMENAME = ?)''',(gameName,))
            gameIDTuple = db.cursor.fetchone()
            gameID = gameIDTuple[0]
            db.cursor.execute('''INSERT INTO Player(PLAYERNAME,GAMEID) VALUES(?,?)''',(player1Name,gameID))
            db.cursor.execute('''INSERT INTO Player(PLAYERNAME,GAMEID) VALUES(?,?)''',(player2Name,gameID))

            db.conn.commit()

        else:
            raise TypeError()


    def shoot(self, gameName, playerName, table, xvel, yvel):#I removed the database stuff for performence issues
        #db = Database()

        #playerNameSingle = playerName[0]
        #gameNameSingle = gameName[0]
        #db.cursor.execute('''SELECT Player.PLAYERID FROM Player WHERE (Player.PLAYERNAME = ?)''',(playerNameSingle,))
        #playerID = db.cursor.fetchone()
        #if playerID is None:
        #    playerID = 1
        #db.cursor.execute('''SELECT Game.GAMEID FROM Game WHERE (Game.GAMENAME = ?)''',(gameNameSingle,))
        #gameID = db.cursor.fetchone()
        #if gameID is None:
        #    gameID = 1

        #db.cursor.execute('''INSERT INTO Shot(GAMEID,PLAYERID) VALUES(?,?)''',(gameID,playerID))
        #db.cursor.execute('''SELECT Shot.SHOTID FROM Shot WHERE (Shot.PLAYERID = ? AND Shot.GAMEID = ?)''',(playerID,gameID))
        #shotID = db.cursor.fetchone()
        #shotIDSingle = shotID[0]
        #if shotIDSingle is None:
        #    shotIDSingle = 1

        #tableID = 0  this workaround is not longer nessecary
        #if shotID == 0:
            #idk what to do ill just keep it at 0
        #else:
        #    self.cursor.execute('''SELECT TableShot.TABLEID FROM TableShot WHERE (TableShot.SHOTID = ?)''',shotID-1)
        #    tableID = self.cursor.fetchone()
        #table.lolYouSunkTheCueBall()#just in case the cue ball was sunk
        cueBall = self.getCue(table)
        if(cueBall.type == phylib.PHYLIB_STILL_BALL):
            cueX = cueBall.obj.still_ball.pos.x
            cueY = cueBall.obj.still_ball.pos.y
        else:
            cueX = cueBall.obj.rolling_ball.pos.x
            cueY = cueBall.obj.rolling_ball.pos.y

        cueBall.type = phylib.PHYLIB_ROLLING_BALL
        cueBall.obj.rolling_ball.pos.x = cueX
        cueBall.obj.rolling_ball.pos.y = cueY
        cueBall.obj.rolling_ball.vel.x = xvel
        cueBall.obj.rolling_ball.vel.y = yvel

        #calculate speed
        x2 = xvel * xvel
        y2 = yvel * yvel
        speed = math.sqrt(x2+y2)

        #if the speed is greater than our constant for still balls then compute acceleration as negitive velocity divided by speed multiplied to our drag constant
        if speed>VEL_EPSILON:
            cueBall.obj.rolling_ball.acc = Coordinate(-1*(cueBall.obj.rolling_ball.vel.x)/ (speed*DRAG),-1*(cueBall.obj.rolling_ball.vel.y)/ (speed*DRAG))

        cueBall.obj.rolling_ball.number = 0

        #call segment over and over
        svgSet = []
        pretime = 0
        postime = 0
        timediff = 0
        frame = 0
        numRolling = table.numRolling()
        while(numRolling != 0):#for some reason looping based on null table causes inf loop so i do my own rolling ball count
            pretime = time.time()
            #pretime = table.time
            table = table.segment()
            postime = time.time()
            #postime = table.time
            timediff = postime-pretime
            timediff = math.floor(timediff/FRAME_INTERVAL)
            for i in range(timediff + 1):
                frame = i * FRAME_INTERVAL
                newTable = table.roll(frame)
                newTable.time = pretime+frame
                svgSet.append(newTable.svg())
                #tableID = db.writeTable(newTable)
                #if tableID is None:
                #    tableID = 1
                #db.cursor.execute('''INSERT INTO TableShot(TABLEID,SHOTID) VALUES(?,?)''',(tableID,shotIDSingle))
            numRolling = table.numRolling()
            #print(table)
        
        #db.conn.commit()
        return svgSet,table

    def getCue(self,table):
        cueBall = None
        for obj in table:
            if obj is not None:
                if obj.type ==phylib.PHYLIB_STILL_BALL:
                    if obj.obj.still_ball.number == 0:
                        #print("foundcueeee")
                        cueBall = obj
                elif obj.type ==phylib.PHYLIB_ROLLING_BALL:
                    if obj.obj.rolling_ball.number == 0:
                        cueBall = obj
        return cueBall


################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def tupleTable(self):#for sending data over to html
        time = self.time
        objs =[]
        for obj in self:
            if obj is not None:
                if obj.type == phylib.PHYLIB_STILL_BALL:
                    objs.append(('s',obj.obj.still_ball.number,obj.obj.still_ball.pos.x,obj.obj.still_ball.pos.y,0,0,0,0))
                elif obj.type == phylib.PHYLIB_ROLLING_BALL:
                    objs.append(('r',obj.obj.rolling_ball.number,obj.obj.rolling_ball.pos.x,obj.obj.rolling_ball.pos.y,obj.obj.rolling_ball.vel.x,obj.obj.rolling_ball.vel.y,obj.obj.rolling_ball.acc.x,obj.obj.rolling_ball.acc.y))
                elif obj.type == phylib.PHYLIB_HOLE:
                    objs.append(('o',0,obj.obj.hole.pos.x,obj.obj.hole.pos.y,0,0,0,0))
                elif obj.type == phylib.PHYLIB_HCUSHION:
                    objs.append(('h',0,0,obj.obj.hcushion.y,0,0,0,0))
                elif obj.type == phylib.PHYLIB_VCUSHION:
                    objs.append(('v',0,obj.obj.vcushion.x,0,0,0,0,0))
        htmlFriendly = (time,objs)
        return htmlFriendly

    #add two methods the first will initialize all the balls for a game the second will see if the cue ball was sunk and if so add it back
    def gameSetup(self):
        #declare new balls
        ball0 = StillBall(0,Coordinate(TABLE_WIDTH/2,TABLE_LENGTH*0.75))
        ball1 = StillBall(1,Coordinate(675,675))
        #ball0 = StillBall(0,Coordinate(TABLE_WIDTH/2,TABLE_LENGTH-TABLE_WIDTH/2))
        #ball1 = StillBall(8,Coordinate(TABLE_WIDTH/2-math.sqrt(BALL_DIAMETER*BALL_DIAMETER/2),TABLE_WIDTH/2-math.sqrt(BALL_DIAMETER*BALL_DIAMETER/2)))
        ball2 = StillBall(2,Coordinate(615,615))
        ball3 = StillBall(3,Coordinate(735,615))
        ball4 = StillBall(4,Coordinate(675,615))
        ball5 = StillBall(5,Coordinate(575,545))
        ball6 = StillBall(6,Coordinate(775,545))
        ball7 = StillBall(7,Coordinate(640,545))
        ball8 = StillBall(8,Coordinate(715,545))
        ball9 = StillBall(9,Coordinate(465,475))
        ball10 = StillBall(10,Coordinate(875,475))
        ball11 = StillBall(11,Coordinate(615,475))
        ball12 = StillBall(12,Coordinate(675,475))
        ball13 = StillBall(13,Coordinate(745,475))
        ball14 = StillBall(14,Coordinate(545,475))
        ball15 = StillBall(15,Coordinate(805,475))
        #add balls to table
        self += ball0
        self += ball1
        self += ball2
        self += ball3
        self += ball4
        self += ball5
        self += ball6
        self += ball7
        self += ball8
        self += ball9
        self += ball10
        self += ball11
        self += ball12
        self += ball13
        self += ball14
        self += ball15

    def lolYouSunkTheCueBall(self):
        cue = 0 #initialize cue to sunk
        for obj in self:
            if obj is not None:
                if obj.type == phylib.PHYLIB_STILL_BALL:
                    if obj.obj.still_ball.number == 0:
                        cue = 1
                        #print("found cue")
                elif obj.type == phylib.PHYLIB_ROLLING_BALL:
                    if obj.obj.rolling_ball.number == 0:
                        cue = 1
                        #print("adding cue rb")
        #if we did not find the cue ball
        if(cue == 0):
            #add the cue ball back on the table
            #print("adding cue")
            ball0 = StillBall(0,Coordinate(TABLE_WIDTH/2,TABLE_LENGTH*0.75))
            self += ball0

    def anotherTurn(self,playerIndex,preTable):
        preBalls = set()
        for obj in preTable:
            if obj is not None:
                if obj.type ==phylib.PHYLIB_STILL_BALL:
                    preBalls.add(obj.obj.still_ball.number)
                elif obj.type ==phylib.PHYLIB_ROLLING_BALL:
                    preBalls.add(obj.obj.rolling_ball.number)
        
        postBalls = set()
        for obj in self:
            if obj is not None:
                if obj.type ==phylib.PHYLIB_STILL_BALL:
                    postBalls.add(obj.obj.still_ball.number)
                elif obj.type ==phylib.PHYLIB_ROLLING_BALL:
                    postBalls.add(obj.obj.rolling_ball.number)

        if(playerIndex == 1):
            toCompare = {1,2,3,4,5,6,7}
        else:
            toCompare = {9,10,11,12,13,14,15}

        anotherTurn = 0
        if((toCompare & preBalls) != (toCompare & postBalls)):
            #if the user sunk one of their balls
            anotherTurn = 1

        return anotherTurn

    #method checks to see if you prempivity sunk black ball (0), didnt sink black ball (1), or sunk black ball to win (2)
    def didYouBeef(self,playerIndex):
        toReturn = 0 #initialize to premtivily sinking black ball
        balls = set()
        if self is None:
            toReturn = 420#debugging purposes
        for obj in self:# loop through table if we find the 8 ball then change return value to 1
            if obj is not None:
                if obj.type ==phylib.PHYLIB_STILL_BALL:
                    balls.add(obj)#also add all the balls on table to a set
                    if obj.obj.still_ball.number == 8:
                        toReturn = 1
                elif obj.type ==phylib.PHYLIB_ROLLING_BALL:
                    balls.add(obj)
                    if obj.obj.rolling_ball.number == 8:
                        toReturn = 1

        if(toReturn == 0):#if this player sunk the 8 ball
            if(playerIndex == 1):
                toCompare = {1,2,3,4,5,6,7}
            else:
                toCompare = {9,10,11,12,13,14,15}

            if((balls & toCompare) =={}):#and this player sunk all their balls
                toReturn = 2#change return value
        
        return toReturn

    def numRolling(self):
        numRolling = 0
        for obj in self:
            if obj is not None:
                if obj.type == phylib.PHYLIB_ROLLING_BALL:
                    numRolling += 1
        return numRolling

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    def roll( self, t):
        new = Table()
        for ball in self:
            if isinstance(ball, RollingBall):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,Coordinate(0,0),Coordinate(0,0),Coordinate(0,0) )
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t )
                # add ball to table
                new += new_ball

            if isinstance(ball, StillBall):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,Coordinate( ball.obj.still_ball.pos.x,ball.obj.still_ball.pos.y ) )
                # add ball to table
                new += new_ball
        #return table
        return new

    # add svg method here
    def svg(self):
        svgToReturn = HEADER
        
        for obj in self:
            if obj is not None:
                if obj.type == phylib.PHYLIB_STILL_BALL:
                    svgToReturn += obj.svg( obj.obj.still_ball.number,obj.obj.still_ball.pos,0,0)
                if obj.type == phylib.PHYLIB_ROLLING_BALL:
                    svgToReturn += obj.svg( obj.obj.rolling_ball.number,obj.obj.still_ball.pos,0,0)
                if obj.type == phylib.PHYLIB_HOLE:
                    svgToReturn += obj.svg( 0,obj.obj.hole.pos,0,0)
                if obj.type == phylib.PHYLIB_HCUSHION:
                    svgToReturn += obj.svg( 0,None,0,obj.obj.hcushion.y)
                if obj.type == phylib.PHYLIB_VCUSHION:
                    svgToReturn += obj.svg( 0,None,obj.obj.vcushion.x,0)
        
        svgToReturn += FOOTER
        return svgToReturn

#declare two functions

#this function will be called to initialize resources
def startGame(gameName,player1Name,player2Name):
    #currently implement these as inside the function scope but they might need to be global
    table = Table()
    table.gameSetup()

    db = Database()
    db.createDB()
    db.writeTable(table)
    #maybe need to insert more things into db here

    game = Game(None,gameName,player1Name,player2Name)

    htmlFriendlyTable = table.tupleTable()
    #we also need this to return a svg string of the table
    svg = table.svg()
    return svg,htmlFriendlyTable

def buildTable(htmlTable):
    table = Table()
    if htmlTable is not None:
        #time = htmlTable[0]
        time = 0.0#reset time should fix
        objects = htmlTable[1]
        table.time = time
        for obj in objects:
            if obj[0] == 's':#add still ball
                ball = StillBall(obj[1],Coordinate(obj[2],obj[3]))
                table += ball
            elif obj[0] == 'r':#add rolling ball
                ball = RollingBall(obj[1],Coordinate(obj[2],obj[3]),Coordinate(obj[4],obj[5]),Coordinate(obj[6],obj[7]))
                table += ball
    return table

# this function will be called when user shoots in html file
def shot(player1Name,htmlTable,gameName,playerName,xVel,yVel):
    table = buildTable(htmlTable)

    tempTable = table
    game = Game(None,gameName,player1Name,playerName)
    returnTuple = game.shoot(gameName,playerName,table,xVel,yVel)
    svgSet = returnTuple[0]
    table = returnTuple[1]
    #I decided to modify the shoot method to return a set containing svg strings for each frame since it made the most sence to implement it there
    #now we need to either generate a bunch of svg files and send them through server or send the strings through server in a way html can handle
    svgString = ""
    for svg in svgSet:
        svgString += svg + "~"#add ~ to split later
        #print(svg)
    svgString = svgString[:-1]#remove ending ~

    #use game obj attributes to get the player index
    if(player1Name == playerName):
        playerIndex = 1
    else:
        playerIndex = 2

    #also reset the cue ball if they sunk it
    table.lolYouSunkTheCueBall()
    #use methods anotherTurn and didYouBeef to perform game logic
    #see if the user gets another turn
    anotherTurn = table.anotherTurn(playerIndex,tempTable)
    #see if the user loses or wins the game
    winner = table.didYouBeef(playerIndex)

    htmlFriendlyTable = table.tupleTable()
    #print(htmlFriendlyTable)
    #print(table)
    cueBall = game.getCue(table)
    if cueBall.type == phylib.PHYLIB_STILL_BALL:
        cueX = cueBall.obj.still_ball.pos.x
        cueY = cueBall.obj.still_ball.pos.y
    else:
        cueX = cueBall.obj.rolling_ball.pos.x
        cueY = cueBall.obj.rolling_ball.pos.y
    cuePos = (cueX,cueY)

    return svgString,anotherTurn,winner,htmlFriendlyTable,cuePos

