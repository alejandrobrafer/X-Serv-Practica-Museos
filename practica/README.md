NOMBRE: Alejandro Bravo Fernández
TITULACIÓN: Ingeniería en Sistemas de Telecomunicaciones y Administración y Dirección de Empresas.
NOMBRE CUENTA DEL LABORATORIO: abravof
NOMBRE USUARIO GITHUB: alejandrobrafer


PRECULIARIDADES DE LA PARTE OBLIGATORIA:
	* En los ficheros donde haya sido necesario emplear información de fuentes externas a la asignatura, se ha añadido un comentario con 'NOTA' como comienzo para especificar la fuente de los datos.
	* En cuanto a la página principal, entendí que debía mostrar los cinco museos más comentados y también el listado completo de los museos accesibles al pulsar el botón "Accesibles" y el listado de todos los museos al pinchar en "Todos".
	* Al actualizar la BBDD se pierde todos los museos seleccionados en las páginas personales así como el total de museos comentados.
	* No recordaba como se actualizaban las tablas de la BBDD para cambiar el modelo.py, por lo tanto lo que hacía era borrar el 'db.sqlite3' y la carpeta 'migrations' y pegar una nueva carpeta 'migrations' inicial. El modelo final, es resultado de varias modificaciones.
	* El menú de un visitante es distinto al de un usuario registrado, permitiendo a este último más funcionalidades.
	* El fichero CSS tiene como base el template RedTie empleado en clase.
	* Uno de las indicaciones que más me ha costado de interpretar ha sido la de la página 70 párrafo segundo. Finalmente, he supuesto que a lo que se refería era a poder mostrar un listado de sólo los museos accesibles en el recurso /
	* El formulario para cambiar el estilo de un usuario registrado necesita que se especifique como se quiere tanto el tamaño de letra como el color de fondo, si dejamos uno como predeterminado, esa variable adquirirá el valor actual y no el anterior.
	* Las caracterísicas iniciales con las que se solicita la práctica están con el usuario ALEX.


FUNCIONALIDADES OPTATIVAS:
	* Eliminar museo de los seleccionados: Opcional no especificada en el enunciado de la práctica que lo que permite es que un usuario registrado y que haya seleccionado cierto museo, pueda quitarlo de su selección a posteriori.
	* Cambiar contraseña de usuario: Opcional no especificada en el enunciado de la práctica que lo que permite es que un usuario registrado con identificador y contraseña pueda modificarla una vez logeado.
	* Inclusión de un favicon: Opcional que muestra una imagen (de elaboración propia) en la barra de búsqueda o por ejemplo al añadir la página a favoritos asociada al sitio.
	* Generación de un canal XML para los contenidos en la página principal: Opcional que muestra un archivo XML de los datos del Home (los cinco museos más comentados, listado de las páginas personales, listado de los museos accesibles y listado con todos los museos).
	* Generación de un canal RSS con los comentarios de la página web: Opcional que permite seguir los comentarios que se han realizado en los museos de la página web. Un usuario/visitante se pude suscribir al canal y seguir los comentarios de los distintos museos.
	* Funcionalidad de registro de usuarios: Opcional que permite a un visitante registrarse en la web y obtener un espacio personal para seleccionar los museos que más le interesen.
	* Uso de Javascript: Opcional reflejada en el mapa que aparece en la página del museo donde se marca su ubicación.
	* Puntuación de museos: Opcional para que cualquier visitante (usuario o no) pueda añadir +1 a los museos de la página. No se ha controlado que el visitante sólo pueda puntuar un determinado museo sólo una vez.


URL DE LA PARTE OBLIGATORIA: https://youtu.be/jSwdaXeWnSA
URL DE LA PARTE OPCIONAL: https://youtu.be/7k7Oz33miDs