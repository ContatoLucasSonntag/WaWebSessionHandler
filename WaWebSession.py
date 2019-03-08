from selenium import webdriver
from selenium.webdriver.firefox.options import Options as fireOptions
import os
import platform


# Stack Overflow Code but I don't have the source anymore :/
def get(driver, key=None):
    if key:
        return driver.execute_script('return window.localStorage.getItem("{}")'.format(key))
    else:
        return driver.execute_script('''
        var items = {}, ls = window.localStorage;
        for (var i = 0, k; i < ls.length; i++)
          items[k = ls.key(i)] = ls.getItem(k);
        return items;
        ''')


class WaWebSession:
    def __init__(self, browser=None):
        try:
            self.platform = platform.system().lower()
            self.driver = None
            self.pStorage = {}
            self.Storage = {}
            if browser:
                if browser.lower() == 'chrome':
                    self.choice = 1
                elif browser.lower() == 'firefox':
                    self.choice = 2
                else:
                    print('Browser not supported.'
                          'Please use WaWebSession(browser="chrome")'
                          '           WaWebSession(browser="firefox")'
                          'or         WaWebSession()')
                    raise SyntaxError
            else:
                print('1) Chrome\n'
                      '2) Firefox\n')
                self.choice = int(input('Select a number from the list: '))
            if self.choice == 1:
                self.Options = webdriver.ChromeOptions()
                self.Options.headless = True
                if self.platform == 'windows':
                    self.dir = os.environ['USERPROFILE'] + '\\Appdata\\Local\\Google\\Chrome\\User Data'
                    self.profiles = []
                    self.profiles.append('')
                    for profileDir in os.listdir(self.dir):
                        if 'Profile' in profileDir:
                            if profileDir != 'System Profile':
                                self.profiles.append(profileDir)
                else:
                    print('Only Windows is supported now.')
                    raise OSError
            else:
                self.Options = fireOptions()
                self.Options.set_preference
                self.Options.headless = True
                if self.platform == 'windows':
                    self.dir = os.environ['APPDATA'] + '\\Mozilla\\Firefox\\Profiles'
                    self.profiles = os.listdir(self.dir)
                else:
                    print('Only Windows is supported by now.')
                    raise OSError
        except Exception as e:
            print('Something went wrong: ', e)
            exit(1)

    def get_active(self, profile=None):
        print('Make sure your browser is closed.')
        self.pStorage = {}
        self.Storage = {}
        if profile:
            if self.choice == 1:
                chromeProfile = self.Options
                chromeProfile.add_argument('user-data-dir=%s' % self.dir + '\\' + profile)
                self.driver = webdriver.Chrome(options=chromeProfile)
            else:
                fireProfile = webdriver.FirefoxProfile(self.dir + '\\' + profile)
                self.driver = webdriver.Firefox(fireProfile, options=self.Options)
            self.driver.get('https://web.whatsapp.com/')
            for key, value in get(self.driver).items():
                try:
                    self.Storage[key] = value
                except UnicodeEncodeError:
                    pass
            self.driver.quit()
            return self.Storage
        else:
            for file in self.profiles:
                if self.choice == 1:
                    chromeProfile = self.Options
                    chromeProfile.add_argument('user-data-dir=%s' % self.dir + '\\' + file)
                    self.driver = webdriver.Chrome(options=chromeProfile)
                else:
                    fireProfile = webdriver.FirefoxProfile(self.dir + '\\' + file)
                    self.driver = webdriver.Firefox(fireProfile, options=self.Options)
                self.Storage = {}
                self.driver.get('https://web.whatsapp.com/')
                for key, value in get(self.driver).items():
                    try:
                        self.Storage[key] = value
                    except UnicodeEncodeError:
                        pass
                self.pStorage[file] = self.Storage
            self.driver.quit()
            return self.pStorage

    def create_new(self):
        options = self.Options
        options.headless = False
        if self.choice == 1:
            self.driver = webdriver.Chrome(options=options)
        else:
            self.driver = webdriver.Firefox(options=options)
        self.driver.get('https://web.whatsapp.com/')
        input('Please log in and press Enter...')
        for key, value in get(self.driver).items():
            try:
                self.Storage[key] = value
            except UnicodeEncodeError:
                pass
        self.driver.quit()
        return self.Storage

    def view(self, dict=None, file=None):  # TODO: improve view method | maybe if localStorage could help
        localStorage = dict
        if not localStorage and not file:
            print('No arguments.\n'
                  'Please use view(dict=localStorage_dict)\n'
                  'or         view(file="path")\n')
            raise SyntaxError
        options = self.Options
        options.headless = False
        if self.choice == 1:
            self.driver = webdriver.Chrome(options=options)
        else:
            self.driver = webdriver.Firefox(options=options)
        if file:
            with open(file, 'r') as stor:
                localStorageFile = stor.readlines()
            lines = []
            for line in localStorageFile:
                line.strip('\n')
                lines.append(line.replace('\n', ''))
            self.driver.get('https://web.whatsapp.com/')
            for line in lines:
                line = str(line)
                stor = line.split(' : ')
                self.driver.execute_script(('window.localStorage.setItem("%s", "%s")' % (stor[0], stor[1])))
            self.driver.refresh()
            input('Press Enter to close WhatsApp Web...')
            self.driver.quit()
        elif str(type(localStorage)) == '<class "dict">':
            for item in localStorage:
                if str(type(localStorage[item])) != '<class "str">':
                    print('Format of dict should be > key:value')
                    raise SyntaxError
                else:
                    if self.choice == 1:
                        self.driver = webdriver.Chrome(chrome_options=options)
                    else:
                        self.driver = webdriver.Firefox(options=options)
                    self.driver.get('https://web.whatsapp.com/')
                    for key in localStorage:
                        self.driver.execute_script(('window.localStorage.setItem("%s", "%s")' % (key, localStorage[key])))
                    self.driver.refresh()
                    input('Press Enter to close WhatsApp Web...')
                    self.driver.quit()
        else:
            print('Format of dict should be > key:value')
            raise SyntaxError

    def save2file(self, localStorage, path, name=None):
        if name:
            try:
                name = str(name)
            except Exception:
                print('Name requires a string')
                raise SyntaxError
        try:  # Is there a better way to do that?
            if os.path.isdir(path):
                pass
        except Exception as e:
            print('Folder does not exist.\n', e)
            raise os.error
        if str(type(localStorage)) == "<class 'dict'>":
            for item in localStorage:
                if str(type(localStorage[item])) == "<class 'str'>":
                    single = True
                    if name:
                        if os.path.isfile(path + '\\' + name + '.lwa'):
                            print('File already exists.')
                            raise os.error
                        with open(path + '\\' + name + '.lwa', 'a') as file:
                            try:
                                file.writelines(item + ' : ' + localStorage[item])
                            except UnicodeEncodeError:
                                pass

                elif str(type(localStorage[item])) == "<class 'dict'>":
                    single = False
                    if name:
                        if os.path.isfile(path + '\\' + name + '.lwa'):
                            print('File already exists.')
                            raise os.error
                    else:
                        if os.path.isfile(path + '\\SessionFile.lwa'):
                            print('File already exists.')
                            raise os.error

                    for key in localStorage[item]:
                        checked = False
                        if name:
                            if item == "":
                                with open(path + '\\' + name + '.lwa', 'a') as file:
                                    try:
                                        file.writelines(key + ' : ' + localStorage[item][key] + '\n')
                                    except UnicodeEncodeError:
                                        pass
                            else:
                                if not checked:
                                    if os.path.isfile(path + '\\' + name + '-' + item + '.lwa'):
                                        print('File already exists.')
                                        raise os.error
                                    checked = True
                                with open(path + '\\' + name + '-' + item + '.lwa', 'a') as file:
                                    try:
                                        file.writelines(key + ' : ' + localStorage[item][key] + '\n')
                                    except UnicodeEncodeError:
                                        pass
                        else:
                            if item == "":
                                with open(path + '\\SessionFile.lwa', 'a') as file:
                                    try:
                                        file.writelines(key + ' : ' + localStorage[item][key] + '\n')
                                    except UnicodeEncodeError:
                                        pass
                            else:
                                if not checked:
                                    if os.path.isfile(path + '\\SessionFile-' + item + '.lwa'):
                                        print('File already exists.')
                                        raise os.error
                                    checked = True
                                with open(path + '\\SessionFile-' + item + '.lwa', 'a') as file:
                                    try:
                                        file.writelines(key + ' : ' + localStorage[item][key] + '\n')
                                    except UnicodeEncodeError:
                                        pass
                    if name:
                        if item == "":
                            print('File saved to: ' + path + '\\' + name + '.lwa')
                        else:
                            print('File saved to: ' + path + '\\SessionFile-' + item + '.lwa')
                    else:
                        if item == "":
                            print('File saved to: ' + path + '\\SessionFile.lwa')
                        else:
                            print('File saved to: ' + path + '\\SessionFile-' + item + '.lwa')
            if single:
                if name:
                    print('File saved to: ' + path + '\\' + name + '.lwa')
                else:
                    print('File saved to: ' + path + '\\SessionFile.lwa')
        else:
            print('Input should be a dict with profiles and localStorage or a dict with key and value')
            # TODO: improve Error msg
            raise SyntaxError


if __name__ == '__main__':
    web = WaWebSession()
    print('1) Save session to file\n'
          '2) View session from a file\n')
    choice = int(input('Select a number from the list: '))
    if choice == 2:
        web.view(file=input('Enter file path: '))
    else:
        if not os.path.isdir('saves'):
            os.mkdir('saves')
        web.save2file(web.get_active(), 'saves')