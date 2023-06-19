import json
import cv2
import time

whitecolor = "#ffffff"
blackcolor = "#000000"


template = {'nodes':[], 'edges':[]}

#print(json.loads(f))

#100x75
#52x39

def convertxy(x,y,width):
    return x + (width*y)

## INIT FUNCTION
def initCanvas(width, height):
    pixwidth = 50
    pixheight = 50
    pixelID = 0
    x = 0
    y = 0
    currcolor = blackcolor

    nodetemp = {'id': '', 'x': x, 'y': y, 'width': pixwidth, 'height': pixheight, 'type': 'text', 'color': ''}

    f = open("./Apple Vault/testing/apples.canvas",'w')

    for i in range(height):
        for j in range(width):
            newnode = dict(nodetemp)

            newnode['id'] = str(pixelID)
            #newnode['id'] = str(random.randint(0,1500))
            pixelID = pixelID+1

            newnode['x'] = x
            newnode['y'] = y
            x = x + pixheight

            newnode['color'] = currcolor
            if(currcolor == blackcolor):
                currcolor = whitecolor
            else:
                currcolor = blackcolor
            template['nodes'].append(newnode)

        y = y + pixwidth
        x = 0
    f.write(json.dumps(template))
    f.close()
## INIT FUNCTION

def drawFrame(cap, currframe):
    f = open("./Apple Vault/testing/apples.canvas","r+")
    frameOut = json.loads(f.read())

    cap.set(cv2.CAP_PROP_POS_FRAMES, currframe)
    res, frame = cap.read()
    height, width, channels = frame.shape
    #Accessing BGR pixel values    
    for x in range(0, height):
        for y in range(0, width):
            #print (str(frame[x,y,2])+","+str(frame[x,y,1])+","+str(frame[x,y,0]))#R Channel Value
            i = convertxy(y,x,width)
            #print("accessing pixel: {}".format(i))
            if(frame[x,y,2] > 100):
                frameOut['nodes'][i]['color'] = whitecolor
            else:
                frameOut['nodes'][i]['color'] = blackcolor
            #print (frame[x,y,1]) #G Channel Value
            #print (frame[x,y,0]) #B Channel Value
    f.seek(0)
    f.write(json.dumps(frameOut))
    f.truncate()
    f.close()

def clearframe():
    f = open("./Apple Vault/testing/apples.canvas","r+")
    frames = json.loads(f.read())
    for i in range(len(frames)):
        frames['nodes'][i]['color'] = blackcolor
    f.seek(0)
    f.write(json.dumps(frames))
    f.truncate()
    f.close()

#initCanvas(100,75)
cap = cv2.VideoCapture("ba-100.mp4")
totalFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

for frame in range(0,totalFrames-1):
    print("Drawing frame: {}/{}".format(frame,totalFrames-1))
    drawFrame(cap, frame)
    #quit()
    time.sleep(3)
cap.release()