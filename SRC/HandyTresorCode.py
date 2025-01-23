# image
arrowImage:byte[16*16] = [
0,0,0,0,0,0,0,15,15,0,0,0,0,0,0,0,
0,0,0,0,0,0,15,15,15,15,0,0,0,0,0,0,
0,0,0,0,0,15,15,0,0,15,15,0,0,0,0,0,
0,0,0,0,15,15,0,0,0,0,15,15,0,0,0,0,
0,0,0,15,15,0,0,0,0,0,0,15,15,0,0,0,
0,0,15,15,0,0,0,0,0,0,0,0,15,15,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,15,15,0,0,0,0,0,0,0,0,15,15,0,0,
0,0,0,15,15,0,0,0,0,0,0,15,15,0,0,0,
0,0,0,0,15,15,0,0,0,0,15,15,0,0,0,0,
0,0,0,0,0,15,15,0,0,15,15,0,0,0,0,0,
0,0,0,0,0,0,15,15,15,15,0,0,0,0,0,0,
0,0,0,0,0,0,0,15,15,0,0,0,0,0,0,0
]
# image
startImage:byte[16*16] = [
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,15,15,15,15,15,15,15,0,0,0,0,0,
0,0,0,15,0,0,0,0,0,0,0,15,0,0,0,0,
0,0,15,0,0,0,0,0,0,0,0,0,15,0,0,0,
0,15,0,0,0,0,0,0,0,0,0,0,0,15,0,0,
0,15,0,0,0,0,15,15,15,0,0,0,0,15,0,0,
0,15,0,0,0,15,15,15,15,15,0,0,0,15,0,0,
0,15,0,0,0,15,15,15,15,15,0,0,0,15,0,0,
0,15,0,0,0,15,15,15,15,15,0,0,0,15,0,0,
0,15,0,0,0,0,15,15,15,0,0,0,0,15,0,0,
0,15,0,0,0,0,0,0,0,0,0,0,0,15,0,0,
0,0,15,0,0,0,0,0,0,0,0,0,15,0,0,0,
0,0,0,15,0,0,0,0,0,0,0,15,0,0,0,0,
0,0,0,0,15,15,15,15,15,15,15,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
]


const LOCK_MODE_EDITING = 0
const LOCK_MODE_RUNNING = 1
const ADDR_LOCK_MODE    = 32768
const ADDR_LOCK_SECS    = 32768 + 1
const SERVO_PIN = C_PIN_01      # Servo on IO01
lockMode:byte   
lockDurationSecs:int 
setPWMFrequency(50) # Servo runs on 50Hz


def unlockServo():
    writePWM(SERVO_PIN, 512)     # 512 is about +90 degrees

def lockServo():
    writePWM(SERVO_PIN, 102) 

def writeSecs():
    pauseCartridgeDetection()
    delay(10)
    byteAddrSize = getI2CByteAddrSize()
    setI2CByteAddrSize(2)
    writeI2CInt(80, ADDR_LOCK_SECS, lockDurationSecs)
    delay(5)
    setI2CByteAddrSize(byteAddrSize)
    resumeCartridgeDetection()

def writeLockMode():
    pauseCartridgeDetection()
    delay(10)
    byteAddrSize = getI2CByteAddrSize()
    setI2CByteAddrSize(2)
    writeI2CByte(80, ADDR_LOCK_MODE, lockMode)
    delay(5)
    setI2CByteAddrSize(byteAddrSize)
    resumeCartridgeDetection()

def readEEPROM():
    pauseCartridgeDetection()
    delay(10)
    byteAddrSize = getI2CByteAddrSize()
    setI2CByteAddrSize(2)
    lockMode = readI2CByte(80, ADDR_LOCK_MODE)
    delay(5)
    lockDurationSecs= readI2CInt(80, ADDR_LOCK_SECS)
    delay(5)
    setI2CByteAddrSize(byteAddrSize)
    resumeCartridgeDetection()

def init():
    lockMode = LOCK_MODE_EDITING 
    lockDurationSec = 60
    writeLockMode()
    writeSecs()

def secsToString()->byte[10]:
    buf = ""
    lockMin = 0
    lockSec = lockDurationSecs
    if lockDurationSecs >= 60:
        lockMin = lockDurationSecs / 60
        lockSec = lockDurationSecs % 60
        if lockMin < 10:
            buf = "0"
        buf = buf + lockMin + ":"
    if lockSec < 10:
        buf = buf + "0"
    buf = buf + lockSec
    return buf

def displaySetting()
    textFont(FONT_ROBOTO_24)
    drawTextCentered(120, 80, "ENTER SECS")
    textFont(FONT_ROBOTO_BOLD_48)
    drawTextCentered(120, 140, secsToString())
    fill(20,20,20)
    noStroke()
    push()
    translate(32,200)
    drawCircle(0,0,20)
    drawSpriteScaled(0, 0, 16, 16, 1, arrowImage)
    textFont(FONT_ROBOTO_16)
    drawText(24,-8,"SELECT")
    translate(110,0)
    drawCircle(0,0,20)
    drawSpriteScaled(0, 0, 16, 16, 1, startImage)
    drawText(24,-8,"START")
    stroke(255,255,255)
    pop()
    
    update()

def displayCountDown()
    textFont(FONT_ROBOTO_24)
    drawTextCentered(120, 80, "LOCKED UNTIL")
    textFont(FONT_ROBOTO_BOLD_48)
    drawTextCentered(120, 140, secsToString())
    update()
    if lockDurationSecs > 0:
        lockDurationSecs--
        writeSecs()
    else:
        lockMode = LOCK_MODE_EDITING
        writeSecs()
        writeLockMode()

    delay(1000)

def drawBorder(buf:byte[]):
    clear()
    noStroke()
    if lockMode == LOCK_MODE_RUNNING:
        fill(255,0,0)
    else:
        fill(0,255,0)
    drawRectangle(0,0,239,239)
    fill(0,0,0)
    drawRectangle(4,60,239-8,240-60-4)
    textFont(FONT_ROBOTO_BOLD_32)
    stroke(0,0,0)
    drawTextCentered(120, 30, buf)
    stroke(255,255,255)
    textFont(FONT_ROBOTO_24)


def onDraw():
    if lockMode == LOCK_MODE_RUNNING:
        drawBorder("LOCKED")
        lockServo()
        displayCountDown()
    else:
        drawBorder("OPEN")
        btn = getButtons()
        if btn.up:
            lockDurationSecs++
        if btn.down and lockDurationSecs >=10:
            lockDurationSecs--
        if btn.middle:
            lockMode = LOCK_MODE_RUNNING
            writeLockMode()
            writeSecs()
        unlockServo()
        displaySetting()
    update()
        

readEEPROM()
if lockMode > 2 or lockDurationSecs == 0:
    init()
