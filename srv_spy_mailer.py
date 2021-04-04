#!/usr/bin/env python
# -*- coding:utf-8 -*-

import smtplib, subprocess, socket
#задаем почту для уведомлений
recipient = 'my@orensupport.ru'


def datatime():
    '''Функция получения времени.

    Формат: 2020.01.28 21:37:38'''
    from datetime import datetime
    return datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")


def send_message(recipient, subject, body):
    '''Функция отправки почты

    Используем стоковый mail -s'''
    process = subprocess.Popen(['mail', '-s', subject, recipient],
                               stdin=subprocess.PIPE)
    process.communicate(body)

def process_spy(process_name):
    '''Детектим запущенные процессы

    Кол-во процессов = 0 - значит что-то пошло не так'''
    proc_status = subprocess.check_output("ps -ef | grep -v grep | grep "+process_name+" | wc -l", shell = True)
    if int(proc_status[0:1]) == 0:
        command2str="service "+process_name+" restart"
        subprocess.call(command2str.split())
        body= 'Warning: Процесс '+process_name+' остановился и был перезапущен.'+'\n'+'Время остановки процесса: '+datatime()+'\n'+'На машине: ' + socket.gethostname()
        send_message(recipient, 'Мониторинг: '+process_name+' перезапущен', body)

#Подсовываем в функцию имена нужных процессов для отслеживания
process_spy('apache2')
process_spy('mysql')
