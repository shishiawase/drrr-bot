import os
import httpx
import logging
import threading
from configparser import ConfigParser

client = httpx.Client(timeout=None)
DRRRUrl = 'https://drrr.com'

def request(url, **params):
    text = False

    if 'headers' in params:
        client.headers = params['headers']

    if 'data' in params:
        data = params['data']
        res = client.post(url, data=data)
        if res.text.startswith('{'): text = res.json()
        return { 'status': res.status_code, 'headers': res.headers, 'text': text }

    res = client.get(url)
    if res.text.startswith('{'): text = res.json()
    return { 'status': res.status_code, 'headers': res.headers, 'text': text }


class Bot:

    events = {}
    _users = {}
    room = {}
    profile = {}
    loops = {}
    queue = []
    rooms = []
    users = []
    loopId = None
    queueON = False
    lastTime = 0
    loc = 'lounge'
    userlist = {'whitelist': [], 'blacklist': []}
    rule = {'enable': False, 'type': '', 'mode': {'whitelist': 'kick', 'blacklist': 'kick'}}

    def __init__(self, name: str = '***', icon: str = 'setton', lang: str = 'en-US', device: str = 'Bot'):

        self.profile['name'] = name
        self.profile['icon'] = icon
        self.profile['lang'] = lang
        self.profile['device'] = device

        logging.basicConfig(format= f'%(asctime)s [BOT {name}]: %(message)s', level=logging.INFO)
    

    class _Timer(threading.Thread):
        def __init__(self, t: int, func):
            threading.Thread.__init__(self)
            threading.Thread.name = f'DRRR _Timer ({func.__name__})'
            self.stopped = threading.Event()
            self.func = func
            self.t = t

        def run(self):
            while not self.stopped.wait(self.t):
                self.func()

        def stop(self):
            self.stopped.set()


    class _Later(threading.Thread):
        def __init__(self, t: int, func):
            threading.Thread.__init__(self)
            threading.Thread.name = 'DRRR _Later'
            self.stopped = threading.Event()
            self.func = func
            self.t = t

        def run(self):
            self.stopped.wait(self.t)
            self.func()

        
    def login(self):

        def getToken():
            return request(f'{DRRRUrl}/?api=json')
            
        
        r = getToken()
        cookie = r['headers']['set-cookie'].partition(';')[0]
        self.profile['cookie'] = cookie
        token = r['text']['token']

        form = {
            'name': self.profile['name'],
            'login': 'ENTER',
            'token': token,
            'language': self.profile['lang'],
            'icon': self.profile['icon']
        }

        t = self._post(f'{DRRRUrl}/?api=json', form)
        while 'drrr' not in t['headers']['set-cookie']:
            t = self._post(f'{DRRRUrl}/?api=json', form)
        
        cookie = t['headers']['set-cookie'].partition(';')[0]
        self.profile['cookie'] = cookie
        self.getProfile()
        logging.info("Login ok")


    def _post(self, url, cmd):
        headers = { 'Cookie': self.profile['cookie'] }
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        headers['User-Agent'] = self.profile['device']

        return request(url, headers=headers, data=cmd)


    def _get(self, url):
        headers = { 'Cookie': self.profile['cookie'] }
        headers['User-Agent'] = self.profile['device']

        return request(url, headers=headers)
    

    def save(self, name='config'):
        profile = self.profile

        config = ConfigParser()
        config.add_section('Config')
        config.set('Config', 'name', profile['name'])
        config.set('Config', 'icon', profile['icon'])
        config.set('Config', 'cookie', profile['cookie'])
        config.set('Config', 'device', profile['device'])

        if not os.path.exists('./config'): os.mkdir('./config')
        with open(f'./config/{name}.ini', 'w') as config_file:
            config.write(config_file)
        
        logging.info('Config saved')
    

    def load(self, name='config'):
        config = ConfigParser()

        if not os.path.isfile(f'./config/{name}.ini'):
            return False
        config.read(f'./config/{name}.ini')

        for i in config.options('Config'):
            self.profile[i] = config.get('Config', i)
        
        self.getProfile()
        logging.info('Config loaded')
        return True


    def _talksFilter(self, talks, time):
        t = []

        for x in talks:
            if x['time'] > time:
                obj = {}

                if 'message' in x['type']:
                    obj['type'] = (x.get('secret') and 'dm') or 'msg'
                else:
                    obj['type'] = x['type']
                    
                obj['user'] = (x.get('from') and x['from']['name']) or (x.get('user') and x['user']['name']) or ''
                obj['url'] = x.get('url') or ''
                obj['trip'] = (x.get('from') and x['from'].get('tripcode')) or (x.get('user') and x['user'].get('tripcode')) or ''
                obj['msg'] = x.get('content') or x.get('message') or ''
                t.append(obj)
        
        return t
    

    def _msgFormat(self, text, me=False):
        if '/me' in text: 
            text = text.replace('/me', '')
            me = True

        def textSplit(t):
            arr = []
            pre = ''
            splText = t.split()
            for x in splText:
                a = pre + ' ' + x
                if not pre:
                    if len(splText) == 1: return [x]
                    pre += x
                elif len(a) <= 135:
                    if splText.index(x) == (len(splText) - 1):
                        arr.append(a)
                        return arr
                    pre = a
                else:
                    if splText.index(x) == (len(splText) - 1):
                        arr.append(pre)
                        arr.append(x)
                        return arr
                    arr.append(pre)
                    pre = x
    
        res = textSplit(text)
        if me:
            arr = []
            for x in res:
                arr.append('/me' + x)
            res = arr
            
        arr = []
        for x in res:
            arr.append({ 'message': x })
        return arr
    

    def _setInfo(self, room):
        self.room = room
        self.users = room.get('users') or []
    

    def getProfile(self):
        r = self._get(f'{DRRRUrl}/profile/?api=json')
        if r['status'] != 200:
            return logging.warning(f"{r['text']}, {r['status']}")

        profile = r['text'].get('profile') or {}
        for i in profile:
            self.profile[i] = profile[i]
    

    def _checkMode(self, t, users):
        arr = []

        for u in users:
            if u['name'] != self.profile['name']:
                if u.get('tripcode'): arr.append('#' + u['tripcode'])
                else: arr.append(u['name'])

        for u in arr:
            if (t == 'whitelist' and u not in self.userlist[t]) or (t == 'blacklist' and u in self.userlist[t]):
                user = ''
                for i in users:
                    if u == i['name'] or u == ('#' + i['tripcode']): user = i['name']
                
                if 'kick' == self.rule['mode'][t]: self.kick(user)
                elif 'ban' == self.rule['mode'][t]: self.ban(user)
                elif 'report' == self.rule['mode'][t]: self.report(user)

        
    def startLoop(self, seconds=1.5):

        if not self.loopId:
            self.loopId = self._Timer(seconds, self._update)
            self.loopId.start()
            logging.info('Bot started')
    

    def stopLoop(self):

        if self.loopId:
            self.loopId.stop()
            self.loopId = None
            logging.info('Bot stopped')


    def _update(self):
        url = DRRRUrl + '/json.php'
        update = self.lastTime

        if update:
            update = update - 60*1000
            url += f'?update={update}'
        
        try:
            r = self._get(url)
            room = r.get('text') or []

            if room.get('error') and 'Not in room' in room['error']:
                self.lounge()
                self.loc = 'lounge'
                return

            self.loc = 'room'
            lastTime = room.get('update') or 0

            if self.lastTime < lastTime:
                self._setInfo(room)
                lastTalks = self._talksFilter(room['talks'], self.lastTime)
                self.lastTime = lastTime
                if self.rule['enable']: self._checkMode(self.rule['type'], self.users)
                self._eventCall(self.events, lastTalks)
        except:
            pass


    def timer(self, seconds=0, minutes=0, hours=0):
        sum_time = seconds + (minutes*60) + (hours*60*60)
        
        def actual_decorator(func):
            def wrapper():
                if sum_time:
                    if func.__name__ not in self.loops:
                        self.loops[func.__name__] = self._Timer(sum_time, func)
                        self.loops[func.__name__].start()
                else:
                    return logging.error('[Timer]: No time set')

            return wrapper()
        return actual_decorator
    

    def later(self, seconds=0, minutes=0, hours=0):
        sum_time = seconds + (minutes*60) + (hours*60*60)

        def actual_decorator(func):
            def wrapper():
                if sum_time:
                    task = self._Later(sum_time, func)
                    task.start()
                else:
                    return logging.error('[Later]: No time set')

            return wrapper()
        return actual_decorator


    def _eventCall(self, events, obj):
        for e in events:
            for o in obj:
                if e in o['type']:
                    if o['trip']: o['trip'] = '#' + o['trip']

                    for f in events[e]:
                        i = list(f.keys())[0]
                        cmd = f[i]['cmd']
                        users = f[i]['users']
                        trips = [users.pop(users.index(x)) for x in users if x.startswith('#')]
                        func = f[i]['func']

                        if (cmd and o['msg'].startswith(cmd)) or not cmd:
                            if ((users and o['user'] in users) or (trips and o['trip'] in trips)) or (not users and not trips):
                                return func(o)

        
    def event(self, types: list[str] = [], command: str = '', users: list[str] = []):
        type_list = ["msg", "dm", "me", "join", "leave", "new-host",
        "new-description", "room-profile", "music", "kick", "ban"]

        for i in types:
            if i not in type_list:
                logging.error(
                    f'[Event]: '
                    f'types empty or this type(s) is not. All types: '
                    f'["msg", "dm", "me", "join", "leave", "new-host", "new-description", "room-profile", "music", "kick", "ban"]'
                )
                os._exit(1)

        def actual_decorator(func):
            obj = {func.__name__: {'cmd': command, 'users': users, 'func': func}}
           
            def wrapper():
                for t in types:
                    self.events[t] = self.events.get(t) or []
                    self.events[t].append(obj)

            return wrapper()
        return actual_decorator
    

    def _cmd(self, cmd):
        url = DRRRUrl + '/room/?ajax=1&api=json'

        r = self._post(url, cmd)
        if r['status'] != 200:
            logging.warning(f"{r['text']}, {r['status']}")
            return r
        return r


    def __cmd(self, cmd):
        self.queue.append(cmd)

        if not self.queueON:
            self.queueON = True

            def _queue():
                if len(self.queue):
                    r = self._cmd(self.queue.pop(0))
                    x = self._Later(1.5, _queue)
                    x.start()
                    return r
                else: self.queueON = False
            
            _queue()
    

    def whitelist(self, add: list[str]=[], addAll: bool=False, remove: list[str]=[], removeAll: bool=False, on: bool=None, mode: str=''):
        if mode: self.rule['mode']['whitelist'] = mode
        if on:
            self.rule['type'] = 'whitelist'
            self.rule['enable'] = True
        elif on is False: self.rule['enable'] = False

        if add:
            for u in add:
                if u not in self.userlist['whitelist']:
                    self.userlist['whitelist'].append(u)
        
        if remove:
            for u in remove:
                for e in self.userlist['whitelist']:
                    if u == e:
                        self.userlist['whitelist'].remove(u)
        
        if addAll:
            for u in self.users:
                if u['name'] != self.profile['name']:
                    if not u.get('tripcode'): self.userlist['whitelist'].append(u['name'])
                    else: self.userlist['whitelist'].append('#' + u['tripcode'])

        if removeAll:
            for e in self.userlist['whitelist']:
                self.userlist['whitelist'].remove(e)
    

    def blacklist(self, add: list[str]=[], remove: list[str]=[], removeAll: bool=False, on: bool=None, mode: str=''):
        if mode: self.rule['mode']['blacklist'] = mode
        if on:
            self.rule['type'] = 'blacklist'
            self.rule['enable'] = True
        elif on is False: self.rule['enable'] = False

        if add:
            for u in add:
                if u not in self.userlist['blacklist']:
                    self.userlist['blacklist'].append(u)

        if remove:
            for u in remove:
                for e in self.userlist['blacklist']:
                    if u == e:
                        self.userlist['blacklist'].remove(u)
        
        if removeAll:
            for e in self.userlist['blacklist']:
                self.userlist['blacklist'].remove(e)


    def lounge(self):
        r = self._get(f'{DRRRUrl}/lounge?api=json')
        if r['status'] != 200:
            return logging.warning(f"{r['text']}, {r['status']}")

        self.rooms = r['text'].get('rooms') or []
    

    def create(self,
        name: str = 'Just',
        description: str = '',
        limit: int = 5,
        lang: str = 'en-US',
        music: bool = False,
        adult: bool = False,
        hidden: bool = False,
    ):

        form = {
            'name': name,
            'description': description,
            'limit': limit,
            'language': lang,
            'music': music,
            'adult': adult,
            'conceal': hidden,
            'submit': 'Create+Room'
        }
        
        r = self._post(f'{DRRRUrl}/create_room/?api=json', form)
        if r['status'] != 200:
            logging.warning(f"{r['text']}, {r['status']}")
            return r
        
        self._update()
        return r
    

    def join(self, id: str):
        r = self._get(f'{DRRRUrl}/room/?id={id}&api=json')
        if r['status'] != 200:
            logging.warning(f"{r['text']}, {r['status']}")
            return r

        self._update()
        return r
    

    def title(self, name: str):
        name = name[:20]
        r = self.__cmd({ 'room_name': name })
        return r
    

    def desc(self, desc: str):
        r = self.__cmd({ 'room_description': desc })
        return r
    

    def host(self, name: str):
        u = ''
        for x in self.users:
            if x['name'] == name:
                u = x
        if not u:
            return logging.warning(f"[Host]: {name} - not found.")
        r = self.__cmd({ 'new_host': u['id'] })
        return r
    

    def dj(self, mode: bool):
        r = self.__cmd({ 'dj_mode': mode })
        return r
    

    def music(self, name: str, url: str):
        r = self.__cmd({ 'music': 'music', 'name': name, 'url': url })
        return r
    

    def msg(self, msg: str, url: str = ''):
        msg = self._msgFormat(msg)

        if url: msg[0]['url'] = url
        for x in msg:
            self.__cmd(x)
    

    def dm(self, name: str, msg: str, url: str = ''):
        u = ''
        msg = self._msgFormat(msg)
        
        for x in self.users:
            if x['name'] == name:
                u = x
        if not u:
            return logging.warning(f"[Dm]: {name} - not found.")

        if url: msg[0]['url'] = url
        for x in msg:
            x['to'] = u['id']
            self.__cmd(x)
    

    def kick(self, name: str):
        u = ''
        for x in self.users:
            if x['name'] == name:
                u = x
        if not u:
            return logging.warning(f"[Kick]: {name} - not found.")
        r = self.__cmd({ 'kick': u['id'] })
        return r
    

    def ban(self, name: str):
        u = ''
        for x in self.users:
            if x['name'] == name:
                self._users[x['name']] = x
                u = x
        if not u: return logging.warning(f"[Ban]: {name} - not found.")
        r = self.__cmd({ 'ban': u['id'] })
        return r
    

    def report(self, name: str):
        u = ''
        for x in self.users:
            if x['name'] == name:
                self._users[x['name']] = x
                u = x
        if not u: return logging.warning(f"[Report]: {name} - not found.")
        r = self.__cmd({ 'report_and_ban_user': u['id'] })
        return r
    

    def unban(self, name: str):
        u = self._users.get(name) or []
        if u:
            r = self.__cmd({ 'unban': u['id'], 'userName': name })
            return r
        else: return False
    

    def leave(self):
        r = self.__cmd({ 'leave': 'leave' })
        return r