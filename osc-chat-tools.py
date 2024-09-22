import os
import time
import threading
from threading import Thread, Lock
import ast
import requests
from collections import defaultdict
import ctypes
import json
import PySimpleGUI as sg
import argparse
from datetime import datetime, timezone
from pythonosc import udp_client
import keyboard
import asyncio
import psutil
import webbrowser
from winsdk.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager
import winsdk.windows.media.control as wmc
from websocket import create_connection # websocket-client
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import socket
import pyperclip
from flask import Flask, request
from werkzeug.serving import make_server
import hashlib
import base64
from pynvml import *
from tendo import singleton
import whisper
import torch
import speech_recognition as sr
import numpy as np
from datetime import datetime, timedelta
from queue import Queue
import pyaudio

# importantest variables :)

run = True
playMsg = True
version = "1.6.0"

# depreciated variables

depreciated_topTextToggle = False #Deprecated, only in use for converting old save files
depreciated_topTimeToggle = False #Deprecated, only in use for converting old save files
depreciated_topSongToggle = False #Deprecated, only in use for converting old save files
depreciated_topCPUToggle = False #Deprecated, only in use for converting old save files
depreciated_topRAMToggle = False #Deprecated, only in use for converting old save files
depreciated_topNoneToggle = True #Deprecated, only in use for converting old save files
depreciated_bottomTextToggle = False #Deprecated, only in use for converting old save files
depreciated_bottomTimeToggle = False #Deprecated, only in use for converting old save files
depreciated_bottomSongToggle = False #Deprecated, only in use for converting old save files
depreciated_bottomCPUToggle = False #Deprecated, only in use for converting old save files
depreciated_bottomRAMToggle = False #Deprecated, only in use for converting old save files
depreciated_bottomNoneToggle = True #Deprecated, only in use for converting old save files
depreciated_hideMiddle = False #Deprecated, only in use for converting old save files
depreciated_topHRToggle = False #Deprecated, only in use for converting old save files
depreciated_bottomHRToggle = False #Deprecated, only in use for converting old save files

# conf variables

conf_message_delay = 1.5 # in conf
conf_messageString = '' #in conf
conf_FileToRead = '' #in conf
conf_scrollText = False #in conf
scrollTexTSpeed = 6
conf_hideSong = False #in conf
conf_hideOutside = True #in conf
conf_showPaused = True #in conf
conf_songDisplay = ' 🎵\'{title}\' ᵇʸ {artist}🎶' #in conf
conf_showOnChange = False #in conf
conf_songChangeTicks = 1 #in conf
conf_minimizeOnStart = False #in conf
conf_keybind_run = '`' #in conf
conf_keybind_afk = 'end' #in conf
conf_topBar = '╔═════════════╗' #in conf
conf_middleBar = '╠═════════════╣' #in conf
conf_bottomBar = '╚═════════════╝' #in conf
conf_avatarHR = False #in conf
conf_blinkOverride = False #in conf
conf_blinkSpeed  = .5 #in conf
conf_useAfkKeybind = False #in conf
conf_toggleBeat = True #in conf
conf_updatePrompt = True #in conf
outOfDate = False
conf_confVersion = '' #in conf
conf_oscListenAddress = '127.0.0.1' #in conf
conf_oscListenPort = '9001' #in conf
conf_oscSendAddress = '127.0.0.1' #in conf
conf_oscSendPort = '9000' #in conf
conf_oscForewordAddress = '127.0.0.1' #in conf
conf_oscForewordPort = '9002' #in conf
conf_oscListen = False #in conf
conf_oscForeword = False #in conf
conf_logOutput = False  #in conf
conf_layoutString = '' #in conf
conf_verticalDivider = "〣" #in conf
conf_cpuDisplay = 'ᴄᴘᴜ: {cpu_percent}%'#in conf
conf_ramDisplay = 'ʀᴀᴍ: {ram_percent}%  ({ram_used}/{ram_total})'#in conf
conf_gpuDisplay = 'ɢᴘᴜ: {gpu_percent}%'#in conf
conf_hrDisplay = '💓 {hr}'#in conf
conf_sttDisplay = 'STT: \'{stt}\''#in conf
conf_playTimeDisplay = '⏳{hours}:{remainder_minutes}'#in conf
conf_mutedDisplay = 'Muted 🔇'#in conf
conf_unmutedDisplay = '🔊'#in conf
conf_darkMode = True #in conf
sendBlank = True
suppressDuplicates = False
sendASAP = False
useMediaManager = True
useSpotifyApi = False
spotifySongDisplay =  '🎵\'{title}\' ᵇʸ {artist}🎶 『{song_progress}/{song_length}』'
spotifyAccessToken = ''
spotifyRefreshToken = ''
spotify_client_id = '915e1de141b3408eb430d25d0d39b380'
pulsoidToken = '' 
usePulsoid = True
useHypeRate = False
hypeRateKey = 'FIrXkWWlf57iHjMu0x3lEMNst8IDIzwUA2UD6lmSxL4BqBUTYw8LCwQlM2n5U8RU' # <- my personal token that may or may not be working depending on how the hyperate gods are feeling today
hypeRateSessionId = ''
whisperModel = 'base.en'
micDevice = 'Default'
sttOutput = ['']
timeDisplayAM = "{hour}:{minute} AM"
timeDisplayPM = "{hour}:{minute} PM"
showSongInfo = True
useTimeParameters = False

########### Program Variables (not in conf) ######### 

code_verifier = '' # for manual code entry
layoutStorage = ''
layoutUpdate = '' # making sure the code for updating the layout editor only run when needed as opposed to every .1 seconds!
output = ''
textParseIterator = 0
msgOutput = ''
afk = False
songName = ''
tickCount = 2
hrConnected = False
heartRate = 0
windowAccess = None
playTime = 0
oscForewordPortMemory = ''
oscForewordAddressMemory = ''
runForewordServer = False
oscListenPortMemory = ''
oscListenAddressMemory = ''
isListenServerRunning = False
listenServer = None
useForewordMemory = False
isAfk = False
isVR = False # Never used as the game never actually updates vrmode (well, it does *sometimes*)
isMute = False
isInSeat = False
voiceVolume = 0
isUsingEarmuffs = False
isBooped= False
isPat = False
vrcPID = None
playTimeDat = time.mktime(time.localtime(psutil.Process(vrcPID).create_time()))
lastSent = ''
sentTime = 0
sendSkipped = False
spotifyAuthCode = None # <- only needed for the spotify linking process (temp var)
spotify_redirect_uri = 'http://localhost:8000/callback'
spotifyLinkStatus = 'Unlinked'
cancelLink = False
spotifyPlayState = ''
pulsoidLastUsed = True
hypeRateLastUsed = False
textStorage = ""
cpu_percent = 0
spotifySongUrl = 'https://spotify.com'
nameToReturn = ''

# check to see if code is already running
try:
    me = singleton.SingleInstance() # also me (who's single)
except:
    ctypes.windll.user32.MessageBoxW(None, u"OSC Chat Tools is already running!.", u"OCT is already running!", 16)
    run = False
    os._exit(0)

def fatal_error(error = None):
  global run
  run = False
  ctypes.windll.user32.MessageBoxW(None, u"OSC Chat Tools has encountered a fatal error.", u"OCT Fatal Error", 16)
  if error != None:
    result = ctypes.windll.user32.MessageBoxW(None, u"The program crashed with an error message. Would you like to copy it to your clipboard?", u"OCT Fatal Error", 3 + 64)
    if result == 6:
      pyperclip.copy(str(datetime.now())+" ["+threading.current_thread().name+"] "+str(error))
  result = ctypes.windll.user32.MessageBoxW(None, u"Open the github page to get support?", u"OCT Fatal Error", 3 + 64)
  if result == 6:
      webbrowser.open('https://github.com/Lioncat6/OSC-Chat-Tools/wiki/Fatal-Error-Crash')
  time.sleep(5)
  os._exit(0)

def afk_handler(unused_address, args):
    global isAfk
    isAfk = args
    #print('isAfk', isAfk)
    outputLog(f'isAfk {isAfk}')
    
def mute_handler(unused_address, args):
    global isMute
    isMute = args
    #print('isMute',isMute)
    outputLog(f'isMute {isMute}')
    
def inSeat_handler(unused_address, args):
    global isInSeat
    isInSeat = args
    #print('isInSeat',isInSeat)
    outputLog(f'isInSeat {isInSeat}')
    
def volume_handler(unused_address, args):
    global voiceVolume
    voiceVolume = args
    #print('voiceVolume',voiceVolume)
    #outputLog(f'voiceVolume {voiceVolume}')

def usingEarmuffs_handler(unused_address, args):
    global isUsingEarmuffs
    isUsingEarmuffs = args
    #print('isUsingEarmuffs', isUsingEarmuffs)
    outputLog(f'isUsingEarmuffs {isUsingEarmuffs}')
    
def vr_handler(unused_address, args):# The game never sends this value from what I've seen
    global isVR
    if args ==1:
        isVR == True
    else:
        isVR == False
    #print('isVR', isVR)
    outputLog(f'isVR {isVR}')

"""def thread_exists(name):
    for thread in threading.enumerate():
        if thread.name == name:
            return True
    return False"""
    
def boop_handler(unused_address, args):  
    global isBooped
    isBooped = args
    outputLog(f'isBooped {isBooped}')

def pat_handler(unused_address, args):  
    global isPat
    if isinstance(args, int) or isinstance(args, float):
      if args > 0:
        isPat = True
      else:
        isPat = False
    else:
      isPat = args
    outputLog(f'isPat {isPat}') 

message_queue = []
queue_lock = Lock()
def outputLog(text):
    text = text.replace("\n", "\n    ")
    print(text)
    global threadName
    threadName = threading.current_thread().name
    def outputQueue():
        global threadName
        timestamp = datetime.now()
        with queue_lock:
            message_queue.append((timestamp, "["+threadName+"] "+text))
        while windowAccess is None:
            time.sleep(.01)
        with queue_lock:
            message_queue.sort(key=lambda x: x[0])
            for message in message_queue:
                if conf_logOutput:
                  with open('OCT_debug_log.txt', 'a+', encoding="utf-8") as f:
                    f.write("\n"+ str(message[0]) + " " + message[1])
                windowAccess.write_event_value('outputSend', str(message[0]) + " " + message[1])
                try:
                  windowAccess['output'].Widget.see('end')
                except Exception as e:
                  if run:
                    pass
                    #fatal_error(e)
            message_queue.clear()
    outputQueueHandler = Thread(target=outputQueue)
    outputQueueHandler.start()

outputLog("OCT Starting...")

try:
  if not os.path.isfile('please-do-not-delete.txt'):
    with open('please-do-not-delete.txt', 'w', encoding="utf-8") as f:
        f.write('[]')
except Exception as e:
  outputLog("Failed to create settings file "+str(e))

def update_checker(startup_check):
  global conf_updatePrompt
  global outOfDate
  global windowAccess
  global version
  url = 'https://api.github.com/repos/Lioncat6/OSC-Chat-Tools/releases'
  try:
    response = requests.get(url)
    if response.ok:
          data = response.json()
          currentVersion = version.lower().replace(' ', '').replace('version', '').replace('v', '')
          githubVersion = data[0]['tag_name'].lower().replace(' ', '').replace('version', '').replace('v', '')
          if [int(part) for part in currentVersion.split('.')] < [int(part) for part in githubVersion.split('.')]:  
            outputLog(f'A new version is available! {githubVersion} > {currentVersion}')
            if conf_updatePrompt or not startup_check:
              def updatePromptWaitThread():
                while windowAccess == None:
                  time.sleep(.1)
                  pass
                windowAccess.write_event_value('updateAvailable', githubVersion)
              updatePromptWaitThreadHandler = Thread(target=updatePromptWaitThread).start()
            outOfDate = True
            def updatePromptWaitThread2():
              while windowAccess == None:
                  time.sleep(.1)
                  pass
              windowAccess.write_event_value('markOutOfDate', '')
            updatePromptWaitThreadHandler2 = Thread(target=updatePromptWaitThread2).start()
          else:
            if not startup_check:
              windowAccess.write_event_value('popup', f'Program is up to date! Version {version}')
            outputLog(f"Program is up to date! Version {version}")
          
    else:
        outputLog('Update Checking Error occurred:', response.status_code)
  except Exception as e:
    outputLog(f'Update Checking Error occurred: {str(e)}')

async def get_media_info():
    sessions = await MediaManager.request_async()
    # This source_app_user_model_id check and if statement is optional
    # Use it if you want to only get a certain player/program's media
    # (e.g. only chrome.exe's media not any other program's).

    # To get the ID, use a breakpoint() to run sessions.get_current_session()
    # while the media you want to get is playing.
    # Then set TARGET_ID to the string this call returns.

    current_session = sessions.get_current_session()
    if current_session:  # there needs to be a media session running
        
        info = await current_session.try_get_media_properties_async()

        # song_attr[0] != '_' ignores system attributes
        info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}

        # converts winrt vector to list
        info_dict['genres'] = list(info_dict['genres'])

        return info_dict

    # It could be possible to select a program from a list of current
    # available ones. I just haven't implemented this here for my use case.
    # See references for more information.
    raise Exception('TARGET_PROGRAM is not the current media session')
  
async def getMediaSession():
    sessions = await MediaManager.request_async()
    session = sessions.get_current_session()
    return session

def mediaIs(state):
    session = asyncio.run(getMediaSession())
    if session == None:
        return False
    return int(wmc.GlobalSystemMediaTransportControlsSessionPlaybackStatus[state]) == session.get_playback_info().playback_status
  
confDataDict = { #this dictionary will always exclude position 0 which is the config version!
  "1.4.1" : ['confVersion', 'topTextToggle', 'topTimeToggle', 'topSongToggle', 'topCPUToggle', 'topRAMToggle', 'topNoneToggle', 'bottomTextToggle', 'bottomTimeToggle', 'bottomSongToggle', 'bottomCPUToggle', 'bottomRAMToggle', 'bottomNoneToggle', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideMiddle', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'topHRToggle', 'bottomHRToggle', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt'],
  "1.4.20" : ['confVersion', 'topTextToggle', 'topTimeToggle', 'topSongToggle', 'topCPUToggle', 'topRAMToggle', 'topNoneToggle', 'bottomTextToggle', 'bottomTimeToggle', 'bottomSongToggle', 'bottomCPUToggle', 'bottomRAMToggle', 'bottomNoneToggle', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideMiddle', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'topHRToggle', 'bottomHRToggle', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput'],
  "1.5.0" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay'],
  "1.5.1" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode'],
  "1.5.2" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode'],
  "1.5.3" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP'],
  "1.5.4" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP'],
  "1.5.5" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken'],
  "1.5.6" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId'],
  "1.5.7" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId','timeDisplayPM', 'timeDisplayAM'],
  "1.5.8" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId','timeDisplayPM', 'timeDisplayAM'],
  "1.5.8.1" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId','timeDisplayPM', 'timeDisplayAM'],
  "1.5.8.2" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId','timeDisplayPM', 'timeDisplayAM'],
  "1.5.9" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId','timeDisplayPM', 'timeDisplayAM', 'showSongInfo'],
  "1.5.9.1" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId','timeDisplayPM', 'timeDisplayAM', 'showSongInfo'],
  "1.5.10" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId','timeDisplayPM', 'timeDisplayAM', 'showSongInfo'],
  "1.5.11" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId','timeDisplayPM', 'timeDisplayAM', 'showSongInfo', 'spotify_client_id'],
  "1.5.12" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId','timeDisplayPM', 'timeDisplayAM', 'showSongInfo', 'spotify_client_id', 'useTimeParameters'],
  "1.5.13" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId','timeDisplayPM', 'timeDisplayAM', 'showSongInfo', 'spotify_client_id', 'useTimeParameters'],
  "1.6.0" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken', 'usePulsoid', 'useHypeRate', 'hypeRateKey', 'hypeRateSessionId','timeDisplayPM', 'timeDisplayAM', 'showSongInfo', 'spotify_client_id', 'useTimeParameters', 'whisperModel', 'micDevice', 'sttDisplay']
}

