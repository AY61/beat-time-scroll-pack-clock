import network, utime, socket
from picoscroll import PicoScroll

#Constants

sh = PicoScroll()

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('SSID', 'Password') #Wifi Settings

blink = 0

offset = [4, 7, 10]

brightness = 64

timezone = 0 #0 is GMT, change to fit your region

max_wait = 15
while max_wait > 0:
    if wlan.isconnected():
        break
    max_wait -= 1
    print('Waiting for Wi‑Fi...')
    #time.wait(1)

if wlan.isconnected():
    print('Wi‑Fi connected, IP:', wlan.ifconfig()[0])

def get_beat_time():

    hour = utime.localtime()[3] + (1 + timezone)
    minute = utime.localtime()[4]
    second = utime.localtime()[5]
    microsecond = 0

    total_seconds = (hour*3600) + (minute*60) + second + (microsecond/1000000)
    beats = round(total_seconds / 86.4, 2)
    beats_string = None
    
    if beats < 10:
        beats_string = "@00" + str(beats)
    elif beats < 100:
        beats_string = "@0" + str(beats)
    else:
        beats_string = "@" + str(beats)

    if len(beats_string) < 7:
        if len(beats_string) < 6:
            beats_string = beats_string + ".00"
        else:
            beats_string = beats_string + "0"

    return beats_string

def vert_line(start_x, start_y, length): #Line always goes top to bottom
    for i in range(length):
        sh.set_pixel(start_x, start_y+i, brightness)

def show_at():
    vert_line(0, 1, 5)
    vert_line(2, 1, 2)
    sh.set_pixel(1, 0, brightness)
    sh.set_pixel(1, 3, brightness)
    sh.set_pixel(1, 6, brightness)
    sh.set_pixel(2, 5, brightness)

def draw_numbers(beat_time):
    
    #first 3 digits
    for i in range(3):
        if beat_time[i+1] == "0":
            vert_line(offset[i], 0, 7)
            vert_line(offset[i]+1, 0, 7)
        elif beat_time[i+1] == "1":
            sh.set_pixel(offset[i], 1, brightness)
            vert_line(offset[i]+1, 0, 7)
        elif beat_time[i+1] == "2":
            vert_line(offset[i], 0, 4)
            vert_line(offset[i]+1, 3, 4)
            sh.set_pixel(offset[i], 0, brightness)
            sh.set_pixel(offset[i]+1, 6, brightness)
        elif beat_time[i+1] == "3":
            vert_line(offset[i]+1, 0, 7)
            sh.set_pixel(offset[i], 0, brightness)
            sh.set_pixel(offset[i], 3, brightness)
            sh.set_pixel(offset[i], 6, brightness)
        elif beat_time[i+1] == "4":
            vert_line(offset[i], 0, 4)
            vert_line(offset[i]+1, 3, 4)
        elif beat_time[i+1] == "5":
            vert_line(offset[i]+1, 3, 4)
            vert_line(offset[i], 0, 4)
            sh.set_pixel(offset[i]+1, 0, brightness)
            sh.set_pixel(offset[i], 6, brightness)
        elif beat_time[i+1] == "6":
            vert_line(offset[i], 0, 7)
            vert_line(offset[i]+1, 3, 4)
        elif beat_time[i+1] == "7":
            sh.set_pixel(offset[i], 0, brightness)
            vert_line(offset[i]+1, 0, 7)
        elif beat_time[i+1] == "8":
            vert_line(offset[i], 0, 3)
            vert_line(offset[i], 4, 3)
            vert_line(offset[i]+1, 0, 7)
        elif beat_time[i+1] == "9":
            vert_line(offset[i], 0, 3)
            vert_line(offset[i]+1, 0, 7)
    
    #after point number
    if beat_time[5] == "0":
        vert_line(15, 0, 7)
        vert_line(16, 0, 7)
    elif beat_time[5] == "1":
        sh.set_pixel(15, 1, brightness)
        vert_line(16, 0, 7)
    elif beat_time[5] == "2":
        vert_line(16, 0, 4)
        vert_line(15, 3, 4)
        sh.set_pixel(15, 0, brightness)
        sh.set_pixel(16, 6, brightness)
    elif beat_time[5] == "3":
        vert_line(16, 0, 7)
        sh.set_pixel(15, 0, brightness)
        sh.set_pixel(15, 3, brightness)
        sh.set_pixel(15, 6, brightness)
    elif beat_time[5] == "4":
        vert_line(15, 0, 4)
        vert_line(16, 3, 4)
    elif beat_time[5] == "5":
        vert_line(16, 3, 4)
        vert_line(15, 0, 4)
        sh.set_pixel(16, 0, brightness)
        sh.set_pixel(15, 6, brightness)
    elif beat_time[5] == "6":
        vert_line(15, 0, 7)
        vert_line(16, 3, 4)
    elif beat_time[5] == "7":
        sh.set_pixel(15, 0, brightness)
        vert_line(16, 0, 7)
    elif beat_time[5] == "8":
        vert_line(15, 0, 3)
        vert_line(15, 4, 3)
        vert_line(16, 0, 7)
    elif beat_time[5] == "9":
        vert_line(15, 0, 3)
        vert_line(16, 0, 7)
    return
        
while True:
    
    sh.clear()
    
    if blink == 0:
        blink = 1
        sh.set_pixel(13, 6, brightness)
    else:
        blink = 0
        sh.set_pixel(13, 6, 0)
        print(beat_time)

    if sh.is_pressed(sh.BUTTON_X):
        if brightness <= 124:
            brightness += 10
        else:
            brightness = 124
            
    if sh.is_pressed(sh.BUTTON_Y):
        if brightness >= 4:
            brightness -= 10
        else:
            brightness = 4
    
    if sh.is_pressed(sh.BUTTON_B):
        sh.scroll_text("Made by AY61", brightness, 30)
        sh.clear()

    beat_time = get_beat_time()
    
    draw_numbers(beat_time)
    
    show_at()
    sh.show()
    utime.sleep(0.56)