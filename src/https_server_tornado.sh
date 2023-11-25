#!/bin/bash
logname='https_server_tornado.log'
pyname='https_server_tornado.py'
pidfile='https_server_tornado.pid'

case "$1" in
    start)
        echo "Starting the server..."
        nohup python -u $pyname >> $logname 2>&1 &
        echo $! > $pidfile  # Save the process ID to a file
        tail -f $logname
        ;;
    stop)
        echo "Stopping the server..."
        if [ -e $pidfile ]; then
            pid=$(cat $pidfile)
            kill $pid
            rm $pidfile
            echo "Server stopped."
        else
            echo "Server is not running."
        fi
        ;;
    status)
        if [ -e $pidfile ]; then
            pid=$(cat $pidfile)
            echo "Server is running with process ID $pid."
        else
            echo "Server is not running."
        fi
        ;;
    *)
        echo "Usage: $0 {start|stop|status}"
        exit 1
        ;;
esac

exit 0