# -*- coding: utf-8 -*-
"""
License boilerplate should be used here.
"""

# python 3 imports
from __future__ import absolute_import, unicode_literals

# imports
from datetime import datetime
import signal
import sys
import telnetlib

# app imports
from server.models import Entry, User


def stophandler(signum, frame):
    print('Program closed')
    sys.exit(0)


class Server:
    def __init__(self, host='127.0.0.1', port=5005, timeout=10):
        self.host = host
        self.port = port
        self.timeout = timeout

    def main(self):
        signal.signal(signal.SIGINT, stophandler)
        try:
            print(
                "Conectando con IP:{} Puerto:{}".format(self.host, self.port))
            t = telnetlib.Telnet()
            # t.close()
            t.open(self.host, port=self.port)
            while True:
                telnetinput = t.read_until(b"HOLA", 1)
                start_time = datetime.now()

                if b"Control" in telnetinput:
                    print("Control at {}".format(start_time.isoformat()))
                    continue

                useridentifier = telnetinput[0:11]
                print(useridentifier)
                user, created = User.get_or_create(
                    useridentifier=useridentifier)
                entry = Entry(
                    date=start_time,
                    useridentifier=useridentifier,
                    username=user.username,
                    extra=telnetinput
                )
                if b"Abre" in telnetinput:  # ex. C64BFCC4B5 Abre
                    print("Open at {}".format(start_time.isoformat()))
                    entry.operation = 'Abre'
                    entry.save()
                elif b"Maestra" in telnetinput:  # ex. 1E02420759 Abre 1E02420759 Maestra
                    print("Master at {}".format(start_time.isoformat()))
                    entry.operation = 'Maestra'
                    entry.save()
                elif b"Negra" in telnetinput:  # ex. 3B4BFCD05C Negra
                    print("Banned at {}".format(start_time.isoformat()))
                    entry.operation = 'Negra'
                    entry.save()
                elif b"Cerrado" in telnetinput:  # ex. 6A4BFCE439 Cerrado
                    print("Not allowed at {}".format(start_time.isoformat()))
                    entry.operation = 'Cerrado'
                    entry.save()
        except Exception as e:
            print(e)
            print("fail connection...")
            pass