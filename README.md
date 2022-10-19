
drrr-bot - modular bot on python for [drrr.com](https://drrr.com)

- [INSTALLATION](#installation)
- [METODS AND OPTIONS](#method-and-options)
- [EXAMPLES](#examples)


# INSTALLATION

- ## Install dependencies:
    ```
    $ pip install httpx
    ```
    
- ## Use this module:
    We import the module into our main.py (or some other name) in further examples, this part will be skipped
    ```python
    from drrr.py import Bot
    
    drrr = Bot('name', 'icon', 'device')
    # Default options for this: name = ***, icon = setton, device = Bot
    # Default use - Bot() without options
    drrr.login() # Login in chat
    drrr.create() # Create room
    # or 
    drrr.join('room id') # Join room
    
    drrr.startLoop() # Always called at the end for continuous data from the site
    ```
