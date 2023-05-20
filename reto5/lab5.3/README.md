# Parte 1
Los códigos se encuentran en esta carpeta

# Parte 2
## 1. Conexión con primario
![image](https://github.com/samuVillegas/topicos-telematica/assets/50517423/300888a1-0cd8-4a76-a466-e886809fad5b)
## 2. Correr con conexión con hdfs
![image](https://github.com/samuVillegas/topicos-telematica/assets/50517423/e24877f3-315a-43f5-9fdc-62082563b905)
## 3. Correr con conexión a s3
![image](https://github.com/samuVillegas/topicos-telematica/assets/50517423/9d21bbc7-f0e4-4485-86a8-f860b7995deb)
## 4. Correr en Jupyter
![image](https://github.com/samuVillegas/topicos-telematica/assets/50517423/f3ea52f1-1112-4b91-b0d7-1b5a4c56fc6b)
## 5. Explicacion de archivo Data_processing_using_PySpark

1 y 2 Creación de sesión de spark y configuracion de variable spark

3. Se carga del dataset ubicado en s3://st0263sdvillegab/sample_data.csv

5. Se listan las columnas del archivo csv
6. Se halla la longitud de la lista de columnas
7. Se lista el número de registros del csv
8. Se lista el punto 5 y 6
9. Se imprime las características de los campos del csv
10. Se imprime las primeras 5 filas del csv
11. Se seleccionan dos columnas y se listas las primeras 5 filas del csv
12. Información básica sobre el csv
13. Se importa tipos de pyspark.sql.types
14. Creación de una nueva columna llamada "age_after_10_yrs" y a cada registro se le suma 10 años 
15. Se agrega otra columna llamada "age_double" para convertir cada age en double. 
16. Se filtran los registros con los que tengan como mobil = a "Vivo"
17. La misma filtración del 15 pero seleccionando las columnas "age"-"ratings"-"mobile"
18. En las siguientes instrucciones podemos hacer groupBy, distinct, mean, count, sum, max, min, agg con las columnas. 



