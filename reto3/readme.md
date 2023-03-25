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
FALTA 
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

Nota: Cuando abrimos el archivo docker-compose-solo-wordpress-with-nfsclient.yml cambiamos <ip-private> por el id del servidor de BD creado en el punto 1

~~~
sudo apt update -y
sudo apt install nfs-common -y
sudo mkdir -p /mnt/wordpress
sudo mount 10.142.0.4:/var/nfs/general /mnt/wordpress
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
  
5. Creamos nuestro DNS
FALTA
6. Configuramos el servidor con el ngnix
FALTA
# IP o nombres de dominio en nube o en la máquina servidor.
DOMINIO: www.samuelvillegas.online
# 5. otra información que considere relevante para esta actividad.
FALTA
# referencias:
## https://github.com/st0263eafit/st0263-231/tree/main/docker-nginx-wordpress-ssl-letsencrypt
