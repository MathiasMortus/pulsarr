from base import *

from ui import ui_settings

sameline = False
sameline_log = False
config_dir = "."

def ui_cls(path='',update=""):
    os.system('cls' if os.name == 'nt' else 'clear')
    logo(path=path,update=update)

def logo(path='',update=""):
    print('                                                         ')
    print('    ____            __                ')
    print('   / __ \______  __/ /___ ___________')
    print('  / / / / ___/ / / / / __ `/ ___/ ___/')
    print(' / /_/ / /__/ /_/ / / /_/ / /  / /    ')
    print(' \____/\___/\__,_/_/\__,_/_/  /_/     ')
    print('                           [v' + ui_settings.version[0] + ']' + update)
    print()


    print(path)
    print()
    sys.stdout.flush()

def set_log_dir(config):
    global config_dir
    config_dir = config

def ui_print(string: str, debug="true"):
    global sameline
    global sameline_log
    try:
        #log
        if ui_settings.log == "true":
            try:
                with open(config_dir + '/ocularr.log', 'a') as f:
                    if string == 'done' and sameline_log:
                        f.write('done' + '\n')
                        sameline_log = False
                    elif sameline_log and string.startswith('done'):
                        f.write(string + '\n')
                        sameline_log = False
                    elif sameline_log and string.endswith('...'):
                        f.write('done' + '\n')
                        f.write('[' + str(datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")) + '] ' + string  + ' ')
                        sameline_log = True
                    elif string.endswith('...'):
                        f.write('[' + str(datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")) + '] ' + string + ' ')
                        sameline_log = True
                    elif not string.startswith('done') and sameline_log:
                        f.write('done' + '\n')
                        f.write('[' + str(datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")) + '] ' + string + '\n')
                        sameline_log = False
                    elif not string.startswith('done'):
                        f.write('[' + str(datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")) + '] ' + string + '\n')
                        sameline_log = False
            except:
                print('[' + str(datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")) + '] logging error: couldnt write into log file at: ' + config_dir + '/ocularr.log')
        #ui
        if debug == "true":
            if string == 'done' and sameline:
                print('done')
                sameline = False
            elif sameline and string.startswith('done'):
                print(string)
                sameline = False
            elif sameline and string.endswith('...'):
                print('done')
                print('[' + str(datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")) + '] ' + string, end=' ')
                sameline = True
            elif string.endswith('...'):
                print('[' + str(datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")) + '] ' + string, end=' ')
                sameline = True
            elif not string.startswith('done') and sameline:
                print('done')
                print('[' + str(datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")) + '] ' + string)
                sameline = False
            elif not string.startswith('done'):
                print('[' + str(datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")) + '] ' + string)
                sameline = False
            sys.stdout.flush()
    except:
        sys.stdout.flush()
