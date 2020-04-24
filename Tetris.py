#Made by: Kouah Mohammed Aymen
#Computer science student at "National Computer science Engineering School, Algiers (ESI)"
#E-mail: jm_kouah@esi.dz
#Github: https://github.com/aymenkouah
#Requires installing "pygame" 
#https:\\pygame.org

import pygame
import time
import random

#initializing the game(pygame)
pygame.init()

#initializing the mixer(for music)
pygame.mixer.init()

#Background music
pygame.mixer.music.load("Undertale-Megalovania.mp3")
pygame.mixer.music.play(loops=-1)


#initialising the screen
screen_dim = [ 800 , 800 ] #both must be multiples of 50 for the game to work
screen = pygame.display.set_mode( (screen_dim[0] , screen_dim[1] ) )




#variables:
running = True #allows the game to keep running
color = (255 , 0 , 0) #the color of the shapes' units
clock = pygame.time.Clock() #setting up a clock to control the game speed
rate = 10 #the fps of the game (clock)
r_count = 0 #Used in rotation of shapesd(decides which form the shape is going to take next)


unit = [ 50 , 50 ] #the dimensions of the unit composing the shapes
shapes = [ "square" , "L" , "line" , "Z" , "T" ] #list containing possible dropped shapes
dropped = [] #list containing already dropped shapes
current_shape = [ ] #list containing all the units' coordinates to draw the shape currently being dropped
shape_name = [] #the name of the shape currently dropping

scored = [0] #the score


#functions:

#creates current_shape
def create_shape(shapes , current_shape , shape_name):
    if current_shape==[] :
        shape_name = [ shapes[random.randint(0, 4)] ]

        if shape_name[0]=="square" :
            current_shape = [ [ 300, -50] , [ 350, -50] , [300 , -100] , [350, -100] ]
        elif shape_name[0]== "L":
            current_shape =  [  [ 350, -50] , [350, -150] , [300, -50] ,  [350 , -100] ]  
        elif shape_name[0]== "line":
            current_shape =  [  [ 300, -50] , [ 300, -100] , [300 , -150] , [300, -200] ] 
        elif shape_name[0]== "Z":
            current_shape =  [ [ 350, -50] , [ 300, -50] ,  [350 , -100] , [400, -100] ]   
        elif shape_name[0]== "T":
            current_shape =  [ [300, -100] , [ 250, -50] , [ 300, -50] , [350 , -50]   ]  
    
    return [ current_shape , shape_name ]


#draws the current shape and the dropped shapes
def draw_shapes(shape , color , dropped):
   
    for i in range(0,len(shape)) :
        pygame.draw.rect( screen , color, ( shape[i][0], shape[i][1] , unit[0], unit[1] ) )
        pygame.draw.rect( screen , ( 0 , 0 , 0 ), ( shape[i][0], shape[i][1] , unit[0], unit[1] ) , 2)

    for i in range(0,len(dropped)) :
        pygame.draw.rect( screen , color, ( dropped[i][0], dropped[i][1] , unit[0], unit[1] ) )
        pygame.draw.rect( screen , (0 , 0 , 0), ( dropped[i][0], dropped[i][1] , unit[0], unit[1] ) , 2)



#moves the current shape
def move_shape(shape , color , direction):
    move = True
    for i in range(0 ,len(shape) ) :
        shape[i][1] += direction[1]
        if (shape[i][0]==0 and direction[0]<0) or (shape[i][0]==screen_dim[0]-50 and direction[0]>0) :
            move = False
        else:
            for k in range(0 , len(dropped) ):
                if shape[i][1]+50>=dropped[k][1] and shape[i][1]+50<=dropped[k][1]+50  and shape[i][0]==dropped[k][0]-50 and direction[0]>0:
                    move = False
                elif shape[i][1]+50>=dropped[k][1] and shape[i][1]+50<=dropped[k][1]+50 and shape[i][0]==dropped[k][0]+50 and direction[0]<0:
                    move = False

    if move:
        for i in range(0 ,len(shape) ) :
            shape[i][0] += direction[0]
            

            
#adds and removes elements from dropped list (manages the dropped list)
def drop(shape , dropped):
    add_to_dropped = False
    for i in range(0, len(shape)):
        if shape[i][1] == screen_dim[1]-50 : 
            add_to_dropped = True    
        else:
            for k in range(0 , len(dropped) ):
                if shape[i][0] == dropped[k][0]:
                    if shape[i][1]+50 == dropped[k][1]:
                        add_to_dropped = True

    if add_to_dropped == True :
        for i in range(0, len(shape)):
            dropped.append( shape[i] )
        shape = []
    
    return shape


