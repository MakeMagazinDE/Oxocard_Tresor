import monitor

const SERVO_PIN = C_PIN_01   # Servo on IO01
monitor.push("Initialize")
setPWMFrequency(50) # Servo runs on 50Hz
writePWM(SERVO_PIN, 102)     # 102 is about -90 degrees
delay(1000) 
writePWM(SERVO_PIN, 512)     # lock is open: 512 is about +90 degrees
monitor.pushc("Servo prepared", MONITOR_GREEN)
