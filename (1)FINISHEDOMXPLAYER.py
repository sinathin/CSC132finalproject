#################################################################################################################################
# Group Member's Name: Sydney A, Garret S, Ankit A
# Date: 11/09/2018
# #description: An MP3 Player that takes music files (.mp3) from a USB drive and is able to play the sound using OMX
# and thus we can maunally show images and song information
###############################################################################################################################
from glob import glob #The glob module finds all the pathnames matching a specified pattern
import subprocess #The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes.
from time import *
import RPi.GPIO as GPIO #Imports the board
from subprocess import Popen, PIPE
import os,sys #The functions that the OS module provides allows you to interface with the underlying operating system that Python is running on
from Tkinter import *
import tkFont #to set the font
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

button1 = 12    #play/pause
button2 = 16    #stop
button3 = 18    #next
button4 = 22    #previous
led = 20 #for LED

#TO STOP SONG IN TESTING TYPE INTO TERMINAL killall omxplayer.bin

#To Set up the Buttons and LED    
GPIO.setup(button1,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button2,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button3,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button4,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(led, GPIO.OUT)
GPIO.output(led, GPIO.LOW)

#############################################################

class PiPlayer(object):
    def __init__(self, music_path): #adds each file location of the song to a list
            self.music_list = [
                    '{file}'.format(file=file)
                    for file in glob('{path}/*mp3'.format(path=music_path))]        #get music list from 
         
            self.current_song = 0 #to figure out which postion were gonna play from
            self.player = None
            self.position = 0 #gets the position of where to pick from
            #a chronological list of the artists name
            self.artistname = ["Kendrick Lamar ft. SZA", "Outkast", "Post Malone", "Rick Astley", "Kanye West", "Plain White T's", "Kanye West", "Beyonce", "Journey"]
            #creates a list with song name
            self.songname = ["All the Stars", "Hey Ya!", "Rockstar", "Never Gonna Give You Up", "Gold Digger", "Hey The Delilah", "Stronger", "Single Ladies", "Don't Stop Believin'"]
            #a list that hold the albumpics #change into exact location
            self.albumimage = ["/media/pi/E09A-39FE/AlbumCovers/allthestars.gif", "/media/pi/E09A-39FE/AlbumCovers/heyya.gif", "/media/pi/E09A-39FE/AlbumCovers/Rockstar.gif" , "/media/pi/E09A-39FE/AlbumCovers/nevergonnagive.gif", "/media/pi/E09A-39FE/AlbumCovers/golddigger.gif", "/media/pi/E09A-39FE/AlbumCovers/heytheredelilah.gif", "/media/pi/E09A-39FE/AlbumCovers/stronger.gif", "/media/pi/E09A-39FE/AlbumCovers/singleladies.gif", "/media/pi/E09A-39FE/AlbumCovers/dontstopbe.gif"]
            #calls the class that makes the frame
            self.FRAME_MAKE()
     
            #self.position = 0 #this tells you the position that you are in the list of songs
    def FRAME_MAKE(self):
        global piclabel #this will allow uss to change the pic as we manuever thru diifferent classes
        global textlabel #able to change the text as its called
        root.geometry("500x500")
        root.title("Music Player") #NAME OF THE FRAME
        root.configure(background="white") #background of the frame

        self.frame = Frame(width=500, height=300,bg="white")

        self.frame.pack_propagate(False) #adding line solves problem #MAY NEED TO CHANGE TO FALSE
        self.frame.pack()

        self.img = PhotoImage(file = self.albumimage[0]) #SETS THE FIRST IMAGE AS THE FIRST SONG
        piclabel=Label(self.frame, image=self.img, bg = "white")
        piclabel.image = self.img #actually sets the image
        piclabel.pack(side = TOP, fill = BOTH)
    #################FOR THE TEXT FRAME###################
        
        self.frame2 = Frame(width=500, height=200, bg="white")

        self.frame2.pack_propagate(False) #adding line solves problem
        self.frame2.pack()
        self.info = info = "Name: " + self.songname[0] + "\n Artist:" + self.artistname[0]
        textlabel=Label(self.frame2, text= self.info, bg = "white")
        textlabel.config(font=("Courier", 18))
        textlabel.pack(side = TOP)
        root.after(200, work_buttons)
        
#########################################################################       
    def play_song(self, song): #To plat the songs
            self.player = subprocess.Popen(["omxplayer", song], stdin=subprocess.PIPE)
            GPIO.output(led, GPIO.HIGH)

    def pause_song(self): #to pause the songs
            if self.player.poll():  #is track playing. 
                    pass
            else:                   #yes, input 'p' to pause
                    self.player.stdin.write("p")
                    if (GPIO.input(led) == 1):
                        GPIO.output(led, GPIO.LOW)
                    else:
                        GPIO.output(led, GPIO.HIGH)
                        
    def stop_song(self):
            if self.player.poll():  #is track playing? if yes, print "q" to terminate
                    pass
            else:
                    self.player.stdin.write("q")
                    GPIO.output(led, GPIO.LOW)

    def next_song(self):
            global piclabel
            global textlabel
            if (self.current_song >= len(self.music_list) - 1):
                #if current place in set is at the end of the list, it will go back to the start
                    self.current_song = 0
                    self.position = 0
            elif (self.current_song < len(self.music_list)):
                    self.current_song = self.current_song + 1
                    self.position = self.position +1

            self.stop_song()                                        #send "q"  
           
           #FOR IMAGE CHANGE:
            newimg = PhotoImage(file = self.albumimage[self.position])
            piclabel.configure(image =  newimg)
            piclabel.image = newimg
            #FOR TEXT CHANGE:
            newtext = "Name: " + self.songname[self.position] + "\n Artist:" + self.artistname[self.position]
            textlabel['text'] = newtext

            self.play_song(self.music_list[self.current_song])      #and play song 
            
    def previous_song(self):
            global piclabel
            global textlabel
            if self.current_song <= 0:
                    self.current_song = len(self.music_list) -1
                    self.position = len(self.music_list) -1
            elif self.current_song > 0:
                    self.current_song = self.current_song - 1
                    self.position = self.position - 1
            self.stop_song()
            
            #FOR IMAGE CHANGE:
            newimg = PhotoImage(file = self.albumimage[self.position])
            piclabel.configure(image =  newimg)
            piclabel.image = newimg
            #FOR TEXT CHANGE:
            newtext = "Name: " + self.songname[self.position] + "\n Artist:" + self.artistname[self.position]
            textlabel['text'] = newtext
            self.play_song(self.music_list[self.current_song])


    def main(self):
            self.play_song(self.music_list[self.current_song])
            
            try: #try and except to catch an exception
                    pass    
                           
            except KeyboardInterrupt:
                    pass

################## TO BUILD THE WINDOW & make buttons work 


def work_buttons(): #checks to see if the button is pushed (GPIO.HIGH)
    if (GPIO.input(button1)== GPIO.HIGH):
            pp.pause_song()
            sleep(0.5)
    if (GPIO.input(button2)==GPIO.HIGH):
            pp.stop_song()
            sleep(0.5)
    if (GPIO.input(button3)==GPIO.HIGH):
            pp.next_song()
            sleep(0.5)
    elif (GPIO.input(button4)==GPIO.HIGH):
            pp.previous_song()
            sleep(0.5)
            
    root.after(20, work_buttons) #root.after allwos us to continuelly check the buttons (TIME (milliseconds), function to run)



root= Tk() #creates TK class
if __name__ == '__main__': #Calls the PiPlayer Object
            pp = PiPlayer('/media/pi/E09A-39FE/pimusic') #creates the Piplayer Object
            pp.main()
            

root.mainloop() #can only be called once and is basically a continous loop tht runs to keep the window open










