#!/bin/bash
source ./caravela.config


if [ "$#" -eq 0 ]; then
    clear
    source ./draw_caravela.sh
    python main.py
else
    case $1 in
        new)
            python ./commands/new/new.py --pref $preffer --dir $projects_directory
            ;;
        goto)
            python ./commands/goto.py $projects_directory
            ;;
        sail)
            python ./commands/sail.py --names "${server_names[@]}" --locations "${server_locations[@]}"
            ;;
        anchor)
            python ./commands/anchor.py
            ;;
        port)
            echo "$1"
            ;;
        import)
            echo "$1"
            ;;
        *)
            echo "Command be unknown"
            ;;
    esac
fi


