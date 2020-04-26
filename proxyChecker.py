class tpctProxyChecker:
    class proxyChecker:
        def __init__(self, proxyIp, proxyPort, proxyUsername=None, proxyPassword=None,
                     testingWebsite='https://www.google.com', timeout=10):
            self.proxyIp = proxyIp
            self.proxyPort = proxyPort
            self.proxyUsername = proxyUsername
            self.proxyPassword = proxyPassword
            self.disconnectionTime = timeout
            self.testingWebsite = testingWebsite
            self.result = self.checkProxy()

        def __bool__(self):
            return self.result

        def __checkProxyHttp(self):
            from requests.adapters import HTTPAdapter
            from requests import exceptions, Session

            httpSession = Session()
            httpSession.mount(self.testingWebsite, HTTPAdapter(max_retries=5))
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
                httpSession.get(self.testingWebsite, timeout=(self.disconnectionTime, 0.1))
                return True
            except (exceptions.ConnectTimeout,
                    exceptions.TooManyRedirects, exceptions.InvalidURL, exceptions.ProxyError,
                    exceptions.InvalidSchema, exceptions.MissingSchema, exceptions.HTTPError) as e:
                return False
            except (exceptions.ReadTimeout, exceptions.ConnectionError) as e:
                return True

        def __checkProxyHttps(self):
            from requests.adapters import HTTPAdapter
            from requests import exceptions, Session

            httpSession = Session()
            httpSession.mount(self.testingWebsite, HTTPAdapter(max_retries=5))
            proxydict = {'http': 'https://%s:%s@%s:%s' % (self.proxyUsername,
                                                          self.proxyPassword,
                                                          self.proxyIp,
                                                          self.proxyPort)
                         if self.proxyUsername else 'https://%s:%s' % (self.proxyIp,
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
                httpSession.get(self.testingWebsite, timeout=(self.disconnectionTime, 0.1))
                return True
            except (exceptions.ConnectTimeout,
                    exceptions.TooManyRedirects, exceptions.InvalidURL, exceptions.ProxyError,
                    exceptions.InvalidSchema, exceptions.MissingSchema, exceptions.HTTPError) as e:
                return False
            except (exceptions.ReadTimeout, exceptions.ConnectionError) as e:
                return True

        def __checkProxySock5(self):
            from requests.adapters import HTTPAdapter
            from requests import exceptions, Session

            httpSession = Session()
            httpSession.mount(self.testingWebsite, HTTPAdapter(max_retries=5))
            proxydict = {'http': 'socks5://%s:%s@%s:%s' % (self.proxyUsername,
                                                           self.proxyPassword,
                                                           self.proxyIp,
                                                           self.proxyPort)
                         if self.proxyUsername else 'socks5://%s:%s' % (self.proxyIp,
                                                                        self.proxyPort),
                         'https': 'socks5://%s:%s@%s:%s' % (self.proxyUsername,
                                                            self.proxyPassword,
                                                            self.proxyIp,
                                                            self.proxyPort)
                         if self.proxyUsername else 'socks5://%s:%s' % (self.proxyIp,
                                                                        self.proxyPort)
                         }
            httpSession.proxies = proxydict
            try:
                httpSession.get(self.testingWebsite.replace('www.', ''), timeout=(self.disconnectionTime, 0.1))
                return True
            except (exceptions.ConnectTimeout,
                    exceptions.TooManyRedirects, exceptions.InvalidURL, exceptions.ProxyError,
                    exceptions.InvalidSchema, exceptions.MissingSchema, exceptions.HTTPError) as e:
                return False
            except (exceptions.ReadTimeout, exceptions.ConnectionError) as e:
                return True

        def __checkProxySock4(self):
            from requests.adapters import HTTPAdapter
            from requests import exceptions, Session

            httpSession = Session()
            httpSession.mount(self.testingWebsite, HTTPAdapter(max_retries=5))
            proxydict = {'http': 'socks4://%s:%s@%s:%s' % (self.proxyUsername,
                                                           self.proxyPassword,
                                                           self.proxyIp,
                                                           self.proxyPort)
                         if self.proxyUsername else 'socks4://%s:%s' % (self.proxyIp,
                                                                        self.proxyPort),
                         'https': 'socks4://%s:%s@%s:%s' % (self.proxyUsername,
                                                            self.proxyPassword,
                                                            self.proxyIp,
                                                            self.proxyPort)
                         if self.proxyUsername else 'socks4://%s:%s' % (self.proxyIp,
                                                                        self.proxyPort)
                         }
            httpSession.proxies = proxydict
            try:
                httpSession.get(self.testingWebsite.replace('www.', ''), timeout=(self.disconnectionTime, 0.1))
                return True
            except (exceptions.ConnectTimeout,
                    exceptions.TooManyRedirects, exceptions.InvalidURL, exceptions.ProxyError,
                    exceptions.InvalidSchema, exceptions.MissingSchema, exceptions.HTTPError) as e:
                return False
            except (exceptions.ReadTimeout, exceptions.ConnectionError) as e:
                return True

        def checkProxy(self):

            test = self.__checkProxyHttp()
            test = self.__checkProxyHttps() if not test else test
            test = self.__checkProxySock4() if not test else test
            test = self.__checkProxySock5() if not test else test

            return test

    def __init__(self):
        from warnings import simplefilter
        simplefilter('ignore')
        self.maxThreadsNumber = None
        self.inputProxies = None
        self.outputWorkingProxies = None
        self.outputNonWorkingProxies = None
        self.finishedProxies = None
        self.proxyUsername = None
        self.proxyPassword = None
        self.proxyIp = None
        self.proxyPort = None
        self.disconnectionTime = None
        self.testingWebsite = None
        self.proxiesReader = None
        self.workingProxiesWriter = None
        self.nonworkingProxiesWriter = None
        self.finishedProxiesWriter = None
        self.totalChecked = False
        self.Pool = dict(started=False, threadsPool=list())
        self.workingCounter = 0
        self.nonWorkingCounter = 0
        self.finishedCounter = 0
        self.start()
        pass

    def threadPoolRemove(self):
        from time import time
        startTime = time()
        while True:
            for thread in self.Pool['threadsPool']:
                if not thread.is_alive():
                    self.Pool['threadsPool'].remove(thread)
                thread.join()
            if self.Pool['started'] and not self.Pool['threadsPool'] and self.totalChecked:
                break
        print('Time taken to scan %s proxies: ' % self.finishedCounter, time()-startTime)
        self.Pool['started'] = False

    def proxyCheckerThread(self, proxyLine):
        proxy = proxyLine.rstrip().rstrip('\\/')
        from re import match
        searchingPattern = '((.*)\:(.*)?@)?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5})'
        splitter = match(searchingPattern, proxy)
        proxyUsername, proxyPassword, proxyIp, proxyPort = splitter.groups()[1:]
        outputProxy = self.proxyChecker(proxyIp, proxyPort, proxyUsername, proxyPassword,
                                        self.testingWebsite, self.disconnectionTime)
        if outputProxy:
            self.workingProxiesWriter.write('%s\n' % proxy)
            self.workingCounter += 1
        else:
            self.nonworkingProxiesWriter.write('%s\n' % proxy)
            self.nonWorkingCounter += 1
        self.finishedCounter += 1
        print("valid: %s - invalid: %s - finished: %s" % (self.workingCounter,
                                                          self.nonWorkingCounter,
                                                          self.finishedCounter), flush=True)
        self.finishedProxiesWriter.write("%s\n" % proxy)
        self.finishedProxiesWriter.flush()
        self.workingProxiesWriter.flush()
        self.nonworkingProxiesWriter.flush()

    def proxylistIterator(self):
        from threading import Thread
        checkerThread = Thread(target=self.threadPoolRemove, daemon=True)
        checkerThread.start()
        self.proxiesReader = open(self.inputProxies, 'r')
        self.workingProxiesWriter = open(self.outputWorkingProxies, 'a+')
        self.nonworkingProxiesWriter = open(self.outputNonWorkingProxies, 'a+')
        self.finishedProxiesWriter = open(self.finishedProxies, 'a+')
        for proxy in self.proxiesReader:
            proxy = proxy.rstrip().rstrip('\\/')
            if not proxy:
                continue
            checked = False
            while not checked:
                try:
                    while len(self.Pool['threadsPool']) == self.maxThreadsNumber:
                        pass
                    proxyThread = Thread(target=self.proxyCheckerThread, args=(proxy,), daemon=True)
                    proxyThread.start()
                    self.Pool['started'] = True
                    self.Pool['threadsPool'].append(proxyThread)
                    break
                except RuntimeError:
                    pass

        checkerThread.join()

        self.totalChecked = True

    def start(self):
        from os import path
        greetingMsg = '''
         _____  ____  ____  _____    ____  ____  ____ ___  ____  _
        /__ __\/  __\/   _\/__ __\  /  __\/  __\/  _ \\  \//\  \//
          / \  |  \/||  /    / \    |  \/||  \/|| / \| \  /  \  / 
          | |  |  __/|  \__  | |    |  __/|    /| \_/| /  \  / /  
          \_/  \_/   \____/  \_/    \_/   \_/\_\\____//__/\\/_/   
        https://www.facebook.com/taylor.ackerley.9
        https://www.github.com/TPCT
        '''
        print(greetingMsg)
        while True:
            if self.workingProxiesWriter:
                self.workingProxiesWriter.close()
            if self.nonworkingProxiesWriter:
                self.nonworkingProxiesWriter.close()
            if self.finishedProxiesWriter:
                self.finishedProxiesWriter.close()
            if self.proxiesReader:
                self.proxiesReader.close()
            self.maxThreadsNumber = None
            self.inputProxies = None
            self.outputWorkingProxies = None
            self.outputNonWorkingProxies = None
            self.finishedProxies = None
            self.proxyUsername = None
            self.proxyPassword = None
            self.proxyIp = None
            self.proxyPort = None
            self.disconnectionTime = None
            self.testingWebsite = None
            self.proxiesReader = None
            self.workingProxiesWriter = None
            self.nonworkingProxiesWriter = None
            self.finishedProxiesWriter = None
            self.totalChecked = False
            self.Pool = dict(started=False, threadsPool=list())
            self.workingCounter = 0
            self.nonWorkingCounter = 0
            self.finishedCounter = 0
            inputProxiesPath = input('Please enter input proxies path: ').strip().strip('\'"')
            nonWorkingProxiesPath = input('Please enter non-working proxies path: ').strip().strip('\'"')
            workingProxiesPath = input('Please enter working proxies path: ').strip().strip('\'"')
            finishedProxiesPath = input('please enter finished Proxies Path: ').strip().strip('\'"')
            disconnectionTime = input('Please enter disconnection time: ').strip()
            threadsNumber = input('please enter threads number: ').strip()
            testingWebsite = input('please enter website to test: ').strip()
            if path.isfile(inputProxiesPath):
                self.inputProxies = inputProxiesPath
                self.outputWorkingProxies = workingProxiesPath if workingProxiesPath else 'validProxies.txt'
                self.outputNonWorkingProxies = nonWorkingProxiesPath if nonWorkingProxiesPath else 'invalidProxies.txt'
                self.finishedProxies = finishedProxiesPath if finishedProxiesPath else 'finishedProxies.txt'
                self.disconnectionTime = int(disconnectionTime) if disconnectionTime.isalnum() else 1
                self.testingWebsite = testingWebsite if testingWebsite else 'https://www.google.com'
                self.maxThreadsNumber = threadsNumber if threadsNumber else 100
                self.proxylistIterator()


tpctProxyChecker()