#rotate the shapes
#-----each shape has a list of possible forms which it can take
def rotate_shape(current_shape , rotate , shape_name, r_count):

    if shape_name[0] == "line" and rotate>0 :       
        base = current_shape[0]
        formsline =[ 
            [ base , [base[0] , base[1] +50 ] , [base[0] , base[1] + 100 ], [base[0] , base[1]-50 ] ] ,
            [ base , [base[0] + 50 , base[1] ] , [base[0] + 100 , base[1] ], [base[0] - 50 , base[1]  ] ]    
        ]
        current_shape = formsline[ r_count%2 ]

    elif shape_name[0] == "L" and rotate>0 :
 
        base = current_shape[0]
        formsL =[ 
            [ base , [base[0] -50 , base[1] ] , [base[0] , base[1] -50 ], [base[0] , base[1]-100 ] ] ,
            [ base , [base[0] , base[1] -50 ] , [base[0] + 50 , base[1] ], [base[0]+100  , base[1]  ] ],
            [ base , [base[0] +50 , base[1] ] , [base[0]  , base[1] +50 ], [base[0]  , base[1] +100  ] ],
            [ base , [base[0] , base[1] +50 ] , [base[0]-50  , base[1] ], [base[0]-100  , base[1]  ] ]     
        ]
        current_shape = formsL[ r_count%4 ]
    
    elif shape_name[0] == "T" and rotate>0 :
        #shapes possible forms
        #line
        base = current_shape[0]
        formsT =[ 
            [ base , [base[0] -50 , base[1] +50 ] , [base[0] , base[1] +50 ], [base[0] +50 , base[1]+50 ] ] ,
            [ base , [base[0] -50 , base[1] ] , [base[0] - 50 , base[1] -50 ], [base[0] -50  , base[1] +50  ] ],
            [ base , [base[0] +50 , base[1] -50 ] , [base[0]  , base[1] -50 ], [base[0] -50  , base[1] -50  ] ],
            [ base , [base[0]  +50 , base[1] ] , [base[0] +50  , base[1] -50 ], [base[0]+50  , base[1] +50 ] ]     
        ]
        current_shape = formsT[ r_count%4 ]
    
    elif shape_name[0] == "Z" and rotate>0 :
        #shapes possible forms
        #line
        base = current_shape[0]
        formsZ =[ 
            [ base , [base[0] -50 , base[1]] , [base[0] , base[1] - 50 ], [base[0] +50 , base[1]-50 ] ] ,
            [ base , [base[0]  , base[1] -50 ] , [base[0] +50 , base[1] ], [base[0] + 50  , base[1] +50  ] ],
            [ base , [base[0] +50 , base[1] ] , [base[0]  , base[1] +50 ], [base[0] -50  , base[1] +50  ] ],
            [ base , [base[0]   , base[1] +50 ] , [base[0] -50  , base[1] ], [base[0]-50  , base[1] -50 ] ]     
        ]
        current_shape = formsZ[ r_count%4 ]

    return current_shape
        
#draws the grid on the backround
def grid(screen_dim):
    i = screen_dim[0]//50
    k = screen_dim[1]//50
    for m in range(0 , i):
        for n in range(0 , k):
            pygame.draw.rect(screen, (255 , 255 , 255 ), (m*50 , n*50 , 50 , 50) , 1)


#decides if the game is over or not(if the player lost or not)
def game_over(dropped):
    for i in range(0, len(dropped)):
        if dropped[i][1]<=0:
            return True
    return False

    
#calculates the score and removes full lines from dropped(lines tha go from edge to edge of the screen )
def score(dropped , scored):
    k = screen_dim[1]//50
    i = screen_dim[0]//50
    m=0
    compare =[]
    while m < k:
        exist=True
        n = -1
        while n<(i-1) and exist==True:
            n += 1
            compare = [ n*50 , m*50 ]
            exist =False
            for d in range( 0 , len(dropped) ):    
                if compare[0]==dropped[d][0] and compare[1]==dropped[d][1]:
                    exist = True

        if exist:
            scored[0] += 1
            
            for s in range(0, i):
                dropped.remove( [ s*50 , m*50] )
            for s in range(0 , len(dropped) ):
                if dropped[s][1] < m*50 :
                    dropped[s][1] += 50 
        else :
            m += 1 

    return dropped






i=0 #used to control the speed of the shapes' movement

#main while loop which allows the game window to keep appearing
while running == True :

    running = not game_over(dropped)
    
    screen.fill((255, 5 , 125))
    
    rotate = 0
    
    direction = [0 , 0]

    #decides the speed of the shapes' movement
    #########################
    i += 1      
    if i == 5:
        i = 0

    if i == 0:
        direction = [ 0, 50 ]
    #########################


    #the for loop used to catch inputs (clicks and types)
    for event in pygame.event.get():
        #setting up an exit method       
        if event.type == pygame.QUIT:
            running = False
        
        #verifying if a button is clicked:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction[0] = 50
            elif event.key == pygame.K_LEFT:
                direction[0] = -50

            elif event.key == pygame.K_DOWN:
                rate = 70

            if event.key == pygame.K_d:
                rotate = 1
                r_count += 1

            if event.key == pygame.K_s:
                rotate = 1
                r_count -= 1
        else:
                rate = 10
            
                
    grid(screen_dim)
    current_shape = drop(current_shape , dropped)
    dropped = score(dropped , scored)
    total = create_shape(shapes , current_shape , shape_name )
    current_shape = total[0]
    shape_name = total[1]
    move_shape(current_shape , color , direction)
    current_shape = rotate_shape(current_shape, rotate , shape_name , r_count)
    draw_shapes( current_shape , color , dropped)
    
    clock.tick(rate)

    #update the screen to see changes
    pygame.display.update()
    

print(f"Your score is{scored}")