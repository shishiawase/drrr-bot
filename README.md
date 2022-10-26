
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
  
  <table style="border-style:hidden;">
    <tr style="border-style:hidden;">
      <td style="border-style:hidden;">
        <div align="center">
          <img src="/assets/setton.svg" width="48" height="48">
          <p align="bottom">setton</p>
        </div>
      </td>
      <td style="border-style: none;">
        <img src="/assets/bakyura-2x.svg" width="48" height="48" align="center">
        <p align="center">bakyura-2x</p>
      </td>
      <td style="border-style: none;">
        <img src="/assets/bakyura.svg" width="48" height="48" align="center">
        <p align="center">bakyura</p> 
      </td>
      <td style="border-style: none;">
        <img src="/assets/eight.svg" width="48" height="48" align="center">
        <p align="center">eight</p> 
      </td>
      <td style="border-style: none;">
        <img src="/assets/gaki-2x.svg" width="48" height="48" align="center">
        <p align="center">gaki-2x</p> 
      </td>
    <tr>
    <tr align="center">
      <td align="center">
        <img src="/assets/gg.svg" width="48" height="48" align="center">
        <p align="center">gg</p> 
      </td>
      <td align="center">
        <img src="/assets/junsui-2x.svg" width="48" height="48" align="center">
        <p align="center">junsui-2x</p> 
      </td>
      <td align="center">
        <img src="/assets/kakka.svg" width="48" height="48" align="center">
        <p align="center">kakka</p> 
      </td>
      <td align="center">
        <img src="/assets/kanra.svg" width="48" height="48" align="center">
        <p align="center">kanra</p> 
      </td>
      <td align="center">
        <img src="/assets/kanra-2x.svg" width="48" height="48" align="center">
        <p align="center">kanra-2x</p> 
      </td>
    <tr>
    <tr align="center">
      <td align="center">
        <img src="/assets/kuromu-2x.svg" width="48" height="48" align="center">
        <p align="center">kuromu-2x</p> 
      </td>
      <td align="center">
        <img src="/assets/kyo-2x.svg" width="48" height="48" align="center">
        <p align="center">kyo-2x</p> 
      </td>
      <td align="center">
        <img src="/assets/rotchi-2x.svg" width="48" height="48" align="center">
        <p align="center">rotchi-2x</p> 
      </td>
      <td align="center">
        <img src="/assets/saki-2x.svg" width="48" height="48" align="center">
        <p align="center">saki-2x</p> 
      </td>
      <td align="center">
        <img src="/assets/san-2x.svg" width="48" height="48" align="center">
        <p align="center">san-2x</p> 
      </td>
    <tr>
    <tr align="center">
      <td align="center">
        <img src="/assets/kuromu-2x.svg" width="48" height="48" align="center">
        <p align="center">kuromu-2x</p> 
      </td>
      <td align="center">
        <img src="/assets/kyo-2x.svg" width="48" height="48" align="center">
        <p align="center">kyo-2x</p> 
      </td>
    </tr>
  </table>
  
  
<div>
      <p><img src="/assets/setton.svg" width="48" height="48" align="bottom">  <b>setton</b></p>
      <p><img src="/assets/bakyura-2x.svg" width="48" height="48" align="bottom">  <b>bakyura-2x</b></p>
      <p><img src="/assets/bakyura.svg" width="48" height="48" align="bottom">  <b>bakyura</b></p>
      <p><img src="/assets/eight.svg" width="48" height="48" align="center">  <b>eight</b></p>
      <p><img src="/assets/gaki-2x.svg" width="48" height="48" align="center">  <b>gaki-2x</b></p>
      <p><img src="/assets/gg.svg" width="48" height="48" align="center">  <b>gg</b></p>
      <p><img src="/assets/junsui-2x.svg" width="48" height="48" align="center">  <b>junsui-2x</b></p>
      <p><img src="/assets/kakka.svg" width="48" height="48" align="center">  <b>kakka</b></p>
      <p><img src="/assets/kanra-2x.svg" width="48" height="48" align="center">  <b>kanra-2x</b></p>
      <p><img src="/assets/kanra.svg" width="48" height="48" align="center">  <b>kanra</b></p>
      <p><img src="/assets/kuromu-2x.svg" width="48" height="48" align="center">  <b>kuromu-2x</b></p>
      <p><img src="/assets/kyo-2x.svg" width="48" height="48" align="center">  <b>kyo-2x</b></p>
      <p><img src="/assets/rotchi-2x.svg" width="48" height="48" align="center">  <b>rotchi-2x</b></p>
      <p><img src="/assets/saki-2x.svg" width="48" height="48" align="center">  <b>saki-2x</b></p>
      <p><img src="/assets/san-2x.svg" width="48" height="48" align="center">  <b>san-2x</b></p>
      <p><img src="/assets/setton-2x.svg" width="48" height="48" align="center">  <b>setton-2x</b></p>
      <p><img src="/assets/sharo-2x.svg" width="48" height="48" align="center">  <b>sharo-2x</b></p>
      <p><img src="/assets/tanaka-2x.svg" width="48" height="48" align="center">  <b>tanaka-2x</b></p>
      <p><img src="/assets/tanaka.svg" width="48" height="48" align="center">  <b>tanaka</b></p>
      <p><img src="/assets/zaika-2x.svg" width="48" height="48" align="center">  <b>zaika-2x</b></p>
      <p><img src="/assets/zaika.svg" width="48" height="48" align="center">  <b>zaika</b></p>
      <p><img src="/assets/zawa.svg" width="48" height="48" align="center">  <b>zawa</b></p>
    </div>
