from glob import glob
import subprocess
from time import sleep
import RPi.GPIO as GPIO
from subprocess import Popen, PIPE
import os,sys

GPIO.setmode(GPIO.BOARD) #may need to change to GPIO.BCM

button1 = 12    #play/pause
button2 = 16    #stop
button3 = 18    #next
button4 = 22    #previous       
    

GPIO.setup(button1,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button2,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button3,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button4,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

#NEED TO SET UP BUTTON


class PiPlayer(object):
    def __init__(self, music_path): #adds each file location of the song to a list
            self.music_list = [
                    '{file}'.format(file=file)
                    for file in glob('{path}/*mp3'.format(path=music_path))]        #get music list from 
         
            self.current_song = 0 #to figure out which postion were gonna play from
            self.player = None

    def play_song(self, song):
            self.player = subprocess.Popen(["omxplayer", song], stdin=subprocess.PIPE)
            
    def pause_song(self):
            if self.player.poll():  #is track playing. 
                    pass
            else:                   #yes, input 'p' to pause
                    self.player.stdin.write("p")

    def stop_song(self):
            if self.player.poll():  #is track playing? if yes, print "q" to terminate
                    pass
            else:
                    self.player.stdin.write("q")

    def next_song(self):
            print len(self.music_list)
            print "song position before clicking next" + self.current_song
            if self.current_song >= len(self.music_list) - 1:       #if current place in set is 
                    self.current_song = 0                           #
            #May need to insert this to go to next song             
            #elif (self.current_song < len(self.music_list):
                  #self.current_song = self.current_song + 1
            self.stop_song()                                        #send "q"
            print "about to next song which is position" + self.current_song
            self.play_song(self.music_list[self.current_song])      #and play song 
            
            
    def previous_song(self):
            print "in previous song"
            if self.current_song <= 0:
                    self.current_song = len(self.music_list) -1
            #elif self.current_song > 0:
                    # self.current_song = self.current_song - 1
            self.stop_song()
            self.play_song(self.music_list[self.current_song])

    

    def main(self):
            print "in main" 
            self.play_song(self.music_list[self.current_song])
            try:
                    pass    #while True:
                           # while not self.player.poll():   #when song not playing
                                   # self.pin_handler()
                                    #sleep(0.5)
                                    #self.next_song()        #play next song
            except KeyboardInterrupt:
                    pass

if __name__ == '__main__':
        print"HERE WE GO"
        pp = PiPlayer('/media/pi/E09A-39FE/pimusic')
        pp.main()

while (True):
    if (GPIO.input(button1)== GPIO.HIGH):
            print"pause/play"
            pp.pause_song()
            sleep(0.5)
    if (GPIO.input(button2)==GPIO.HIGH):
            print"stop"
            pp.stop_song()
            sleep(0.5)
    if (GPIO.input(button3)==GPIO.HIGH):
            print"next"
            pp.next_song()
            sleep(0.5)
    elif (GPIO.input(button4)==GPIO.HIGH):
            print"previous"
            pp.previous_song()
            sleep(0.5)
