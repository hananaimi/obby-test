for i in {1..5}
do
    curl -s http://localhost:8081/home >/dev/null
    sleep 5
done

for i in {1..5}
do
    curl -s http://localhost:8081/shop >/dev/null
    sleep 5
done

for i in {1..5}
do
    curl -s http://localhost:8081/blog >/dev/null
    sleep 5
done