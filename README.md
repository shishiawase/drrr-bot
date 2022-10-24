
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
`*` - mark of the optional parameter

`drrr.login()`
| Parameter | Type | Description |
|:---------:|:----:|:-----------:|
| - | - | _Required_. Login in chat, always called after creating a bot class instance |

```python

drrr.login()                         # _Required_. Always called after creating a bot class 
                                     # instance
                                    
drrr.save(*name)                     # Save current profile. Default name - 'config'

drrr.load(*name)                     # Load profile from the 'configs' folder in the root.
                                     # Default name - 'config'

drrr.startLoop(*seconds)
```
