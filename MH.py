import requests,re, time, pygame
import sys
raspi = True
led = 4
if(raspi):
    import RPi.GPIO as pi
    pi.setmode(pi.BCM)
    pi.setwarnings(False)
    pi.setup(led, pi.OUT)
    pi.output(led,0)

pygame.mixer.init()
pygame.mixer.music.load("clapping.wav")

url="http://bossan.musikhjalpen.se/insamling/sektionerna-lith-nkpg"

def main(argv=None):
    print str(argv[0])
    currentValue = int(argv[0])
    while(True):
        data = requests.get(url)
        for line in data.text.split('\n'):
            if "large-text" in line:
                number = re.search('\d{1,9}', line)
		number = int(number.group(0))
                if(number > currentValue):
		    diff = number-currentValue	
                    print 'New value!'
		    print diff
                    blink(diff)
                    currentValue = number
                else:
                    print 'No new value!'
        time.sleep(30)
    if raspi:
        pi.cleanup()
def blink(diff):
    print 'blink'
    diff = int(diff/5)
    pygame.mixer.music.play()
    if raspi:
        pi.output(led, 1)
        time.sleep(diff)
        pi.output(led, 0)


if __name__ == "__main__":
    main(sys.argv[1:])

