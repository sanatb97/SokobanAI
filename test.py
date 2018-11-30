"""
	Sprites:
	-Man - moves, object
	-Boulders - moves, object
	-Wall - doesn't move, not an object
	-Goals - doesn't move, not an object
"""
import pygame
import time
pygame.init()

class moveableObs(object):
	def clearCurrPos(self):
		'''
		clears the screen in GUI where the calling object is present.
		If the current position has a goal state, it blits a goal state at that point instead of clearing the GUI.
		'''
		if(self.ongoal==0):
			gameDisplay.fill(white, rect=(self.x,self.y,50,50))
		else:
			gameDisplay.blit(goalSprite,(self.x,self.y))

	def handleKeyPress(self):
		'''
		sets target based on keypress, and calls moveTo which takes further decision/action.
		'''
		currCol=self.x/50
		currRow=self.y/50
		horizontal=1
		
		if event.key==pygame.K_LEFT:
			targetCol=currCol-1
			targetRow=currRow
			offset=-50
			return self.moveTo(targetRow,targetCol,currRow,currCol,offset,horizontal)
				
		elif event.key==pygame.K_RIGHT:
			targetCol=currCol+1
			targetRow=currRow
			offset=50
			return self.moveTo(targetRow,targetCol,currRow,currCol,offset,horizontal)
			
		elif event.key==pygame.K_UP:
			horizontal=0
			targetCol=currCol
			targetRow=currRow-1
			offset=-50
			return self.moveTo(targetRow,targetCol,currRow,currCol,offset,horizontal)
			
		elif event.key==pygame.K_DOWN:
			horizontal=0
			targetCol=currCol
			targetRow=currRow+1
			offset=50
			return self.moveTo(targetRow,targetCol,currRow,currCol,offset,horizontal)
			
	def moveTo(self,targetRow,targetCol,currRow,currCol,offset,horizontal):
		'''
		Decides whether the object can be moved or not.
		If yes, also check whether the object is going to a goal.
			If it is, set self.ongoal=1
			If no, set self.ongoal=0
		Based on keypress, changes coordinates of calling object.
		Does not update position on GUI. That is done by updatePos.
		However, clears current position of calling object from the GUI by calling clearCurrPos().
		'''

		currentGrid=gameMap[currRow][currCol]
		target=gameMap[targetRow][targetCol]

		if(target==-1):
			#target is a wall
			#if the object being moved is a boulder, tell man that the boulder can't be moved
			if(self.__class__.__name__=='boulder'):
				return 0

		elif(target==-2):
			#target is a floor tile

			#change gameMap
			#moving the man who is on goal
			if(currentGrid==-5):
				gameMap[currRow][currCol]=-4
				gameMap[targetRow][targetCol]=-3

			#moving a boulder who is on goal
			elif(currentGrid<=-10):
				#decrement number of boulders on goal
				boulder.bouldersOnGoal-=1
				gameMap[currRow][currCol]=-4
				gameMap[targetRow][targetCol]=currentGrid/10*-1-1
			
			#moving an object which is on floor
			else:
				gameMap[currRow][currCol]=-2
				gameMap[targetRow][targetCol]=currentGrid

			#update GUI
			self.clearCurrPos()
			if(horizontal==1):
				self.x+=offset
			else:
				self.y+=offset
			self.ongoal=0
			self.updatePos()

			#if object being moved is a boulder, tell man that the boulder has been moved
			if(self.__class__.__name__=='boulder'):
				return 1

		elif(target==-4):
			#target is a goal state

			#change gameMap
			#moving the man who is on goal to another goal
			if(currentGrid==-5):
				gameMap[currRow][currCol]=-4
				gameMap[targetRow][targetCol]=currentGrid

			#moving a boulder who is on goal to another goal
			elif(currentGrid<=-10):
				gameMap[currRow][currCol]=-4
				gameMap[targetRow][targetCol]=currentGrid
			
			#moving a man which is on floor to a goal
			elif(currentGrid==-3):
				gameMap[currRow][currCol]=-2
				gameMap[targetRow][targetCol]=-5

			#moving a boulder which is on floor to a goal
			else:
				#increment number of boulders on goal
				boulder.bouldersOnGoal+=1
				gameMap[currRow][currCol]=-2
				gameMap[targetRow][targetCol]=-1*(currentGrid+1)*10

			#update GUI
			self.clearCurrPos()
			if(horizontal==1):
				self.x+=offset
			else:
				self.y+=offset
			
			self.ongoal=1
			self.updatePos()

			#if object being moved is a boulder, tell man that the boulder has been moved
			if(self.__class__.__name__=='boulder'):
				return 1

		elif(target>=0 or target<=-10):
			#target is a boulder
			#if object being moved is a boulder, tell man that the boulder can't be moved
			if(self.__class__.__name__=='boulder'):
				return 0

			#this part reached only if object being moved is the man
			if(target<=-10):
				boulderIndex=target/10*-1-1
			else:
				boulderIndex=target

			moveTheMan=boulderlist[boulderIndex].handleKeyPress()
			if(moveTheMan==1):
				#change gameMap
				
				#target boulder is on the floor
				if(target>=0):
					#moving man who is on floor to another floor tile
					if(currentGrid==-3):
						gameMap[currRow][currCol]=-2
						gameMap[targetRow][targetCol]=-3

					#moving man who is on goal to a floor tile
					elif(currentGrid==-5):
						gameMap[currRow][currCol]=-4
						gameMap[targetRow][targetCol]=-3

				#target boulder is on a goal
				else:
					#moving man who is on floor to a goal
					if(currentGrid==-3):
						gameMap[currRow][currCol]=-2
						gameMap[targetRow][targetCol]=-5

					#moving man who is on goal to a goal
					elif(currentGrid==-5):
						gameMap[currRow][currCol]=-4
						gameMap[targetRow][targetCol]=-5

				#update GUI
				self.clearCurrPos()
				if(horizontal==1):
					self.x+=offset
				else:
					self.y+=offset
				
				if(target<=-10):
					self.ongoal=1
				else:
					self.ongoal=0
				self.updatePos()

	def updatePos(self):
		'''
		blits the sprite of calling object onto it's current coordinates.
		If onGoal=0, blits normal sprite.
		If onGoal=1, blits onGoal sprite.
		onGoal sprite means the man/boulder is on the goal, not on the floor.
		'''
		if(self.ongoal==0):
			gameDisplay.blit(self.sprite,(self.x,self.y))
		
		else:
			gameDisplay.blit(self.onGoalSprite,(self.x,self.y))

