from base import *

import content
import arr
from ui import ui_settings

class setting:
    def __init__(self, name, prompt, cls, key, required=False, entry="", test=None, help="", hidden=False,
                    subclass=False, oauth=False, moveable=True, preflight=False, radio=False, special=False):
        self.name = name
        self.prompt = prompt
        self.cls = cls
        self.key = key
        self.required = required
        self.entry = entry
        self.test = test
        self.hidden = hidden
        self.subclass = subclass
        self.oauth = oauth
        self.help = help
        self.moveable = moveable
        self.preflight = preflight
        self.radio = radio
        self.special = special

    def input(self):
        if self.special:
            self.cls.setup(self.cls)
            return
        elif self.moveable:
            if not self.help == "":
                print(self.help)
                print()
            print('Current ' + self.name + ': "' + str(getattr(self.cls, self.key)) + '"')
            print()
            print('0) Back')
            print('1) Edit')
            print()
            choice = input('Choose an action: ')
        else:
            choice = '1'
        if choice == '1':
            if not isinstance(getattr(self.cls, self.key), list):
                if self.oauth:
                    device_code, user_code = self.cls.oauth()
                    print(self.prompt + str(user_code))
                    console_input = self.cls.oauth(device_code)
                    setattr(self.cls, self.key, console_input)
                    return True
                else:
                    console_input = input(
                        self.prompt + '- current value "' + str(getattr(self.cls, self.key)) + '": ')
                    setattr(self.cls, self.key, console_input)
                    return True
            else:
                lists = getattr(self.cls, self.key)
                if self.radio:
                    print()
                    print('0) Back')
                    if len(lists) > 0:
                        print('1) Change ' + self.entry)
                        print('2) Edit ' + self.entry)
                    else:
                        print('1) Add ' + self.entry)
                    print()
                    choice = input('Choose an action: ')
                elif self.moveable:
                    print()
                    print('0) Back')
                    print('1) Add ' + self.entry)
                    if len(lists) > 0:
                        print('2) Edit ' + self.entry + 's')
                    print()
                    choice = input('Choose an action: ')
                else:
                    choice = '2'
                if choice == '1':
                    if self.subclass:
                        back = False
                        while not back:
                            print()
                            print('0) Back')
                            services = []
                            indices = []
                            index = 0
                            for service in self.cls.__subclasses__():
                                if not service.name in getattr(self.cls,
                                                                self.key) and not '(NOT FUNCTIONAL)' in service.name:
                                    print(str(index + 1) + ') ' + service.name)
                                    indices += [str(index + 1)]
                                    services += [service]
                                    index += 1
                            print()
                            choice = input('Choose a ' + self.entry + ': ')
                            if choice in indices:
                                service = services[int(choice) - 1]
                                service.setup(service, new=True)
                                back = True
                            elif choice == '0':
                                back = True
                    elif self.oauth:
                        edit = []
                        lists = getattr(self.cls, self.key)
                        for prompt in self.prompt:
                            if "code" in prompt:
                                try:
                                    device_code, user_code = self.cls.oauth()
                                except:
                                    print("It seems that this authentification service could not be reached. Please try again at a later time.")
                                    return
                                print(prompt + str(user_code))
                                edit += [self.cls.oauth(device_code)]
                            else:
                                edit += [input(prompt)]
                        lists += [edit]
                        setattr(self.cls, self.key, lists)
                    else:
                        edit = []
                        for prompt in self.prompt:
                            edit += [input(prompt)]
                        lists += [edit]
                        setattr(self.cls, self.key, lists)
                        return True
                elif choice == '2':
                    if not self.radio:
                        print()
                        print('0) Back')
                        indices = []
                        for index, entry in enumerate(lists):
                            if self.moveable:
                                print(str(index + 1) + ') Edit ' + self.entry + ' ' + str(index + 1) + ': ' + str(
                                    entry))
                            else:
                                print(str(index + 1) + ') ' + str(entry))
                            indices += [str(index + 1)]
                        print()
                        index = input('Choose a ' + self.entry + ': ')
                    else:
                        index = '1'
                        indices = ['1', ]
                    back3 = False
                    while not back3:
                        if index == '0':
                            back3 = True
                        if index in indices:
                            if self.moveable and not self.radio:
                                print()
                                print(self.entry.capitalize() + ' ' + index + ': ' + str(lists[int(index) - 1]))
                                print()
                                print('0) Back')
                                print('1) Edit')
                                print('2) Delete')
                                if len(lists) > 1:
                                    print('3) Move')
                                print()
                                choice = input('Choose an action: ')
                            else:
                                choice = '1'
                            back2 = False
                            while not back2:
                                print()
                                if choice == '0':
                                    back2 = True
                                    back3 = True
                                if choice == '1':
                                    if self.subclass:
                                        for service in self.cls.__subclasses__():
                                            if str(lists[int(index) - 1]) == service.name:
                                                service.setup(service)
                                                return True
                                    elif self.oauth:
                                        edit = []
                                        for prompt in self.prompt:
                                            if "code" in prompt:
                                                device_code, user_code = self.cls.oauth()
                                                print(prompt + str(user_code))
                                                edit += [self.cls.oauth(device_code)]
                                            else:
                                                edit += [input(prompt)]
                                        lists[int(index) - 1] = edit
                                        setattr(self.cls, self.key, lists)
                                        return True
                                    else:
                                        edit = []
                                        for k, prompt in enumerate(self.prompt):
                                            response = input(
                                                prompt + '- current value "' + lists[int(index) - 1][k] + '": ')
                                            edit += [response]
                                        lists[int(index) - 1] = edit
                                        setattr(self.cls, self.key, lists)
                                        return True
                                if choice == '2':
                                    del lists[int(index) - 1]
                                    return True
                                if choice == '3':
                                    back = False
                                    while not back:
                                        print('0) Back')
                                        for i in indices:
                                            print(i + ') Position ' + i)
                                        print()
                                        choice = input('Move ' + self.entry + ' ' + index + ' to: ')
                                        if choice == '0':
                                            back = True
                                        if choice in indices:
                                            temp = copy.deepcopy(lists[int(index) - 1])
                                            del lists[int(index) - 1]
                                            lists.insert(int(choice) - 1, temp)
                                            setattr(self.cls, self.key, lists)
                                            return True

    def setup(self):
        if isinstance(getattr(self.cls, self.key), list):
            print()
            working = False
            while not working:
                if self.subclass:
                    print(self.help)
                    print()
                    services = []
                    indices = []
                    index = 0
                    for service in self.cls.__subclasses__():
                        if not '(NOT FUNCTIONAL)' in service.name and not service.name == 'Overseerr':
                            print(str(index + 1) + ') ' + service.name)
                            indices += [str(index + 1)]
                            services += [service]
                            index += 1
                    print()
                    choice = input('Choose a ' + self.entry + ': ')
                    if choice in indices:
                        service = services[int(choice) - 1]
                        service.setup(service, new=True)
                        working = True
                else:
                    edit = []
                    print(self.name + ' - current value: ' + str(getattr(self.cls, self.key)))
                    print()
                    if not self.help == '':
                        print(self.help)
                        print()
                    if self.oauth:
                        edit = []
                        lists = getattr(self.cls, self.key)
                        for prompt in self.prompt:
                            if "code" in prompt:
                                try:
                                    device_code, user_code = self.cls.oauth()
                                except:
                                    print("it seems this authentification service could not be reached right now. Please try again later.")
                                    return
                                print(prompt + str(user_code))
                                edit += [self.cls.oauth(device_code)]
                            else:
                                edit += [input(prompt)]
                        lists += [edit]
                        setattr(self.cls, self.key, lists)
                    else:
                        lists = getattr(self.cls, self.key)
                        for prompt in self.prompt:
                            edit += [input(prompt)]
                        lists = [edit, ]
                        setattr(self.cls, self.key, lists)
                    if self.name == 'Plex users':
                        url = 'https://discover.provider.plex.tv/library/sections/watchlist/all?X-Plex-Token=' + \
                                content.services.plex.users[0][1]
                        response = content.services.plex.session.get(url, headers=content.services.plex.headers)
                        if response.status_code == 200:
                            working = True
                        else:
                            print()
                            print("Looks like this plex token does not work. Please enter a valid token.")
                            print()
                    else:
                        working = True
        else:
            working = False
            while not working:
                print(self.name + ' - current value: ' + str(getattr(self.cls, self.key)))
                print()
                if not self.help == '':
                    print(self.help)
                    print()
                if self.oauth:
                    device_code, user_code = self.cls.oauth()
                    print(self.prompt + str(user_code))
                    console_input = self.cls.oauth(device_code)
                    setattr(self.cls, self.key, console_input)
                else:
                    console_input = input(self.prompt)
                    setattr(self.cls, self.key, console_input)
                if self.name == 'Real Debrid API Key':
                    url = 'https://api.real-debrid.com/rest/1.0/torrents?limit=2&auth_token=' + console_input
                    response = debrid.services.realdebrid.session.get(url)
                    if response.status_code == 200:
                        working = True
                    else:
                        print()
                        print("Looks like the api key does not work. Please enter a valid api key.")
                        print()
                else:
                    working = True

    def set(self, value):
        setattr(self.cls, self.key, value)

    def get(self):
        return getattr(self.cls, self.key)

