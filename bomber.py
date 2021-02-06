#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import shutil
import sys
import subprocess
import string
import random
import json
import re
import time
import argparse

from concurrent.futures import ThreadPoolExecutor, as_completed

from utils.decorators import MessageDecorator
from utils.provider import APIProvider

try:
    import requests
    from colorama import Fore, Style
except ImportError:
    print("\tНекоторые зависимости не могут быть импортированы (возможно, не установлены)")
    print(
        "Введите `pip3 install -r requirements.txt` чтобы "
        " установить все пакеты")
    sys.exit(1)


def readisdc():
    with open("isdcodes.json") as file:
        isdcodes = json.load(file)
    return isdcodes


def get_version():
    try:
        return open(".version", "r").read().strip()
    except Exception:
        return '1.0'


def clr():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def bann_text():
    clr()
    logo = """
             ███   ██          ██    ███       ███
         ███     ██          ██    ████     ████
       ███       ██          ██    ██ ██   ██ ██
      ██         ██          ██    ██  ██ ██  ██
      ██         ██          ██    ██   ██    ██
      ██         ██          ██    ██         ██
      ██         ██          ██    ██         ██
      ██         ██          ██    ██         ██
      ██         ██          ██    ██         ██
      ███        ██          ██    ██         ██
        ████     ████      ████    ██         ██
          ████       ██████        ██         ██
                                         """
    version = "Версия: "+__VERSION__
    contributors = "Создатели: "+" ".join(__CONTRIBUTORS__)
    print(random.choice(ALL_COLORS) + logo + RESET_ALL)
    mesgdcrt.SuccessMessage(version)
    mesgdcrt.SectionMessage(contributors)
    print()


def check_intr():
    try:
        requests.get("https://motherfuckingwebsite.com")
    except Exception:
        bann_text()
        mesgdcrt.FailureMessage("Обнаружено плохое интернет-соединение")
        sys.exit(2)


def format_phone(num):
    num = [n for n in num if n in string.digits]
    return ''.join(num).strip()


def do_zip_update():
    success = False

    # Download Zip from git
    # Unzip and overwrite the current folder

    if success:
        mesgdcrt.SuccessMessage("TBomb была обновлена до воследней версии")
        mesgdcrt.GeneralMessage(
            "Пожалуйста, запустите скрипт еще раз, чтобы загрузить последнюю версию")
    else:
        mesgdcrt.FailureMessage("Не удалось обновить TBomb.")
        mesgdcrt.WarningMessage(
            "последняя версия https://github.com/Flashk3/TBomb.git")

    sys.exit()