def loadConfig(f):
  try:
      fixed_list = ast.literal_eval(f.read())
      if type(fixed_list[0]) is str:
        conf_confVersion = fixed_list[0]
        confLoaderIterator = 1
        if len(fixed_list) != len(confDataDict[conf_confVersion]):
          raise Exception('Data list length mismatch')
        for i, x in enumerate(confDataDict[conf_confVersion]):
          globals()[x] = fixed_list[i]
          #print(f"{x} = {fixed_list[i]}")
        #print("Successfully Loaded config file version "+fixed_list[0])
        outputLog("Successfully Loaded config file version "+fixed_list[0])
      else:
        #print('Config file is Too Old! Not Updating Values...')
        outputLog('Config file is Too Old! Not Updating Values...')
  except Exception as e:
      #print('Config File Load Error! Not Updating Values...')
      outputLog('Config File Load Error! Not Updating Values...\n'+str(e))
  if conf_confVersion == "1.4.1" or conf_confVersion ==  "1.4.20":
    outputLog("Converting old layout system, please update your config by pressing apply!")
    if depreciated_topTextToggle:
      conf_layoutString = conf_layoutString + '{text(0)}'
    if depreciated_topTimeToggle:
      conf_layoutString = conf_layoutString + '{time(0)}'
    if depreciated_topSongToggle:
      conf_layoutString = conf_layoutString + '{song(0)}'
    if depreciated_topCPUToggle:
      conf_layoutString = conf_layoutString + '{cpu(0)}'
    if depreciated_topRAMToggle:
      conf_layoutString = conf_layoutString + '{ram(0)}'
    if not depreciated_hideMiddle and (depreciated_topTextToggle or depreciated_topTimeToggle or depreciated_topSongToggle or depreciated_topCPUToggle or depreciated_topRAMToggle) and (depreciated_bottomTextToggle or depreciated_bottomTimeToggle or depreciated_bottomSongToggle or depreciated_bottomCPUToggle or depreciated_bottomRAMToggle):
      conf_layoutString = conf_layoutString + '{div(0)}'
    if depreciated_bottomTextToggle:
      conf_layoutString = conf_layoutString + '{text(0)}'
    if depreciated_bottomTimeToggle:
      conf_layoutString = conf_layoutString + '{time(0)}'
    if depreciated_bottomSongToggle:
      conf_layoutString = conf_layoutString + '{song(0)}'
    if depreciated_bottomCPUToggle:
      conf_layoutString = conf_layoutString + '{cpu(0)}'
    if depreciated_bottomRAMToggle:
      conf_layoutString = conf_layoutString + '{ram(0)}'

if os.path.isfile('please-do-not-delete.txt'):
  with open('please-do-not-delete.txt', 'r', encoding="utf-8") as f:
    loadConfig(f)
      
forewordServerLastUsed = conf_oscForeword

layoutDisplayDict = {
    "playtime(" : "⌚Play Time",
    "text(" : "💬Text",
    "time(" : "🕒Time",
    "song(" : "🎵Song",
    "cpu(" : "⏱️CPU Usage",
    "ram(" : "🚦RAM Usage",
    "gpu(" : "⏳GPU Usage",
    "hr(" : "💓Heart Rate",
    "mute(" : "🔇Mute Status",
    "stt(" : "⌨Speech To Text",
    "div(" : "☵Divider"
                      }

def layoutPreviewBuilder(layout, window):
  def returnDisp(a):
    global layoutDisplayDict
    for x in layoutDisplayDict:
      if x in a:
        return layoutDisplayDict[x]

  try:
    layoutList = ast.literal_eval("["+layout.replace("{", "\"").replace("}", "\",")[:-1]+"]")
    layoutLen = len(layoutList)
    if layoutLen <=15:
      for x in range(layoutLen+1, 16):
        window['layout'+str(x)].update(visible=False)
      
      if layoutLen > 0:
        for x in range(1, layoutLen+1):
          window['layout'+str(x)].update(visible=True)
          window['text'+str(x)].update(value=returnDisp(layoutList[x-1]))
          if "3" in layoutList[x-1]:
            window['divider'+str(x)].update(value=True)
            window['newLine'+str(x)].update(value=True)
          elif "2" in layoutList[x-1]:
            window['newLine'+str(x)].update(value=True)
            window['divider'+str(x)].update(value=False)
          elif "1" in layoutList[x-1]: 
            window['divider'+str(x)].update(value=True)
            window['newLine'+str(x)].update(value=False)
          else:
            window['divider'+str(x)].update(value=False)
            window['newLine'+str(x)].update(value=False)

    else:
      for x in range(1, 16):
        window['layout'+str(x)].update(visible=False)
  except:
    for x in range(1, 16):
      window['layout'+str(x)].update(visible=False)
 
def refreshAccessToken(oldRefreshToken):
  global spotifyRefreshToken
  global spotifyAccessToken
  global spotify_client_id
  token_url = 'https://accounts.spotify.com/api/token'
  data = {
      'grant_type': 'refresh_token',
      'refresh_token': oldRefreshToken,
      'client_id': spotify_client_id
    }       
  response = requests.post(token_url, data=data)
  if response.status_code != 200: 
    raise Exception('AccessToken refresh error... '+str(response.json()))
  #print(response.json())
  spotifyRefreshToken = response.json().get('refresh_token')
  spotifyAccessToken =  response.json().get('access_token')    

def getSpotifyPlaystate():
  global spotifySongUrl
  global spotifyRefreshToken
  global spotifyAccessToken
  
  def get_playstate(accessToken):
    global spotifyRefreshToken
    global spotifyAccessToken
    #print(spotifyAccessToken)
    #print(accessToken)
    headers = {
        'Authorization': 'Bearer ' + accessToken,
    }

    response = requests.get('https://api.spotify.com/v1/me/player', headers=headers)
    if response.status_code == 204:
      data = ''
    else:
      data = response.json()
    return data
  try:
      playState = get_playstate(spotifyAccessToken)
      if playState != '' and playState != None:
        if 'error' in str(playState):
          raise Exception(str(playState))
  except Exception as e:
      if "expired" in str(e):
        outputLog("Attempting to regenerate outdated access token...\nReason: "+str(e))
        refreshAccessToken(spotifyRefreshToken)
        def waitThread():
          while windowAccess == None:
              time.sleep(.1)
              pass
          windowAccess.write_event_value('Apply', '')
        waitThreadHandler = Thread(target=waitThread).start()  
        playState = get_playstate(spotifyAccessToken) 
      else:
        outputLog("Spotify connection error... retrying\nFull Error: "+str(e))
        playState = get_playstate(spotifyAccessToken) 
  if playState == None:
    playState = ''
  return playState

def loadSpotifyTokens():  
  global spotifyLinkStatus 
  outputLog("Loading spotify tokens...")
  def get_profile(accessToken):
      headers = {
          'Authorization': 'Bearer ' + accessToken,
      }
      response = requests.get('https://api.spotify.com/v1/me', headers=headers)
      data = response.json()
      if response.status_code != 200:
        raise Exception(response.json())
      return data
  try:
    outputLog("Trying old access token...")
    profile = get_profile(spotifyAccessToken)
  except Exception as e:
    outputLog("Attempting to regenerate outdated access token...\nReason: "+str(e))
    refreshAccessToken(spotifyRefreshToken)    
    profile = get_profile(spotifyAccessToken)
  linkedUserName = profile.get('display_name')  
  outputLog("Spotify linked to "+linkedUserName+" successfully!")
  spotifyLinkStatus = 'Linked to '+linkedUserName  

try:
  if spotifyAccessToken != '' and spotifyAccessToken != None:
    loadSpotifyTokens()
except Exception as e:
  if "timed out" in str(e): 
    outputLog('Spotify API Timed out... tokens may be invalid\nFull Error: '+str(e))
    spotifyLinkStatus = 'Status Unknown'
  elif "Max retries" in str(e) or "aborted" in str(e):
    outputLog('Spotify API connection error... tokens may be invalid. Are you connected to the internet?\nFull Error: '+str(e))
    spotifyLinkStatus = 'Status Unknown'
  else:
    spotifyLinkStatus = 'Error - Please Relink!'
    spotifyAccessToken = ''
    spotifyRefreshToken = ''
    outputLog("Spotify token load error! Please relink!\nFull Error: "+str(e))

