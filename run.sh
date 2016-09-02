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
    printf "${RED}REMOVED ALL 'JUNK' FILES.${NORMAL}\n\n"
}


install_dependencies(){
    printf "${YELLOW}INSTALLING REQUIRED DEPENDENCIES...${NORMAL}\n"
    pip install pdoc
    pip install -e .
    printf "${GREEN}DONE.${NORMAL}\n\n"
}

new_docs(){
    rm -rf ./docs
    pdoc --html --overwrite --html-dir ./docs tktable.py
    printf "${GREEN}NEW DOCUMENTATION GENERATED.${NORMAL}\n\n"
}

new_virtualenv(){
    # Creates and switches to the new virtual environment
    printf "${YELLOW}CREATING NEW VIRTUAL ENVIRONMENT...${NORMAL}\n"

    command -v virtualenv
    rc=$?; 
    if [[ $rc != 0 ]]; then 
        printf "${RED}COMMAND 'virtualenv' NOT FOUND.\nINSTALLING IT USING 'pip3.5'...${NORMAL}\n";
        pip3.5 install virtualenv
    fi

    virtualenv venv
    printf "${GREEN}DONE.${NORMAL}\n\n"

    source venv/bin/activate
    printf "${YELLOW}USING THE NEWLY CREATED VIRTUAL ENVIRONMENT...${NORMAL}\n\n"

    # installing dependencies inside the virtual environment
    install_dependencies
    new_docs
    tktable_demo -test

    deactivate
    printf "${YELLOW}EXITED FROM VIRTUAL ENVIRONMENT.${NORMAL}\n\n"
}

run() {
    clean
    new_virtualenv
    clean
}

run