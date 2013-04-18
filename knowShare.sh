
case "$1" in 
    start)
	echo "=========================================Starting knowSharePid Server============================================"
	nohup python manage.py runserver 0.0.0.0:9000 &
	LASTPID=$!
	echo $LASTPID > knowShare.pid
    ;;
    stop)
	echo "=========================================Stoping knowSharePid Server============================================"
	KNOWSHAREPID=$(cat /root/knowledgeShare/knowShare.pid)
	echo $KNOWSHAREPID
	pkill -9 -P $KNOWSHAREPID
    ;;
esac
exit 0