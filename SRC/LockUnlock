import monitor

const SERVO_PIN = C_PIN_01            # Servo on IO01
setPWMFrequency(50)                   # Servo runs on 50Hz
locked = true

def toggleState():
    if locked:
        monitor.pushc("OPEN", MONITOR_GREEN)
        writePWM(SERVO_PIN, 512)      # 512 is about +90 degrees
    else:
        monitor.pushc("LOCKED", MONITOR_RED)
        writePWM(SERVO_PIN, 102)      # 102 is about -90 degrees    
    locked = not locked

def onClick():
    toggleState()

toggleState()
