
drrr-bot - modular bot on python for [drrr.com](https://drrr.com)

- [INSTALLATION](#installation)
- [METHODS AND PARAMETERS](#methods-and-parameters)
    - [Events](#events)
    - [timer and later](#timer-and-later)
    - [whitelist and blacklist](#whitelist-and-blacklist)
- [EXAMPLES](#examples)
- [OTHER](#other)

`*` - _marked optional parameters_

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
```
## Events

Work with chat events, Thanks to this decorator, the function below it will pay attention only to the events that were given, ignoring the rest.

- All types in events:
  `["msg", "dm", "me", "join", "leave", "new-host","new-description", "room-profile", "music", "kick", "ban"]`
  
  ```python
  @drrr.event(types, *command, *users)    # @Decorator. 
  def someFunc(obj):                      # 'obj' in your function ALWAYS REQUIRED
      pass                  
                                          # types (List):
                                          #  ⤷ What events will the function respond to. A complete
                                          #  ⤷ list of events can be found in EVENTS
                                          # command (String):
                                          #  ⤷ A specific text command in chat for execution
                                          # users (List):
                                          #  ⤷ Users on which the event will respond
                                          # obj (dict):
                                          #  ⤷ Stores user information: type, user, msg, url, trip
                                        
  ```

- Setting a greeting at the entrance, example:
  ```python
  @drrr.event(['join'])
  def greetings(obj):
      drrr.msg(f'Hello @{obj['user']})

  # Output:
    # Steave joined.
    # Bot: Hello @Steave
  ```
  More [examples](#examples)

## timer and later

Method for calling functions through a fixed time

- Used:
  ```python
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
- Example keep room:
  ```python
  @drrr.timer(minutes=10)
  def keep():
      drrr.dm(drrr.profile['name'], 'keep')
  
  # every 10 minutes will send to himself in dm 'keep'
  ```
  
## whitelist and Blacklist

It may allow only certain users to enter the room or on the contrary prohibit it
- Used:
  ```python
  drrr.blacklist(*add, *remove, *removeAll, *on, *mode)
  drrr.whitelist(*add, *addAll, *remove, *removeAll, *on, *mode)
  
  # add (List): adds users to the whitelist, you can also add a trip '#tripcode'
  # addAll (bool): adds all users current room in whitelist
  # remove (List): deleted user from whitelist
  # removeAll (bool): deleted all from whitelist
  # on (bool): enable whitelist set - true, disable - false
  # mode (String): set mode - 'kick', 'ban', 'report'. Default - 'kick'
  ```
- Example:
  ```python
  drrr.whitelist(['Kate'], on=true)
  # Now only the Kate can enter the room, the rest of the users will be kicked
  
  drrr.blacklist(['John'], on=true)
  # Now all can enter the room, only the John will kicked from the room
  
  # When one of the methods is turned on, for example a blacklist, the whitelist
  # is automatically disabled
  ```
---

# EXAMPLES

---

# OTHER

- __Icons__:
  
  <div id="badges">
    <p><img src="/assets/setton.svg" width="48" height="48" align="center">  <b>setton</b></p>
  </div>
