
drrr-bot - modular bot on python for [drrr.com](https://drrr.com)

- [INSTALLATION](#installation)
- [METHODS AND PARAMETERS](#methods-and-parameters)
    - [Events](#events)
    - [timer and later](#timer-and-later)
    - [whitelist and blacklist](#whitelist-and-blacklist)
- [EXAMPLES](#examples)
- [OTHER](#other)

`*` - _marked optional parameters_

packages: requests


# INSTALLATION

Download the module with examples here - [releases](https://github.com/shishiawase/drrr-bot/releases) 
or just download `drrr.py` from the repository folder

- ## Use this module:
    Import the module into our `main.py` (or some other name) in further examples, this part will be skipped
    ```python
    from drrr import Bot, logging
    
    drrr = Bot('name', 'icon', 'device')
    drrr.logger.setLevel(level=logging.WARNING)   # Default set INFO
                                        
    # We determine the main parameters of the bot.
    # If you simply call Bot (), the default parameters
    # will be set: ('***', 'setton', 'Bot')
    # Existing icons and devices can be viewed in "OTHER"
                                         
    # And an example of use:
    
    drrr.login() # Login in chat
    drrr.join('room id') # Join room
    drrr.msg('Hello') # Send message to the general chat
    
    drrr.startLoop() # Always called at the end for continuous data from the site
    ```
    Or use the example in the folder with the module `main.py` and edit it as you wish
    
    And run
    ```
    $ python main.py 
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

drrr.desc(desc)                         # Set description for room
                                        # desc (String)
                                       
drrr.host(name)                         # Transfer host
                                        # name (String)
                                        
drrr.dj(mode)                           # Enable/Disable dj mode
                                        # mode (bool)

drrr.music(name, url)                   # Play music

                                        # name (String):
                                        # ⤷ Set name for music
                                        # url (String):
                                        # ⤷ Url link to music

drrr.msg(msg, *url)                     # Sending a message to a common chat (any length, bot will split
                                        # one large into several messages
                                        
                                        # msg (String):
                                        # ⤷ Message text
                                        # url (String):
                                        # ⤷ Add url link

drrr.dm(name, msg, *url)                # Sending a private message to a common chat (any length, bot will split
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

Work with chat events, thanks to this decorator, the function below it will pay attention only to the events that were given, ignoring the rest.

- All types in events:
  `["msg", "dm", "me", "join", "leave", "new-host", "new-description", "room-profile", "music", "kick", "ban"]`
  
  ```python
  @drrr.event(types, *command, *users)    
  def someFunc(e):                      
      pass                  
                                          
  # @Decorator.                                         
  # 'e' in your function ALWAYS REQUIRED                                        
  # types (List):                                        
  #  ⤷ What events will the function respond to. A complete
  #  ⤷ list of events can be found in EVENTS
  # command (String):
  #  ⤷ A specific text command in chat for execution (supports regular expressions)
  #  ⤷ work only with ['msg', 'dm', 'me']
  # users (List):
  #  ⤷ Users on which the event will respond
  # e (Class):
  #  ⤷ Stores user information: type, user, msg, url, trip
                                        
  ```

- Setting a greeting at the entrance, example:
  ```python
  @drrr.event(['join'])
  def greetings(ej):
      drrr.msg(f'Hello @{e.user}')

  # Output:
    # Steave joined.
    # Bot: Hello @Steave
  
  
  @drrr.event(['msg'], '^/tagme')
  def greetings(e):
      drrr.msg(f'@{e.user}')

  # Output:
    # Steave: pls /tagme!  |  will not work because '^' reg exp and the message should start with /tagme
    # Steave: /tagme       |  work
    # Bot: @Steave
  ```
  More [examples](#examples)

## timer and later

Method for calling functions through a fixed time

- Used:
  ```python
  
  # @Decorator. 
  
  @drrr.timer(*seconds, *minutes, *hours, *args) 
  def hello():                            
      drrr.msg('Hi everyone')                            
  # Repeatedly calls a function with a fixed time delay
  # args - transfers arguments to a function - type ()
  # between each call

  @drrr.later(*seconds, *minutes, *hours, *args)
  def hello():                            
      drrr.msg('Hi everyone')
  # Сall the function once after a fixed time
    
  # You can set the interval both in seconds and in minutes, hours
  # or all at once together

  # To stop a certain timer, just do it:
  drrr.loops['hello'].stop() # where is 'hello' the name of the function that you launched in the timer
  ```
- Example keep room:
  ```python
  @drrr.timer(minutes=10, args=(drrr.profile['name'], 'keep'))
  def keep(bot_name, msg):
      drrr.dm(bot_name, msg)
  
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

- Moderate
  ```python
  # simple commands for moderation
  
  admins = ['#firsttrip', '#sectrip']
  
  @drrr.event(['msg', 'dm'], '/kick', admins)
  def kick(e):
      user = e.msg.replace('/kick ', '')
      drrr.kick(user)
  
  @drrr.event(['msg', 'dm'], '/ban', admins)
  def ban(e):
      user = e.msg.replace('/ban ', '')
      drrr.ban(user)
  
  @drrr.event(['msg', 'dm'], '/host', admins)
  def host(e):
      drrr.host(e.user)
  
  @drrr.event(['msg', 'dm'], '/title', admins)
  def title(e):
      m = e.msg.replace('/title ', '')
      drrr.title(m)
  
  @drrr.event(['msg', 'dm'], '/desc', admins)
  def desc(e):
      m = e.msg.replace('/desc ', '')
      drrr.desc(m)
  ```

- Lucky game
  ```python
  import random
  
  # roulette for departure from the room
  
  def rand(n, u):
      match n:
          case "0":
              drrr.kick(u)
          case "1":
              drrr.ban(u)
          case "2":
              drrr.report(u)
          case "3":
              drrr.msg(f'You are lucky! @{u}')
  
  @drrr.event(['msg'], '/luck')
  def luck(e):
      rand(random.randint(0, 3), e.user)
  ```

- Lock room
  ```python
  # adds everyone to the whitelist and does not let anyone new into the room
  
  @drrr.event(['msg'], '/lock', ['yourName', '#trip'])
  def lock(e):
      drrr.whitelist(addAll=True, on=True)
      drrr.msg('Whitelist enabled')
  
  @drrr.event(['msg'], '/unlock', ['yourName', '#trip'])
  def unlock(e):
      drrr.whitelist(removeAll=True, on=False)
      drrr.msg('Whitelist disabled')
  ```

- Random pics
  ```python
  import requests
  
  # send random image
  
  @drrr.event(['msg'], '/waifu')
  def waifu(e):
      r = requests.get('https://api.waifu.pics/sfw/waifu').json()
      drrr.msg('♥', r['url'])
  ```
---

# OTHER

- __Devices__:
  - Pc
  - Phone
  - Tablet
  - Tv
  - Bot

- __Icons__:
  
  <table>
    <tr>
      <td align="center">
          <img src="/assets/setton.svg" width="48" height="48" align="center">
          <p align="center">setton</p>
      </td>
      <td td align="center">
        <img src="/assets/bakyura-2x.svg" width="48" height="48">
        <p align="center">bakyura-2x</p>
      </td>
      <td td align="center">
        <img src="/assets/bakyura.svg" width="48" height="48" align="center">
        <p align="center">bakyura</p> 
      </td>
      <td td align="center">
        <img src="/assets/eight.svg" width="48" height="48" align="center">
        <p align="center">eight</p> 
      </td>
      <td td align="center">
        <img src="/assets/gaki-2x.svg" width="48" height="48" align="center">
        <p align="center">gaki-2x</p> 
      </td>
    <tr>
    <tr>
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
    <tr>
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
    <tr>
      <td align="center">
        <img src="/assets/setton-2x.svg" width="48" height="48" align="center">
        <p align="center">setton-2x</p> 
      </td>
      <td align="center">
        <img src="/assets/sharo-2x.svg" width="48" height="48" align="center">
        <p align="center">sharo-2x</p> 
      </td>
      <td align="center">
        <img src="/assets/tanaka-2x.svg" width="48" height="48" align="center">
        <p align="center">tanaka-2x</p> 
      </td>
      <td align="center">
        <img src="/assets/tanaka.svg" width="48" height="48" align="center">
        <p align="center">tanaka</p> 
      </td>
      <td align="center">
        <img src="/assets/zaika-2x.svg" width="48" height="48" align="center">
        <p align="center">zaika-2x</p> 
      </td>
    <tr>
    <tr>
      <td align="center">
        <img src="/assets/zaika.svg" width="48" height="48" align="center">
        <p align="center">zaika</p> 
      </td>
      <td align="center">
        <img src="/assets/zawa.svg" width="48" height="48" align="center">
        <p align="center">zawa</p> 
      </td>
    </tr>
  </table>
