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

        from requests import adapters
        adapters.DEFAULT_RETRIES = 1

        def __checkProxyHttp(self):
            from requests import Session
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
            result = False
            with Session() as httpSession:
                httpSession.proxies = proxydict
                try:
                    httpSession.get(self.testingWebsite, timeout=self.disconnectionTime)
                    result = True
                except KeyboardInterrupt:
                    raise
                except:
                    pass
            return result

        def __checkProxyHttps(self):
            from requests import Session
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
            result = False
            with Session() as httpSession:
                httpSession.proxies = proxydict
                try:
                    httpSession.get(self.testingWebsite, timeout=self.disconnectionTime)
                    result = True
                except KeyboardInterrupt:
                    raise
                except:
                    pass
            return result

        def __checkProxySock5(self):
            from requests import Session

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

            result = False

            with Session() as httpSession:
                httpSession.proxies = proxydict
                try:
                    httpSession.get(self.testingWebsite.replace('www.', ''), timeout=self.disconnectionTime)
                    result = True
                except KeyboardInterrupt:
                    raise
                except:
                    pass
            return result

        def __checkProxySock4(self):
            from requests import Session

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
            result = False
            with Session() as httpSession:
                httpSession.proxies = proxydict
                try:
                    httpSession.get(self.testingWebsite.replace('www.', ''), timeout=self.disconnectionTime)
                    result = True
                except KeyboardInterrupt:
                    raise
                except:
                    pass
            return result

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
        self.printingThreadVar = None
        self.totalChecked = False
        self.stopPrinting = False
        self.validProxies = list()
        self.Pool = dict(started=False, threadsPool=list(), threadsPoolCounter=0)
        self.workingCounter = 0
        self.nonWorkingCounter = 0
        self.finishedCounter = 0
        self.status = 'start'
        self.pool = 'False'
        self.start()

    def threadPoolRemove(self):
        from time import time
        startTime = time()
        counter = 0
        while self.Pool['threadsPool'] or not self.totalChecked:
            thread = self.Pool['threadsPool'][counter % len(self.Pool['threadsPool'])] if self.Pool['threadsPool'] \
                else None
            if thread and not thread.is_alive():
                self.Pool['threadsPool'].remove(thread)
                self.Pool['threadsPoolCounter'] -= 1
            elif thread and thread.is_alive():
                counter += 1
        self.Pool['started'] = False
        self.stopPrinting = True
        self.printingThreadVar.join()
        print('Time taken to scan %s proxies: ' % self.finishedCounter, time()-startTime)

    def proxyCheckerThread(self, proxyLine):
        proxy = proxyLine.rstrip().rstrip('\\/')
        if proxy in self.validProxies:
            return
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
        self.finishedProxiesWriter.write("%s\n" % proxy)
        self.finishedProxiesWriter.flush()
        self.workingProxiesWriter.flush()
        self.nonworkingProxiesWriter.flush()

    def printingThread(self):
        finishedCounter = 0
        status = ''
        pooling = 'True'
        while not self.stopPrinting:
            if finishedCounter != self.finishedCounter or status != self.status or pooling != self.pool:
                print('Valid proxies:', self.workingCounter,
                      '- Invalid proxies:', self.nonWorkingCounter,
                      '- Total proxies:', self.finishedCounter,
                      '- status:', self.status,
                      '- Pooling: ', self.pool)
                finishedCounter = self.finishedCounter
                status = self.status
                pooling = self.pool

    def proxylistIterator(self):
        from threading import Thread
        from os import stat
        checkerThread = Thread(target=self.threadPoolRemove, daemon=True)
        self.printingThreadVar = Thread(target=self.printingThread, daemon=True)
        checkerThread.start()
        self.printingThreadVar.start()
        self.proxiesReader = open(self.inputProxies, 'r')
        self.workingProxiesWriter = open(self.outputWorkingProxies, 'a+')
        if stat(self.outputWorkingProxies).st_size != 0:
            self.workingProxiesWriter.seek(0)
            self.validProxies += self.workingProxiesWriter.read().splitlines(False)
            self.validProxies = list(set(self.validProxies))
            self.workingProxiesWriter.seek(0)
            self.workingProxiesWriter.truncate()
            self.workingProxiesWriter.writelines([x + '\n' for x in self.validProxies])
        self.nonworkingProxiesWriter = open(self.outputNonWorkingProxies, 'a+')
        self.finishedProxiesWriter = open(self.finishedProxies, 'a+')
        for proxy in self.proxiesReader:
            proxy = proxy.rstrip().rstrip('\\/')
            if not proxy:
                continue
            while True:
                try:
                    if self.Pool['threadsPoolCounter'] < self.maxThreadsNumber:
                        self.pool = 'False'
                        proxyThread = Thread(target=self.proxyCheckerThread, args=(proxy,), daemon=True)
                        proxyThread.start()
                        self.Pool['started'] = True
                        self.Pool['threadsPool'].append(proxyThread)
                        self.Pool['threadsPoolCounter'] += 1
                        break
                    else:
                        self.pool = 'True'
                except RuntimeError:
                    self.pool = 'Waiting'
                except Exception as e:
                    print('an error occurred in main iterator', e)
                    input()

        self.totalChecked = True
        checkerThread.join()

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
            self.validProxies = list()
            self.Pool = dict(started=False, threadsPool=list(), threadsPoolCounter=0)
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
                self.disconnectionTime = int(disconnectionTime) if disconnectionTime.isnumeric() else 1
                self.testingWebsite = testingWebsite if testingWebsite else 'https://www.google.com'
                self.maxThreadsNumber = float(threadsNumber) if threadsNumber.isnumeric() else 100
                self.proxylistIterator()


tpctProxyChecker()