class man(moveableObs):
	def __init__(self,x_init,y_init,onGoalAtStart=0):
		'''
		ongoal: whether man is on goal right now
		x: x coordinate on screen
		y: y coordinate on screen
		sprite: sprite of man
		onGoalSprite: sprite of man on goal
		'''
		self.ongoal=onGoalAtStart
		self.x=x_init
		self.y=y_init
		self.sprite=pygame.image.load('sprites/man3.png')
		self.onGoalSprite=pygame.image.load('sprites/manongoal.png')
		self.updatePos()

class boulder(moveableObs):
	boulderSprite=pygame.image.load('sprites/pineco.png')
	numOfBoulders=0
	bouldersOnGoal=0
	def __init__(self,x_init,y_init,onGoalAtStart=0):
		'''
		ongoal: whether man is on goal right now
		x: x coordinate on screen
		y: y coordinate on screen
		sprite: sprite of man
		onGoalSprite: sprite of man on goal
		'''
		boulder.numOfBoulders+=1
		self.ongoal=onGoalAtStart
		self.x=x_init
		self.y=y_init
		self.sprite=boulderSprite
		self.onGoalSprite=pygame.image.load('sprites/boulderongoal.png')
		self.updatePos()


def makeMapArray(levelNum='3'):
	'''
	Reads the level text file, and generates a gamemap.
	The various objects are represented as:
		Walls: -1
		Floor: -2
		Man:   -3
		Goal:  -4
		Man on goal: -5
		Boulder on goal: -1*(bouldernum+1)*10
		Boulder: bouldernum, which represents the index of the boulder oject in the list of boulder objects
			The boulderobject list is made in the initialise board function, where all these objects are placed on the GUI
	'''
	level=open('levels/project_levels/level'+levelNum,'r').read()
	outerArray=list()
	innerArray=[]
	characterMap={'$':0, '#':-1, ' ':-2, '@':-3, '.': -4, '+':-5}
	
	for char in level:
		if char!='\n':
			if(char=='*'):
				#if a boulder is found on a goal, store it as -1*(bouldernum+1)*10
				#note that this formula ensures boulderongoal is always represented as a num<=-10.
				#hence, while gameplay if the num<=-10, we know it's a boulder on goal
				#we can access the corresponding boulder object by using the expression:
				# currentBoulder= -1*num/10 -1
				#Using currentBoulder, we can access the boulder object from the boulderlist. 
				#Also, since a boulder was added, increment bouldernum by 1

				#%%---why use bouldernum+1 instead of bouldernum to represent boulderongoal:
				#%%---if bouldernnum=0, then the resulting value will be 0, which represents the first boulder not on a goal,
				#%%---hence causing a conflict. We must ensure that boulderongoal is always<=-10, hence start from bouldernum+1
				innerArray.append((characterMap['$']+1)*10*-1)
				characterMap['$']+=1
			else:
				innerArray.append(characterMap[char])
				#if a boulder was added, increment bouldernum
				if char=='$':
					characterMap['$']+=1
		else:
			outerArray.append(innerArray)
			innerArray=[]
	outerArray.append(innerArray)
	return outerArray

