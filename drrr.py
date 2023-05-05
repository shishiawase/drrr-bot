import os
import re
import json
import logging
import requests as req
import threading
from dataclasses import dataclass

DRRRUrl = 'https://drrr.com'
requests = req.Session()

def request(url, **params):

    @dataclass
    class response:
        status: int
        headers: dict
        text: dict | bool

    text = False
    headers = params.get('headers') or None

    if 'data' in params:
        data = params['data']
        res = requests.post(url, headers=headers, data=data)
        if res.text.startswith('{'): text = res.json()
        return response(res.status_code, res.headers, text)

    res = requests.get(url, headers=headers)
    if res.text.startswith('{'): text = res.json()
    return response(res.status_code, res.headers, text)

def rJson(name: str):
    if not os.path.isfile(f'./configs/{name}.json'):
        return False

    with open(f'./configs/{name}.json', 'r+') as f:
        obj = json.load(f)
        return obj


def wJson(name: str, profile: dict):
    if not os.path.exists('./configs'): os.mkdir('./configs')

    obj = {
        'name': profile['name'],
        'icon': profile['icon'],
        'cookie': profile['cookie'],
        'device': profile['device']
    }

    with open(f'./configs/{name}.json', 'w') as f:
        f.write(json.dumps(obj))


def get_logger(
logger_name,
level = logging.ERROR):

    log = logging.getLogger(logger_name)
    log.setLevel(level=logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s: [%(name)s][%(levelname)s] --- %(message)s')

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    ch.setLevel(level=level)

    log.addHandler(ch)
    return  log


class Bot:

    events = {}
    _users = {}
    room = {}
    profile = {}
    loops = {}
    queue = []
    rooms = []
    users = []
    lastTime = 0
    loopId = None
    queueON = False
    loc = 'lounge'
    userlist = {'whitelist': [], 'blacklist': []}
    rule = {'enable': False, 'type': '', 'mode': {'whitelist': 'kick', 'blacklist': 'kick'}}

    def __init__(self, name: str = '***', icon: str = 'setton',
        device: str = 'Bot', lang: str = 'en-US'):

        self.logger = get_logger(f'DRRR({name[:20]})')

        self.profile['name'] = name[:20]
        self.profile['icon'] = icon
        self.profile['lang'] = lang
        self.profile['device'] = device
        

    class _Timer(threading.Thread):
        def __init__(self, t: int, func, args: tuple = ()):

            threading.Thread.__init__(self)
            threading.Thread.name = f'DRRR _Timer ({func.__name__})'
            self.stopped = threading.Event()
            self.func = func
            self.t = t
            self.args = args

        def run(self):
            while not self.stopped.wait(self.t):
                self.func(*self.args)

        def stop(self):
            self.stopped.set()


    class _Later(threading.Thread):
        def __init__(self, t: int, func, args: tuple = ()):
            threading.Thread.__init__(self)
            threading.Thread.name = f'DRRR _Later ({func.__name__})'
            self.stopped = threading.Event()
            self.func = func
            self.t = t
            self.args = args

        def run(self):
            self.stopped.wait(self.t)
            self.func(*self.args)

        
    def login(self):

        def getToken():
            return request(f'{DRRRUrl}/?api=json')
            
        
        r = getToken()
        cookie = r.headers['set-cookie'].partition(';')[0]
        
        self.profile['cookie'] = cookie
        token = r.text['token']

        form = {
            'name': self.profile['name'],
            'login': 'ENTER',
            'token': token,
            'language': self.profile['lang'],
            'icon': self.profile['icon']
        }

        t = self._post(f'{DRRRUrl}/?api=json', form)
        while 'drrr' not in t.headers['set-cookie']:
            t = self._post(f'{DRRRUrl}/?api=json', form)
        
        cookie = t.headers['set-cookie'].partition(';')[0]
        self.profile['cookie'] = cookie
        self.getProfile()

        self.logger.info("Login ok")


    def _post(self, url, cmd):
        headers = { 'Cookie': self.profile['cookie'] }
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        headers['User-Agent'] = self.profile['device']

        return request(url, headers=headers, data=cmd)


    def _get(self, url):
        headers = { 'Cookie': self.profile['cookie'] }
        headers['User-Agent'] = self.profile['device']

        return request(url, headers=headers)
    

    def save(self, name: str = 'config'):
        wJson(name, self.profile)
        self.logger.info('Config saved')
    

    def load(self, name: str = 'config'):
        obj = rJson(name)

        if obj:
            logging.basicConfig(format= f'%(asctime)s [{obj["name"]}][%(levelname)s]%(message)s', level=self.log_level)

            for i in obj:
                self.profile[i] = obj[i]
            self.logger.info('Config loaded')
            self._update()

            return True
        return False


    def _talksFilter(self, talks, time):
        t = []
        
        for x in talks:
            if x['time'] > time:

                class Obj:
                    def __init__(self):
                        if 'message' in x['type']:
                            self.type = (x.get('secret') and 'dm') or 'msg'
                        else:
                            self.type = x['type']
                    
                        self.user = (x.get('from') and x['from']['name']) or (x.get('user') and x['user']['name']) or ''
                        self.url = x.get('url') or ''
                        self.trip = (x.get('from') and x['from'].get('tripcode')) or (x.get('user') and x['user'].get('tripcode')) or ''
                        self.msg = x.get('content') or x.get('message') or ''
                        
                t.append(Obj())
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
    

    def getProfile(self):
        r = self._get(f'{DRRRUrl}/profile/?api=json')
        if r.status != 200:
            return self.logger.warning(f"[getProfile]: {r.status} {r.text}")

        profile = r.text.get('profile') or {}
        for i in profile:
            self.profile[i] = profile[i]
    

    def _checkMode(self, t, users):
        arr = []
        _users = []

        for u in users:
            if u['name'] != self.profile['name']:
                if u.get('tripcode'): arr.append('#' + u['tripcode'])
                arr.append(u['name'])

        for u in arr:
            if (t == 'whitelist' and u not in self.userlist[t]) or (t == 'blacklist' and u in self.userlist[t]):
                for i in users:
                    if (u == i['name'] or u == ('#' + i['tripcode'])) and i['name'] not in _users:
                        _users.append(i['name'])
                
        for user in _users:
            if 'kick' == self.rule['mode'][t]: self.kick(user)
            elif 'ban' == self.rule['mode'][t]: self.ban(user)
            elif 'report' == self.rule['mode'][t]: self.report(user)

        
    def startLoop(self, seconds=1.5):

        if not self.loopId:
            self.loopId = self._Timer(seconds, self._update)
            self.loopId.start()
            self.logger.info('Loop started')
    

    def stopLoop(self):

        if self.loopId:
            self.loopId.stop()
            self.loopId = None
            self.logger.info('Loop stopped')


    def _update(self):
        url = DRRRUrl + '/json.php'
        update = self.lastTime

        if update:
            update = update - 60*1000
            url += f'?update={update}'
        
        try:
            r = self._get(url)
            room = r.text or []
            self.users = room.get('users') or []

            if room.get('error') and 'Not in room' in room['error']:
                self.lounge()
                self.loc = 'lounge'
                return
               

            self.loc = 'room'
            self.room = room
            lastTime = (room.get('talks') and room['talks'][-1].get('time')) or 0

            if self.lastTime < lastTime:
                if not self.lastTime:
                    self.lastTime = lastTime
                    return

                lastTalks = self._talksFilter(room['talks'], self.lastTime)
                self.lastTime = lastTime

                if self.rule['enable']: self._checkMode(self.rule['type'], self.users)
                self._eventCall(self.events, lastTalks)
        except:
            pass


    def timer(self,
        seconds=0,
        minutes=0,
        hours=0,
        count: int = None,
        func_count = None,
        args: tuple = ()):

        sum_time = seconds + (minutes*60) + (hours*60*60)
        
        def actual_decorator(func):
            def wrapper():
                if sum_time:
                    if func.__name__ not in self.loops:
                        self.loops[func.__name__] = self._Timer(
                            sum_time,
                            func,
                            count=count,
                            func_count=func_count,
                            args=args)
                        self.loops[func.__name__].start()
                else:
                    return self.logger.error('[Timer]: No time set')

            return wrapper()
        return actual_decorator
    

    def later(self, seconds=0, minutes=0, hours=0, args: tuple = ()):
        sum_time = seconds + (minutes*60) + (hours*60*60)

        def actual_decorator(func):
            def wrapper():
                if sum_time:
                    task = self._Later(sum_time, func, args=args)
                    task.start()
                else:
                    return self.logger.error('[Later]: No time set')

            return wrapper()
        return actual_decorator


    def _eventCall(self, events, obj):
        for e in events:
            for o in obj:
                if e in o.type:
                    if o.trip: o.trip = '#' + o.trip

                    for f in events[e]:
                        i = list(f.keys())[0]
                        cmd = f[i]['cmd']
                        users = f[i]['users']
                        trips = [users.pop(users.index(x)) for x in users if x.startswith('#')]
                        func = f[i]['func']

                        if (cmd and re.search(rf'{cmd}', o.msg)) or not cmd:
                            if ((users and o.user in users) or (trips and o.trip in trips)) or (not users and not trips):
                                func(o)

        
    def event(self, types: list[str] = [], command: str = '', users: list[str] = []):
        type_list = ["msg", "dm", "me", "join", "leave", "new-host",
        "new-description", "room-profile", "music", "kick", "ban"]

        for i in types:
            if i not in type_list:
                self.logger.error(
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
        if r.status != 200:
            
            self.logger.warning(f"[{list(cmd.keys())[0]}]: {r.status} {r.text}")
            return r
        return r


    def __cmd(self, cmd):
        self.queue.append(cmd)

        if not self.queueON:
            self.queueON = True
            self._cmd(self.queue.pop(0))

            def q():
                if len(self.queue):
                    self._cmd(self.queue.pop(0))
                    self._Later(1.5, q).start()
                else: self.queueON = False
            
            self._Later(1.5, q).start()
    

    def whitelist(self, add: list[str]=[], addAll: bool=False, remove: list[str]=[], removeAll: bool=False, on: bool=None, mode: str=''):
        if mode: self.rule['mode']['whitelist'] = mode

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
            self.userlist['whitelist'] = []
        
        if on:
            self.rule['type'] = 'whitelist'
            self.rule['enable'] = True
            self._checkMode(self.rule['type'], self.users)
        elif on is False: self.rule['enable'] = False
    

    def blacklist(self, add: list[str]=[], remove: list[str]=[], removeAll: bool=False, on: bool=None, mode: str=''):
        if mode: self.rule['mode']['blacklist'] = mode

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
            self.userlist['blacklist'] = []
        
        if on:
            self.rule['type'] = 'blacklist'
            self.rule['enable'] = True
            self._checkMode(self.rule['type'], self.users)
        elif on is False: self.rule['enable'] = False


    def lounge(self):
        r = self._get(f'{DRRRUrl}/lounge?api=json')
        if r.status != 200:
            return self.logger.warning(f"[Lounge]: {r.status} {r.text}")

        self.rooms = r.text.get('rooms') or []
    

    def create(self,
        name: str = 'Just',
        desc: str = '',
        limit: int = 5,
        lang: str = 'en-US',
        music: bool = False,
        adult: bool = False,
        hidden: bool = False,
    ):
        
        form = {
            'name': name[:20],
            'description': desc[:140],
            'limit': limit,
            'language': lang,
            'music': str(music).lower(),
            'adult': str(adult).lower(),
            'conceal': str(hidden).lower(),
            'submit': 'Create+Room'
        }

        r = self._post(f'{DRRRUrl}/create_room/?api=json', form)
        if 'error' in r.text:
            self.logger.warning(f"[Create]: {r.text['error']}")
        if r.status != 200:
            self.logger.warning(f"[Create]: {r.status} {r.text}")
            return r
        
        self._update()
        return r
    

    def join(self, id: str):
        r = self._get(f'{DRRRUrl}/room/?id={id}&api=json')
        if 'error' in r.text:
            self.logger.warning(f"[Join]: {r.text['error']}")
        if r.status != 200:
            self.logger.warning(f"[Join]: {r.status} {r.text}")
            return r

        self._update()
        return r
    

    def title(self, name: str):
        name = name[:20]
        r = self.__cmd({ 'room_name': name })
        return r
    

    def desc(self, desc: str):
        desc = desc[:140]
        r = self.__cmd({ 'room_description': desc })
        return r
    

    def host(self, name: str):
        u = ''
        for x in self.users:
            if x['name'] == name:
                u = x
        if not u:
            return self.logger.warning(f"[Host]: {name} - not found.")
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
            return self.logger.warning(f"[Dm]: {name} - not found.")

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
            return self.logger.warning(f"[Kick]: {name} - not found.")
        r = self.__cmd({ 'kick': u['id'] })
        return r
    

    def ban(self, name: str):
        u = ''
        for x in self.users:
            if x['name'] == name:
                self._users[x['name']] = x
                u = x
        if not u: return self.logger.warning(f"[Ban]: {name} - not found.")
        r = self.__cmd({ 'ban': u['id'] })
        return r
    

    def report(self, name: str):
        u = ''
        for x in self.users:
            if x['name'] == name:
                self._users[x['name']] = x
                u = x
        if not u: return self.logger.warning(f"[Report]: {name} - not found.")
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