def uiThread():
  global fontColor
  global bgColor
  global accentColor
  global scrollbarColor
  global buttonColor
  global scrollbarBackgroundColor
  global tabBackgroundColor
  global tabTextColor

  global version
  global msgOutput
  global conf_message_delay
  global conf_messageString
  global playMsg
  global run
  global afk
  global conf_FileToRead
  global conf_scrollText
  global conf_hideSong
  global depreciated_hideMiddle
  global conf_hideOutside
  global conf_showPaused
  global conf_songDisplay
  global songName
  global conf_showOnChange
  global conf_songChangeTicks
  global conf_minimizeOnStart
  global conf_keybind_run
  global conf_keybind_afk
  global conf_topBar
  global conf_middleBar
  global conf_bottomBar
  global pulsoidToken
  global whisperModel
  global micDevice
  global windowAccess
  global conf_avatarHR
  global conf_blinkOverride
  global conf_blinkSpeed
  global conf_useAfkKeybind
  global conf_toggleBeat
  global conf_updatePrompt
  global outOfDate
  global conf_confVersion
  global conf_oscListenAddress
  global conf_oscListenPort
  global conf_oscSendAddress
  global conf_oscSendPort
  global conf_oscForewordAddress
  global conf_oscForewordPort
  global conf_oscListen
  global conf_oscForeword
  global conf_logOutput
  global conf_layoutString
  global conf_verticalDivider
  global layoutDisplayDict
  global conf_cpuDisplay
  global conf_ramDisplay
  global conf_gpuDisplay
  global conf_hrDisplay
  global conf_sttDisplay
  global conf_playTimeDisplay
  global conf_mutedDisplay
  global conf_unmutedDisplay
  global conf_darkMode
  global sendBlank
  global suppressDuplicates
  global sendASAP
  
  global timeDisplayAM
  global timeDisplayPM
  
  global useMediaManager
  global useSpotifyApi
  global spotifySongDisplay
  global spotifyAccessToken
  global spotifyRefreshToken
  global cancelLink
  global spotifyLinkStatus
  global spotify_client_id
  
  global usePulsoid
  global useHypeRate
  global hypeRateKey
  global hypeRateSessionId

  global showSongInfo
  
  global useTimeParameters
  
  if conf_darkMode:
    bgColor = '#333333'
    accentColor = '#4d4d4d'
    fontColor = 'grey85'
    buttonColor = accentColor
    scrollbarColor = accentColor
    scrollbarBackgroundColor = accentColor
    tabBackgroundColor = accentColor
    tabTextColor = fontColor
  else: 
    bgColor = '#64778d'
    accentColor = '#528b8b'
    fontColor = 'white'
    buttonColor = '#283b5b'
    scrollbarColor = '#283b5b'
    scrollbarBackgroundColor = '#a6b2be'
    tabBackgroundColor = 'white'
    tabTextColor = 'black'
  
  sg.set_options(sbar_frame_color=fontColor)
  sg.set_options(scrollbar_color=scrollbarColor)
  sg.set_options(button_color=(fontColor, buttonColor))
  sg.set_options(text_color=fontColor)
  sg.set_options(background_color=bgColor)
  sg.set_options(element_background_color=bgColor)
  sg.set_options(text_element_background_color=bgColor)
  sg.set_options(sbar_trough_color=scrollbarBackgroundColor)
  sg.set_options(border_width=0)
  sg.set_options(use_ttk_buttons=True)
  sg.set_options(input_elements_background_color=fontColor)
  
  layout_layout =  [[sg.Column(
              [[sg.Text('Configure chatbox layout', background_color=accentColor, font=('Arial', 12, 'bold')), sg.Checkbox('Text file read - defined in the behavior tab\n(This will disable everything else)', default=False, key='scroll', enable_events= True, background_color='dark slate blue')],
              [sg.Column([
                [sg.Text('Add Elements', font=('Arial', 12, 'bold'))],
                [sg.Text('Every Element is customizable from the Behavior Tab', font=('Arial', 10, 'bold'))],
                [sg.Text('*', text_color='cyan', font=('Arial', 12, 'bold'), pad=(0, 0)), sg.Text('= Requires OSC Listening To Function')],
                [sg.Text('💬Text', font=('Arial', 12, 'bold')), sg.Push(), sg.Text('A configurable text object', ), sg.Push(), sg.Button('Add to Layout', key='addText')],
                [sg.Text('🕒Time', font=('Arial', 12, 'bold')), sg.Push(), sg.Text('Display your current time', ), sg.Push(), sg.Button('Add to Layout', key='addTime')],
                [sg.Text('🎵Song', font=('Arial', 12, 'bold')), sg.Push(), sg.Text('Customizable song display', ), sg.Push(), sg.Button('Add to Layout', key='addSong')],
                [sg.Text('⏱️CPU', font=('Arial', 12, 'bold')), sg.Push(), sg.Text('Display CPU Utilization %', ), sg.Push(), sg.Button('Add to Layout', key='addCPU')],
                [sg.Text('🚦RAM', font=('Arial', 12, 'bold')), sg.Push(), sg.Text('Display RAM Usage %', ), sg.Push(), sg.Button('Add to Layout', key='addRAM')],
                [sg.Text('⏳GPU', font=('Arial', 12, 'bold')), sg.Push(), sg.Text('Display GPU Utilization %', ), sg.Push(), sg.Button('Add to Layout', key='addGPU')],
                [sg.Text('💓HR', font=('Arial', 12, 'bold')), sg.Push(), sg.Text('Display Heart Rate', ), sg.Push(), sg.Button('Add to Layout', key='addHR')],
                [sg.Text('🔇Mute', font=('Arial', 12, 'bold')), sg.Text('*', text_color='cyan', pad=(0, 0), font=('Arial', 12, 'bold')), sg.Push(), sg.Text('Display Mic Mute Status', ), sg.Push(), sg.Button('Add to Layout', key='addMute')],
                [sg.Text('⌚Play Time', font=('Arial', 12, 'bold')), sg.Push(), sg.Text('Show Play Time', ), sg.Push(), sg.Button('Add to Layout',  key='addPlaytime')],
                [sg.Text('⌨️STT', font=('Arial', 12, 'bold')), sg.Push(), sg.Text('Speech recognition object', ), sg.Push(), sg.Button('Add to Layout', key='addSTT')],
                [sg.Text('☵Divider', font=('Arial', 12, 'bold')), sg.Push(), sg.Text('Horizontal Divider', ), sg.Push(), sg.Button('Add to Layout',  key='addDiv')],
                
                ],size=(350, 520), scrollable=True, vertical_scroll_only=True, element_justification='center'), sg.Column([
                  [sg.Text('Arrange Elements', font=('Arial', 12, 'bold'))],
                  [sg.Text('➥ = New Line  ┋ = Vertical Divider')],
                  [sg.Column([
                    [sg.Column([[sg.Button('❌', key='delete1'), sg.Button('⬆️', disabled=True, key='up1'), sg.Button('⬇️', key='down1'), sg.Text('---', key='text1',  font=('Arial', 10, 'bold')), sg.Checkbox('┋', key="divider1", enable_events=True, font=('Arial', 10, 'bold')), sg.Checkbox('➥', enable_events=True, key="newLine1")]], key='layout1', element_justification='left')],
                    [sg.Column([[sg.Button('❌', key='delete2'), sg.Button('⬆️', key='up2'), sg.Button('⬇️', key='down2'), sg.Text('---', key='text2',  font=('Arial', 10, 'bold')), sg.Checkbox('┋', enable_events=True, key="divider2",  font=('Arial', 10, 'bold')), sg.Checkbox('➥', enable_events=True, key="newLine2")]], key='layout2', element_justification='left')],
                    [sg.Column([[sg.Button('❌', key='delete3'), sg.Button('⬆️', key='up3'), sg.Button('⬇️', key='down3'), sg.Text('---', key='text3',  font=('Arial', 10, 'bold')), sg.Checkbox('┋', enable_events=True, key="divider3",  font=('Arial', 10, 'bold')), sg.Checkbox('➥', enable_events=True, key="newLine3")]], key='layout3', element_justification='left')],
                    [sg.Column([[sg.Button('❌', key='delete4'), sg.Button('⬆️', key='up4'), sg.Button('⬇️', key='down4'), sg.Text('---', key='text4',  font=('Arial', 10, 'bold')), sg.Checkbox('┋', enable_events=True, key="divider4",  font=('Arial', 10, 'bold')), sg.Checkbox('➥', enable_events=True, key="newLine4")]], key='layout4', element_justification='left')],
                    [sg.Column([[sg.Button('❌', key='delete5'), sg.Button('⬆️', key='up5'), sg.Button('⬇️', key='down5'), sg.Text('---', key='text5',  font=('Arial', 10, 'bold')), sg.Checkbox('┋', enable_events=True, key="divider5",  font=('Arial', 10, 'bold')), sg.Checkbox('➥', enable_events=True, key="newLine5")]], key='layout5', element_justification='left')],
                    [sg.Column([[sg.Button('❌', key='delete6'), sg.Button('⬆️', key='up6'), sg.Button('⬇️', key='down6'), sg.Text('---', key='text6',  font=('Arial', 10, 'bold')), sg.Checkbox('┋', enable_events=True, key="divider6",  font=('Arial', 10, 'bold')), sg.Checkbox('➥', enable_events=True, key="newLine6")]], key='layout6', element_justification='left')],
                    [sg.Column([[sg.Button('❌', key='delete7'), sg.Button('⬆️', key='up7'), sg.Button('⬇️', key='down7'), sg.Text('---', key='text7',  font=('Arial', 10, 'bold')), sg.Checkbox('┋', enable_events=True, key="divider7",  font=('Arial', 10, 'bold')), sg.Checkbox('➥', enable_events=True, key="newLine7")]], key='layout7', element_justification='left')],
                    [sg.Column([[sg.Button('❌', key='delete8'), sg.Button('⬆️', key='up8'), sg.Button('⬇️', key='down8'), sg.Text('---', key='text8',  font=('Arial', 10, 'bold')), sg.Checkbox('┋', enable_events=True, key="divider8",  font=('Arial', 10, 'bold')), sg.Checkbox('➥', enable_events=True, key="newLine8")]], key='layout8', element_justification='left')],
                    [sg.Column([[sg.Button('❌', key='delete9'), sg.Button('⬆️', key='up9'), sg.Button('⬇️', key='down9'), sg.Text('---', key='text9',  font=('Arial', 10, 'bold')), sg.Checkbox('┋', enable_events=True, key="divider9",  font=('Arial', 10, 'bold')), sg.Checkbox('➥', enable_events=True, key="newLine9")]], key='layout9', element_justification='left')],
                    [sg.Column([[sg.Button('❌', key='delete10'), sg.Button('⬆️', key='up10'), sg.Button('⬇️', key='down10'), sg.Text('---', key='text10',  font=('Arial', 10, 'bold')), sg.Checkbox('┋', enable_events=True, key="divider10",  font=('Arial', 10, 'bold')), sg.Checkbox('➥', enable_events=True, key="newLine10")]], key='layout10', element_justification='left')],
                    [sg.Column([[sg.Button('❌', key='delete11'), sg.Button('⬆️', key='up11'), sg.Button('⬇️', key='down11'), sg.Text('---', key='text11',  font=('Arial', 10, 'bold')), sg.Checkbox('┋', enable_events=True, key="divider11",  font=('Arial', 10, 'bold')), sg.Checkbox('➥', enable_events=True, key="newLine11")]], key='layout11', element_justification='left')],
                    [sg.Column([[sg.Button('❌', key='delete12'), sg.Button('⬆️', key='up12'), sg.Button('⬇️', key='down12'), sg.Text('---', key='text12',  font=('Arial', 10, 'bold')), sg.Checkbox('┋', enable_events=True, key="divider12",  font=('Arial', 10, 'bold')), sg.Checkbox('➥', enable_events=True, key="newLine12")]], key='layout12', element_justification='left')],
                    [sg.Column([[sg.Button('❌', key='delete13'), sg.Button('⬆️', key='up13'), sg.Button('⬇️', key='down13'), sg.Text('---', key='text13',  font=('Arial', 10, 'bold')), sg.Checkbox('┋', enable_events=True, key="divider13",  font=('Arial', 10, 'bold')), sg.Checkbox('➥', enable_events=True, key="newLine13")]], key='layout13', element_justification='left')],
                    [sg.Column([[sg.Button('❌', key='delete14'), sg.Button('⬆️', key='up14'), sg.Button('⬇️', key='down14'), sg.Text('---', key='text14',  font=('Arial', 10, 'bold')), sg.Checkbox('┋', enable_events=True, key="divider14",  font=('Arial', 10, 'bold')), sg.Checkbox('➥', enable_events=True, key="newLine14")]], key='layout14', element_justification='left')],
                    [sg.Column([[sg.Button('❌', key='delete15'), sg.Button('⬆️', key='up15'), sg.Button('⬇️', key='down15'), sg.Text('---', key='text15',  font=('Arial', 10, 'bold')), sg.Checkbox('┋', enable_events=True, key="divider15",  font=('Arial', 10, 'bold')), sg.Checkbox('➥', enable_events=True, key="newLine15")]], key='layout15', element_justification='left')],
                    ], key="layout_editor", scrollable=True, vertical_scroll_only=True, element_justification='left', size=(335, 300))],
                  [sg.Text('Manual Edit', font=('Arial', 12, 'bold')), sg.Button('?', font=('Arial', 12, 'bold'), key="manualHelp")],
                  [sg.Text('Wrap object in { }. Spaces are respected.')],
                  [sg.Multiline('', key='layoutStorage', size=(45, 5), font=('Arial', 10, 'bold'))]
                  ], size=(360, 520), element_justification='center')]
              ]
  ,  expand_x=True, expand_y=True, background_color=accentColor, element_justification='left')]]

  behaviour_misc_layout = [
    [sg.Column([
                  [sg.Text('File to use for the text file read functionality')],
                  [sg.Button('Open File'), sg.Text('', key='message_file_path_display')]
              ], size=(379, 70))],
    [sg.Column([
                  [sg.Text('Delay between frame updates, in seconds')],
                  [sg.Text('If you are getting a \'Timed out for x seconds\' message,\ntry adjusting this')],
                  [sg.Slider(range=(1.5, 10), default_value=1.5, resolution=0.1, orientation='horizontal', size=(40, 15), key="msgDelay", trough_color=scrollbarBackgroundColor)]
      ], size=(379, 110))],
    [sg.Column([
      [sg.Text('Advanced Sending Options')],
      [sg.Checkbox('Clear the chatbox when toggled or on program close\nTurn off if you are getting issues with the chatbox blinking', key='sendBlank', default=True)],
      [sg.Checkbox('Skip sending duplicate messages', key='suppressDuplicates', default=False)],
      [sg.Checkbox('Send next message as soon as any data is updated\nOnly skips delay if previous message was skipped', key='sendASAP', default=False)]
    ], size=(379, 155))]
  ]
  behaviour_text_layout = [
    [sg.Column([
                  [sg.Text('Text to display for the message. One frame per line\nTo send a blank frame, use an asterisk(*) by itself on a line.\n\\n and \\v are respected.', justification='center')],
                  [sg.Multiline(default_text='OSC Chat Tools\nBy Lioncat6',
                      size=(50, 10), key='messageInput')]
    ], size=(379, 240))],
  ]
  behaviour_time_layout = [
    [sg.Column([
                  [sg.Text('Template to use for Time display\nVariables:{hour}, {minute}, {time_zone}, {hour24}')],
                  [sg.Text('AM:'), sg.Push(),  sg.Input(key='timeDisplayAM', size=(30, 1))],
                  [sg.Text('PM:'), sg.Push(), sg.Input(key='timeDisplayPM', size=(30, 1))],
                  [sg.Checkbox('Send Time parameters to avatar (Uses vrcosc parameters)', default=False, key='useTimeParameters')]
              ], size=(379, 130))],
  ]
  behaviour_song_layout = [[sg.Column([
    [sg.Column([
                  [sg.Text("Select audio info source:")],
                  [sg.Checkbox("Windows Now Playing", key='useMediaManager', default=True, enable_events=True), sg.Checkbox("Spotify API", key='useSpotifyApi', default=False, enable_events=True)], #Its called the Now Playing Session Manager btw
                  ], size=(379, 80))],
    [sg.Column([
                  [sg.Text("Windows Now Playing settings:")],
                  [sg.Text('Template to use for song display.\nVariables: {artist}, {title}, {album_title}, {album_artist}')],
                  [sg.Input(key='songDisplay', size=(50, 1))]
    ], size=(379, 100))],
    [sg.Column([
                  [sg.Text("Spotify settings:")],
                  [sg.Text('Template to use for song display.\nVariables: {artist}, {title}, {album_title}, {album_artist}, \n{song_progress}, {song_length}, {volume}, {song_id}')],
                  [sg.Input(key='spotifySongDisplay', size=(50, 1))],
                  [sg.Text('Spotify Client ID'), sg.Button("?", key='client_id_help', font='bold'), sg.Text('<- If linking fails, click here!', font="bold")],
                  [sg.Input(key='spotify_client_id', size=(50, 1))],
                  [sg.Button("Link Spotify 🔗", key="linkSpotify", button_color="#00a828", font="System"), sg.Text('Unlinked', key='spotifyLinkStatus', font="System", text_color='orange')],
    ], size=(379, 195))],
    [sg.Column([
                  [sg.Text('Music Settings:')],
                  [sg.Checkbox('Show \"⏸️\" after song when song is paused', default=True, key='showPaused', enable_events= True)],
                  [sg.Checkbox('Hide song when music is paused', default=False, key='hideSong', enable_events= True)],
                  [sg.HorizontalSeparator()],
                  [sg.Checkbox('Only show music on song change', default=False, key='showOnChange', enable_events=True)],
                  [sg.Text('Amount of frames to wait before the song name disappears')],
                  [sg.Slider(range=(1, 5), default_value=2, resolution=1, orientation='horizontal', size=(40, 15), key="songChangeTicks", trough_color=scrollbarBackgroundColor)]
              ], size=(379, 220))],
  ], background_color=accentColor, scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, size=(440, 300),)]]
  behaviour_cpu_layout = [
    [sg.Column([
                  [sg.Text('Template to use for CPU display.\nVariables: {cpu_percent}')],
                  [sg.Input(key='cpuDisplay', size=(50, 1))]
              ], size=(379, 80))],
  ]
  behaviour_ram_layout = [
    [sg.Column([
                  [sg.Text('Template to use for RAM display. Variables:\n{ram_percent}, {ram_available}, {ram_total}, {ram_used}')],
                  [sg.Input(key='ramDisplay', size=(50, 1))]
              ], size=(379, 80))],
  ]
  behaviour_gpu_layout = [
    [sg.Column([
                  [sg.Text('Template to use for GPU display.\nVariables: {gpu_percent}')],
                  [sg.Input(key='gpuDisplay', size=(50, 1))]
              ], size=(379, 80))],
  ]
  behaviour_hr_layout = [
    [sg.Column([
                  [sg.Text('Template to use for Heart Rate display.\nVariables: {hr}')],
                  [sg.Input(key='hrDisplay', size=(50, 1))]
              ], size=(379, 80))],
    [sg.Column([
                  [sg.Text('Heartrate Settings:')],
                  [sg.Text("Select heart rate data source:")],
                  [sg.Checkbox("Pulsoid", key='usePulsoid', default=True, enable_events=True), sg.Checkbox("HypeRate", key='useHypeRate', default=False, enable_events=True)],
                  [sg.Checkbox('Pass through heartrate avatar parameters\neven when not running', default=False, key='avatarHR', enable_events= True)],
                  [sg.Checkbox('Heart Rate Beat', default=True, key='toggleBeat', enable_events=True)],
                  [sg.Checkbox('Override Beat', default=False, key='blinkOverride', enable_events=True)],
                  [sg.Text('Blink Speed (If Overridden)')],
                  [sg.Slider(range=(0, 5), default_value=.5, resolution=.01, orientation='horizontal', size=(40, 15), key="blinkSpeed", trough_color=scrollbarBackgroundColor)]
              ], size=(379, 250))],
    [sg.Column([
      [sg.Text('Pulsoid Settings:')],
      [sg.Text('Pulsoid Token:'), sg.Button('Get Token 💓', key='getPulsoidToken', font="System", button_color="#f92f60")],
        [sg.Input(key='pulsoidToken', size=(50, 1))],
    ], size=(379, 90))],
    [sg.Column([
      [sg.Text('HypeRate Settings:')],
      [sg.Text('HypeRate API Key:'), sg.Button('Get Key 💞', key='getHypeRateKey', font="System", button_color="#f92f60")],
        [sg.Input(key='hypeRateKey', size=(50, 1))],
      [sg.Text('HypeRate Session ID:'),],
        [sg.Input(key='hypeRateSessionId', size=(50, 1))],
    ], size=(379, 130))]
  ]
  behaviour_mute_layout = [
    [sg.Column([
                  [sg.Text('Template to use for Mute Toggle display')],
                  [sg.Text('Muted:'), sg.Push(),  sg.Input(key='mutedDisplay', size=(30, 1))],
                  [sg.Text('Unmuted:'), sg.Push(), sg.Input(key='unmutedDisplay', size=(30, 1))]
              ], size=(379, 80))],
  ]
  behaviour_playtime_layout = [
    [sg.Column([
                  [sg.Text('Template to use for Play Time display.\nVariables: {hours}, {remainder_minutes}, {minutes}')],
                  [sg.Input(key='playTimeDisplay', size=(50, 1))]
              ], size=(379, 80))],
  ]
  behaviour_stt_layout = [
    [sg.Column([
                  [sg.Text('Template to use for STT display.\nVariables: {stt}')],
                  [sg.Input(key='sttDisplay', size=(50, 1))]
              ], size=(379, 80))],
    [sg.Column([
      [sg.Text('Whisper Settings:')],
      [sg.Text('Whisper Model:'), sg.Combo(whisper.available_models(), key='whisperModel', readonly=True, size=(30, 1))],
      [sg.Button('Switch Loaded Model', key='loadModel', font="System", button_color="#f92f60")],
      [sg.Text('Microphone Device:'), sg.Combo(mic_devices, key='micDevice', readonly=True, size=(30, 1))]
    ], size=(379, 150))]
  ]
  behaviour_divider_layout = [
    [sg.Column([
                  [sg.Text('Divider Settings:')],
                  [sg.Text('Top Divider:')],
                  [sg.Input(key='topBar', size=(50, 1))],
                  [sg.Text('Middle Divider:')],
                  [sg.Input(key='middleBar', size=(50, 1))],
                  [sg.Text('Bottom Divider:')],
                  [sg.Input(key='bottomBar', size=(50, 1))],
                  [sg.Text('Vertical Divider:')],
                  [sg.Input(key='verticalDivider', size=(50, 1))],
                  [sg.Checkbox('Remove outside dividers', default=True, key='hideOutside', enable_events= True)],
                ], size=(379, 270))],
  ]
  behavior_layout = [
    [   
          sg.TabGroup([[
                  sg.Tab('❔Misc.', [[sg.Column(behaviour_misc_layout, background_color=accentColor, scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, size=(440, 300),)]], background_color=accentColor),
                  sg.Tab('💬Text', [[sg.Column(behaviour_text_layout, background_color=accentColor, scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, size=(440, 300),)]], background_color=accentColor),
                  sg.Tab('🕒Time', [[sg.Column(behaviour_time_layout, background_color=accentColor, scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, size=(440, 300),)]], background_color=accentColor),
                  sg.Tab('🎵Song', behaviour_song_layout, background_color=accentColor),
                  sg.Tab('⏱️CPU', [[sg.Column(behaviour_cpu_layout, background_color=accentColor, scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, size=(440, 300),)]], background_color=accentColor),
                  sg.Tab('🚦RAM', [[sg.Column(behaviour_ram_layout, background_color=accentColor, scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, size=(440, 300),)]], background_color=accentColor),
                  sg.Tab('⏳GPU', [[sg.Column(behaviour_gpu_layout, background_color=accentColor, scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, size=(440, 300),)]], background_color=accentColor),
                  sg.Tab('💓HR', [[sg.Column(behaviour_hr_layout, background_color=accentColor, scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, size=(440, 300),)]], background_color=accentColor),
                  sg.Tab('🔇Mute', [[sg.Column(behaviour_mute_layout, background_color=accentColor, scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, size=(440, 300),)]], background_color=accentColor),
                  sg.Tab('⌚Play Time', [[sg.Column(behaviour_playtime_layout, background_color=accentColor, scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, size=(440, 300),)]], background_color=accentColor),
                  sg.Tab('⌨STT', [[sg.Column(behaviour_stt_layout, background_color=accentColor, scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, size=(440, 300),)]], background_color=accentColor),
                  sg.Tab('☵Divider', [[sg.Column(behaviour_divider_layout, background_color=accentColor, scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, size=(440, 300),)]], background_color=accentColor),
              ]], 
              key='behaviorTabs', selected_title_color='white', selected_background_color='gray', expand_x=True, expand_y=True, size=(440, 300), font=('Arial', 11, 'normal'), tab_background_color=tabBackgroundColor, tab_border_width=0, title_color=tabTextColor, 
          )
      ],
  ]
  """behavior_layout =  [[sg.Column([
              [sg.Text('Configure chatbox behavior', background_color=accentColor, font=('Arial', 12, 'bold'))],
              [sg.Column(text_conf_layout, background_color=accentColor)],
              [sg.Column(time_conf_layout, background_color=accentColor)],
              [sg.Column(misc_conf_layout, background_color=accentColor)],
              [sg.Column(song_conf_layout, background_color=accentColor)],
              [sg.Column(cpu_conf_layout, background_color=accentColor)],
              [sg.Column(ram_conf_layout, background_color=accentColor)],
              [sg.Column(gpu_conf_layout, background_color=accentColor)],
              [sg.Column(hr_conf_layout, background_color=accentColor)],
              [sg.Column(playTime_conf_layout, background_color=accentColor)],
              [sg.Column(mute_conf_layout, background_color=accentColor)],
              [sg.Column(divider_conf_layout, background_color=accentColor)],             
              
              
              ]
  , scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, background_color=accentColor)]]"""

  keybindings_layout = [[sg.Column(
              [
                
              ]
  , scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, background_color=accentColor)]]

  preview_layout = [[sg.Column(
              [[sg.Text('Preview (Not Perfect)', background_color=accentColor, font=('Arial', 12, 'bold')),sg.Text('', key='sentCountdown')],
              [sg.Column([
                [sg.Text('', key = 'messagePreviewFill', font=('Arial', 12 ), auto_size_text=True, size=(23, 100), justification='center')]
              ], size=(379, 150))]
              ]
  
  , scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, background_color=accentColor)]]
  
  options_layout = [[sg.Column(
              [[sg.Text('Configure Program', background_color=accentColor, font=('Arial', 12, 'bold'))],
                [sg.Column([
                  [sg.Checkbox('Minimize on startup', default=False, key='minimizeOnStart', enable_events= True)],
                  [sg.Checkbox('Show update prompt', default=True, key='updatePrompt', enable_events= True)],
                  [sg.Checkbox('Dark Mode (applies on restart)', default=False, key='darkMode', enable_events=True)],
                  [sg.Checkbox('Show song info on bottom ribbon', default=True, key ='showSongInfo')]
                ], size=(379, 115))],
                [sg.Text('Keybindings Configuration', background_color=accentColor, font=('Arial', 12, 'bold'))],
              [sg.Text('You must press Apply for new keybinds to take affect!', background_color=accentColor)],
                [sg.Column([
                  [sg.Text('Toggle Run'), sg.Frame('',[[sg.Text('Unbound', key='keybind_run', background_color=accentColor, pad=(10, 0))]],background_color=accentColor), sg.Button('Bind Key', key='run_binding')],
                  [sg.Checkbox('Use keybind', default=True, enable_events=True, key='useRunKeybind', disabled=True)],
                  [sg.Text('Toggle Afk'), sg.Frame('',[[sg.Text('Unbound', key='keybind_afk', background_color=accentColor, pad=(10, 0))]],background_color=accentColor), sg.Button('Bind Key', key='afk_binding')],
                  [sg.Checkbox('Use keybind (Otherwise, uses OSC to check afk status)', default=False, enable_events=True, key='useAfkKeybind')]
                ], expand_x=True, size=(379, 130))]
              ]
  , scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, background_color=accentColor)]]
  
  osc_layout = [[sg.Column(
              [[sg.Text('OSC Options - Experimental\n(Turning on debug logging is recommended)', background_color=accentColor, font=('Arial', 12, 'bold'))],
              [sg.Column([
                  [sg.Text('OSC Listen Options')],
                  [sg.Checkbox('Use OSC Listen', key='oscListen')],
                  [sg.Text('Address: '), sg.Input('', size=(30, 1), key='oscListenAddress')],
                  [sg.Text('Port: '), sg.Input('', size=(30, 1), key='oscListenPort')]
                ], size=(379, 120))],
              [sg.Column([
                  [sg.Text('OSC Send Options')],
                  [sg.Text('Address: '), sg.Input('', size=(30, 1), key='oscSendAddress')],
                  [sg.Text('Port: '), sg.Input('', size=(30, 1), key='oscSendPort')]
                ], size=(379, 90))],
              [sg.Column([
                  [sg.Text('OSC Forwarding Options\nRepeats all listened data to another address for other programs')],
                  [sg.Checkbox('Use OSC Forwarding', key='oscForeword')],
                  [sg.Text('Address: '), sg.Input('', size=(30, 1), key='oscForewordAddress')],
                  [sg.Text('Port: '), sg.Input('', size=(30, 1), key='oscForewordPort')]
                ], size=(379, 120))],
              [sg.Column([
                  [sg.Text('Avatar Debugging')],
                  [sg.Text('Path:'), sg.Input('', size=(30, 1), key='debugPath')],
                  [sg.Text('Value'), sg.Input('', size=(30, 1), key='debugValue'), sg.Combo([int, float, bool, str], default_value=int, readonly=True, size=(10, 1), key='debugType')],
                  [sg.Button('Send', key='sendDebug')]
                ], size=(379, 110))]
              ]  , scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, background_color=accentColor)]]
  
  output_layout =  [[sg.Column(
              [[sg.Text('Program Output', background_color=accentColor, font=('Arial', 12, 'bold')), sg.Checkbox('Log to file (OCT_debug_log.txt)', default=False, key='logOutput', background_color=accentColor)],
              [sg.Multiline('', disabled=True, key='output', size=(53, 30), background_color='DarkSlateGrey', text_color='white', expand_x=True, expand_y=True)]
              ] , expand_x=True, expand_y=True, background_color=accentColor)]]
  
  menu_def = [['&File', ['A&pply', '&Reset', '---', 'Open Config File', 'Open Debug Log', '---','E&xit', 'Re&start' ]],
          ['&Help', ['&About', '---', 'Submit Feedback', '---', 'Open &Github Page', '&Check For Updates', '&FAQ', '---', 'Discord']]]
  
  topMenuBar = sg.Menu(menu_def, key="menuBar")

  right_click_menu = ['&Right', ['Copy', 'Paste']]

  layout = [
      [[topMenuBar]],
      [   
          sg.TabGroup([[
                  sg.Tab('🧩Layout', layout_layout, background_color=accentColor),
                  sg.Tab('🤖Behavior', behavior_layout, background_color=accentColor),
                  sg.Tab('📺Preview', preview_layout, background_color=accentColor),
                  #sg.Tab('⌨Keybindings', keybindings_layout, background_color=accentColor),
                  sg.Tab('💻Options', options_layout, background_color=accentColor),
                  sg.Tab('📲OSC Options', osc_layout, background_color=accentColor),
                  sg.Tab('💾Output', output_layout, background_color=accentColor)
              ]], 
              key='mainTabs', tab_location='lefttop', selected_title_color='white', selected_background_color='gray', expand_x=True, expand_y=True, size=(440, 300), font=('Arial', 11, 'normal'), tab_background_color=tabBackgroundColor, tab_border_width=0, title_color=tabTextColor
          )
      ],
      [sg.Button('Apply', tooltip='Apply all changes to options'), sg.Button('Reset'), sg.Text(" Version "+str(version), key='versionText'), sg.Checkbox('Run?', default=True, key='runThing', enable_events= True, background_color='peru'), sg.Checkbox('AFK', default=False, key='afk', enable_events= True, background_color='#cb7cef'), sg.Push(), sg.Text("⏸️", key='spotifyPlayStatus', font = ('Helvetica', 11), visible=False, pad=(0, 0)), sg.Text("---", key='spotifySongName', enable_events=True, font = ('Helvetica', 11, 'underline'), visible=False, pad=(0, 0)), sg.Text("『00:00/00:00』", key='spotifyDuration', font = ('Helvetica', 11), visible=False, pad=(0, 0)), sg.Image("./assets/Spotify.png", key='spotifyIcon', visible=False)]]

  window = sg.Window('OSC Chat Tools', layout, default_element_size=(12, 1), resizable=True, finalize= True, size=(900, 620), right_click_menu=right_click_menu, icon="osc-chat-tools.exe", titlebar_icon="osc-chat-tools.exe")
  window.set_min_size((500, 350))

  def resetVars():
    window['messageInput'].update(value='OSC Chat Tools\nBy Lioncat6')
    window['msgDelay'].update(value=1.5)
    window['songDisplay'].update(value=' 🎵\'{title}\' ᵇʸ {artist}🎶')
    window['showOnChange'].update(value=False)
    window['songChangeTicks'].update(value=2)
    window['hideOutside'].update(value=True)
    window['showPaused'].update(value=True)
    window['hideSong'].update(value=False)
    window['minimizeOnStart'].update(value=False)
    window['keybind_run'].update(value='`')
    window['keybind_afk'].update(value='end')
    window['topBar'].update(value='╔═════════════╗')
    window['middleBar'].update(value='╠═════════════╣')
    window['bottomBar'].update(value='╚═════════════╝')
    window['pulsoidToken'].update(value='')
    window['whisperModel'].update(value='base.en')
    window['micDevice'].update(value='Default')
    window['avatarHR'].update(value=False)
    window['blinkOverride'].update(value=False)
    window['blinkSpeed'].update(value=.5)
    window['useAfkKeybind'].update(value=False)
    window['toggleBeat'].update(value=True)
    window['updatePrompt'].update(value=True)
    window['oscListenAddress'].update(value='127.0.0.1')
    window['oscListenPort'].update(value='9001')
    window['oscSendAddress'].update(value='127.0.0.1')
    window['oscSendPort'].update(value='9000')
    window['oscForewordAddress'].update(value='127.0.0.1')
    window['oscForewordPort'].update(value='9002')
    window['oscListen'].update(value=False)
    window['oscForeword'].update(value=False)
    window['logOutput'].update(value=False)
    window['layoutStorage'].update(value='')
    window['verticalDivider'].update(value='〣')
    window['cpuDisplay'].update(value='ᴄᴘᴜ: {cpu_percent}%')
    window['ramDisplay'].update(value='ʀᴀᴍ: {ram_percent}%  ({ram_used}/{ram_total})')
    window['gpuDisplay'].update(value='ɢᴘᴜ: {gpu_percent}%')
    window['hrDisplay'].update(value='💓 {hr}')
    window['sttDisplay'].update(value='STT: {stt}')
    window['playTimeDisplay'].update(value='⏳{hours}:{remainder_minutes}')
    window['mutedDisplay'].update(value='Muted 🔇')
    window['unmutedDisplay'].update(value='🔊')
    window['darkMode'].update(value=True)
    window['sendBlank'].update(value=True)
    window['suppressDuplicates'].update(value=False)
    window['sendASAP'].update(value=False)
    window['useMediaManager'].update(value=True)
    window['useSpotifyApi'].update(value=False)
    window['spotifySongDisplay'].update(value='🎵\'{title}\' ᵇʸ {artist}🎶 『{song_progress}/{song_length}』')
    window['usePulsoid'].update(value=True)
    window['useHypeRate'].update(value=False)
    window['hypeRateKey'].update(value='FIrXkWWlf57iHjMu0x3lEMNst8IDIzwUA2UD6lmSxL4BqBUTYw8LCwQlM2n5U8RU')
    window['hypeRateSessionId'].update(value='')
    window['timeDisplayAM'].update(value="{hour}:{minute} AM")
    window['timeDisplayPM'].update(value="{hour}:{minute} PM")
    window['showSongInfo'].update(value=True)
    window['useTimeParameters'].update(value=False)
    #Disc Spotify
    global spotifyAccessToken
    global spotifyRefreshToken
    global useSpotifyApi
    global useMediaManager
    spotifyAccessToken = ''
    spotifyRefreshToken = ''
    spotifyLinkStatus = 'Unlinked'
    window['useSpotifyApi'].update(value=False)
    window['useMediaManager'].update(value=True)
    useSpotifyApi = False
    useMediaManager = True
    window.write_event_value('Apply', '')
    window['spotifyLinkStatus'].update(value=spotifyLinkStatus)
    window['spotifyLinkStatus'].update(text_color='orange')
    window['linkSpotify'].update(text="Link Spotify 🔗", button_color="#00a828")
    #Apply
    window.write_event_value('Apply', '')

  def updateUI():
    global bgColor
    global accentColor
    global fontColor
    global buttonColor
    global scrollbarColor 
    global scrollbarBackgroundColor
    global tabBackgroundColor
    global tabTextColor
    global playMsg
    global msgOutput
    global sentTime
    global sent
    global sendSkipped
    global conf_message_delay
    global spotifyLinkStatus
    global spotifyAccessToken
    global spotifyRefreshToken
    global usePulsoid
    global useHypeRate
    global hypeRateKey
    global hypeRateSessionId
    global timeDisplayAM
    global timeDisplayPM
    global showSongInfo
    global spotify_client_id
    
    global layoutUpdate
    
    global useTimeParameters
    
    # update the UI
    if os.path.isfile('please-do-not-delete.txt'):
      try:
        window['msgDelay'].update(value=conf_message_delay)
        window['messageInput'].update(value=conf_messageString)
        window['message_file_path_display'].update(value=conf_FileToRead)
        window['scroll'].update(value=conf_scrollText)
        window['hideSong'].update(value=conf_hideSong)
        window['hideOutside'].update(value=conf_hideOutside)
        window['showPaused'].update(value=conf_showPaused)
        window['songDisplay'].update(value=conf_songDisplay)
        window['showOnChange'].update(value=conf_showOnChange)
        window['songChangeTicks'].update(value=conf_songChangeTicks)
        window['minimizeOnStart'].update(value=conf_minimizeOnStart)
        window['keybind_run'].update(value=conf_keybind_run)
        window['keybind_afk'].update(value=conf_keybind_afk)
        window['topBar'].update(value=conf_topBar)
        window['middleBar'].update(value=conf_middleBar)
        window['bottomBar'].update(value=conf_bottomBar)
        window['pulsoidToken'].update(value=pulsoidToken)
        window['whisperModel'].update(value=whisperModel)
        window['micDevice'].update(value=micDevice)
        window['avatarHR'].update(value=conf_avatarHR) 
        window['useAfkKeybind'].update(value=conf_useAfkKeybind)
        window['updatePrompt'].update(value=conf_updatePrompt)
        window['oscListenAddress'].update(value=conf_oscListenAddress)
        window['oscListenPort'].update(value=conf_oscListenPort)
        window['oscSendAddress'].update(value=conf_oscSendAddress)
        window['oscSendPort'].update(value=conf_oscSendPort)
        window['oscForewordAddress'].update(value=conf_oscForewordAddress)
        window['oscForewordPort'].update(value=conf_oscForewordPort)
        window['oscListen'].update(value=conf_oscListen)
        window['oscForeword'].update(value=conf_oscForeword)
        window['logOutput'].update(value=conf_logOutput)
        window['layoutStorage'].update(value=conf_layoutString)
        window['verticalDivider'].update(value=conf_verticalDivider)
        window['cpuDisplay'].update(value=conf_cpuDisplay)
        window['ramDisplay'].update(value=conf_ramDisplay)
        window['gpuDisplay'].update(value=conf_gpuDisplay)
        window['hrDisplay'].update(value=conf_hrDisplay)
        window['sttDisplay'].update(value=conf_sttDisplay)
        window['playTimeDisplay'].update(value=conf_playTimeDisplay)
        window['mutedDisplay'].update(value=conf_mutedDisplay)
        window['unmutedDisplay'].update(value=conf_unmutedDisplay)
        window['darkMode'].update(value=conf_darkMode)
        window['sendBlank'].update(value=sendBlank)
        window['suppressDuplicates'].update(value=suppressDuplicates)
        window['sendASAP'].update(value=sendASAP)
        window['useMediaManager'].update(value=useMediaManager)
        window['useSpotifyApi'].update(value=useSpotifyApi)
        window['spotifySongDisplay'].update(value=spotifySongDisplay)
        window['usePulsoid'].update(value=usePulsoid)
        window['useHypeRate'].update(value=useHypeRate)
        window['hypeRateKey'].update(value=hypeRateKey)
        window['hypeRateSessionId'].update(value=hypeRateSessionId)
        window['timeDisplayAM'].update(value=timeDisplayAM)
        window['timeDisplayPM'].update(value=timeDisplayPM)
        window['showSongInfo'].update(value=showSongInfo)
        window['spotify_client_id'].update(value=spotify_client_id)
        window['useTimeParameters'].update(value=useTimeParameters)
        
        if spotifyLinkStatus != 'Unlinked':
          window['spotifyLinkStatus'].update(value=spotifyLinkStatus)
          if 'Error' in spotifyLinkStatus and not 'Linked' in spotifyLinkStatus:   
            window['spotifyLinkStatus'].update(text_color='red')
            window['linkSpotify'].update(text='Relink Spotify ⚠️', button_color= "red")
          elif 'Unknown' in spotifyLinkStatus:
            window['spotifyLinkStatus'].update(text_color='#c68341')
            window['linkSpotify'].update(text='Unlink Spotify 🔗', button_color= "#c68341")
          else:
            window['spotifyLinkStatus'].update(text_color='green')
            window['linkSpotify'].update(text='Unlink Spotify 🔗', button_color= "#c68341")
          window.write_event_value('Apply', '')    
      except Exception as e:
        outputLog('Failed to update UI\n'+str(e))
        pass
    # Update various parts of the UI on loop until there is a fatal error or some other issue causes the program to stop.
    while run:
      try:
        window['messagePreviewFill'].update(value=msgOutput.replace("\v", "\n"))
        window['runThing'].update(value=playMsg)
        window['afk'].update(value=afk)   
        layoutStorageAccess = window['layoutStorage'].get()
        if layoutStorageAccess != layoutUpdate:
          layoutPreviewBuilder(layoutStorageAccess, window)
          layoutUpdate = layoutStorageAccess
        if playMsg:
          sentTime = sentTime + 0.1    
        if sendSkipped:
          window['sentCountdown'].update('Last sent: '+str(round(sentTime, 1)) +"/"+ "30" +" [Skipped Send]")
        else:
          window['sentCountdown'].update('Last sent: '+str(round(sentTime, 1)) +"/"+ str(conf_message_delay))
        if not playMsg or not 'song(' in conf_layoutString or not showSongInfo:
          window['spotifyPlayStatus'].update(visible=False)
          window['spotifySongName'].update(visible=False)
          window['spotifyDuration'].update(visible=False)
          window['spotifyIcon'].update(visible=False)
      except Exception as e:
        if run:
          pass
          #fatal_error(e)
      if run:
        time.sleep(.1)
  
  updateUIThread = Thread(target=updateUI)
  updateUIThread.start()

  if conf_minimizeOnStart:
    window.minimize()  
  windowAccess = window

  # Config is saved when a window event occurs until the exit event triggers or the window is closed.
  while True:
      event, values = window.read()
      #print(event, values)
      if event == sg.WIN_CLOSED or event == "Exit":
          break
      if event == 'Reset':
          answer = sg.popup_yes_no("Are you sure?\nThis will erase all of your entered text and reset the configuration file!")
          if answer == "Yes":
            resetVars()
      if event == 'Open File':
          message_file_path = sg.popup_get_file('Select a File', title='Select a File')
          window['message_file_path_display'].update(value=message_file_path)
      if event == 'Apply':
          conf_confVersion = version
          conf_message_delay = values['msgDelay']
          conf_messageString = values['messageInput']
          conf_FileToRead = window['message_file_path_display'].get()
          conf_scrollText = values['scroll']
          conf_hideSong = values['hideSong']
          conf_hideOutside = values['hideOutside']
          conf_showPaused = values['showPaused']
          conf_songDisplay = values['songDisplay']
          conf_showOnChange = values['showOnChange']
          conf_songChangeTicks = values['songChangeTicks']
          conf_minimizeOnStart = values['minimizeOnStart']
          conf_keybind_run = window['keybind_run'].get()
          conf_keybind_afk = window['keybind_afk'].get()
          conf_topBar = values['topBar']
          conf_middleBar = values['middleBar']
          conf_bottomBar = values['bottomBar']
          pulsoidToken = values['pulsoidToken']
          whisperModel = values['whisperModel']
          micDevice = values['micDevice']
          conf_avatarHR = values['avatarHR']
          conf_blinkOverride = values['blinkOverride']
          conf_blinkSpeed = values['blinkSpeed']
          conf_useAfkKeybind = values['useAfkKeybind']
          conf_toggleBeat = values['toggleBeat']
          conf_updatePrompt = values['updatePrompt']
          conf_oscListenAddress = values['oscListenAddress']
          conf_oscListenPort = values['oscListenPort']
          conf_oscSendAddress = values['oscSendAddress']
          conf_oscSendPort = values['oscSendPort']
          conf_oscForewordAddress = values['oscForewordAddress']
          conf_oscForewordPort = values['oscForewordPort']
          conf_oscListen = values['oscListen']
          conf_oscForeword = values['oscForeword']
          conf_logOutput = values['logOutput']
          conf_layoutString = values['layoutStorage']
          conf_verticalDivider = values['verticalDivider']
          conf_cpuDisplay = values['cpuDisplay']
          conf_ramDisplay = values['ramDisplay']
          conf_gpuDisplay = values['gpuDisplay']
          conf_hrDisplay = values['hrDisplay']
          conf_sttDisplay = values['sttDisplay']
          conf_playTimeDisplay = values['playTimeDisplay']
          conf_mutedDisplay = values['mutedDisplay']
          conf_unmutedDisplay = values['unmutedDisplay']
          conf_darkMode = values['darkMode']
          sendBlank = values['sendBlank']
          suppressDuplicates = values['suppressDuplicates']
          sendASAP = values['sendASAP']
          useMediaManager = values['useMediaManager']
          useSpotifyApi = values['useSpotifyApi']
          spotifySongDisplay = values['spotifySongDisplay']
          usePulsoid = values['usePulsoid']
          useHypeRate = values['useHypeRate']
          hypeRateKey = values['hypeRateKey']
          hypeRateSessionId = values['hypeRateSessionId']
          timeDisplayAM = values['timeDisplayAM']
          timeDisplayPM = values['timeDisplayPM']
          showSongInfo = values['showSongInfo']
          spotify_client_id = values['spotify_client_id']
          useTimeParameters = values['useTimeParameters']
          try:
            with open('please-do-not-delete.txt', 'w', encoding="utf-8") as f:
              f.write(str([conf_confVersion, conf_message_delay, conf_messageString, conf_FileToRead, conf_scrollText, conf_hideSong, conf_hideOutside, conf_showPaused, conf_songDisplay, conf_showOnChange, conf_songChangeTicks, conf_minimizeOnStart, conf_keybind_run, conf_keybind_afk,conf_topBar, conf_middleBar, conf_bottomBar, pulsoidToken, conf_avatarHR, conf_blinkOverride, conf_blinkSpeed, conf_useAfkKeybind, conf_toggleBeat, conf_updatePrompt, conf_oscListenAddress, conf_oscListenPort, conf_oscSendAddress, conf_oscSendPort, conf_oscForewordAddress, conf_oscForeword, conf_oscListen, conf_oscForeword, conf_logOutput, conf_layoutString, conf_verticalDivider,conf_cpuDisplay, conf_ramDisplay, conf_gpuDisplay, conf_hrDisplay, conf_playTimeDisplay, conf_mutedDisplay, conf_unmutedDisplay, conf_darkMode, sendBlank, suppressDuplicates, sendASAP,useMediaManager, useSpotifyApi, spotifySongDisplay, spotifyAccessToken, spotifyRefreshToken, usePulsoid, useHypeRate, hypeRateKey, hypeRateSessionId, timeDisplayPM, timeDisplayAM, showSongInfo, spotify_client_id, useTimeParameters, whisperModel, micDevice, conf_sttDisplay]))
          except Exception as e:
            sg.popup('Error saving config to file:\n'+str(e))
      if event == 'Check For Updates':
        update_checker(False)
      if event == 'Open Github Page':
        webbrowser.open('https://github.com/Lioncat6/OSC-Chat-Tools')
      if event == 'About':
        about_popop_layout =  [[sg.Text('OSC Chat Tools by', font=('Arial', 11, 'bold'), pad=(0, 20)), sg.Text('Lioncat6', font=('Arial', 12, 'bold'))],[sg.Text('Modules Used:',font=('Arial', 11, 'bold'))], [sg.Text('- PySimpleGUI\n - argparse\n - datetime\n - pythonosc (udp_client)\n - keyboard\n - asyncio\n - psutil\n - webbrowser\n - winsdk (windows.media.control)\n - websocket-client\n - pyperclip')], [sg.Button('Ok')]]
        about_window = sg.Window('About', about_popop_layout, keep_on_top=True)
        event, values = about_window.read()
        about_window.close()
      if event == 'manualHelp':
        manual_help_layout =  [[sg.Column([
          [sg.Text('Manual Editing Guide', font=('Arial', 11, 'bold'))],
          [sg.Text('Warning: Manually editing the layout can cause errors if done incorrectly!', text_color='#e60000')],
          [sg.Text('Note: While putting plain text in the layout editor is supported,\nit will break the visual editor!', text_color="#6699ff", justification='center')],
          [sg.Text('Objects:', font=('Arial', 10, 'bold'))],
          [sg.Text(str(layoutDisplayDict).replace("\"", "").replace("(", "(data)").replace("\'", "").replace(",", "\n").replace("{", "").replace("}", "").replace(": ", " : "), font=('Arial', 11, 'bold'), justification='center')],
          [sg.Text('Data Guide (Defaults to 0):', font=('Arial', 10, 'bold'))],
          [sg.Text("0 : No Data\n1 : Vertical Line\n2 : New Line\n3 : Both Vertical Line and New Line", font=('Arial', 11, 'bold'), justification='center')],
        ],element_justification='center')]                      
        ,[sg.Text()], 
        [sg.Button('Ok')]]
        manual_help_window = sg.Window('About', manual_help_layout, keep_on_top=True)
        event, values = manual_help_window.read()
        manual_help_window.close()
      if event == 'runThing':
        msgPlayToggle()
      if event == 'Open Config File':
        if os.path.isfile('please-do-not-delete.txt'):
          try:
            os.system("start "+ 'please-do-not-delete.txt')
          except Exception as e:
            sg.Popup('Error opening config file: '+e)
        else:
          sg.Popup('Error opening config file: File not found')
      if event == 'Open Debug Log':
        if os.path.isfile('OCT_debug_log.txt'):
          try:
            os.system("start "+ 'OCT_debug_log.txt')
          except Exception as e:
            sg.Popup('Error opening debug log: '+e)
        else:
          sg.Popup('Error opening debug log: File not found')
      if event == 'Discord':
        webbrowser.open('https://discord.com/invite/qeBTyA8uqX')
      if event == 'Submit Feedback':
        webbrowser.open('https://github.com/Lioncat6/OSC-Chat-Tools/issues')
      if event == 'afk':
        afk = values['afk']
      if event == 'run_binding':
        run_binding_layout = [[sg.Text('Press any key to bind to \'Toggle Run\'')],[sg.Text('', key='preview_bind')],[sg.Button('Ok', disabled=True, key='Ok'), sg.Button('Cancel', disabled=True, key='Cancel')]]
        run_binding_window = sg.Window('Bind \'Toggle Run\'', run_binding_layout, size=(300, 90), element_justification='center', no_titlebar=True, modal=True)
        def checkPressThread():
          run_binding_window['preview_bind'].update(value=keyboard.read_key())
          run_binding_window['Ok'].update(disabled=False)
          run_binding_window['Cancel'].update(disabled=False)
        checkThread = Thread(target=checkPressThread)
        checkThread.start()
        while True:
          event, values = run_binding_window.read()
          if event == 'Cancel':
            break
          if event == 'Ok':
            window['keybind_run'].update(value=run_binding_window['preview_bind'].get())
            break
        run_binding_window.close()
      if event == 'afk_binding':
        run_binding_layout = [[sg.Text('Press any key to bind to \'Toggle Afk\'')],[sg.Text('', key='preview_bind')],[sg.Button('Ok', disabled=True, key='Ok'), sg.Button('Cancel', disabled=True, key='Cancel')]]
        run_binding_window = sg.Window('Bind \'Toggle Afk\'', run_binding_layout, size=(300, 90), element_justification='center', no_titlebar=True, modal=True)
        def checkPressThread():
          run_binding_window['preview_bind'].update(value=keyboard.read_key())
          run_binding_window['Ok'].update(disabled=False)
          run_binding_window['Cancel'].update(disabled=False)
        checkThread = Thread(target=checkPressThread)
        checkThread.start()
        while True:
          event, values = run_binding_window.read()
          if event == 'Cancel':
            break
          if event == 'Ok':
            window['keybind_afk'].update(value=run_binding_window['preview_bind'].get())
            break
        run_binding_window.close()
      if event == 'mediaManagerError':
        sg.popup_error('Media Manager Failure. Please restart your system.\n\nIf this problem persists, please report an issue on github: https://github.com/Lioncat6/OSC-Chat-Tools/issues.\nFull Error:\n'+str(values[event]), keep_on_top="True")
        break
      if event == 'heartRateError':
        playMsg = False
        sg.popup('Heart Rate Error:\nAre you connected to the internet?\nPlease double check your token, key, or session id in the behavior tab and then toggle run to try again.\n\nIf this problem persists, please report an issue on github: https://github.com/Lioncat6/OSC-Chat-Tools/issues')
      if event == 'scrollError':
        playMsg = False
        sg.popup('File Read Error: Please make sure you have a file selected to scroll though in the behavior tab, then toggle Run to try again!\nFull Error:\n' + str(values[event]), keep_on_top="True")
      if event == 'updateAvailable':
        update_available_layout = [
              [sg.Column([
                [sg.Text('A new update is available!')],
                [sg.Text(values['updateAvailable']+" > " + version.replace('v', ''))],
                [sg.Text("\nYou can disable this popup in the options tab")]
              ], element_justification='center')],
              [sg.Button("Close"), sg.Button("Download")]]
        updateWindow = sg.Window('Update Available!', update_available_layout, finalize=True)
        while run:
          event, values = updateWindow.read()
          if event == sg.WIN_CLOSED or event == 'Close':
            updateWindow.close()
            break
          if event == 'Download':
            webbrowser.open('https://github.com/Lioncat6/OSC-Chat-Tools/releases/latest')
      if event == 'markOutOfDate':
        if not "Update" in window['versionText'].get():
          window['versionText'].update(value=window['versionText'].get()+" - New Update Available")
      if event == 'popup':
        sg.popup(values['popup'])
      if event == 'FAQ':
        webbrowser.open('https://github.com/Lioncat6/OSC-Chat-Tools/wiki/FAQ')
      if event == 'outputSend':
        current_text = values['output']
        if current_text == '':
          new_text = values[event]
        else:
          new_text = current_text + '\n' + values[event]
        window['output'].update(new_text)
      if event == 'listenError':
        outputLog(f'listenError {str(values[event])}')
        conf_oscListen = False
        conf_oscForeword = False
        window['oscListen'].update(value=False)
        window['oscForeword'].update(value=False)
        sg.popup('Please make sure no other program is listening to the osc and try re-enabling osc Listen/Foreword options.\n\nOSC Listen and Foreword have been disabled to this won\'t happen on startup')
        window.write_event_value('Apply', '')
      def layoutStorageAdd(a):
        if len(ast.literal_eval("["+window['layoutStorage'].get().replace("{", "\"").replace("}", "\",")[:-1]+"]")) < 15:
          window['layoutStorage'].update(value=values['layoutStorage']+" {"+a+"}")
        else:
          sg.popup("You have reached the limit of objects in the layout.\nYou can still add more in the manual edit section,\nhowever the UI will not reflect it")
      if event == 'addText':
        layoutStorageAdd("text(0)")
      if event == 'addTime':
        layoutStorageAdd("time(0)")
      if event == 'addSong':
        layoutStorageAdd("song(0)")
      if event == 'addCPU':
        layoutStorageAdd("cpu(0)")
      if event == 'addRAM':
        layoutStorageAdd("ram(0)")
      if event == 'addGPU':
        layoutStorageAdd("gpu(0)")
      if event == 'addHR':
        layoutStorageAdd("hr(0)")
      if event == 'addMute':
        layoutStorageAdd("mute(0)")
      if event == 'addSTT':
        layoutStorageAdd("stt(0)")
      if event == 'addDiv':
        layoutStorageAdd("div(0)")
      if event == 'addPlaytime':
        layoutStorageAdd("playtime(0)")
      def layoutMove(pos, up):
        layList = ast.literal_eval("["+window['layoutStorage'].get().replace("{", "\"").replace("}", "\",")[:-1]+"]")
        pos = pos-1
        if up:
          layList.insert(pos-1, layList.pop(pos))
        else:
          layList.insert(pos+1, layList.pop(pos))
        window['layoutStorage'].update(value=str(layList).replace("[", "").replace("\']", "}").replace("\"]", "}").replace("\",", "}").replace("\',", "}").replace("\"", "{").replace("\'", "{").replace("]", ""))
      def toggleValues(pos, data):
        layList = ast.literal_eval("["+window['layoutStorage'].get().replace("{", "\"").replace("}", "\",")[:-1]+"]")
        pos = pos-1
        editpos = layList[pos].find("(")+1
        if data == 1:
          layList[pos] = layList[pos][:editpos] + '1' + layList[pos][editpos+1:]
        elif data == 2:
          layList[pos] = layList[pos][:editpos] + '2' + layList[pos][editpos+1:]
        elif data == 3:
          layList[pos] = layList[pos][:editpos] + '3' + layList[pos][editpos+1:]
        else:
          layList[pos] = layList[pos][:editpos] + '0' + layList[pos][editpos+1:]
        if layList[pos][editpos+1:editpos+2] != ")":
          layList[pos] = layList[pos][:editpos+1] + ')' + layList[pos][editpos+1:]
        window['layoutStorage'].update(value=str(layList).replace("[", "").replace("\']", "}").replace("\"]", "}").replace("\",", "}").replace("\',", "}").replace("\"", "{").replace("\'", "{").replace("]", ""))
      for x in range(1, 16):
        try:
          if event == "delete"+str(x):
            listMod = ast.literal_eval("["+window['layoutStorage'].get().replace("{", "\"").replace("}", "\",")[:-1]+"]")
            del listMod[x-1]
            window['layoutStorage'].update(value=str(listMod).replace("[", "").replace("\']", "}").replace("\"]", "}").replace("\",", "}").replace("\',", "}").replace("\"", "{").replace("\'", "{").replace("]", ""))
          if event == "up"+str(x):
            layoutMove(x, True)
          if event == "down"+str(x):
            layoutMove(x, False)
          if event == "divider"+str(x) or event == "newLine"+str(x):
            if values['divider'+str(x)] and values['newLine'+str(x)]:
              toggleValues(x, 3)
            elif values['divider'+str(x)] and (not values['newLine'+str(x)]):
              toggleValues(x, 1)
            elif (not values['divider'+str(x)]) and values['newLine'+str(x)]:
              toggleValues(x, 2)
            else:
              toggleValues(x, 0)
        except Exception as e:
          pass
      if event == 'Copy':
        keyboard.press_and_release('ctrl+c')
      if event == 'Paste':
        keyboard.press_and_release('ctrl+v')
      if event == 'getPulsoidToken':
        webbrowser.open('https://pulsoid.net/oauth2/authorize?response_type=token&client_id=8070496f-f886-4030-8340-96d1d68b25cb&redirect_uri=&scope=data:heart_rate:read&state=&response_mode=web_page')
      if event == 'getHypeRateKey':
        webbrowser.open('https://github.com/Lioncat6/OSC-Chat-Tools/wiki/HypeRate-Keys')
      if event == 'loadModel':
        audio_model = whisper.load_model(whisperModel)
      if event == 'useSpotifyApi':
        if spotifyAccessToken != '':
          window['useSpotifyApi'].update(value=True)
          window['useMediaManager'].update(value=False)
        else:
          sg.popup('Please link Spotify first!')
          window['useSpotifyApi'].update(value=False)
      if event == 'useMediaManager':
        window['useMediaManager'].update(value=True)
        window['useSpotifyApi'].update(value=False)
      if event == 'useHypeRate':
        if hypeRateSessionId != '':
          window['useHypeRate'].update(value=True)
          window['usePulsoid'].update(value=False)
        else:
          sg.popup('Please add a hyperate session id first!')
          window['useHypeRate'].update(value=False)
      if event == 'usePulsoid':
        window['usePulsoid'].update(value=True)
        window['useHypeRate'].update(value=False)
      if event == 'linkSpotify':
        isError = True
        isLink = True
        if "Unlinked" in spotifyLinkStatus or "Error" in spotifyLinkStatus:
          linking_layout = [[sg.Text('')],[sg.Text('Linking Spotify...')],[sg.Button('Cancel'), sg.Button('Manual Code Entry')]]
          spotify_link_window = sg.Window('Linking Spotify...', linking_layout, size=(300, 90), element_justification='center', no_titlebar=True, modal=True)
          global linkedUserName
          linkedUserName = 'Canceled'
          def spotifyLinkManager():
            global linking
            global linkedUserName
            linkedUserName = linkSpotify()
            linking = False
            try:
              spotify_link_window.write_event_value('done', 'done') 
            except Exception as e:
              pass
          spotifyLinkThread = Thread(target=spotifyLinkManager).start()
          linking = True
          while linking:
            event, values = spotify_link_window.read()
            if event == 'Cancel':
              cancelLink = True
              linking = False
              break
            elif event == 'Manual Code Entry':
              manualCode = ''
              manualOverrideLayout = [[sg.Text('')],[sg.Text('Manual Code Entry')],[sg.Input(key='manualCode', size=(30, 1))],[sg.Button('Enter'), sg.Button('Cancel')]]
              manualOverrideWindow = sg.Window('Manual Code Entry', manualOverrideLayout, size=(300, 120), element_justification='center', no_titlebar=False, modal=True,)
              while linking:
                event, values = manualOverrideWindow.read()
                if event == 'Cancel':
                  break
                if event == 'Enter':
                  manualCode = values["manualCode"]
                  break
              manualOverrideWindow.close()
              if manualCode:
                try:
                  def getAccessToken(code):
                    token_url = 'https://accounts.spotify.com/api/token'
                    data = {
                        'grant_type': 'authorization_code',
                        'code': code,
                        'redirect_uri': spotify_redirect_uri,
                        'client_id': spotify_client_id,      
                        'code_verifier': code_verifier
                    }
                    response = requests.post(token_url, data=data)
                    if response.status_code != 200:
                      raise Exception('Access token fetch error '+str(response.status_code)+' : '+response.text)
                    spotifyRefreshToken = response.json().get('refresh_token')
                    return response.json().get('access_token')
                  
                  spotifyAccessToken = getAccessToken(manualCode)
                  
                  def get_profile(accessToken):
                      headers = {
                          'Authorization': 'Bearer ' + accessToken,
                      }

                      response = requests.get('https://api.spotify.com/v1/me', headers=headers)
                      if response.status_code != 200:
                        raise Exception('Profile fetch error '+str(response.status_code)+' : '+response.text)
                      data = response.json()
                      return data
                  profile = get_profile(spotifyAccessToken)
                  nameToReturn = profile.get('display_name')
                  sg.popup("Spotify linked to "+nameToReturn+" successfully via manual code entry!")
                  outputLog("Spotify linked to "+nameToReturn+" successfully via manual code entry!")
                  window['spotifyLinkStatus'].update(value='Linked to '+nameToReturn)
                  spotifyLinkStatus = 'Linked to '+nameToReturn
                  window['spotifyLinkStatus'].update(text_color='green')
                  window['linkSpotify'].update(text='Unlink Spotify 🔗', button_color= "#c68341")
                  useMediaManager = False
                  useSpotifyApi = True
                  window['useSpotifyApi'].update(value=True)
                  window['useMediaManager'].update(value=False)
                  window.write_event_value('Apply', '')
                  isError = False
                  isLink = False
                except Exception as e:
                  linkedUserName = "Error"
                  useSpotifyApi = False
                  window['spotifyLinkStatus'].update(value='Authentication Error')
                  spotifyLinkStatus = 'Authentication Error'
                  window['spotifyLinkStatus'].update(text_color='red')
                  window['linkSpotify'].update(text='Relink Spotify ⚠️', button_color= "red")
                  cancelLink = True
                  sg.popup("Manual Linking Error "+ str(e))
                  outputLog("Manual Linking Error "+ str(e))
              else:
                isLink = False
                linkedUserName = 'Canceled'
                cancelLink = True
                sg.popup("Canceled!")
                break
            else:
              linking = False
              break
          
          spotify_link_window.close()
          window.write_event_value('Apply', '')
          if linkedUserName == 'Error' and isError:
            window['spotifyLinkStatus'].update(value='Authentication Error')
            spotifyLinkStatus = 'Authentication Error'
            window['spotifyLinkStatus'].update(text_color='red')
            window['linkSpotify'].update(text='Relink Spotify ⚠️', button_color= "red")
          elif linkedUserName == 'Canceled':
            pass
          elif isLink:
            window['spotifyLinkStatus'].update(value='Linked to '+linkedUserName)
            spotifyLinkStatus = 'Linked to '+linkedUserName
            window['spotifyLinkStatus'].update(text_color='green')
            window['linkSpotify'].update(text='Unlink Spotify 🔗', button_color= "#c68341")
            useMediaManager = False
            useSpotifyApi = True
            window['useSpotifyApi'].update(value=True)
            window['useMediaManager'].update(value=False)
            window.write_event_value('Apply', '')
        else:    
          spotifyAccessToken = ''
          spotifyRefreshToken = ''
          spotifyLinkStatus = 'Unlinked'
          window['useSpotifyApi'].update(value=False)
          window['useMediaManager'].update(value=True)
          useSpotifyApi = False
          useMediaManager = True
          window.write_event_value('Apply', '')
          window['spotifyLinkStatus'].update(value=spotifyLinkStatus)
          window['spotifyLinkStatus'].update(text_color='orange')
          window['linkSpotify'].update(text="Link Spotify 🔗", button_color="#00a828")
      if event == 'spotifyApiError':
        retryError = "No"
        if useSpotifyApi:
          retryError = sg.popup_yes_no('A Spotify fetch error has occurred, would you like to retry?\n\nThis could be caused by an internet connection issue.')
        if retryError == "Yes":
          pass
        elif useSpotifyApi:
          window['useSpotifyApi'].update(value=False)
          window['useMediaManager'].update(value=True)
          useSpotifyApi = False
          useMediaManager = True
          spotifyLinkStatus = 'Error - Please Relink!'
          spotifyAccessToken = ''
          spotifyRefreshToken = ''
          window.write_event_value('Apply', '')
          outputLog("Spotify api fetch error! Please relink!\nFull Error: "+str(values[event]))
          window['spotifyLinkStatus'].update(value=spotifyLinkStatus)
          window['spotifyLinkStatus'].update(text_color='red')
          window['linkSpotify'].update(text='Relink Spotify ⚠️', button_color= "red")
          sg.popup('Spotify api fetch error!\nAutomatically reverted to using Windows Now Playing\nPlease relink spotify in the behavior tab to continue...\nFull Error: '+str(values[event]))
      if event == 'sendDebug':
        try:
          valueToSend = eval("values['debugType'](values['debugValue'])")
          client.send_message(values['debugPath'], valueToSend)
          outputLog(f"{values['debugPath']} => {values['debugValue']} | {type(valueToSend)}")
        except Exception as e:
          outputLog(f"Error sending debug command for reason: {e}")
      if event == 'updateSpotifySongName':
        if showSongInfo:
          nameToDisplay = values[event][0] + ' ᵇʸ ' +values[event][4]
          playPause = values[event][1]
          elapsedTime = values[event][2]
          duration = values[event][3]
          if len(nameToDisplay) >30:
            nameToDisplay = nameToDisplay[:30]+"..."
          if playPause:
            window['spotifyPlayStatus'].update(value='▶️', visible=True)
          else:
            window['spotifyPlayStatus'].update(value='⏸️', visible=True)
          window['spotifySongName'].update(value=nameToDisplay, visible=True)
          if useSpotifyApi:
            window['spotifyDuration'].update(value=f'『{elapsedTime}/{duration}』', visible=True)
            window['spotifyIcon'].update(visible=True)
          else:
            window['spotifyDuration'].update(visible=False)
            window['spotifyIcon'].update(visible=False)
      if event == 'spotifySongName':
        try:
          if spotifySongUrl != '':
            webbrowser.open(spotifySongUrl)
        except Exception as e:
          pass
      if event == 'client_id_help':
        webbrowser.open('https://github.com/Lioncat6/OSC-Chat-Tools/wiki/Spotify-Client-ID')
      if event == 'Restart':
        sg.popup('Implementing this would take way too long.')
  window.close()
  playMsg = False
  run = False
  try:
    listenServer.shutdown()
    listenServer.server_close()
  except:
    pass
  if conf_logOutput:
    with open('OCT_debug_log.txt', 'a+', encoding="utf-8") as f:
        f.write("\n"+str(datetime.now())+" OCT Shutting down...")