settings_list = [
    ['Content Services', [
        setting('Content Services', [''], content.services, 'active', entry="content service", subclass=True,
                moveable=False, required=True, preflight=True,
                help='Please choose at least one content service that plex_debrid should monitor for new content.'),
        setting('Plex users', ['Please provide a name for this Plex user: ',
                                'Please provide the Plex token for this Plex user: '], content.services.plex, 'users', entry="user",
                help="Please create a plex user by providing a name and a token. To find the plex token for this user, open your favorite browser, log in to this plex account on 'https://plex.tv' and then visit 'https://plex.tv/devices.xml'. Pick a 'token' from one of the listed devices.",
                hidden=True),
        setting('Plex auto remove',
                'Please choose which media type/s should be removed from your watchlist after successful download ("movie","show","both" or "none"): ',
                content.services.plex.watchlist, 'autoremove', hidden=True,
                help='By default, movies are removed from your watchlist after a successful download. In this setting you can choose to automatically remove shows, shows and movies or nothing.'),
        setting('Trakt users', ['Please provide a name for this Trakt user: ',
                                'Please open your favorite browser, log into this Trakt user and open "https://trakt.tv/activate". Enter this code: '],
                content.services.trakt, 'users', entry="user", oauth=True, hidden=True),
        setting('Trakt lists', [''], content.services.trakt, 'lists', hidden=True),
        setting('Trakt auto remove',
                'Please choose which media type/s should be removed from your watchlist after successful download ("movie","show","both" or "none"): ',
                content.services.trakt.watchlist, 'autoremove', hidden=True,
                help='By default, movies are removed from your watchlist after a successful download. In this setting you can choose to automatically remove shows, shows and movies or nothing.'),
        setting('Trakt early movie releases', 'Please enter "true" or "false": ', content.services.trakt, 'early_releases', help="plex_debrid can check for early releases of movies by checking trakt for 'latest releases' lists. You can turn this feature on or off.",hidden=True),
        setting('Overseerr users', ['Please choose a user: '], content.services.overseerr, 'users', entry="user",
                help="Please specify which users requests should be downloaded by plex_debrid.", hidden=True),
        setting('Overseerr API Key', 'Please specify your Overseerr API Key: ', content.services.overseerr, 'api_key', hidden=True),
        setting('Overseerr Base URL', 'Please specify your Overseerr base URL: ', content.services.overseerr, 'base_url',
                hidden=True),
    ]
        ],
    ['Library Services', [
        setting('Library collection service', [''], content.classes.library, 'active', entry="library collection service", subclass=True,
                radio=True, required=True, preflight=True,
                help='Please choose one library collection service that plex debrid will use to determine your current media collection.'),
        setting('Library update services', [''], content.classes.refresh, 'active', entry="libary update service", subclass=True,
                radio=False, required=True, preflight=True,
                help='Please choose at least one libary update service that plex debrid should update after a complete download'),
        setting('Library ignore services', [''], content.classes.ignore, 'active', entry="libary ignore service", subclass=True,
                radio=False, required=True, preflight=True,
                help='Please choose at least one libary ignore service that plex debrid should use to ignore content that could repeatedly not be found.'),
        setting('Trakt library user', [''], content.services.trakt.library, 'user', hidden=True),
        setting('Trakt refresh user', [''], content.services.trakt.library.refresh, 'user', hidden=True),
        setting('Plex library refresh', [''], content.services.plex.library.refresh, 'sections', hidden=True,moveable=False),
        setting('Plex library partial scan', 'Please enter "true" or "false": ', content.services.plex.library.refresh, 'partial', hidden=True, help="Specify wether or not plex_debrid should attempt to partially scan your plex libraries."),
        setting('Plex library refresh delay', 'Please enter a number (e.g 420 or 69.69): ', content.services.plex.library.refresh, 'delay', hidden=True, help="Specify the amount of seconds plex_debrid should wait between adding a torrent and scanning your plex libraries."),
        setting('Plex server address', 'Please enter your Plex server address: ', content.services.plex.library, 'url', hidden=True),
        setting('Plex library check', [
            'Please specify a library section number that should be checked for existing content before download: '],
                content.services.plex.library, 'check', hidden=True, entry="section",
                help='By default, your entire library (including plex shares) is checked for existing content before a download is started. This setting allows you limit this check to specific library sections. To find a section number, go to "https://app.plex.tv", open your the library you want to include in the check and look for the "source=" parameter in the url.'),
        setting('Plex ignore user', '', content.services.plex.library.ignore, 'user', hidden=True),
        setting('Trakt ignore user', '', content.services.trakt.library.ignore, 'user', hidden=True),
        setting('Local ignore list path', 'Please provide a path where the list ignored media items should be saved: ', content.services.textfile.library.ignore, 'path', hidden=True),
        setting('Jellyfin API Key', 'Please specify your Jellyfin API Key: ', content.services.jellyfin, 'api_key', hidden=True),
        setting('Jellyfin server address', 'Please enter your Jellyfin server address: ', content.services.jellyfin.library, 'url', hidden=True),
    
    ]
        ],
    ['Arr Services', [
        setting('Sonarr Base URL',
                'Please enter your Sonarr base URL (e.g., http://localhost:8989): ',
                arr.services.sonarr, 'base_url', required=True, preflight=True,
                help='The base URL where your Sonarr instance is accessible.'),
        setting('Sonarr API Key',
                'Please enter your Sonarr API Key: ',
                arr.services.sonarr, 'api_key', required=True, preflight=True, hidden=True,
                help='Found in Sonarr under Settings → General → Security'),
        setting('Sonarr Quality Profile ID',
                'Please enter the Quality Profile ID (default: 1): ',
                arr.services.sonarr, 'quality_profile_id', hidden=True,
                help='The quality profile to use for TV shows'),
        setting('Sonarr Root Folder',
                'Please enter the root folder path: ',
                arr.services.sonarr, 'root_folder_path', required=True, preflight=True, hidden=True,
                help='Where TV shows will be stored (e.g., /data/media/tv)'),
        setting('Radarr Base URL',
                'Please enter your Radarr base URL (e.g., http://localhost:7878): ',
                arr.services.radarr, 'base_url', required=True, preflight=True,
                help='The base URL where your Radarr instance is accessible.'),
        setting('Radarr API Key',
                'Please enter your Radarr API Key: ',
                arr.services.radarr, 'api_key', required=True, preflight=True, hidden=True,
                help='Found in Radarr under Settings → General → Security'),
        setting('Radarr Quality Profile ID',
                'Please enter the Quality Profile ID (default: 1): ',
                arr.services.radarr, 'quality_profile_id', hidden=True,
                help='The quality profile to use for movies'),
        setting('Radarr Root Folder',
                'Please enter the root folder path: ',
                arr.services.radarr, 'root_folder_path', required=True, preflight=True, hidden=True,
                help='Where movies will be stored (e.g., /data/media/movies)'),
    ]
        ],
    ['UI Settings', [
        setting('Show Menu on Startup', 'Please enter "true" or "false": ', ui_settings, 'run_directly'),
        setting('Debug printing', 'Please enter "true" or "false": ', ui_settings, 'debug'),
        setting('Log to file', 'Please enter "true" or "false": ', ui_settings, 'log'),
        setting('Watchlist loop interval (sec)', 'Please enter an integer value in seconds: ', ui_settings, 'loop_interval_seconds'),
        setting('version', 'No snooping around! :D This is for compatability reasons.', ui_settings, 'version',
                hidden=True),
    ]
        ],
]
