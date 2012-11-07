mysql -u root -p < 1_create_paso.sql
mysql -u root -p oldprojects < 2_newprojs.sql
mysql -u root -p < 3_cambio_database.sql
python cambia_database.py