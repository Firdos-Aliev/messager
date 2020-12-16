import dis


class ServerVerifier(type):
    """Мета класс сервера"""
    def __init__(cls, clsname, bases, clsdict):

        components = []

        for function in clsdict:
            try:
                ret = dis.get_instructions(clsdict[function])
            except Exception as e:
                print(e)
            for i in ret:
                components.append(i.argval)

        if 'connect' in components:
            raise TypeError("Connect в серверной части")
        if not ('AF_INET' in components):
            raise TypeError("Не TCP соединение")
        if not ('SOCK_STREAM' in components):
            raise TypeError("Не TCP соединение")
        type.__init__(cls, clsname, bases, clsdict)


class ClientVerifier(type):
    """Мета класс клиента"""
    def __init__(cls, clsname, bases, clsdict):

        super().__init__(clsname, bases, clsdict)
        components = []
        ret = []
        for function in clsdict:
            try:
                ret = dis.get_instructions(clsdict[function])
            except Exception as e:
                pass
                #print(e)
            for i in ret:
                components.append(i.argval)

        if 'accept' in components:
            raise TypeError("Connect в серверной части")
        if 'listen' in components:
            raise TypeError("Connect в серверной части")
        if not ('AF_INET' in components):
            print("----------------------------------------------------------------------------")
            raise TypeError("Не TCP соединение")
        if not ('SOCK_STREAM' in components):
            print("----------------------------------------------------------------------------")
            raise TypeError("Не TCP соединение")
        type.__init__(cls, clsname, bases, clsdict)
