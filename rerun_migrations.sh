echo "Removing old migrations:\n"
./remove_old_migrations.sh
echo "\nRecreating database:\n"
python3.6 manage.py reset_db
echo "\nCreating new migrations:\n"
python3.6 manage.py makemigrations
echo "\nMigrating:\n"
python3.6 manage.py migrate
echo "\nDone."
