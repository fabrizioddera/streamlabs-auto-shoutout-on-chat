#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
import json
sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references

import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#   Import your Settings class
from SoInChat_Module import SoInChatSettings
#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "AutoShoutout in chat"
Website = "https://www.streamlabs.com"
Description = "Auto shoutout for users joining channel"
Creator = "Fabrizio"
Version = "1.0.0.0"

#---------------------------
#   Define Global Variables
#---------------------------
global SettingsFile
SettingsFile = ""
global ScriptSettings
ScriptSettings = SoInChatSettings()

users = ""

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():

    #   Load settings
    SettingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
    ScriptSettings = SoInChatSettings(SettingsFile)

    global users
    users = list(map(str.strip, ScriptSettings.Users.split(',')))

    return

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):

    global users

    userName = getUserName(data.RawData)
    if data.IsChatMessage() and userName in users :
        users.remove(userName)
        Log(' '.join(users))
        Parent.SendStreamMessage("!" + ScriptSettings.Command + " " + userName)
   
    return

#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():
    return

# Get username from message
def getUserName(rawMessage):
    array=rawMessage.split(";")
    for data in array:
        if data.find("display-name") > -1:
            arrayOfData=data.split("=")
            return arrayOfData[1]

def getRaider(message):
    array=message.split(" ")
    return array[0]

#---------------------------
#   [Optional] Parse method (Allows you to create your own custom $parameters) 
#---------------------------
def Parse(parseString, userid, username, targetid, targetname, message):
    
    if "$myparameter" in parseString:
        return parseString.replace("$myparameter","I am a cat!")
    
    return parseString

#---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
#---------------------------
def ReloadSettings(jsonData):
    # Execute json reloading here
    ScriptSettings.__dict__ = json.loads(jsonData)
    Log(str(ScriptSettings.__dict__))
    ScriptSettings.Save(SettingsFile)
    return

#---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
#---------------------------
def Unload():
    return

#---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
#---------------------------
def ScriptToggled(state):
    return

def Log(message):
    Parent.Log("AutoSO", message)
    return
