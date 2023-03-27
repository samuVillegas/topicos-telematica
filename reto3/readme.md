# info de la materia: st0263 Tipicos en Telemática
#
# Estudiante(s): Samuel David Villegas Bedoya, sdvillegab@eafit.edu.co
#
# Profesor: Edwin Nelson Montoya Munera, emontoya@eafit.edu.co
# Reto3
#
# 1. Descripción Actividad
Lo que se pretendía en esta actividad es mostrar el escalamiento de una plataforma monolítica como Wordpress, teniendo capa de datos, servicios y presentación. En total se debían montar 5 nodos ( 1 Balanceador, 2 Wordpress, 1 BD y 1 NFS)

## 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
1. En general se cumplió con el objetivo de montar la arquitectura pedida
## 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
1. Existe un problema con la implementación y es la visualización de archivos estáticos, que posiblemente se solucione agregando algo en la configuración del ngnix.
# 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

2.1 Arquitectura

![image](https://user-images.githubusercontent.com/50517423/227924368-9a999352-6fd0-402a-8d6e-2c1264a70646.png)

En la imagen podemos ver una arquitectura que tiene en total 5 nodos explicados en el punto 1. 

En la capa superior tenemos el acceso a la plataforma por medio de nuestro dominio, el cual está conectado con nuestro servidor de ngnix que tendrá nuestra configuración del ssl y servirá como balanceador de las n instancias de "Wordpress" que queramos poner en la capa de servicios, en nuestro caso solo serán dos nodos, pero lo bueno de esta arquitectura es que nos permite tener esa escalabilidad si llega a ser necesario. La capa de servicios es montada con contenedores e imagenes de docker que apuntan la base de datos a el servidor que creamos de base de datos, y para los archivos a un servidor NFS que nos permitira consultar los archivos de wordpress entre maquinas sin necesidad de tenerlo en todos los nodos de servicio. 

Nota: Si se quisiera realizar una mejora a esta arquitectura se podría implementar a nivel de datos ya que si se cae el servidor de base de datos o de NFS el sistema no funcionaría correctamente. 

# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
1. Primero debemos de crear las 5 maquinas virtuales que tenemos que utilizar con las siguientes configuraciones
- Ubuntu 20.04  
- Para 4 de ellos le ponemos ips privadas estaticas (NFS, BD, WORDPRESS1, WORDPRESS2) y para uno que sería el balanceador una ip pública estatica (NGNIX)
- Solo le habilitamos http y https al de la ip pública
- Puede ser cualquier tipo de máquina, las que se utilizaron fueron E2 small de GCP. 
2. Luego debemos de configurar la máquina de la base de datos así: 
~~~
sudo apt update
sudo apt install docker.io -y
sudo apt install docker-compose -y
sudo apt install git -y
git clone https://github.com/st0263eafit/st0263-231.git
cd st0263-231/docker-nginx-wordpress-ssl-letsencrypt
sudo docker-compose -f docker-compose-solo-wordpress-db.yml up -d
~~~
Allí instalamos docker y docker-compose y creamos un contenedor con una imagen de mysql

3. Luego configuramos el servidor que nos servirá para compartir los archivos de wordpress entre nodos (NFS)
~~~
sudo apt update
sudo apt install nfs-kernel-server -y
sudo mkdir /var/nfs/general -p
sudo chown nobody:nogroup /var/nfs/general
sudo nano /etc/exports
~~~~
Pegamos Lo siguiente: 
~~~
/var/nfs/general    ip_privada_server_wordpress_1(rw,sync,no_subtree_check)
/var/nfs/general    ip_privada_server_wordpress_2(rw,sync,no_subtree_check)
~~~
(Control + x , enter) => Para guardar el archivo

Luego ejecutamos: 
~~~~
sudo systemctl restart nfs-kernel-server
~~~~

4. Configuramos nuestros servidores de wordpress asi:

Nota: Cuando abrimos el archivo docker-compose-solo-wordpress-with-nfsclient.yml cambiamos <ip-private> por la ip privada del servidor de BD creado en el punto 1

~~~
sudo apt update -y
sudo apt install nfs-common -y
sudo mkdir -p /mnt/wordpress
sudo mount ip_servidor_nfs:/var/nfs/general /mnt/wordpress
sudo apt install docker.io -y
sudo apt install docker-compose -y
sudo apt install git -y
sudo systemctl enable docker
sudo systemctl start docker
git clone https://github.com/st0263eafit/st0263-231.git
cd st0263-231/docker-nginx-wordpress-ssl-letsencrypt
sudo nano docker-compose-solo-wordpress-with-nfsclient.yml
sudo docker-compose -f docker-compose-solo-wordpress-with-nfsclient.yml up -d
~~~
  
5. Creamos nuestro Dominio
  
Para este paso necesitamos crear un dominio en algún proveedor y que tengamos acceso a las configuraciones del mismo. 
  
6. Configuramos el servidor con el ngnix
~~~
sudo apt-get update
sudo apt-get install nginx -y 
sudo systemctl start nginx
sudo systemctl enable nginx
sudo add-apt-repository ppa:certbot/certbot
sudo apt install letsencrypt -y
sudo certbot --server https://acme-v02.api.letsencrypt.org/directory -d *.nuestrodominio --manual --preferred-challenges dns-01 certonly
~~~
**SSL**
El último comando lo que nos permitirá es crear un certificado ssl, para esto seguimos los pasos que nos dicen en consola, siendo el más importante verificar el dominio, para esto cerbot nos pedirá crear un registro txt en la configuración de nuestro dominio con un nombre y valor que el nos proporcione, creamos el registro y luego le damos aceptar en consola, el validará que si tengamos el registro. Si todo está bien, nos generará en cierta ubicación de nuestra maquina los certificados, los cuales pondremos en nuestro ngnix.config. 
  
Nota: Se recomienda verificar el registro en algún programa de lookup antes de darle aceptar
  
**ngnix.config**
  
Accedemos al ngnix.config
~~~
sudo nano /etc/nginx/nginx.conf
~~~

Ponemos el siguiente contenido:
~~~
events {}
http {
    upstream dominio {
        server 10.142.0.2;
        server 10.142.0.5;
    }
    server {
        listen  80 default_server;
        server_name dominio www.dominio;
        listen 443 ssl;
        ssl on;
        ssl_certificate /etc/letsencrypt/live/dominio/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/dominio/privkey.pem;

        location / {
                proxy_pass http://dominio;
        }
    }

 server{
    if ($host = www.dominio) {
        return 301 https://$host$request_uri;
    }
    if ($host = dominio) {
        return 301 https://$host$request_uri;
    }
    server_name dominio www.dominio;
    listen 80;
    return 404;
  }

}
~~~
  
# IP o nombres de dominio en nube o en la máquina servidor.
DOMINIO: www.samuelvillegas.online

# referencias:
## https://github.com/st0263eafit/st0263-231/tree/main/docker-nginx-wordpress-ssl-letsencrypt
