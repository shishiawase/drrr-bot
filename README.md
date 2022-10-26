
drrr-bot - modular bot on python for [drrr.com](https://drrr.com)

- [INSTALLATION](#installation)
- [FUNCTIONS AND PARAMETERS](#functions-and-parameters)
    - [login](#login)
    - [save](#savename)
    - [load](#load)
    - [startLoop](#startLoop)
    - [stopLoop](#stopLoop)
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
                                         # Existing icons and devices can be viewed in "other"
                                         
    # And an example of use:
    
    drrr.login() # Login in chat
    drrr.join('room id') # Join room
    drrr.msg('Hello') # Send message to the general chat
    
    drrr.startLoop() # Always called at the end for continuous data from the site
    ```
    
***

# FUNCTIONS AND PARAMETERS


- `drrr.login()`
    | Parameter | Type | Description |
    |:---------:|:----:|:-----------:|
    | - | - | _Required_. Login in chat, always called after creating a bot class instance |
- `drrr.save(name)`
    | Parameter | Type | Description |
    |:---------:|:----:|:-----------:|
    | - | - | Save current profile. Default name - 'config' |
    | name | String | _Optional_. Set a name for the saved profile |
- `drrr.load(name)`
    | Parameter | Type | Description |
    |:---------:|:----:|:-----------:|
    | - | - | Load current profile. Default name - 'config' |
    | name | String | _Optional_. Set a name for the loaded profile |
- `drrr.startLoop(seconds)`
    | Parameter | Type | Description |
    |:---------:|:----:|:-----------:|
    | - | - | _Required_. Always called at the end for continuous data from the site |
    | seconds | int, float | _Optional_. Set a frequency for the date update in seconds. Default - 1.5 sec |
- `drrr.stopLoop()`
    | Parameter | Type | Description |
    |:---------:|:----:|:-----------:|
    | - | - | Loop stop |

```python

# -------------Required functions in code-------------

drrr.login()                         # Always called after creating a bot class 
                                     # instance
                                  
drrr.startLoop(*seconds)             # Always called at the end for continuous data from the site
                                       # [seconds]: set a frequency for the date update in seconds.
                                       # Default - '1.5'

# -----------------All other functions----------------
                                    
drrr.save(*name)                     # Save current profile.
                                       # name (String): 
                                         # Set a name for the saved config. Default - 'config'
drrr.load(*name)                     # Load profile.
                                     # name (String):
                                     #  ⤷ Set a name for the loaded config. Default - 'config'

drrr.startLoop(*seconds)
```
