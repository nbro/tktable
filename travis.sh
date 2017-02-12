#!/usr/bin/env bash

# colors used when printing
GREEN=$(tput setaf 2)
RED=$(tput setaf 1)
NORMAL=$(tput sgr0)
YELLOW=$(tput setaf 3)

clean() {
    find . -type f -name "*.py[co]" -delete
    find . -type d -name "__pycache__" -delete
    rm -rf tktable.egg-info
    rm -rf venv    
    printf "${RED}All 'junk' files removed.${NORMAL}\n\n"
}


install_dependencies(){
    printf "${YELLOW}Installing required dependencies...${NORMAL}\n"
    # pip install pdoc
    pip install -e .
    printf "${GREEN}Done.${NORMAL}\n\n"
}

new_docs(){
    printf "\n${YELLOW}Creating new documentation under './docs'...${NORMAL}\n"
    rm -rf ./docs
    pdoc --html --overwrite --html-dir ./docs tktable.py
    printf "${GREEN}Done.${NORMAL}\n\n"
}


assert_virtualenv_installed()
{
    command -v virtualenv
    if [ $? != 0 ];
    then
        printf "${RED}Command 'virtualenv' not found.\nInstalling it using 'pip3.5'...${NORMAL}\n";
        pip3.5 install virtualenv
    fi
}

new_virtualenv(){
    # Creates and switches to the new virtual environment
    printf "${YELLOW}Creating new virtual environment...${NORMAL}\n"

    assert_virtualenv_installed

    virtualenv venv
    printf "${GREEN}done.${NORMAL}\n\n"

    source venv/bin/activate
    printf "${YELLOW}Using newly created virtual environment...${NORMAL}\n\n"

    # installing dependencies inside the virtual environment
    install_dependencies
    # new_docs
    tktable_demo -test

    deactivate
    printf "${YELLOW}Exited from virtual environment.${NORMAL}\n\n"
}

main() {
    clean
    new_virtualenv
    clean
}

main