#!/bin/bash

detect_distro() {
    if [[ "$OSTYPE" == linux-android* ]]; then
            distro="termux"
    fi

    if [ -z "$distro" ]; then
        distro=$(ls /etc | awk 'match($0, "(.+?)[-_](?:release|version)", groups) {if(groups[1] != "os") {print groups[1]}}')
    fi

    if [ -z "$distro" ]; then
        if [ -f "/etc/os-release" ]; then
            distro="$(source /etc/os-release && echo $ID)"
        elif [ "$OSTYPE" == "darwin" ]; then
            distro="darwin"
        else 
            distro="invalid"
        fi
    fi
}

pause() {
    read -n1 -r -p "Нажмите любую кнопку для продолжения..." key
}
banner() {
    clear
    echo -e "\e[1;31m"
    if ! [ -x "$(command -v figlet)" ]; then
        echo 'Представляю TBomb'
    else
        figlet Cum
    fi
    if ! [ -x "$(command -v toilet)" ]; then
        echo -e "\e[4;34m Перевод был создан \e[1;32mFlashk3 \e[0m"
    else
        echo -e "\e[1;34mСоздано \e[1;34m"
        toilet -f mono12 -F border Flashk3
    fi
    echo -e "\e[1;34m Welcome\e[0m"
    echo -e "\e[1;32m to the \e[0m"
    echo -e "\e[4;32m CumZone \e[0m"
    echo " "

}

init_environ(){
    declare -A backends; backends=(
        ["arch"]="pacman -S --noconfirm"
        ["debian"]="apt-get -y install"
        ["ubuntu"]="apt -y install"
        ["termux"]="apt -y install"
        ["fedora"]="yum -y install"
        ["redhat"]="yum -y install"
        ["SuSE"]="zypper -n install"
        ["sles"]="zypper -n install"
        ["darwin"]="brew install"
        ["alpine"]="apk add"
    )

    INSTALL="${backends[$distro]}"

    if [ "$distro" == "termux" ]; then
        PYTHON="python"
        SUDO=""
    else
        PYTHON="python3"
        SUDO="sudo"
    fi
    PIP="$PYTHON -m pip"
}

install_deps(){
    
    packages=(openssl git $PYTHON $PYTHON-pip figlet toilet)
    if [ -n "$INSTALL" ];then
        for package in ${packages[@]}; do
            $SUDO $INSTALL $package
        done
        $PIP install -r requirements.txt
    else
        echo "Вы не установили deperences."
        echo "Пожалуйста проверьте установлен ли у вас Python и git."
        echo "Вы можете извлекать TBomb.sh"
        exit
    fi
}

banner
pause
detect_distro
init_environ
if [ -f .update ];then
    echo "Все требования найдены...."
else
    echo 'Установка требований....'
    echo .
    echo .
    install_deps
    echo This Script Was Made By SpeedX > .update
    echo 'Требования установлены....'
    pause
fi
while :
do
    banner
    echo -e "\e[4;31m Please Read Instruction Carefully !!! \e[0m"
    echo " "
    echo "Нажмите 1 чтобы нажать бомбандировку SMS "
    echo "Нажмите 1 чтобы нажать бомбандировку  CALL"
    echo "Нажмите 1 чтобы нажать бомбандировку MAIL"
    echo "Нажмите 4 для обновления (работает на Linux или Linux эмуляторов) "
    echo "Нажмите 5 чтобы закрыть нахуй это хуйню "
    read ch
    clear
    if [ $ch -eq 1 ];then
        $PYTHON bomber.py --sms
        exit
    elif [ $ch -eq 2 ];then
        $PYTHON bomber.py --call
        exit
    elif [ $ch -eq 3 ];then
        $PYTHON bomber.py --mail
        exit
    elif [ $ch -eq 4 ];then
        echo -e "\e[1;34m Установка файлов..."
        rm -f .update
        $PYTHON bomber.py --update
        echo -e "\e[1;34m запустите Bobmer заново..."
        pause
        exit
    elif [ $ch -eq 5 ];then
        banner
        exit
    else
        echo -e "\e[4;32m Неизвестная команда !!! \e[0m"
        pause
    fi
done
