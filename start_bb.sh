#!/bin/bash
# start_xvfb.sh

# Основные переменные
user="ubuntu"    # пользователь из под которого будет запускаться приложение
resolution="700x500x24"    # разрешение экрана виртуального X-сервера
command=nohup python3 /home/ubuntu/bollinger_bot2/bollinger_bot2.py > /home/ubuntu/bb.log 2>&1 &    # программа, которая будет запускаться в фоне

# Запуск виртуального X-сервера и нашей программы внутри него, где
# xvfb-run - скрипт-обёртка для Xvfb
# /tmp/${user}.xvfb.auth - файл, в который запишется MAGIC-COOKIE для авторизации в X-сервере. К этому файлу имеет доступ на чтение только $user
# -screen 0 ${resolution} -auth /tmp/${user}.xvfb.auth - параметры передаваемые Xvfb при запуске
# Номер X-сервера по умолчанию :99, но его можно изменить используя ключ --server-num, если это необходимо

start_command="/usr/bin/xvfb-run -f /tmp/${user}.xvfb.auth -s '-screen 0 ${resolution} -auth /tmp/${user}.xvfb.auth' $command"

# Проверяем имя пользователя. Если оно не совпадает с $user, то запускаем с помощью "su".
# Это необходимо для правильного запуска из под пользователя root (например, при старте системы)

if ( [ "$(whoami)" = "$user" ] ) then
        bash -c "$start_command"
else
        su -c "$start_command" -l $user
fi