def initialiseBoard(gameMap,width,height,goalSprite,boulderlist):
	'''
	Reads the gameMap and blits all the objects to GUI accordingly
	'''
	wallSprite=pygame.image.load('sprites/brick.png')

	for row in range(height):
		for col in range(width):
			currItem=gameMap[row][col]

			if(currItem>=0):
				#creates a boulder object, displays it on the GUI and appends it to the boulderlist
				boulderlist.append(boulder(col*50,row*50))
				
			elif(currItem==-1):
				#displays wall on GUI
				gameDisplay.blit(wallSprite,(col*50,row*50))

			elif(currItem==-3):
				#creates a man object and displays on the GUI
				manOb=man(col*50,row*50)

			elif(currItem==-4):
				#displays goal on GUI
				gameDisplay.blit(goalSprite,(col*50,row*50))

			elif(currItem==-5):
				#creates a man object, intialised to stand on the goal, and displays on GUI
				manOb=man(col*50,row*50,1)

			elif(currItem<=-10):
				#creates a boulder object, intialised to stand on the goal, and displays on GUI
				boulderlist.append(boulder(col*50,row*50,1))

	return manOb

def message_display(text, font_size,display_width, display_height):
    '''
	function to display text to screen.
	text centred at display_width/2 and display_height/2
    '''
    largeText = pygame.font.Font('freesansbold.ttf',font_size)
    TextSurf = largeText.render(text, True, black)
    TextRect = TextSurf.get_rect()
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()

def levelCleared(gameDisplay):
	'''
	displays level cleared screen.
	Options to restart level,
	choose another level,
	or quit
	'''
	gameDisplay.fill(white)
	message_display('Level Cleared!',30,50*width,25*height)
	message_display("Restart: r",20,50*width,50*height)
	message_display("Change level: l",20,50*width,70*height)
	message_display("Quit: q",20,50*width,90*height)

#def reverttoStart(gameDisplay,level):


