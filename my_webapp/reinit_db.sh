rm -f dev.db
rm -r migrations/

touch dev.db

echo 'STARTING db init'
docker-compose run --rm manage db init
echo 'STARTING db migrate'
docker-compose run --rm manage db migrate
echo 'STARTING db upgrade'
docker-compose run --rm manage db upgrade