def processMessage(a):
  returnList = []
  if conf_messageString.count('\n')>0:
    posForLoop = 0
    for x in range(conf_messageString.count('\n')):
      returnList.append(conf_messageString[posForLoop:conf_messageString.find('\n', posForLoop+1)].replace('\n', ''))
      posForLoop = conf_messageString.find('\n', posForLoop+1)
    returnList.append(conf_messageString[posForLoop:len(conf_messageString)].replace('\n', ''))
  else:
    returnList.append(conf_messageString)
  return returnList

if __name__ == "__main__":
  def oscClientDef():
    global client
    while run:
      parser2 = argparse.ArgumentParser()
      parser2.add_argument("--ip", default=conf_oscSendAddress,
          help="The ip of the OSC server")
      parser2.add_argument("--port", type=int, default=conf_oscSendPort,
          help="The port the OSC server is listening on")
      args2 = parser2.parse_args()                                                                                        

      client = udp_client.SimpleUDPClient(args2.ip, args2.port)
      time.sleep(.5)
  oscClientDefThread = Thread(target=oscClientDef)
  oscClientDefThread.start()

  dispatcher = Dispatcher()
  dispatcher.map("/avatar/parameters/AFK", afk_handler)
  dispatcher.map("/avatar/parameters/VRMode", vr_handler) # The game never sends this value from what I've seen
  dispatcher.map("/avatar/parameters/MuteSelf", mute_handler)
  #dispatcher.map("/avatar/parameters/InStation", inSeat_handler)
  #dispatcher.map("/avatar/parameters/Voice", volume_handler)
  #dispatcher.map("/avatar/parameters/Earmuffs", usingEarmuffs_handler)
  dispatcher.map("/avatar/parameters/Boop", boop_handler)
  dispatcher.map("/avatar/parameters/boop", boop_handler)
  dispatcher.map("/avatar/parameters/Booped", boop_handler)
  dispatcher.map("/avatar/parameters/Contact/Receiver/Boop", boop_handler)
  dispatcher.map("/avatar/parameters/HeadPat", pat_handler)
  dispatcher.map("/avatar/parameters/Pat", pat_handler)
  dispatcher.map("/avatar/parameters/PatBool", pat_handler)
  dispatcher.map("/avatar/parameters/Headpat", pat_handler)
  dispatcher.map("/avatar/parameters/Contact/Receiver/Pat", pat_handler)

  def oscForwardingManager():
    global runForewordServer
    global oscListenAddressMemory
    global oscListenPortMemory
    global oscForewordAddressMemory
    global oscForewordPortMemory
    global conf_oscForeword
    global conf_oscListen
    global useForewordMemory
    global windowAccess
    time.sleep(.1)
    listen_socket = None
    forward_sockets = []
    while run:
        global runForewordServer
        global oscListenAddressMemory
        global oscListenPortMemory
        global oscForewordAddressMemory
        global oscForewordPortMemory
        global conf_oscForeword
        global conf_oscListen
        global useForewordMemory
        global windowAccess
        # Create a socket to listen for incoming data
        def create_sockets():
            nonlocal listen_socket
            global runForewordServer
            global oscListenAddressMemory
            global oscListenPortMemory
            global oscForewordAddressMemory
            global oscForewordPortMemory
            global conf_oscForeword
            global conf_oscListen
            global useForewordMemory
            global windowAccess
            try:
                listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                listen_socket.bind((conf_oscListenAddress, int(conf_oscListenPort)))
                listen_socket.settimeout(.5)
            except Exception as err:
                def WaitThread(err):
                    while windowAccess == None:
                        time.sleep(.1)
                        pass
                    windowAccess.write_event_value('listenError', str(err))
                updatePromptWaitThreadHandler = Thread(target=WaitThread, args=(err,)).start()

        # Set the IP addresses and port numbers to forward data to
        if conf_oscForeword:
            forward_addresses = [
                ('127.0.0.1', 61394), #for the listen server
                (conf_oscForewordAddress, int(conf_oscForewordPort)),
            ]
        else:
            forward_addresses = [
                ('127.0.0.1', 61394) #for the listen server
            ]

        def dataSender():
            global runForewordServer
            global oscListenAddressMemory
            global oscListenPortMemory
            global oscForewordAddressMemory
            global oscForewordPortMemory
            global conf_oscForeword
            global conf_oscListen
            global useForewordMemory
            global windowAccess
            nonlocal forward_sockets
            runForewordServer = True
            #print('Starting Forwarding server on '+str(forward_addresses))
            create_sockets()
            outputLog('Starting Forwarding server on '+str(forward_addresses))
            oscListenAddressMemory = conf_oscListenAddress
            oscListenPortMemory = conf_oscListenPort
            oscForewordPortMemory = conf_oscForewordPort
            oscForewordAddressMemory = conf_oscForewordAddress
            useForewordMemory = conf_oscForeword
            forward_sockets = [
              socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
              for _ in forward_addresses
            ]
            while run and runForewordServer:
                try:
                    data, addr = listen_socket.recvfrom(1024)

                    # Forward the data to each forward socket
                    if 'Contact' in str(data):
                      print(data)
                    for forward_socket, (ip, port) in zip(forward_sockets, forward_addresses):
                        forward_socket.sendto(data, (ip, port))
                except Exception as e:
                  time.sleep(.01)
                  pass
                

        if conf_oscForeword:
            if not runForewordServer:
              if forewordServerLastUsed != conf_oscForeword:
                outputLog("Foreword Server Toggled On... Waiting For Listen Server To Change Ports...")
                time.sleep(3)
              else:
                dataSenderThread = Thread(target=dataSender)
                dataSenderThread.start()
        time.sleep(.1)
        if oscListenAddressMemory != conf_oscListenAddress or oscListenPortMemory != conf_oscListenPort or oscForewordPortMemory != conf_oscForewordPort or oscForewordAddressMemory != conf_oscForewordAddress or useForewordMemory != conf_oscForeword or useForewordMemory != conf_oscForeword:
            if conf_oscForeword:
                #print('Foreword/Listen Server Config Updated, Restarting Forwarding Server...\n')
                outputLog('Foreword/Listen Server Config Updated, Restarting Forwarding Server...\n')
                runForewordServer = False
                time.sleep(.5)
                if not runForewordServer:
                    dataSenderThread = Thread(target=dataSender)
                    dataSenderThread.start()
        if runForewordServer and not(conf_oscForeword):
            if listen_socket is not None:
                listen_socket.close()
            for forward_socket in forward_sockets:
                forward_socket.close()
            runForewordServer = False
            #print('No OSC Foreword/Listening Options are selected, stopping Forwarding Server...')
            outputLog('No OSC Foreword/Listening Options are selected, stopping Forwarding Server...')
        time.sleep(.5)

    # Close all sockets on shutdown
    if listen_socket is not None:
        listen_socket.close()
    for forward_socket in forward_sockets:
        forward_socket.close()
  oscForwardingManagerThread = Thread(target=oscForwardingManager)
  oscForwardingManagerThread.start()
  def oscListenServerManager():
      global conf_oscListenAddress
      global conf_oscListenPort
      global conf_oscListen
      global isListenServerRunning
      global forewordServerLastUsed
      while run:
          if conf_oscListen:
              parser = argparse.ArgumentParser()
              if conf_oscForeword:
                parser.add_argument("--ip",
                  default='127.0.0.1', help="The ip to listen on")
                parser.add_argument("--port",
                    type=int, default=61394, help="The port to listen on")
              else:
                parser.add_argument("--ip",
                  default=conf_oscListenAddress, help="The ip to listen on")
                parser.add_argument("--port",
                    type=int, default=conf_oscListenPort, help="The port to listen on")
              args = parser.parse_args()
              def listenServerThread():
                  global isListenServerRunning
                  global conf_oscListenAddress
                  global conf_oscListenPort
                  global listenServer
                  try:
                      if conf_oscForeword:
                        location = "127.0.0.1:61394"
                      else:
                        location = f"{str(conf_oscListenAddress)}:{str(conf_oscListenPort)}"
                      outputLog('Attempting To Start Listen Server on '+location)
                      listenServer = osc_server.ThreadingOSCUDPServer(
                          (args.ip, args.port), dispatcher)
                      #print("Osc Listen Server Serving on {}".format(listenServer.server_address))
                      outputLog("Osc Listen Server Serving on {}".format(listenServer.server_address))
                      sockett = listenServer.socket
                      sockett.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                      
                      isListenServerRunning = True
                      
                      listenServer.serve_forever()           
                  except Exception as e:
                      #print('Osc Listen Server Failed to Start, Retying...'+str(e))
                      outputLog(f'Osc Listen Server Failed to Start, Retying...\nPlease make sure another program isn\'t using {location}\n'+str(e))
                      pass

              if not isListenServerRunning:
                  oscServerThread = Thread(target=listenServerThread)
                  oscServerThread.start()
          if not conf_oscListen and isListenServerRunning:
            #print('No OSC Listen Options are Selected, Shutting Down OSC Listen Server...')
            outputLog('No OSC Listen Options are Selected, Shutting Down OSC Listen Server...')
            isListenServerRunning = False
            listenServer.shutdown()
            listenServer.server_close()
          if conf_oscForeword != forewordServerLastUsed  and isListenServerRunning:
            outputLog('Foreword Server Toggled, Restarting Listen Server...')
            isListenServerRunning = False
            try:
              listenServer.shutdown()
              listenServer.server_close()
            except:
              pass
            forewordServerLastUsed = conf_oscForeword
          time.sleep(.5)

  oscServerManagerThread = Thread(target=oscListenServerManager)
  oscServerManagerThread.start()

  
  
  def sendMsg(a):
    global msgOutput
    global conf_message_delay
    global conf_messageString
    global playMsg
    global run
    global songName
    global conf_songDisplay
    global conf_songChangeTicks
    global tickCount
    global conf_topBar
    global conf_middleBar
    global conf_bottomBar
    global pulsoidToken
    global whisperModel
    global micDevice
    global conf_avatarHR
    global conf_blinkOverride
    global conf_blinkSpeed
    global conf_useAfkKeybind
    global conf_toggleBeat
    global conf_layoutString
    global conf_verticalDivider
    global conf_cpuDisplay
    global conf_ramDisplay
    global conf_gpuDisplay
    global conf_hrDisplay
    global conf_sttDisplay
    global conf_playTimeDisplay
    global conf_mutedDisplay
    global conf_unmutedDisplay
    global playTimeDat
    global timeDisplayAM
    global timeDisplayPM
    #stupid crap
    global letsGetThatTime
    global songInfo
    global cpuDat
    global ramDat
    global hrInfo
    global gpuDat
    global lastSent
    global sentTime
    global sendSkipped
    #end of stupid crap
    global timeVar
    timeVar = time.time()
    if playMsg:
      #message Assembler:
      if not conf_scrollText and not afk:
        
        def msgGen(a):
          global conf_verticalDivider
          global letsGetThatTime
          global songInfo
          global cpuDat
          global ramDat
          global hrInfo
          global sttOutput
          global msgOutput
          global conf_hideSong
          global conf_showPaused
          global gpuDat
          global timeVar
          global useSpotifyApi
          global useMediaManager
          global timeDisplayAM
          global timeDisplayPM
          def checkData(msg, data):
            lf = "\v"
            if data == 1 or data == 3:
              msg = msg + " " + conf_verticalDivider
            if data == 2 or data == 3:
              msg =  msg + lf
            return msg
          def time(data=0):
            global timeDisplayAM
            global timeDisplayPM
            now = datetime.now()
            hour24 = now.strftime("%H")
            hour = now.strftime("%H")
            minute = now.strftime("%M")
            time_zone = datetime.now().astimezone().tzname()
            if time_zone == 'Central Daylight Time':
              time_zone = 'CDT'
            if int(hour) >= 12:
                hour = int(hour)-12
                if int(hour) == 0:
                  hour = 12 
                letsGetThatTime = timeDisplayPM.format_map(defaultdict(str, hour=hour, minute=minute, time_zone=time_zone, hour24=hour24))     
            else:
                if int(hour) == 0:
                  hour = 12 
                letsGetThatTime = timeDisplayAM.format_map(defaultdict(str, hour=hour, minute=minute, time_zone=time_zone, hour24=hour24))       
            return(checkData(letsGetThatTime, data))
          def text(data=0):
            return(checkData(a.replace("\\n", "\v").replace("\\v", "\v"), data))
          def song(data=0):
            global songInfo
            global useSpotifyApi
            global useMediaManager
            global spotifyLinkStatus
            global spotifyAccessToken
            global spotifyRefreshToken
            global spotifyPlayState
            if useMediaManager:
              try:
                current_media_info = asyncio.run(get_media_info())
                artist = current_media_info['artist']
                title = current_media_info['title']
                album_title = current_media_info['album_title'] 
                album_artist = current_media_info['album_artist'] 
                mediaPlaying = mediaIs('PLAYING')
              except Exception as e:
                artist = ''
                title = ''
                album_title = ''
                album_artist = ''
                mediaPlaying = False
                if 'TARGET_PROGRAM' in str(e):
                  #outputLog('Can\'t get media info, please make sure an application is playing audio')
                  pass
                else:
                  if windowAccess != None:
                    try:
                        outputLog('mediaManagerError '+str(e))
                        windowAccess.write_event_value('mediaManagerError', e)
                    except:
                      pass
              if mediaPlaying or (not conf_showPaused):
                songInfo = conf_songDisplay.format_map(defaultdict(str, artist=artist,title=title,album_title=album_title, album_artist=album_artist))
              else:
                songInfo=conf_songDisplay.format_map(defaultdict(str, artist=artist,title=title,album_title=album_title, album_artist=album_artist))+" ⏸️"
                
            else:
              def formatTime(seconds = 0):
                  minutes = int(seconds // 60)
                  remaining_seconds = int(seconds % 60)
                  return f"{minutes}:{remaining_seconds:02}"
              global spotifySongDisplay
              playState = spotifyPlayState
              
              if playState != None and playState != '': 
                try:
                  artist = playState.get('item').get('artists')[0].get('name')
                  title = playState.get('item').get('name')
                  album_title = playState.get('item').get('album').get('name')
                  album_artist = playState.get('item').get('artists')[0].get('name')
                  song_progress = formatTime(playState.get('progress_ms')/1000)
                  song_length = formatTime(playState.get('item').get('duration_ms')/1000)
                  volume = str(playState.get('device').get('volume_percent'))
                  song_id = playState.get('item').get('id')
                  mediaPlaying = playState.get('is_playing')
                except:
                  artist = ''
                  title = ''
                  album_title = ''
                  album_artist = '' 
                  song_progress = formatTime(0)
                  song_length = formatTime(0)
                  volume = '0'
                  song_id = 'N/A'
                  mediaPlaying = False
              else:
                artist = ''
                title = ''
                album_title = ''
                album_artist = '' 
                song_progress = formatTime(0)
                song_length = formatTime(0)
                volume = '0'
                song_id = 'N/A'
                mediaPlaying = False

              if mediaPlaying or (not conf_showPaused):
                songInfo = spotifySongDisplay.format_map(defaultdict(str, artist=artist,title=title,album_title=album_title, album_artist=album_artist, song_progress=song_progress, song_length=song_length, volume=volume, song_id=song_id))
              else:
                songInfo=spotifySongDisplay.format_map(defaultdict(str, artist=artist,title=title,album_title=album_title, album_artist=album_artist, song_progress=song_progress, song_length=song_length, volume=volume, song_id=song_id))+"⏸️"
            global spotifySongUrl
            try:
              if useSpotifyApi:
                spotifySongUrl = playState.get('item').get('external_urls').get('spotify')
                windowAccess.write_event_value('updateSpotifySongName', [title, mediaPlaying, song_progress, song_length, artist])
              else:
                spotifySongUrl = ''
                windowAccess.write_event_value('updateSpotifySongName', [title, mediaPlaying, 0, 0, artist])
            except Exception as e:
              #print(e)
              pass
            
            global conf_showOnChange
            global conf_songChangeTicks
            global tickCount
            #global songInfo
            global songName
            if conf_hideSong and not mediaPlaying or title == '':
              return ''
            else:
              if conf_showOnChange:
                if songInfo != songName:
                  tickCount = conf_songChangeTicks
                  songName = songInfo
                if tickCount != 0:
                  tickCount = tickCount-1
                  return(checkData(songInfo, data))
                else:
                  return ''
              else:
                return(checkData(songInfo, data))
          def cpu(data=0):
            cpu_percent = str(psutil.cpu_percent())
            cpuDat = conf_cpuDisplay.format_map(defaultdict(str, cpu_percent=cpu_percent))
            return (checkData(cpuDat, data))
          def ram(data=0): 
            psutilVirtualMemory = psutil.virtual_memory()
            ram_percent = str(int(psutilVirtualMemory[2]))
            ram_used = str(round(int(psutilVirtualMemory[0])/1073741824-int(psutilVirtualMemory[1])/1073741824, 1))
            ram_available = str(round(int(psutilVirtualMemory[1])/1073741824, 1))
            ram_total = str(round(int(psutilVirtualMemory[0])/1073741824, 1))
            ramDat = conf_ramDisplay.format_map(defaultdict(str, ram_percent=ram_percent, ram_available=ram_available, ram_total=ram_total, ram_used=ram_used))
            return (checkData(ramDat, data))
          def gpu(data=0):
            try:
              nvmlInit()
              handle = nvmlDeviceGetHandleByIndex(0)
              info = nvmlDeviceGetUtilizationRates(handle)
              #print(info)
              gpu_percent = info.gpu
              vram_percent = info.memory
              nvmlShutdown()
            except:
              gpu_percent = "0"
              vram_percent = "0"
            #gpu_percent = str(round((GPUtil.getGPUs()[0].load*100), 1))
            #gpu_percent = "0"
            gpuDat = conf_gpuDisplay.format_map(defaultdict(str, gpu_percent=gpu_percent, vram_percent=vram_percent))
            return (checkData(gpuDat, data))
          def hr(data=0):
            hr = str(heartRate)
            if hr == "0" or hr == "1":
              hr = "-"
            hrInfo = conf_hrDisplay.format_map(defaultdict(str, hr=hr))
            return (checkData(hrInfo, data))
          def mute(data=0):
            return (checkData("Mute Coming Soon", data))
          def stt(data=0):
            stt = " ".join(map(str, sttOutput[-2:]))
            if stt == None:
              stt = '-'
            sttInfo = conf_sttDisplay.format_map(defaultdict(str, stt=stt))
            return checkData(sttInfo, data)
          def div(data=0):
            return (checkData(conf_middleBar, data))
          def mute(data=0):
            if isMute: 
              return (checkData(conf_mutedDisplay, data))
            else:
              return (checkData(conf_unmutedDisplay, data))
          def playtime(data=0):
            global timeVar
            try:
              minutes = int((timeVar-playTimeDat)/60)
              hours, remainder_minutes = divmod(minutes, 60)
              if vrcPID == None:
                minutes = 0
                hours = 0
                remainder_minutes = 0
            except Exception as e:
              minutes = 0
              hours = 0
              remainder_minutes = 0
            playDat = conf_playTimeDisplay.format_map(defaultdict(str, hours="{:02d}".format(hours), remainder_minutes="{:02d}".format(remainder_minutes), minutes="{:02d}".format(minutes)))
            return(checkData(playDat, data))
          try:
            msgOutput = eval("f'"f'{conf_layoutString}'"'")
          except Exception as e:
            msgOutput = "Layout Error!\v"+str(e)
          if msgOutput[-len(conf_verticalDivider+" "):] == conf_verticalDivider+" ":
            msgOutput = msgOutput[:-len(conf_verticalDivider+" ")-1]
          if msgOutput[-len(conf_middleBar+" "):] == conf_middleBar+" ":
            msgOutput = msgOutput[:-len(conf_middleBar+" ")]
          if "\v " in msgOutput[-2:]:
            msgOutput = msgOutput[:-2]
          if "\v" in msgOutput[-2:]:
            msgOutput = msgOutput[:-1]
          if not conf_hideOutside:
            msgOutput = conf_topBar + " "+ msgOutput + " " +conf_bottomBar 
          msgOutput = msgOutput.replace("\\n", "\v").replace("\\v", "\v")
        msgGen(a)
      elif afk:
        msgOutput = conf_topBar+a+conf_bottomBar
      else:
        msgOutput = a
      if playMsg:
        if (str(msgOutput) != lastSent) or (not suppressDuplicates) or sentTime > 30:
          client.send_message("/chatbox/input", [ str(msgOutput), True, False])
          lastSent = str(msgOutput)
          sentTime = 0
          sendSkipped = False
        else:
          sendSkipped = True
      msgDelayMemory = conf_message_delay
      for x in range(int(conf_message_delay*10)):
        if not playMsg or not run or ((msgDelayMemory != conf_message_delay) and sendASAP) or sendSkipped == True:
          break
        time.sleep(.1)

def timeParameterUpdate():
  while run:
    global useTimeParameters
    if useTimeParameters:
      now = datetime.now()
      hour = now.strftime("%H")
      minute = now.strftime("%M")
      second = now.strftime("%S")
      isPm = False
      if int(hour) >= 12:
          hour = int(hour)-12
          if int(hour) == 0:
            hour = 12    
            isPm = True
      else:
          if int(hour) == 0:
            hour = 12  
          isPm = False
      try:
        client.send_message("/avatar/parameters/Hours", int(hour))
        client.send_message("/avatar/parameters/Minutes", int(minute))
        client.send_message("/avatar/parameters/Seconds", int(second))
        client.send_message("/avatar/parameters/Period", isPm)
      except Exception as e:
        outputLog("Error sending time parameters:\n"+str(e))
    time.sleep(1)

# Get available microphone devices
p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
num_devices = info.get('deviceCount')

mic_devices = []
for i in range(num_devices):
    device_info = p.get_device_info_by_host_api_device_index(0, i)
    if device_info.get('maxInputChannels') > 0:
        mic_devices.append(device_info.get('name'))
audio_model = whisper.load_model(whisperModel)
phrase_time = None
record_timeout = 2
phrase_timeout = 3
audio_data_queue = Queue()
source = sr.Microphone(sample_rate=16000, device_index=3)
r = sr.Recognizer()
r.energy_threshold = 1000
r.dynamic_energy_threshold = False
#with source:
#  r.adjust_for_ambient_noise(source)

def record_callback(_, audio:sr.AudioData) -> None:
  data = audio.get_raw_data()
  audio_data_queue.put(data)

r.listen_in_background(source, record_callback, phrase_time_limit=record_timeout)

def sttThread():
  while run:
    try:
      global phrase_time
      global sttOutput
      if not audio_data_queue.empty():
        phrase_complete = False
        now = datetime.now(timezone.utc)
        if phrase_time and now - phrase_time > timedelta(seconds=phrase_timeout):
            phrase_complete = True
        phrase_time = now
        audio_data = b''.join(audio_data_queue.queue)
        audio_data_queue.queue.clear()
        audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
        result = audio_model.transcribe(audio_np, fp16=torch.cuda.is_available())
        transcription = result['text'].strip()
        
        #if phrase_complete or not sttOutput:
        sttOutput.append(" " + transcription)
        #else:
        #sttOutput[-1] += transcription
      else:
        time.sleep(.01)
    except KeyboardInterrupt:
      break
whisperThread = Thread(target=sttThread).start()

def hrConnectionThread():
  while run:
    global hrConnected
    global heartRate
    global pulsoidToken
    global client
    global conf_blinkOverride
    global conf_blinkSpeed
    global conf_useAfkKeybind
    global conf_toggleBeat
    global ws
    global pulsoidLastUsed
    global hypeRateLastUsed
    if ("hr(" in conf_layoutString or conf_avatarHR) and (playMsg or conf_avatarHR):
      if not hrConnected:
        try:
          url = "wss://dev.pulsoid.net/api/v1/data/real_time?access_token="+pulsoidToken+"&response_mode=text_plain_only_heart_rate"
          if useHypeRate:
            url = "wss://app.hyperate.io/socket/websocket?token="+hypeRateKey
          ws = create_connection(url)
          ws.settimeout(.4)
          hrConnected = True
          def heartRateListen():
              global ws
              global heartRate
              global pulsoidLastUsed
              global hypeRateLastUsed
              global hrConnected
              join_msg = {
                    "topic": "hr:"+hypeRateSessionId,  # replace <ID> with the user session id
                    "event": "phx_join",
                    "payload": {},
                    "ref": 0
                }
              if useHypeRate:
                ws.send(json.dumps(join_msg))
              while run:
                  try:
                    event = ws.recv()
                    if usePulsoid:
                      heartRate = event
                    else:
                      try:
                        heartRate = json.loads(event).get('payload').get('hr')
                        if heartRate == None:
                          heartRate = 1
                      except Exception as e:
                        outputLog('Refreshing hyperate...')
                        ws = create_connection(url)
                        ws.send(json.dumps(join_msg))
                    client.send_message("/avatar/parameters/isHRActive", True)
                    client.send_message("/avatar/parameters/isHRConnected", True)
                    client.send_message("/avatar/parameters/HR", int(heartRate))
                    
                  except Exception as e:
                    if not 'Connection timed out' in str(e):
                      outputLog(str(e))
                      hrConnected = False
                      break
                    pass
                    time.sleep(.01)
                  if not run or not hrConnected:
                      break
          heartRateListenThread = Thread(target=heartRateListen)
          heartRateListenThread.start()
          def blinkHR():
            global blinkThread
            global heartRate
            global conf_blinkOverride
            global conf_blinkSpeed
            global conf_toggleBeat
            while hrConnected and run and (playMsg or conf_avatarHR):
              if conf_toggleBeat:
                client.send_message("/avatar/parameters/isHRBeat", True)
                time.sleep(.1)
                client.send_message("/avatar/parameters/isHRBeat", False)
                if conf_blinkOverride:
                  time.sleep(conf_blinkSpeed)
                if heartRate == '':
                  heartRate = 0
                else:
                  if int(heartRate) <= 0:
                    heartRate = 1
                  if 60/int(heartRate) > 5:
                    time.sleep(1)
                  else:
                    time.sleep(60/int(heartRate))
          blinkHRThread = Thread(target=blinkHR)
          blinkHRThread.start()
          #print('Pulsoid Connection Started...')
          if usePulsoid:
            outputLog('Heart Rate Connection Started... Connected to Pulsoid')
            pulsoidLastUsed = True
            hypeRateLastUsed = False
          else:
            outputLog('Heart Rate Connection Started... Connected to HypeRate')
            pulsoidLastUsed = False
            hypeRateLastUsed = True
        except Exception as e:
          if windowAccess != None:
            if playMsg:
              windowAccess.write_event_value('heartRateError', e)
    if (((not "hr(" in conf_layoutString and not conf_avatarHR) or not (playMsg or conf_avatarHR)) or (pulsoidLastUsed and useHypeRate) or (hypeRateLastUsed and usePulsoid)) and hrConnected:
      hrConnected = False
      #print('Pulsoid Connection Stopped')
      if (pulsoidLastUsed and useHypeRate) or (hypeRateLastUsed and usePulsoid):
        outputLog('Switching HR Data source...')
      heartRate = 0
      if pulsoidLastUsed:
        outputLog('Pulsoid Connection Stopped')
      else:
        outputLog('HypeRate Connection Stopped')
    time.sleep(.5)
pulsoidLastUsed = usePulsoid
hypeRateLastUsed = useHypeRate
pulsoidConnectionThread = Thread(target=hrConnectionThread).start()

def spotifyConnectionManager():
  global spotifyPlayState
  while run:
    if playMsg and "song(" in conf_layoutString and useSpotifyApi and windowAccess != None:
      try:
        if spotifyAccessToken == '':
          raise Exception('Spotify access token missing!\nCheck output tab for more details...')
        spotifyPlayState = getSpotifyPlaystate()
      except Exception as e:  
        if "timed out" in str(e): 
          outputLog('Spotify API Timed out... retrying in 5 seconds\nFull Error: '+str(e))
          time.sleep(5)
        elif "Max retries" in str(e) or "aborted" in str(e):
          outputLog('Spotify API Timed out... retrying in 5 seconds\nFull Error: '+str(e))
          time.sleep(5)
        else: 
          spotifyPlayState = ''
          windowAccess.write_event_value('spotifyApiError', str(e)) 
    for x in range(2): #This sets the polling rate of the spotify api!!! Value is seconds minus 1, so a timeout of 3 seconds would be 2
      if run:
        time.sleep(1)
spotifyConnectionThread = Thread(target=spotifyConnectionManager).start()

def linkSpotify():
  outputLog('Begin Spotify Linking...')
  global spotify_client_id
  global spotify_redirect_uri
  global checkForCancel
  global NameToReturn
  global spotifyAccessToken
  global spotifyRefreshToken
  global code_verifier
  
  code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')
  code_verifier = code_verifier.rstrip('=')

  code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
  code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8')
  code_challenge = code_challenge.replace('=', '')

  auth_url = 'https://accounts.spotify.com/authorize'
  params = {
      'client_id': spotify_client_id,
      'response_type': 'code',
      'scope': "user-read-playback-state, user-read-currently-playing",
      'redirect_uri': spotify_redirect_uri,
      'code_challenge_method': 'S256',
      'code_challenge': code_challenge
  }
  spotify_auth_url = requests.Request('GET', auth_url, params=params).prepare().url
  
  outputLog("Attempting to open url: \n"+spotify_auth_url)
  
  app = Flask(__name__)
  server = make_server('127.0.0.1', 8000, app)
  
  @app.route('/callback')


  def callback():
      global authCode
      global spotifyAccessToken
      global spotifyRefreshToken
      global checkForCancel
      global nameToReturn
      global cancelLink
      def shutdown():
        server.shutdown()
      if 'error' in request.args:
        outputLog('Spotify Link Error: '+str(request.args.get('error')))
        shutdownThread = Thread(target=shutdown).start()
        cancelLink = True
        nameToReturn = 'Error'
        return """<!DOCTYPE html> <html> <head> <title>OSC Chat Tools | Spotify Authorization</title> <link rel="icon" type="image/x-icon" href="https://raw.githubusercontent.com/Lioncat6/OSC-Chat-Tools/main/oscicon.ico"> </head> <body> <style> body { font-family: sans-serif; background-color: darkslategrey; color: whitesmoke; } .mainbox { position: absolute; left: 50%; top: 50%; -webkit-transform: translate(-50%, -50%); transform: translate(-50%, -50%); } h1 { text-align: center; } p { text-align: center; } img { display: block; margin-left: auto; margin-right: auto; width: 50%; } </style> <div class="mainbox"> <img src="https://raw.githubusercontent.com/Lioncat6/OSC-Chat-Tools/main/oscicon.ico"> <h1 class="maintext">Authorization Failed</h1><p class="subtext">If you did not cancel the authentication at the previous screen please submit a bug report at <a href='https://github.com/Lioncat6/OSC-Chat-Tools/issues'>https://github.com/Lioncat6/OSC-Chat-Tools/issues</a></p><div><p>Full error:<b style="color:red;"> """+str(request.args.get('error'))+""" </b></p></div> </div> </body> </html>"""
      try:   
        code = request.args.get('code')
        #print('Authorization code:', code)
        authCode = code 
        def getAccessToken(code):
            global spotifyRefreshToken
            token_url = 'https://accounts.spotify.com/api/token'
            data = {
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': spotify_redirect_uri,
                'client_id': spotify_client_id,      
                'code_verifier': code_verifier
            }
            response = requests.post(token_url, data=data)
            if response.status_code != 200:
              raise Exception('Access token fetch error '+str(response.status_code)+' : '+response.text)
            spotifyRefreshToken = response.json().get('refresh_token')
            return response.json().get('access_token')

        spotifyAccessToken = getAccessToken(code)
        #print('Access token:', accessToken)
        
        def get_profile(accessToken):
            headers = {
                'Authorization': 'Bearer ' + accessToken,
            }

            response = requests.get('https://api.spotify.com/v1/me', headers=headers)
            if response.status_code != 200:
              raise Exception('Profile fetch error '+str(response.status_code)+' : '+response.text)
            data = response.json()
            return data
        profile = get_profile(spotifyAccessToken)
        shutdownThread = Thread(target=shutdown).start()
        nameToReturn = profile.get('display_name')
        outputLog("Spotify linked to "+nameToReturn+" successfully!")
        return """<!DOCTYPE html> <html> <head> <title>OSC Chat Tools | Spotify Authorization</title> <link rel="icon" type="image/x-icon" href="https://raw.githubusercontent.com/Lioncat6/OSC-Chat-Tools/main/oscicon.ico"> </head> <body> <style> body { font-family: sans-serif; background-color: darkslategrey; color: whitesmoke; } .mainbox { position: absolute; left: 50%; top: 50%; -webkit-transform: translate(-50%, -50%); transform: translate(-50%, -50%); } h1 { text-align: center; } p { text-align: center; } img { display: block; margin-left: auto; margin-right: auto; width: 50%; } </style> <div class="mainbox"> <img src="https://raw.githubusercontent.com/Lioncat6/OSC-Chat-Tools/main/oscicon.ico"> <h1 class="maintext">Authorization Successful</h1><p class="subtext">You can now close this tab and return to OCT</p> <div><p>Linked to:<b style="color:green;"> """+profile.get('display_name')+""" </b></p></div> </div> </body> </html>"""
      except Exception as e:
        shutdownThread = Thread(target=shutdown).start()
        cancelLink = True
        nameToReturn = 'Error'
        outputLog('Spotify Link Error: '+str(e))
        return """<!DOCTYPE html> <html> <head> <title>OSC Chat Tools | Spotify Authorization</title> <link rel="icon" type="image/x-icon" href="https://raw.githubusercontent.com/Lioncat6/OSC-Chat-Tools/main/oscicon.ico"> </head> <body> <style> body { font-family: sans-serif; background-color: darkslategrey; color: whitesmoke; } .mainbox { position: absolute; left: 50%; top: 50%; -webkit-transform: translate(-50%, -50%); transform: translate(-50%, -50%); } h1 { text-align: center; } p { text-align: center; } img { display: block; margin-left: auto; margin-right: auto; width: 50%; } </style> <div class="mainbox"> <img src="https://raw.githubusercontent.com/Lioncat6/OSC-Chat-Tools/main/oscicon.ico"> <h1 class="maintext">Authorization Failed</h1><p class="subtext">If you did not cancel the authentication at the previous screen please submit a bug report at <a href='https://github.com/Lioncat6/OSC-Chat-Tools/issues'>https://github.com/Lioncat6/OSC-Chat-Tools/issues</a></p><div><p>Full error:<b style="color:red;"> """+str(e)+""" </b></p></div> </div> </body> </html>"""
  
  webbrowser.open_new(spotify_auth_url)
  
  def spotifyLinkCancelCheck():
    global checkForCancel
    checkForCancel = True
    global cancelLink
    global nameToReturn
    while checkForCancel:
      time.sleep(.1)
      if cancelLink:
        outputLog("Spotify linking canceled")
        server.shutdown()
        checkForCancel = False
        cancelLink = False
        break
  spotifyLinkCancelCheckThread= Thread(target=spotifyLinkCancelCheck).start()
  server.serve_forever()
  checkForCancel = False 
  return nameToReturn

def runmsg():
  global textParseIterator
  global playMsg
  global afk
  global conf_FileToRead
  global conf_scrollText
  global textStorage
  while playMsg:
    textStorage = conf_messageString
    if not afk and not conf_scrollText:
      for x in processMessage(conf_messageString):
        if afk or conf_scrollText or (not playMsg) or (not run) or (conf_messageString != textStorage):
          textStorage = conf_messageString
          break
        if x == "*":
          sendMsg(" ㅤ")
        else:
          sendMsg(" "+x)
        
    elif afk:
      sendMsg('\vAFK\v')
      sendMsg('\vㅤ\v')
    elif conf_scrollText:
      try:
        fileToOpen = open(conf_FileToRead, "r", encoding="utf-8")
        fileText = fileToOpen.read()
        if textParseIterator + 144 < len(fileText):
          sendMsg(fileText[textParseIterator:textParseIterator+144])
          textParseIterator = textParseIterator +144
        else: 
          sendMsg(fileText[textParseIterator:textParseIterator+len(fileText)-textParseIterator])
          textParseIterator = 0
      except Exception as e:
        windowAccess.write_event_value('scrollError', e)
        sendMsg('')
    else:
      sendMsg('')
  textParseIterator = 0
  if sendBlank:
    client.send_message("/chatbox/input", [ "", True, False])
    
def msgPlayCheck():
  if keyboard.is_pressed(conf_keybind_run):
    msgPlayToggle()

def msgPlayToggle():
  global playMsg
  if playMsg:
      playMsg = False
      time.sleep(.5)
  else:
    playMsg = True  
    msgThread = Thread(target=runmsg)
    msgThread.start()
    time.sleep(.5) 
    
def afkCheck():
  global isAfk
  global afk
  if conf_useAfkKeybind:
    if keyboard.is_pressed(conf_keybind_afk):
      afkToggle()
  elif isAfk:
    afk = True
  else:
    afk = False
    
def afkToggle():
  global afk
  afk = not afk
  time.sleep(.5) 

def restartMsg():
  global playMsg
  playMsg = False
  time.sleep(1.5)
  playMsg = True  
  msgThread = Thread(target=runmsg)
  msgThread.start()

def vrcRunningCheck():
  global vrcPID
  global playTimeDat
  def pid_check(pid):
    try:
      if psutil.pid_exists(vrcPID):
        return True
      else:
        return False
    except:
      return False
  while run:
    if not pid_check(vrcPID): 
      vrcPID = None
      for proc in psutil.process_iter():
          if not run:
            break
          if "VRChat.exe" in proc.name():
              vrcPID = proc.pid
              break
          time.sleep(.01)
      playTimeDat = time.mktime(time.localtime(psutil.Process(vrcPID).create_time()))
    time.sleep(1)

vrcRunningCheckThread = Thread(target=vrcRunningCheck)
vrcRunningCheckThread.start()
msgThread = Thread(target=runmsg)
msgThread.start()
mainUI = Thread(target=uiThread)
mainUI.start()
update_checker(True)
timeParameterThread = Thread(target=timeParameterUpdate).start()

while run:
  msgPlayCheck()
  afkCheck()
  time.sleep(.01)