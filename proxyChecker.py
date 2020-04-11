class tpctProxyChecker:
    def __init__(self):
        from requests import Session
        self.session = Session
        self.inputProxies = None  # file that contains input proxies
        self.outputWorkingProxies = None  # file that will contain Working Proxies
        self.outputNonWorkingProxies = None  # file that non-working proxies will be appended to
        self.proxyUsername = None  # username used to login to the proxy
        self.proxyPassword = None  # password used to login to the proxy
        self.proxyIp = None  # proxy Server Ip
        self.proxyPort = None  # listening port for the proxy
        self.disconnectionTime = None  # time taken to block request
        self.testingWebsite = None  # website to test
        self.start()
        pass

    def __checkProxyHttp(self):
        httpSession = self.session()
        proxydict = {'http': 'http://%s:%s@%s:%s' % (self.proxyUsername,
                                                     self.proxyPassword,
                                                     self.proxyIp,
                                                     self.proxyPort)
        if self.proxyUsername else 'http://%s:%s' % (self.proxyIp,
                                                     self.proxyPort),
                     'https': 'http://%s:%s@%s:%s' % (self.proxyUsername,
                                                      self.proxyPassword,
                                                      self.proxyIp,
                                                      self.proxyPort)
                     if self.proxyUsername else 'http://%s:%s' % (self.proxyIp,
                                                                  self.proxyPort)
                     }
        httpSession.proxies = proxydict
        try:
            resp = httpSession.get(self.testingWebsite, timeout=self.disconnectionTime)
            resp = httpSession.get('https://ipinfo.io/json', timeout=self.disconnectionTime).json()
            return True, 'http', True if resp['ip'] == self.proxyIp else False
        except:
            pass
        return False, None, None

    def __checkProxyHttps(self):
        httpSession = self.session()
        proxydict = {'http': 'https://%s:%s@%s:%s' % (self.proxyUsername,
                                                     self.proxyPassword,
                                                     self.proxyIp,
                                                     self.proxyPort)
        if self.proxyUsername else 'http://%s:%s' % (self.proxyIp,
                                                     self.proxyPort),
                     'https': 'https://%s:%s@%s:%s' % (self.proxyUsername,
                                                       self.proxyPassword,
                                                       self.proxyIp,
                                                       self.proxyPort)
                     if self.proxyUsername else 'https://%s:%s' % (self.proxyIp,
                                                                   self.proxyPort)
                     }
        httpSession.proxies = proxydict
        try:
            resp = httpSession.get(self.testingWebsite, timeout=self.disconnectionTime)
            resp = httpSession.get('https://ipinfo.io/json', timeout=self.disconnectionTime).json()
            return True, 'https', True if resp['ip'] == self.proxyIp else False
        except:
            pass
        return False, None, None

    def __checkProxySock5(self):
        httpSession = self.session()
        proxydict = {'http': 'sock5://%s:%s@%s:%s' % (self.proxyUsername,
                                                      self.proxyPassword,
                                                      self.proxyIp,
                                                      self.proxyPort)
        if self.proxyUsername else 'sock5://%s:%s' % (self.proxyIp,
                                                      self.proxyPort),
                     'https': 'sock5://%s:%s@%s:%s' % (self.proxyUsername,
                                                       self.proxyPassword,
                                                       self.proxyIp,
                                                       self.proxyPort)
                     if self.proxyUsername else 'sock5://%s:%s' % (self.proxyIp,
                                                                   self.proxyPort)
                     }
        httpSession.proxies = proxydict
        try:
            resp = httpSession.get(self.testingWebsite, timeout=self.disconnectionTime)
            resp = httpSession.get('https://ipinfo.io/json', timeout=self.disconnectionTime).json()
            return True, 'sock4', True if resp['ip'] == self.proxyIp else False
        except:
            pass
        return False, None, None

    def __checkProxySock4(self):
        httpSession = self.session()
        proxydict = {'http': 'sock4://%s:%s@%s:%s' % (self.proxyUsername,
                                                      self.proxyPassword,
                                                      self.proxyIp,
                                                      self.proxyPort)
        if self.proxyUsername else 'sock4://%s:%s' % (self.proxyIp,
                                                      self.proxyPort),
                     'https': 'sock4://%s:%s@%s:%s' % (self.proxyUsername,
                                                       self.proxyPassword,
                                                       self.proxyIp,
                                                       self.proxyPort)
                     if self.proxyUsername else 'sock4://%s:%s' % (self.proxyIp,
                                                                   self.proxyPort)
                     }
        httpSession.proxies = proxydict
        try:
            resp = httpSession.get(self.testingWebsite, timeout=self.disconnectionTime)
            resp = httpSession.get('https://ipinfo.io/json', timeout=self.disconnectionTime).json()
            return True, 'sock4', True if resp['ip'] == self.proxyIp else False
        except:
            pass
        return False, None, None

    def checkProxy(self):
        """ used to check the proxy if it's working or not.
            used to detect working proxy type (sock4, sock5, http, https)
            :return: this function returns tuple dictionary of (proxyType) -> (proxyProtection) for every working proxy"""

        tests = [self.__checkProxyHttp(),
                 self.__checkProxyHttps(),
                 self.__checkProxySock4(),
                 self.__checkProxySock5()]
        resultDict = dict()

        for (available, Type, protection) in tests:
            if available:
                resultDict[Type] = protection

        return resultDict

    def proxylistIterator(self):
        """
        used to iterate over the proxies in input file and check if there's any working proxy
        create two files (workingProxyFile, nonWorkingProxyFile) and writing to them
        :return: None
        """
        import re
        with open(self.inputProxies, 'r') as proxiesReader, open(self.outputWorkingProxies, 'a+') as workingProxiesWriter,\
                open(self.outputNonWorkingProxies, 'a+') as nonworkingProxiesWriter:
            searchingPattern = '((.*)\:(.*)?@)?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5})'
            for proxy in proxiesReader:
                proxy = proxy.rstrip().rstrip('\\/')
                splitter = re.match(searchingPattern, proxy)
                self.proxyUsername, self.proxyPassword, self.proxyIp, self.proxyPort = splitter.groups()[1:]
                print('[Proxy IP: %s, Port: %s]' % (self.proxyIp, self.proxyPort), end='')
                outputProxy = self.checkProxy()
                if outputProxy:
                    workingProxiesWriter.write('%s -> %s\n' % (proxy, outputProxy))
                    print(' --->  Working')
                else:
                    nonworkingProxiesWriter.write('%s\n' % proxy)
                    print(' --->  Not Working')
                workingProxiesWriter.flush()
                nonworkingProxiesWriter.flush()

    def start(self):
        from os import path
        greetingMsg = '''
         _____  ____  ____  _____    ____  ____  ____ ___  ____  _
        /__ __\/  __\/   _\/__ __\  /  __\/  __\/  _ \\  \//\  \//
          / \  |  \/||  /    / \    |  \/||  \/|| / \| \  /  \  / 
          | |  |  __/|  \__  | |    |  __/|    /| \_/| /  \  / /  
          \_/  \_/   \____/  \_/    \_/   \_/\_\\____//__/\\/_/   
        https://www.facebook.com/taylor.ackerly.9
        https://www.github.com/TPCT
        '''
        print(greetingMsg)
        while True:
            inputProxiesPath = input('Please enter input proxies path: ').strip().strip('\'"')
            nonWorkingProxiesPath = input('Please enter non-working proxies path: ').strip().strip('\'"')
            workingProxiesPath = input('Please enter working proxies path: ').strip().strip('\'"')
            disconnectionTime = input('Please enter disconnection time: ').strip()
            testingWebsite = input('please enter website to test: ').strip()
            if path.isfile(inputProxiesPath) and \
               nonWorkingProxiesPath.strip().strip('/\\') and \
               workingProxiesPath.strip().strip('/\\') and str(disconnectionTime).isalnum():
                self.inputProxies = inputProxiesPath
                self.outputWorkingProxies = workingProxiesPath
                self.outputNonWorkingProxies = nonWorkingProxiesPath
                self.disconnectionTime = int(disconnectionTime)
                self.testingWebsite = testingWebsite
                self.proxylistIterator()


tpctProxyChecker()

