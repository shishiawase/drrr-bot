
drrr-bot - modular bot on python for [drrr.com](https://drrr.com)

- [INSTALLATION](#installation)
- [METHODS AND PARAMETERS](#methods-and-parameters)
    - [Events](#events)
    - [Timers](#timers)
    - [Whitelist and blacklist](#whitelist-and-blacklist)
- [EXAMPLES](#examples)
- [OTHER](#other)

***

# INSTALLATION

- ## Install dependencies:
    ```
    $ pip install httpx
    ```
    
- ## Use this module:
    We import the module into our main.py (or some other name) in further examples, this part will be skipped
    ```python
    from drrr.py import Bot
    
    drrr = Bot('name', 'icon', 'device') # We determine the main parameters of the bot.
                                         # If you simply call Bot (), the default parameters
                                         # will be set: ('***', 'setton', 'Bot')
                                         # Existing icons and devices can be viewed in "OTHER"
                                         
    # And an example of use:
    
    drrr.login() # Login in chat
    drrr.join('room id') # Join room
    drrr.msg('Hello') # Send message to the general chat
    
    drrr.startLoop() # Always called at the end for continuous data from the site
    ```
    
***

# METHODS AND PARAMETERS

`*` - marked optional parameters

```python

--------------Required_methods_in_code--------------

drrr.login()                            # Always called after creating a bot class 
                                        # instance
                                  
drrr.startLoop(*seconds)                # Always called at the end for continuous data from the site

                                        # seconds (int, float):
                                        #  ⤷ set a frequency for the date update in seconds.
                                        #  ⤷ Default - '1.5'

--------------------Other_methods-------------------
                                    
drrr.save(*name)                        # Save current profile.
                                     
                                        # name (String):
                                        #  ⤷ Set a name for the saved config. Default - 'config'
                                     
drrr.load(*name)                        # Load profile.

                                        # name (String):
                                        #  ⤷ Set a name for the loaded config. Default - 'config'

drrr.stopLoop()                         # Loop stop

@drrr.event(['join'], *command, *users) # @Decorator. Work with chat events, for example print 
def someFunc(obj):                      # the name in the console of the user who joined
    print(obj['name'])                  # the room. 'obj' in your function ALWAYS REQUIRED
    
                                        # types (List):
                                        #  ⤷ What events will the function respond to. A complete
                                        #  ⤷ list of events can be found in EVENTS
                                        # command (String):
                                        #  ⤷ A specific text command in chat for execution
                                        # users (List):
                                        #  ⤷ Users on which the event will respond
                                        # obj (dict):
                                        #  ⤷ Stores user information: type, name, msg, url, trip

drrr.lounge()                           # Update lounge informations
drrr.profile                            # Information about the current profile
drrr.rooms                              # List of rooms in chat. Pre-call drrr.lounge() to update the list
drrr.room                               # Current room data. First you need to join the room or create it
drrr.users                              # List of users in the room
drrr.loc                                # Current location 'lounge' or 'room'

drrr.create(                            # Creating a room
    *name,                              
    *desc,                              # name (String):
    *limit,                             # ⤷ Set a room name. Default - 'Just'
    *lang,                              # desc (String):
    *music,                             # ⤷ Set a description. Default - ''
    *adult,                             # limit (int):
    *hidden                             # ⤷ Set users limit for room 2-20. Default - 5
)                                       # lang (String):
                                        # ⤷ Set room localization. Default - 'en-US'
                                        # music (bool):
                                        # ⤷ Enable music in the room. Default - false
                                        # adult (bool):
                                        # ⤷ Room 18+. Default - false
                                        # hidden (bool):
                                        # ⤷ Hide the room. Default - false
 
drrr.join(id)                           # Join the room with ID
                                        # id (String)

drrr.title(name)                        # Set name for room
                                        # name (String)

drrr.desc(name)                         # Set description for room
                                        # name (String)
                                       
drrr.host(name)                         # Transfer host
                                        # name (String)
                                        
drrr.dj(mode)                           # Enable/Disable dj mode
                                        # mode (bool)

drrr.music(name, url)                   # Play music

                                        # name (String):
                                        # ⤷ Set name for music
                                        # url (String):
                                        # ⤷ Url link to music

drrr.msg(msg, url)                      # Sending a message to a common chat (any length, bot will split
                                        # one large into several messages
                                        
                                        # msg (String):
                                        # ⤷ Message text
                                        # url (String):
                                        # ⤷ Add url link

drrr.dm(name, msg, url)                 # Sending a private message to a common chat (any length, bot will split
                                        # one large into several messages
                                        
                                        # name (String):
                                        # ⤷ Username
                                        # msg (String):
                                        # ⤷ Message text
                                        # url (String):
                                        # ⤷ Add url link

drrr.kick(name)                         # Kick user                                        
drrr.ban(name)                          # Ban user                  | name                      
drrr.report(name)                       # Ban and report user       | (String)
drrr.unban(name)                        # Unban user

drrr.leave()                            # Leave the room

--------------------------Timers-------------------------

@drrr.timer(*seconds, *minutes, *hours) # @Decorator. Repeatedly calls a function with a fixed time delay 
def hello():                            # between each call
    drrr.msg('Hi everyone')                            


@drrr.later(*seconds, *minutes, *hours) # @Decorator. Сall the function once after a fixed time
def hello():                            
    drrr.msg('Hi everyone')
    
# You can set the interval both in seconds and in minutes, hours
# or all at once together

# To stop a certain timer, just do it:
drrr.loops['hello'].stop() # where is 'hello' the name of the function that you launched in the timer
```
## Events

## Timers

## Whitelist and Blacklist

---

# EXAMPLES

---

# OTHER