def do_git_update():
    success = False
    try:
        print(ALL_COLORS[0]+"Обновление "+RESET_ALL, end='')
        process = subprocess.Popen("git checkout . && git pull ",
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        while process:
            print(ALL_COLORS[0]+'.'+RESET_ALL, end='')
            time.sleep(1)
            returncode = process.poll()
            if returncode is not None:
                break
        success = not process.returncode
    except Exception:
        success = False
    print("\n")

    if success:
        mesgdcrt.SuccessMessage("TBomb была обновлена до последней версии")
        mesgdcrt.GeneralMessage(
            "Пожалуйста перезапустите скрипт для обновления версии")
    else:
        mesgdcrt.FailureMessage("Не удалось обновить TBomb.")
        mesgdcrt.WarningMessage("Обязательно установите 'git' ")
        mesgdcrt.GeneralMessage("Затем запустите команду:")
        print(
            "git checkout . && "
            "git pull https://github.com/Flashk3/TBomb.git HEAD")
    sys.exit()


def update():
    if shutil.which('git'):
        do_git_update()
    else:
        do_zip_update()

def check_for_updates():
    mesgdcrt.SectionMessage("Проверка обновлений")
    fver = requests.get(
            "https://raw.githubusercontent.com/TheSpeedX/TBomb/master/.version"
            ).text.strip()
    if fver != __VERSION__:
        mesgdcrt.WarningMessage("Доступно обновление")
        mesgdcrt.GeneralMessage("Начало обновления...")
        update()
    else:
        mesgdcrt.SuccessMessage("TBomb был обновлен")
        mesgdcrt.GeneralMessage("Запуск TBomb")


def notifyen():
    try:
        noti = requests.get(
            "https://raw.githubusercontent.com/TheSpeedX/TBomb/master/.notify"
            ).text.upper()
        if len(noti) > 10:
            mesgdcrt.SectionMessage("Уведомлений: " + noti)
            print()
    except Exception:
        pass


def get_phone_info():
    while True:
        target = ""
        cc = input(mesgdcrt.CommandMessage(
            "Введите код страны (с +): "))
        cc = format_phone(cc)
        if not country_codes.get(cc, False):
            mesgdcrt.WarningMessage(
                "код страны который вы ввели ({cc})"
                " Неизвестный или неподдерживаемый код страны".format(cc=cc))
            continue
        target = input(mesgdcrt.CommandMessage(
            "Введите номер телефона грешника: +" + cc + " "))
        target = format_phone(target)
        if ((len(target) <= 6) or (len(target) >= 12)):
            mesgdcrt.WarningMessage(
                "номер грешника ({target})".format(target=target) +
                "Номер недействительный")
            continue
        return (cc, target)


def get_mail_info():
    mail_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    while True:
        target = input(mesgdcrt.CommandMessage("Введите почту грешника: "))
        if not re.search(mail_regex, target, re.IGNORECASE):
            mesgdcrt.WarningMessage(
                "Почта грешника ({target})".format(target=target) +
                " Почта недействительна")
            continue
        return target


def pretty_print(cc, target, success, failed):
    requested = success+failed
    mesgdcrt.SectionMessage("Идет бомбардировка - подождите")
    mesgdcrt.GeneralMessage(
        "Пожалуйста, оставайтесь подключенными к Интернету во время бомбандировки")
    mesgdcrt.GeneralMessage("Цель         : " + cc + " " + target)
    mesgdcrt.GeneralMessage("Отправлено   : " + str(requested))
    mesgdcrt.GeneralMessage("Успешно      : " + str(success))
    mesgdcrt.GeneralMessage("Провалено    : " + str(failed))
    mesgdcrt.WarningMessage(
        "Этот инструмент был создан только для развлекательных и исследовательских целей.")
    mesgdcrt.SuccessMessage("TBomb was created by Flashk3")


def workernode(mode, cc, target, count, delay, max_threads):

    api = APIProvider(cc, target, mode, delay=delay)
    clr()
    mesgdcrt.SectionMessage("Подготовка бомбардировщика - проявите терпение")
    mesgdcrt.GeneralMessage(
        "Пожалуйста, оставайтесь подключенными к Интернету во время бомбандировки")
    mesgdcrt.GeneralMessage("API Версия    : " + api.api_version)
    mesgdcrt.GeneralMessage("Цель          : " + cc + target)
    mesgdcrt.GeneralMessage("Количество    : " + str(count))
    mesgdcrt.GeneralMessage("Ядер          : " + str(max_threads) + " threads")
    mesgdcrt.GeneralMessage("Задержка      : " + str(delay) +
                            " секунд")
    mesgdcrt.WarningMessage(
        "Этот инструмент был создан только для развлекательных и исследовательских целей")
    print()
    input(mesgdcrt.CommandMessage(
        "Нажмите [CTRL+Z] чтобы отменить атаку на Казахстан или [ENTER] чтобы начать"))

    if len(APIProvider.api_providers) == 0:
        mesgdcrt.FailureMessage("Твоя страна или цель не поддерживается")
        mesgdcrt.GeneralMessage("Не стесняйтесь обращаться к нам")
        input(mesgdcrt.CommandMessage("Нажмите [ENTER] чтобы выйти"))
        bann_text()
        sys.exit()

    success, failed = 0, 0
    while success < count:
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            jobs = []
            for i in range(count-success):
                jobs.append(executor.submit(api.hit))

            for job in as_completed(jobs):
                result = job.result()
                if result is None:
                    mesgdcrt.FailureMessage(
                        "Достигнут предел бомбардировки вашей цели")
                    mesgdcrt.GeneralMessage("Попробуйте позже !!")
                    input(mesgdcrt.CommandMessage("Нажмите [ENTER] чтобы выйти"))
                    bann_text()
                    sys.exit()
                if result:
                    success += 1
                else:
                    failed += 1
                clr()
                pretty_print(cc, target, success, failed)
    print("\n")
    mesgdcrt.SuccessMessage("Бомбандировка Казахстана успешна!")
    time.sleep(1.5)
    bann_text()
    sys.exit()


def selectnode(mode="sms"):
    mode = mode.lower().strip()
    try:
        clr()
        bann_text()
        check_intr()
        check_for_updates()
        notifyen()

        max_limit = {"sms": 500, "call": 15, "mail": 200}
        cc, target = "", ""
        if mode in ["sms", "call"]:
            cc, target = get_phone_info()
            if cc != "91":
                max_limit.update({"sms": 100})
        elif mode == "mail":
            target = get_mail_info()
        else:
            raise KeyboardInterrupt

        limit = max_limit[mode]
        while True:
            try:
                message = ("Введите номер для {type}".format(type=mode.upper()) +
                           " чтобы отправить (Max {limit}): ".format(limit=limit))
                count = int(input(mesgdcrt.CommandMessage(message)).strip())
                if count > limit or count == 0:
                    mesgdcrt.WarningMessage("Вы отправили " + str(count)
                                            + " {type}".format(
                                                type=mode.upper()))
                    mesgdcrt.GeneralMessage(
                        "Автоматическое ограничение значения"
                        " для {limit}".format(limit=limit))
                    count = limit
                delay = float(input(
                    mesgdcrt.CommandMessage("введите время ожидания перед сообщениями (в секундах): "))
                    .strip())
                # delay = 0
                max_thread_limit = (count//10) if (count//10) > 0 else 1
                max_threads = int(input(
                    mesgdcrt.CommandMessage(
                        "введите количество сообщений (Рекомендованно: {max_limit}): "
                        .format(max_limit=max_thread_limit)))
                    .strip())
                max_threads = max_threads if (
                    max_threads > 0) else max_thread_limit
                if (count < 0 or delay < 0):
                    raise Exception
                break
            except KeyboardInterrupt as ki:
                raise ki
            except Exception:
                mesgdcrt.FailureMessage("Внимательно прочтите инструкции !!!")
                print()

        workernode(mode, cc, target, count, delay, max_threads)
    except KeyboardInterrupt:
        mesgdcrt.WarningMessage("Получен вызов INTR - Выход...")
        sys.exit()


mesgdcrt = MessageDecorator("icon")
if sys.version_info[0] != 3:
    mesgdcrt.FailureMessage("TBomb работает только на версии Python 3")
    sys.exit()

try:
    country_codes = readisdc()["isdcodes"]
except FileNotFoundError:
    update()


__VERSION__ = get_version()
__CONTRIBUTORS__ = ['SpeedX', 't0xic0der', 'scpketer', 'Stefan']

ALL_COLORS = [Fore.GREEN, Fore.RED, Fore.YELLOW, Fore.BLUE,
              Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
RESET_ALL = Style.RESET_ALL

description = """TBomb - Ваше дружественное приложение для рассылки спама

TBomb можно использовать для многих целей, включая -
\t Предоставление уязвимых API через Интернет
\t Дружественный спам
\t Тест детектора спама и многое другое ....

TBomb не предназначен для злонамеренного использования.
"""

parser = argparse.ArgumentParser(description=description,
                                 epilog='Написано SpeedX, переведенно Flashk3 !!!')
parser.add_argument("-sms", "--sms", action="store_true",
                    help="Начать бомбандировку с SMS модом")
parser.add_argument("-call", "--call", action="store_true",
                    help="Начать бомбандировку с CALL модом")
parser.add_argument("-mail", "--mail", action="store_true",
                    help="Начать бомбандировку с CALL модом")
parser.add_argument("-u", "--update", action="store_true",
                    help="обновить")
parser.add_argument("-c", "--contributors", action="store_true",
                    help="show current TBomb contributors")
parser.add_argument("-v", "--version", action="store_true",
                    help="Посмотреть правильную версию")


if __name__ == "__main__":
    args = parser.parse_args()
    if args.version:
        print("Версия: ", __VERSION__)
    elif args.contributors:
        print("Создатели: ", " ".join(__CONTRIBUTORS__))
    elif args.update:
        update()
    elif args.mail:
        selectnode(mode="mail")
    elif args.call:
        selectnode(mode="call")
    elif args.sms:
        selectnode(mode="sms")
    else:
        choice = ""
        avail_choice = {"1": "SMS", "2": "CALL",
                        "3": "MAIL (Not Yet Available)"}
        try:
            while (choice not in avail_choice):
                clr()
                bann_text()
                print("опции:\n")
                for key, value in avail_choice.items():
                    print("[ {key} ] {value} BOMB".format(key=key,
                                                          value=value))
                print()
                choice = input(mesgdcrt.CommandMessage("Выберите : "))
            selectnode(mode=avail_choice[choice].lower())
        except KeyboardInterrupt:
            mesgdcrt.WarningMessage("Получен INTR пакет, выход из программы...")
            sys.exit()
    sys.exit()
