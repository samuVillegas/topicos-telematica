# Reto 2

## Comandos de configuaración inicial

### Instalación de paquetes
```
sudo apt-get upgrade -y
 
sudo apt-get update -y

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash

source ~/.bashrc

nvm install 18.13.0

sudo apt-get install npm -y

sudo apt-get install git -y

sudo apt install apt-transport-https ca-certificates curl software-properties-common -y

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable" -y

sudo apt update -y

sudo apt install docker-ce -y

sudo npm install pm2 -g
```

### Ejecutamos docker para el servidor mom de RabbitMQ
```
sudo docker run -d -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.9-management
```

### Clonamos el proyecto
```
git clone https://github.com/samuVillegas/topicos-telematica.git
```
### Configuramos el servidor del microservicio que utiliza MOM

Accedemos a la carpeta e instalamos dependencias
```
cd ~ && cd topicos-telematica/reto2/server-mom/
npm i
```
Luego creamos un archivo .env en la ruta actual con la siguiente información
```
PORT=4000
PORT_SERVER_MOM=5672
```
Ejecutamos el servidor
```
pm2 start server.js --name server-mom
```

### Configuramos el servidor del microservicio que utiliza GRPC

Accedemos a la carpeta e instalamos dependencias
```
cd ~ && cd topicos-telematica/reto2/server-grpc/
npm i
```
Luego creamos un archivo .env en la ruta actual con la siguiente información
```
PORT=50051
```
Ejecutamos el servidor
```
pm2 start server.js --name server-grpc
```

### Configuramos el Gateway

Accedemos a la carpeta e instalamos dependencias
```
cd ~ && cd topicos-telematica/reto2/gateway/
npm i
```
Luego creamos un archivo .env en la ruta actual con la siguiente información
```
PORT=3000
PORT_SERVER_GRPC=50051
PORT_SERVER_MOM=5672
```
Ejecutamos el servidor
```
pm2 start server.js --name gateway
```

# Comandos cada vez que se inicia la instancia

```
sudo docker run -d -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.9-management
sleep 5
cd ~ && cd topicos-telematica/reto2/server-grpc/
pm2 start server.js --name server-grpc
cd ~ && cd topicos-telematica/reto2/gateway/
pm2 start server.js --name gateway
cd ~ && cd topicos-telematica/reto2/server-mom/
pm2 start server.js --name server-mom

```

# Configuración de script inicial

1. Creamos un archivo llamado startup.sh en (~) y le ingresamos el siguiente contenido
```
sudo docker run -d -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.9-management
sleep 5
cd ~ && cd topicos-telematica/reto2/server-grpc/
pm2 start server.js --name server-grpc
cd ~ && cd topicos-telematica/reto2/gateway/
pm2 start server.js --name gateway
cd ~ && cd topicos-telematica/reto2/server-mom/
pm2 start server.js --name server-mom
```
2. Le damos permiso al archivo
```
sudo chmod +x startup.sh
```
3. Abrimos el archivo .bashrc así 
```
nano ~/.bashrc
```
e ingresamos en la última parte del archivo la ruta del startup.sh, en este caso sería: 
```
/home/ubuntu/startup.sh &
```
Esto permitirá que cuando cada vez que nos conectemos a la consola se ejecuten los servicios necesarios. 

***Nota:*** Posiblemente si nos conectamos una segunda vez a la consola nos salgan errores, esto sucede porque ya tendríamos los servicios montados 

# Temas importante para ejecutar proyecto en instancia creada en AWS
1. Se debe de iniciar la instancia y luego acceder a la consola para que los comandos iniciales se ejecuten correctamente
2. Se debe habilitar el puerto 3000 como regla de entrada para hacer las peticiones en API REST
3. El SO del servidor fue montado en Ubuntu

# Descripción de servicios
1. GET /list_files => Obtiene todos los archivos que existan
2. GET /find_file/{name_file} => Obtiene todos los archivos filtrados por el "name_file"
