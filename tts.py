#!/usr/local/bin/python3.5
# -*- coding: utf-8 -*-
from gtts import gTTS 
import os
import sys
import subprocess

path = os.getcwd()+'/q_videos/'
img_path = os.getcwd()+'/assets/images/default_avatar.png'

def google_tts(text='', filename='default.mp4'):
	# print(filename)
	# return ''
	mytext = text.replace('_', ' ')
	
	# Language in which you want to convert 
	language = 'en-IN'
	  
	# Passing the text and language to the engine,  
	# here we have marked slow=False. Which tells  
	# the module that the converted audio should  
	# have a high speed 
	myobj = gTTS(text=mytext, lang=language, slow=False) 	
	  
	# Saving the converted audio in a mp4 file named 	
	fname = path+filename
	myobj.save(fname)
	os.system('chmod -R 777 '+fname)	
	
	#duration = os.system("ffmpeg -i "+fname+" 2>&1 | grep Duration | cut -d ' ' -f 4 | sed s/,//")
	#print("duration :"+duration)
	cmd = "ffmpeg -i "+fname+" 2>&1 | grep Duration | cut -d ' ' -f 4 | sed s/,//"
	# out = subprocess.check_output(cmd, shell=True)
	# print(out)
	process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None, shell=True)

	#Launch the shell command:
	output = process.communicate()
	duration = output[0].decode('utf-8').replace('\n', '')
	#print(duration)

	# subtitle section
	subtitle_file = filename.split('.')
	subtitle_path = os.getcwd()+"/q_videos/"+subtitle_file[0]+".srt"
	#print(subtitle_path)
	
	f = open(subtitle_path, "a")
	f.write("1\n")
	f.write("00:00:00,00 --> 00:00:08,00\n")
	f.write(mytext)
	f.close()
	
	os.system('chmod -R 777 '+subtitle_path)

	# Create combined video section
	#drawtext = "drawtext=text='"+mytext+"': fontcolor=white: fontsize=15: box=1: boxcolor=black@0.5: boxborderw=5: x=(w-text_w)/2: y=((h-text_h)/2)+150"
	drawtext = "subtitles="+subtitle_path+":force_style='Fontname=Arial,Fontsize=10,PrimaryColour=&Hffffff,SecondaryColour=&Hffffff,OutlineColour=&H44000000,BackColour=&H0,BorderStyle=3,Shadow=0,MarginV=60'"
	command = 'ffmpeg -y -loop 1 -framerate 15 -i '+img_path+' -i '+fname+' -c:v libx264 -filter_complex "'+drawtext+'" -c:a aac -shortest -strict -2 -t '+duration+' '+fname
	print(command)
	os.system(command)

	# delete subtitle file
	os.system('rm -f '+subtitle_path)
	
if __name__ == '__main__':
	#n = len(sys.argv)
	#print(sys.argv)		
	google_tts(text=sys.argv[1], filename=sys.argv[2])