def gameStart(gameDisplay,display_width,display_height):
	'''
	Displays the level select screen
	'''

	gameDisplay.fill(white)
	message_display("Enter level number",20,display_width,display_height-100)
	message_display("between 0 to 9",20,display_width,display_height)
	pygame.display.update()

	while True:
		for event in pygame.event.get():
				if event.type==pygame.QUIT:
					stopGame=True
					break

				if event.type==pygame.KEYDOWN:
					#As per the key presses, level is chosen
					#If key is not a number between 0 and 9, level is defaulted to 9
					gameDisplay.fill(white)
					pygame.display.update()
					
					if event.key==pygame.K_0 or event.key==pygame.K_KP0:
						return '1'
					elif event.key==pygame.K_1 or event.key==pygame.K_KP1:
						return '2'
					elif event.key==pygame.K_2 or event.key==pygame.K_KP2:
						return '3'
					elif event.key==pygame.K_3 or event.key==pygame.K_KP3:
						return '4'
					elif event.key==pygame.K_4 or event.key==pygame.K_KP4:
						return '5'
					elif event.key==pygame.K_5 or event.key==pygame.K_KP5:
						return '6'
					elif event.key==pygame.K_6 or event.key==pygame.K_KP6:
						return '7'
					elif event.key==pygame.K_7 or event.key==pygame.K_KP7:
						return '8'
					elif event.key==pygame.K_8 or event.key==pygame.K_KP8:
						return '9'
					else:
						return '10'


if __name__ == '__main__':
	#colours
	black=(0,0,0)
	white=(255,255,255)

	#getting level
	gameDisplay=pygame.display.set_mode((500,500))
	level=gameStart(gameDisplay,500,500)

	#making map
	gameMap=makeMapArray(level)
	print(gameMap)
	width=len(gameMap[0])
	height=len(gameMap)

	#sprites
	boulderSprite=pygame.image.load('sprites/pineco.png')
	goalSprite=pygame.image.load('sprites/goal.png')

	#list of all boulders
	boulderlist=list()

	#setting game display parameters
	gameDisplay=pygame.display.set_mode((50*width,50*(height+1)))
	pygame.display.set_caption('Sokoban')
	gameDisplay.fill(white)


	#placing objects onto gameDisplay, and getting the man object and boulderlist
	manOb=initialiseBoard(gameMap,width,height,goalSprite,boulderlist)
	
	#start clock
	clock=pygame.time.Clock()

	#game loop
	stopGame=False
	success=False
	while not stopGame:
		if success==False:
			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					stopGame=True
					break

				if event.type==pygame.KEYDOWN:
					if event.key==pygame.K_r:
						#gameMap,boulderlist,manOb=revertToStart(gameDisplay,level)
						gameDisplay.fill(white)
						gameMap=makeMapArray(level)
						boulderlist=list()
						boulder.numOfBoulders=0
						boulder.bouldersOnGoal=0
						manOb=initialiseBoard(gameMap,width,height,goalSprite,boulderlist)
						break
					
					elif event.key==pygame.K_a:
						#code for ai
						pass
					else:
						manOb.handleKeyPress()
						if(boulder.bouldersOnGoal==boulder.numOfBoulders):
							print("success")
							success=True
							break

		elif success==True:
			levelCleared(gameDisplay)

			#This sub while loop is for the Level cleared screen.
			#Level cleared screen remains as long as success=True
			while success==True:
				for event in pygame.event.get():

					if event.type==pygame.QUIT:
						stopGame=True	#exit main game loop
						success=False	#exit current level cleared screen loop
						break			#exit event capture loop

					elif event.type==pygame.KEYDOWN:
						
						if(event.key==pygame.K_r):
							success=False
							gameDisplay.fill(white)
							gameMap=makeMapArray(level)
							boulderlist=list()
							boulder.numOfBoulders=0
							boulder.bouldersOnGoal=0
							manOb=initialiseBoard(gameMap,width,height,goalSprite,boulderlist)
							print("Restarting after winning")
							break

						elif(event.key==pygame.K_l):
							success=False
							level=gameStart(gameDisplay,width*50,(height+1)*50)
							gameDisplay.fill(white)
							gameMap=makeMapArray(level)
							width=len(gameMap[0])
							height=len(gameMap)
							gameDisplay=pygame.display.set_mode((50*width,50*(height+1)))
							gameDisplay.fill(white)

							boulderlist=[]
							boulder.numOfBoulders=0
							boulder.bouldersOnGoal=0
							manOb=initialiseBoard(gameMap,width,height,goalSprite,boulderlist)
							print("in level choose",level)
							break

						elif(event.key==pygame.K_q):
							stopGame=True	#exit main game loop
							success=False	#exit current level cleared screen loop
							break			#exit event capture loop

		pygame.display.update()
		clock.tick(60)


	pygame.quit()
	quit()
