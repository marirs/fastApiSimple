#!/bin/sh

ProgName=$(basename $0)
  
sub_help(){
    echo "Usage: $ProgName <subcommand>\n"
    echo "Subcommands:"
    echo "    run     Run development server with uvicorn"
    echo "    test    Run all tests"
    echo "    cover   Analys test coverage"
    echo ""
}
  
sub_run(){
    uvicorn server.asgi:app --reload --workers 2 --proxy-headers
}
  
sub_test(){
    pytest
}
  
sub_cover(){
    pytest -s --cov-report term-missing --cov server
}
  
subcommand=$1
case $subcommand in
    "" | "-h" | "--help")
        sub_help
        ;;
    *)
        shift
        sub_${subcommand} $@
        if [ $? = 127 ]; then
            echo "Error: '$subcommand' is not a known subcommand." >&2
            echo "       Run '$ProgName --help' for a list of known subcommands." >&2
            exit 1
        fi
        ;;
esac