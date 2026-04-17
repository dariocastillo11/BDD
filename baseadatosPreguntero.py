import pygame
import random
import sys
import time
import textwrap
import sys
import time
import textwrap

pygame.init()
WIDTH, HEIGHT = 480, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("📘 Quiz de Bases de Datos")
font = pygame.font.SysFont("segoe ui", 16)
font_title = pygame.font.SysFont("segoe ui", 28, bold=True)
font_subtitle = pygame.font.SysFont("segoe ui", 18, bold=True)
font_button = pygame.font.SysFont("segoe ui", 14, bold=True)
clock = pygame.time.Clock()

# Colores oscuro profesional
WHITE = (255, 255, 255)
BLACK = (20, 20, 30)
DARK_BG = (25, 30, 45)
DARKER_BG = (15, 20, 30)
PRIMARY = (66, 165, 245)
PRIMARY_HOVER = (41, 128, 185)
SUCCESS = (76, 175, 80)
DANGER = (244, 67, 54)
WARNING = (255, 193, 7)
GRAY = (189, 195, 199)
LIGHT_GRAY = (189, 195, 199)
TEXT_COLOR = (230, 240, 245)
ACCENT = (156, 39, 176)
LIGHT_BG = DARK_BG

estado = "menu"  # puede ser "menu", "quiz", "teoria"
scroll_offset = 0


def draw_button(text, x, y, w, h, color, shadow=True):
    rect = pygame.Rect(x, y, w, h)
    # Sombra
    if shadow:
        shadow_color = (0, 0, 0)
        pygame.draw.polygon(screen, shadow_color, [
            (x + 3, y + 3), (x + w + 3, y + 3), 
            (x + w + 3, y + h + 3), (x + 3, y + h + 3)
        ])
    # Botón
    pygame.draw.rect(screen, color, rect, border_radius=10)
    # Texto
    txt = font.render(text, True, WHITE)
    screen.blit(txt, (x + (w - txt.get_width()) // 2, y + (h - txt.get_height()) // 2))
    return rect


def render_text_surface(text_lines, width):
    ancho_visible = WIDTH - 50
    surface = pygame.Surface((ancho_visible, len(text_lines) * 35))
    surface.fill(WHITE)
    y = 0

    for line in text_lines:
        # Colores por sección
        if line.startswith("📌") or line.startswith("🧱"):
            color = PRIMARY
            font_used = pygame.font.SysFont("segoe ui", 26, bold=True)
            extra_space = 15
        elif line.startswith("🔁") or line.startswith("🔣"):
            color = ACCENT
            font_used = pygame.font.SysFont("segoe ui", 26, bold=True)
            extra_space = 15
        elif line.startswith("📚"):
            color = WARNING
            font_used = pygame.font.SysFont("segoe ui", 26, bold=True)
            extra_space = 15
        elif line.startswith("💡"):
            color = PRIMARY
            font_used = font_button
            extra_space = 10
        elif line.startswith("- "):
            color = TEXT_COLOR
            font_used = font
            extra_space = 5
        else:
            color = TEXT_COLOR
            font_used = font
            extra_space = 5

        # Renderizar línea
        rendered = font_used.render(line, True, color)
        surface.blit(rendered, (10, y))
        y += rendered.get_height() + extra_space

    return surface
def mostrar_teoria():
    global scroll_offset
    teoria_texto = """
📌 MODELO ENTIDAD-RELACIÓN (DER)
- Las interrelaciones uno a muchos (1:N) generan una clave foránea en la entidad del lado “muchos”. No se crea una nueva tabla salvo que la relación tenga atributos propios.
- Las interrelaciones muchos a muchos (N:M) se transforman en una nueva tabla con dos claves foráneas que apuntan a las claves primarias de las entidades vinculadas.
- Las interrelaciones uno a uno (1:1) se pueden implementar agregando una clave foránea en la entidad con menor cantidad de registros, que apunta a la otra.
- Las relaciones de especialización (“es un”) se implementan usualmente con una clave foránea que también es clave primaria, apuntando a la entidad general.
- Los atributos de una relación se colocan en la entidad o tabla que los representa según el tipo de vínculo y la cardinalidad.

🧱 CLAVES
- Clave primaria (PK): identifica de forma única a cada tupla. Debe ser única y no puede contener valores nulos.
- Clave candidata: es un conjunto mínimo de atributos que también pueden identificar de manera única una tupla. Una de ellas se elige como PK.
- Clave foránea (FK): es un atributo o conjunto de atributos que referencia a la clave primaria de otra tabla.
- No se permite que una PK o clave candidata contenga nulos. Una FK puede tener nulos si no hay obligatoriedad de la relación.

🔁 NORMALIZACIÓN
- 1FN (Primera Forma Normal): todos los atributos contienen valores atómicos. No debe haber listas ni grupos repetidos.
- 2FN (Segunda Forma Normal): cumple con 1FN y todos los atributos no clave dependen de toda la clave (no hay dependencias parciales si hay clave compuesta).
- 3FN (Tercera Forma Normal): cumple 2FN y no tiene dependencias transitivas (un atributo no clave no debe depender de otro atributo no clave).
- FNBC (Forma Normal de Boyce-Codd): toda dependencia funcional tiene como determinante una clave candidata. Es una forma más estricta que 3FN.

🔣 DEPENDENCIAS FUNCIONALES
- Una dependencia funcional (DF) expresa que si dos tuplas coinciden en un conjunto de atributos X, también deben coincidir en un conjunto Y (X → Y).
- DF trivial: cuando Y está incluido en X. No aporta información.
- DF no trivial: Y no está incluido en X. Este tipo de DF se usa para encontrar claves y analizar normalización.
- Clausura de F (F+): conjunto de todas las dependencias funcionales que se pueden inferir a partir de un conjunto F inicial. Se usa para encontrar claves candidatas.

📚 DDL y DML
- DDL (Data Definition Language): permite definir y modificar la estructura de la base de datos. Ejemplos: CREATE TABLE, ALTER TABLE, DROP TABLE.
- DML (Data Manipulation Language): permite consultar y modificar los datos dentro de las tablas. Ejemplos: SELECT, INSERT, UPDATE, DELETE.

💡 OTROS CONCEPTOS
- Tupla: es una fila de una tabla, representa una instancia del conjunto de datos.
- Atributo: es una columna de la tabla.
- Dominio: conjunto de valores válidos que puede tomar un atributo.
- Instancia de relación: conjunto actual de tuplas que forman parte de una tabla en un momento específico.
- Álgebra relacional: lenguaje formal para consultar bases de datos relacionales. Una de sus operaciones, la división, sirve para consultas tipo “para todo”.

👉 Usá la rueda del mouse o las teclas ↑ y ↓ para moverte por esta teoría en la interfaz.
"""
    wrapped = []
    for linea in teoria_texto.strip().split("\n"):
        wrapped += textwrap.wrap(linea, width=90) if linea.strip() != "" else [""]
    return render_text_surface(wrapped, WIDTH - 40)
# Preguntas reales (pueden cargarse desde archivo si querés)
preguntas_respuestas = [
    ("Si una interrelación uno a muchos tiene un atributo genera un atributo en la tabla del lado de muchos.", "V"),
    ("Las dependencias funcionales son un caso especial de las dependencias multivaluadas.", "V"),
    ("Un DDL(data definition language) provee un lenguaje para indicar los atributos de una tabla entre otras cosas.", "V"),
    ("En un DER una interrelación uno a uno de tipo 'es un' genera un nuevo campo o conjunto de campos en la tabla que tiene menor cantidad de registros y es una clave foránea que apunta a la clave de la tabla que tiene mayor cantidad de registros.", "V"),
    ("La dependencia funcional X -> Y es trivial si Y es un subconjunto de X(Y c X).", "V"),
    ("Si tengo una relación de la forma EMPLEADO(Legajo,DNI,Nombre, Apellido, Telefono) donde un empleado puede tener más de un teléfono la clave será el conjunto de atributos ('Legajo', 'Teléfono') y el conjunto ('DNI', 'Teléfono') es clave candidata.", "V"),
    ("Una relación uno a muchos en un DER da origen a una nueva tabla.", "F"),
    ("En el análisis de las Formas Normales cada relación se analiza de manera separada del resto de las relaciones.", "V"),
    ("Un DDL(data definition language) provee un lenguaje para la formulación de consultas entre otras cosas.", "F"),
    ("En un DER una interrelación muchos a muchos genera un nuevo atributo/s en la tabla que más tuplas tiene y que es clave foránea hacia la clave principal de la tabla que tiene menos registros.", "F"),
    ("Una dependencia funcional no trivial es aquella queaa tiene del lado izquierdo una clave candidata.", "F"),
    ("Si tengo una relación de la forma EMPLEADO(Legajo, Nombre, Apellido, Telefono) donde un empleado puede tener más de un teléfono, el atributo 'Legajo' es la clave principal y el atributo 'Telefono' es clave candidata.", "F"),
    ("Si tengo una relación de la forma EMPLEADO(Legajo, Nombre, Apellido, Telefono) donde un empleado puede tener más de un teléfono, la clave será el conjunto (Legajo, Telefono).", "V"),
    ("Un DDL(data definition language) provee un lenguaje para eliminar un registro entre otras cosas.", "F"),
    ("En un DER una interacción uno a muchos genera una nueva tabla con dos campos o conjuntos de campos que son claves foráneas a cada una de las claves de ambas tablas.", "F"),
    ("Si una relación cumple con la Forma Normal 3 necesariamente cumple con la Forma Normal 2.", "V"),
    ("Si una interrelación uno a muchos en un DER tiene un atributo este se convierte en un atributo de la entidad del lado uno.", "F"),
    ("Las claves candidatas no necesariamente cumplen con la condición de minimalidad.", "F"),
    ("El conjunto de todas las tuplas posibles de una instancia de relación es el resultado del producto cartesiano de todos los dominios de los atributos de la relación.", "V"),
    ("Las dependencias funcionales determinan que algunas tuplas no son válidas para el dominio del problema que las define.", "V"),
    ("Las dependencias funcionales junto con las dependencias multivaluadas se utilizan para determinar las claves principales y las candidatas.", "F"),
    ("El dominio de un atributo de una relación puede ser un conjunto infinito.", "V"),
    ("Una clave candidata no cumple con el requisito de minimalidad como una clave principal o primaria.", "F"),
    ("El análisis del cumplimiento de las formas normales se realiza por cada esquema de relación independiente de los otros.", "V"),
    ("La forma normal de Boyce Codd es lo suficientemente genérica para detectar todas las anomalías de actualización que pueden producirse.", "F"),
    ("Las formas normales son de cumplimiento obligatorio para un diseño correcto de una Base de Datos.", "F"),
    ("Un esquema indeseable no puede ser implementado en un SGBD.", "F"),
    ("Un DML no es estrictamente un lenguaje de computacion sino una forma de modelar el dominio del problema.", "F"),
    ("Cada tupla es una instancia de un esquema de relación.", "V"),
    ("Las dependencias funcionales se definen en base al dominio del problema.", "V"),
    ("Cuando normalizo una relación lo que hago es dividir la relación para que cumpla con las formas normales.", "V"),
    ("Una relación puede tener una o varias dependencias multivaluadas.", "V"),
    ("La Implicación de Dependencias funcionales permite descomponer una dependencia funcional en varias para normalizar una relación.", "V"),
    ("La operación de división del Álgebra relacional me permite determinar si todos los valores clave de una relación son valor de un campo en otra relación.", "V"),
    ("Si un esquema está normalizado significa que no puede ser subdividido sin pérdida de información.", "V"),
    ("Las claves se deducen a partir de las Dependencias Funcionales y de las Multivaluadas.", "F"),
    ("A todos los atributos de una relación se les puede definir un dominio.", "V"),
    ("Si una relación no tiene dependencias funcionales ni de junta no se le puede definir una clave principal.", "F"),
    ("Una clave foránea siempre apunta a una clave de otra relación.", "F"),
    ("Cuando encontramos un ciclo en el DER y determinamos que hay información redundante, da lo mismo eliminar cualquier interrelación que forma parte del ciclo para eliminar la redundancia.", "F"),
    ("La clausura de F (F+) la utilizo para determinar la clave.", "V"),
    ("Si un conjunto de atributos me determina toda la relación entonces es una clave.", "F"),
    ("Si en una relación encuentro más de una clave quiere decir que la relación está desnormalizada.", "F"),
    ("Una dependencia funcional no trivial es la que tiene más de un atributo del lado izquierdo.", "F"),
    ("Para guardar un árbol jerárquico de datos utilizo una relación con una FK a sí misma.", "V"),
    ("Nunca puedo permitir nulos en los atributos que constituyen una FK.", "F"),
    ("Nunca puedo permitir nulos en los atributos que constituyen una PK.", "V"),
    ("Nunca puedo permitir nulos en los atributos que constituyen una clave candidata.", "V"),
    ("Una relación uno a muchos surge del analisis del dominio del problema.", "V"),
    ("Un DDL (data definition language) provee un lenguaje para crear un nuevo schema entre otras cosas.", "V"),
    ("El cumplimiento de una Forma Normal por parte de una relación es independiente del cumplimiento o no de las FN por otras relaciones vinculadas de la misma base de datos.", "V"),
    ("Una interrelacion muchos a muchos genera una nueva tabla con dos atributos que son claves foraneas a cada una de las claves de ambas tablas.", "V"),
    ("Dada la relación PERSONA(DNI, nombrepersona, apellidopersona, DNIhijo) donde la persona puede tener más de un hijo, esta relación cumple con la forma normal 2 y no cumple con la forma normal 3.", "V"),
    ("Dada la relación PERSONA(DNI, DNIHijoDelaPersona, ProfesionDelaPersona) donde la persona puede tener más de un hijo y más de una profesión, esta relación no cumple con la forma normal 2.", "V"),
    ("Tengo una base de datos en MongoDB y una relación 1:N donde se estima tener un N muy grande, conviene Modelarlo como una coleccion separada?", "V"),
    ("En un DER una interrelación uno a uno de tipo 'es un' genera un nuevo campo o conjunto de campos en la tabla que tiene mayor cantidad de registros y es una clave foránea que apunta a la clave de la tabla que tiene menor cantidad de registros.", "F"),
    ("Una interrelacion uno a muchos genera un atributo clave foranea en la relación del lado del uno que apunta al lado de muchos.", "F"),
    ("Es condición necesaria para que un esquema de relación esté en FNBC que todas las DFs no tengan atributos no clave que dependan de parte de la clave.", "V"),
    ("Un esquema de relación es el conjunto de los atributos de la relación.", "V"),
    ("Para que un esquema de relación se encuentre en 3ra forma Normal no debe existir una dependencia funcional no trivial que no tenga como lado izquierdo una clave candidata.", "F"),
    ("El dominio de un atributo siempre es un conjunto finito.", "F"),
    ("En un diagrama DER una interrelacion uno a muchos, al transformarse a un diseño de esquemas de relación, genera un tercer esquema de relación con claves foraneas apuntando a ambas de las dos entidades vinculadas.", "F"),
    ("En un diagrama DER una interrelacion muchos a muchos, al transformarse a un diseño de esquemas de la relación, genera un tercer esquema de relación con claves foraneas apuntando a ambas de las dos entidades vinculadas.", "V"),
    ("Para que un conjunto de atributos sea una clave candidata no debe cumplir con la condición de minimalidad como la clave principal.", "F"),
    ("Un DML (Data Management Language) provee un lenguaje para la formulacion de consultas entre otras cosas.", "V"),
    ("Las claves candidatas de una relación cumplen con las mismas condiciones que la clave principal.", "V"),
    ("Una SGBD debe garantizar la calidad de los datos.", "F"),
    ("En un DER una interrelacion uno a muchos genera una nueva tabla con dos campos o conjuntos de campos que son claves foraneas a cada una de las claves de ambas tablas.", "F"),
    ("Un DDL (data definition language) provee un lenguaje para indicar los atributos de una tabla entre otras cosas.", "V"),
    ("Una dependencia funcional no trivial es aquella que tiene del lado izquierdo una clave foranea.", "F"),
    ("Un DML (Data Manipulation Language) no es estrictamente un lenguaje de computacion sino una forma de modelar el dominio del problema.", "F"),
    ("Una dependencia funcional trivial es aquella que tiene del lado izquierdo una clave foranea.", "F"),
    ("Una dependencia funcional trivial es aquella que tiene del lado izquierdo una clave candidata.", "F"),
    ("Los gestores de bases de Datos Relacionales deben proveer un DDL (Data Definition Language) para generar el diccionario de datos.", "V"),
    ("La siguiente expresión que se usa en la definición de una dependencia funcional: Si t1[X] = t2[X]  no puede haber t1[Y] ≠ t2[Y] En las tuplas donde se repitan los valores de X obligatoriamente se deben repetir los valores de Y para que exista Dependencia Funcional", "V"),
    ("una transaccion se define en base al análisis del dominio del problema ","V"),
    ("una transaccion se define al momento de la operación y las implementa la aplicación cliente.","V"),
    ("una transaccion se define como un conjunto de operaciones que no pueden fallar","F"),
    ("una transaccion se define como un conjunto de operaciones que obligatoriamente deben ser recuperadas por el SGBD.","F"),
    ("una trnsaccion es parte del diseño de la base de datos.","F"),
     ("La implicación de las dependencias funcionales es la capacidad que tienen las DFs de poder deducir un nuevo conjunto de DFs a partir de un conjunto dado","V"),
     ("La implicación de las dependencias funcionales se utiliza para la determinación de las claves de un esquema de relación ","V"),
     ("La implicación de las dependencias funcionales se puede determinar usando los axiomas de inferencia.","V"),
     (" la implicacion de las dependencias funcionales  permiten identificar un esquema indeseable","V"),
     ("la implicacion de las dependencias funcionales requiere que F (implicante) tenga mas de una DF","F"),
     ("Una clave no puede contener todos los atributos de una relación.","F"),
     ("Si un conjunto de atributos determina a toda la relación entonces ese conjunto es clave. ","F"),
     ("El conjunto de todos los atributos siempre es clave.","F"),
     ("Las claves candidatas son aquellas que no cumplen con la condición de minimalidad","F"),
     


]
preguntas_respuestas_parcial2 = [
   ("Un índice hash bitmap la pseudoclave es un número binario.", "V"),
("Los predicados de junta pueden tener un operador que no sea de igualdad.", "V"),
("En una ejecución optimizada los predicados locales se ejecutan primero.", "V"),
("El uso del Left Join siempre produce filas con campos con valor null.", "F"),
("Las transacciones sólo pueden actuar sobre una tabla.", "F"),
("Los predicados locales solo pueden ser comparaciones de igualdad.", "F"),
("No hay conflicto cuando una transacción quiere tomar un cierre de escritura y otra tiene un cierre de lectura sobre el mismo ítem.", "F"),
("Hay un conflicto cuando una transacción quiere tomar un cierre de lectura y otra ya tiene un cierre de escritura sobre el mismo ítem.", "V"),
("Hay conflicto cuando una transacción quiere tomar un cierre de escritura y otra ya tiene un cierre de lectura sobre el mismo ítem.", "V"),
("A los usuarios de una base de datos se les debe otorgar los mínimos privilegios necesarios.", "V"),
("En Group By no se pueden poner llamadas a funciones, solo atributos.", "F"),
("Los índices tipo HASH son óptimos en consultas del tipo 'WHERE atributo ='.", "V"),
("En Group By solo se pueden recuperar columnas que estén en la lista, sean dependientes de ella o funciones de agregación.", "V"),
("Un predicado local filtra las tuplas de solo una tabla en la consulta.", "V"),
("El operador de un JOIN siempre debe vincular tablas por una FK.", "F"),
("Un índice hash bitmap aumenta la profundidad del directorio cuando se completa cualquier frame.", "F"),
("Un índice hash bitmap aumenta la profundidad del directorio cuando se completa un frame de profundidad d' igual a d.", "F"),
("Los predicados de junta solo pueden tener un operador de igualdad.", "F"),
("Los BTree son óptimos en consultas del tipo 'WHERE monto >'.", "V"),
("El SQL injection se mitiga usando consultas parametrizadas desde las aplicaciones cliente.", "V"),
("Un predicado local filtra las tuplas resultantes de un join.", "F"),
("Los predicados de junta se ejecutan antes que los predicados locales en una consulta optimizada.", "F"),
("En un índice hash bitmap la función hash genera un número binario a partir de la clave.", "V"),
("Un índice hash bitmap utiliza buckets cuando se completa cualquier frame.", "F"),
("Los predicados de junta filtran tuplas del producto cartesiano de dos tablas.", "V"),
("El operador de un join puede ser cualquier expresión lógica válida.", "V"),
("Las transacciones son lógicamente atómicas.", "V"),
("Una ejecución de dos o más transacciones concurrentes se denomina 'serializable' si se ejecutan una tras otra y no entrelazadas.", "F"),
("Hay conflicto cuando una transacción pide un bloqueo y otra ya lo tiene, y uno es de escritura.", "V"),
("En seguridad se deben dar a los usuarios los mínimos atributos necesarios para realizar sus tareas.", "V"),
("En una consulta con Group By no deben seleccionarse atributos que no estén en el Group By ni sean dependientes de estos.", "V"),
("La optimización de una consulta ejecuta primero los predicados de junta y luego los predicados locales.", "F"),
("Un índice denso exige que los registros de la tabla estén ordenados.", "F"),
("Un índice árbol B+ siempre está equilibrado.", "V"),
("La elección de usar un índice depende solo de las claves, no del estado de los datos.", "F"),
("La concurrencia se produce cuando dos usuarios acceden simultáneamente a la base de datos.", "F"),
("Los locks se utilizan para lograr la serialización de la ejecución de transacciones concurrentes.", "V"),
("Una transacción puede quedar grabada a medias si se respetan las claves foráneas.", "F"),
("Toda transacción puede ser serializada.", "F"),
("El recovery manager asegura que todas las transacciones quedan grabadas y completamente ejecutadas.", "F"),
("Una transacción puede encapsular una sola operación.", "V"),
("Toda operación sobre la base de datos es parte de una transacción.", "V"),
("El recovery manager vuelve la base al estado del último check point.", "F"),
("La cláusula Having del Select es un filtro aplicado tras procesar From, Where y Group By si existen.", "V"),
("Para usar la cláusula Having se requiere que haya un Group By.", "F"),
("El uso del Left Outer Join siempre produce filas con campos con valor null.", "F"),
("Un Select no siempre devuelve una tabla, puede devolver un escalar.", "F"),
("Una Subconsulta interna puede hacer referencia a tablas de la consulta externa.", "V"),
("Hay tipos de índices que funcionan mejor que otros según el estado de los datos.", "F"),
("El manejo de la concurrencia no debe permitir que una transacción acceda a los datos hasta que otras transacciones los liberen.", "V"),
("Un conflicto se produce siempre que una transacción quiere acceder a un dato y otra ya tiene un lock tomado.", "F"),
("La recuperación necesita sólo de los datos del log de transacciones para reconstruir la base.", "V"),
("El optimizador de consultas elige el plan de mínimo costo basado en estimaciones.", "V"),
("Solo se pueden usar Subconsultas en el Where cuando no están afectadas por un join.", "F"),
("Las restricciones de clave foránea son parte de la estructura de la base de datos.", "V"),
("Una SGBD debe garantizar la calidad de los datos.", "F"),
("Las reglas de negocio no se pueden modelar usando Store Procedures.", "F"),
("Usar Store Procedure ayuda a mejorar la seguridad de la base de datos.", "V"),
("Todas las operaciones de una transacción deben actuar sobre una misma tabla.", "F"),
("La ejecución correcta de transacciones concurrentes exige que se ejecuten en serie.", "F"),
("Un índice B+ garantiza una cantidad fija de accesos para encontrar una clave.", "V"),
("Un índice no denso exige que las claves en el archivo destino estén ordenadas.", "V"),
("costo(A |X| B) = costo(B |X| A).", "F"),
("Una ejecución concurrente es serializable si produce el mismo resultado que una ejecución en serie.", "V"),
("Un índice hash-bitmap usa buckets como listas enlazadas al completar una página.", "V"),
("El uso de índices no genera costos adicionales, solo mejora el rendimiento.", "F"),
("Una transacción es un conjunto de operaciones que deben actuar sobre un solo ítem.", "F"),
("Explique (con sus palabras) cómo funciona el mecanismo de cierre de dos fases y por qué.", None),
("El dominio de un atributo de una relación puede ser un conjunto finito.", "V"),
("Es posible usar un índice no denso que indexe un índice denso que indexe un archivo tipo montículo.", "V"),
("El SQL-Injection afecta consultas dinámicas con datos ingresados por el usuario.", "V"),
("Las transacciones se usan para mantener la integridad de datos según el dominio del problema.", "V"),
("Cualquier predicado válido en HAVING también es válido en WHERE.", "F"),
("ROLLBACK deshace una transacción que no recibió COMMIT.", "V"),
("Una transacción con COMMIT puede ser deshecha con ROLLBACK.", "F"),
("La profundidad de un índice Bitmap establece cuántas claves puede contener sin regenerarse.", "V"),
("GROUP BY es obligatorio para cualquier consulta con funciones de agregación en SELECT.", "F"),
("No se puede crear un índice con más de un atributo.", "F"),
("En un índice HASH las claves no deben repetirse.", "V"),
("La optimización de consultas busca los planes menos costosos.", "V"),
("El cliente de base de datos define el comienzo y fin de una transacción.", "F"),
("No puede existir una transacción que encapsule una sola transacción.", "V"),
("La concurrencia no permite que una transacción acceda a datos bloqueados por otra.", "V"),
("La concurrencia ocurre cuando dos transacciones acceden simultáneamente a la base de datos.", "F"),
("El cierre en dos fases garantiza la serialización de transacciones concurrentes.", "V"),
("Un archivo Heap está ordenado.", "F"),
("El optimizador ejecuta primero los predicados de junta y luego los locales.", "F"),
("En B+ los nodos pueden tener cualquier cantidad de posiciones ocupadas.", "F"),
("Un índice B+ usa hashing para almacenar claves.", "F"),
("Todas las hojas en un árbol B+ tienen la misma profundidad.", "V"),
("El bloqueo en dos fases garantiza serialización de transacciones concurrentes.", "V"),
("Índices bitmap extensibles usan función hash para direccionar páginas.", "F"),
("Un índice agrupado mantiene direcciones de páginas con registros clave.", "V"),
("Si una transacción sin COMMIT falla, se reconstruye desde el check point.", "V"),
("Predicados de junta filtran tuplas del producto cartesiano entre tablas.", "V"),
("Predicados de junta generan una relación con atributos y tuplas válidas de ambas tablas.", "V"),
("Left Outer Join siempre genera tantas filas como la tabla izquierda.", "F"),
("Los predicados de junta también se llaman predicados locales.", "F"),
("Es posible un SELECT sin cláusula FROM.", "V"),
("Conflicto si dos transacciones quieren escritura sobre el mismo ítem.", "V"),
("Toda condición válida en WHERE lo es también en HAVING.", "F"),
("¿En qué formato almacena MongoDB las colecciones?", None),
("En una ejecución optimizada los predicados locales se ejecutan al final.", "F"),
("En MySQL al definir una tabla se puede elegir entre varias colaciones.", "V"),
("La cláusula HAVING solo se puede aplicar si existe la cláusula GROUP BY.", "F"),
("En GROUP BY se pueden usar funciones y atributos simples.", "V"),
("Un índice tiene costo solo al crearlo y no al operar sobre la base de datos.", "F"),
("No se pueden usar schemas en MongoDB.", "F"),
("Los predicados locales solo pueden ser comparaciones de igualdad.", "F"),
("Left Join siempre genera misma cantidad de registros que la tabla izquierda.", "F"),
("Si dos transacciones acceden al mismo ítem al mismo tiempo, son concurrentes.", "V"),
("MongoDB admite transacciones ACID.", "V"),
("Crear muchos índices mejora el rendimiento sin costo.", "F"),
("Una ejecución entrelazada es serializable si da el mismo resultado que la no entrelazada.", "V"),
("¿Qué SGBD recomendarías para una startup con cambios frecuentes?", None),
("El SQL injection ocurre al concatenar datos externos en consultas.", "V"),
("DDL permite hacer consultas sobre la base de datos.", "F"),
("Las claves candidatas cumplen las mismas condiciones que la clave principal.", "V"),
("Una interrelación muchos a muchos genera un tercer esquema con FKs hacia las entidades.", "V"),
("DML permite formular consultas sobre los datos.", "V"),
("Una clave candidata no necesita cumplir la condición de minimalidad.", "F"),
("Una interrelación uno a muchos genera un tercer esquema con FKs a ambas entidades.", "F"),
("El método de dos fases puede producir deadlocks.", "V"),
("Las formas normales se verifican por cada relación de forma independiente.", "V"),
("La FN de Boyce-Codd detecta todas las anomalías de actualización.", "F"),
("Las formas normales son obligatorias para un diseño correcto de BD.", "F"),
("Para estar en 3FN, no debe haber DFs no triviales sin clave candidata a la izquierda.", "F"),
("Un índice no denso puede indexar a uno denso que indexa un archivo tipo montículo.", "V"),
("El dominio de un atributo siempre es finito.", "F"),
("Una DF no trivial es la que tiene como lado izquierdo una clave candidata.", "F"),
("Un esquema de relación es el conjunto de atributos de la relación.", "V"),
("Para que un esquema esté en FNBC, ninguna DF debe depender de parte de una clave.", "V"),
("Una interrelación uno a muchos genera una FK en el lado uno hacia el lado muchos.", "F")
]


random.shuffle(preguntas_respuestas)  # 👈 Esto las mezcla al azar

respuestas_usuario = [None] * len(preguntas_respuestas)
respondidas = [False] * len(preguntas_respuestas)

indice_actual = 0
respuestas_usuario = [None] * len(preguntas_respuestas)
respondidas = [False] * len(preguntas_respuestas)
mostrar_feedback = False
color_feedback = WHITE
mensaje_feedback = ""
feedback_time = 0

teoria_surface = mostrar_teoria()

def draw_result_button(text, x, y, w, h, color_fill, border=True):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, color_fill, rect, border_radius=8)


def mostrar_resultado_final():
    screen.fill(DARK_BG)
    correctas = sum(1 for i, (p, r) in enumerate(preguntas_respuestas) if respuestas_usuario[i] == r)
    incorrectas = len(preguntas_respuestas) - correctas
    porcentaje = int((correctas / len(preguntas_respuestas)) * 100) if preguntas_respuestas else 0
    titulo = font_title.render("✓ Resultado", True, PRIMARY)
    screen.blit(titulo, (WIDTH//2 - titulo.get_width()//2, 150))
    screen.blit(font_subtitle.render(f"Correctas: {correctas}", True, SUCCESS), (80, 230))
    screen.blit(font_subtitle.render(f"Incorrectas: {incorrectas}", True, DANGER), (80, 280))
    screen.blit(font_subtitle.render(f"Porcentaje: {porcentaje}%", True, PRIMARY), (80, 330))
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


def draw_result_button(text, x, y, w, h, color_fill, border=True):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, color_fill, rect, border_radius=10)
    if border:
        pygame.draw.rect(screen, WHITE, rect, 3, border_radius=10)
    txt = font_button.render(text, True, WHITE)
    screen.blit(txt, (x + (w - txt.get_width()) // 2, y + (h - txt.get_height()) // 2))
    return rect

def render_wrapped_text(text, x, y, max_width, line_spacing=5):
    lines = textwrap.wrap(text, width=60)
    for i, line in enumerate(lines):
        rendered_line = font.render(line, True, TEXT_COLOR)
        screen.blit(rendered_line, (x, y + i * (rendered_line.get_height() + line_spacing)))
# BUCLE PRINCIPAL
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if estado == "menu":
            screen.fill(DARK_BG)
            titulo = font_title.render("📘 Quiz BD", True, PRIMARY)
            screen.blit(titulo, (WIDTH//2 - titulo.get_width()//2, 60))
            btn_p1 = draw_button("Parcial 1", WIDTH//2 - 100, 150, 200, 50, PRIMARY)
            btn_p2 = draw_button("Parcial 2", WIDTH//2 - 100, 210, 200, 50, PRIMARY)
            btn_ambos = draw_button("Ambos", WIDTH//2 - 100, 270, 200, 50, PRIMARY)
            btn_teoria = draw_button("Teoría", WIDTH//2 - 100, 330, 200, 50, ACCENT)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_p1.collidepoint(event.pos):
                    preguntas_respuestas = preguntas_respuestas.copy()  # Parcial 1
                    random.shuffle(preguntas_respuestas)
                    respuestas_usuario = [None] * len(preguntas_respuestas)
                    respondidas = [False] * len(preguntas_respuestas)
                    indice_actual = 0
                    mostrar_feedback = False
                    estado = "quiz"
                elif btn_p2.collidepoint(event.pos):
                    preguntas_respuestas = preguntas_respuestas_parcial2.copy()  # Parcial 2
                    random.shuffle(preguntas_respuestas)
                    respuestas_usuario = [None] * len(preguntas_respuestas)
                    respondidas = [False] * len(preguntas_respuestas)
                    indice_actual = 0
                    mostrar_feedback = False
                    estado = "quiz"
                elif btn_ambos.collidepoint(event.pos):
                    preguntas_respuestas = preguntas_respuestas.copy() + preguntas_respuestas_parcial2.copy()
                    random.shuffle(preguntas_respuestas)
                    respuestas_usuario = [None] * len(preguntas_respuestas)
                    respondidas = [False] * len(preguntas_respuestas)
                    indice_actual = 0
                    mostrar_feedback = False
                    estado = "quiz"
                elif btn_teoria.collidepoint(event.pos):
                    estado = "teoria"

        elif estado == "teoria":
            screen.fill(DARK_BG)
            altura_visible = HEIGHT - 100
            alto_total = teoria_surface.get_height()
            scroll_offset = max(0, min(scroll_offset, alto_total - altura_visible))
            ancho_visible = teoria_surface.get_width()
            visible_area = pygame.Rect(0, scroll_offset, ancho_visible, altura_visible)
            fragmento_visible = teoria_surface.subsurface(visible_area).copy()
            screen.blit(fragmento_visible, (20, 20))
            btn_volver = draw_button("Menú", 20, HEIGHT - 60, 100, 40, ACCENT)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_volver.collidepoint(event.pos):
                    estado = "menu"
                    scroll_offset = 0
            elif event.type == pygame.MOUSEWHEEL:
                scroll_offset -= event.y * 20
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    scroll_offset += 20
                elif event.key == pygame.K_UP:
                    scroll_offset -= 20
                elif event.key == pygame.K_ESCAPE:
                    estado = "menu"
                    scroll_offset = 0

            scroll_offset = max(0, min(scroll_offset, teoria_surface.get_height() - HEIGHT + 40))

        elif estado == "quiz":
            screen.fill(DARK_BG)
            total = len(preguntas_respuestas)
            aciertos = sum(1 for i, (p, r) in enumerate(preguntas_respuestas) if respuestas_usuario[i] == r)
            progreso_txt = f"{indice_actual + 1}/{total} | {aciertos} ✓"
            progreso_render = font_subtitle.render(progreso_txt, True, PRIMARY)
            screen.blit(progreso_render, (WIDTH//2 - progreso_render.get_width()//2, 10))
            pregunta, correcta = preguntas_respuestas[indice_actual]
            render_wrapped_text(f"P{indice_actual + 1}: {pregunta}", 20, 40, WIDTH - 40)

            if respuestas_usuario[indice_actual]:
                respuesta_txt = f"Tu respuesta: {respuestas_usuario[indice_actual]}"
                screen.blit(font.render(respuesta_txt, True, TEXT_COLOR), (20, 200))

            btn_ant = draw_button("← Anterior", 20, 680, 100, 35, ACCENT)
            btn_menu = draw_button("Menú", 130, 680, 90, 35, DANGER)
            btn_sig = draw_button("Siguiente →", 230, 680, 100, 35, ACCENT)
            btn_salir = draw_button("Salir", 340, 680, 80, 35, WARNING)

            if not respondidas[indice_actual] and not mostrar_feedback:
                btn_v = draw_button("Verdadero", WIDTH//2 - 110, 280, 100, 50, PRIMARY)
                btn_f = draw_button("Falso", WIDTH//2 + 10, 280, 100, 50, PRIMARY)
            elif respondidas[indice_actual]:
                elegida = respuestas_usuario[indice_actual]
                color_v = PRIMARY if elegida == "V" else LIGHT_GRAY
                color_f = PRIMARY if elegida == "F" else LIGHT_GRAY
                borde_v = (correcta == "V")
                borde_f = (correcta == "F")
                draw_result_button("Verdadero", WIDTH//2 - 110, 280, 100, 50, color_v, border=borde_v)
                draw_result_button("Falso", WIDTH//2 + 10, 280, 100, 50, color_f, border=borde_f)

            if mostrar_feedback:
                pygame.draw.rect(screen, color_feedback, pygame.Rect(250, 350, 400, 40), border_radius=6)
                screen.blit(font.render(mensaje_feedback, True, WHITE), (260, 355))
                if pygame.time.get_ticks() - feedback_time > 1000:
                    mostrar_feedback = False
                    if indice_actual < len(preguntas_respuestas) - 1:
                        indice_actual += 1
                    else:
                        mostrar_resultado_final()

            if event.type == pygame.MOUSEBUTTONDOWN and not mostrar_feedback:
                if not respondidas[indice_actual]:
                    if btn_v.collidepoint(event.pos):
                        respuestas_usuario[indice_actual] = "V"
                        respondidas[indice_actual] = True
                        mostrar_feedback = True
                        feedback_time = pygame.time.get_ticks()
                        mensaje_feedback = "✅ ¡Correcto!" if correcta == "V" else f"❌ Incorrecto. Era '{correcta}'"
                        color_feedback = SUCCESS if correcta == "V" else DANGER
                    elif btn_f.collidepoint(event.pos):
                        respuestas_usuario[indice_actual] = "F"
                        respondidas[indice_actual] = True
                        mostrar_feedback = True
                        feedback_time = pygame.time.get_ticks()
                        mensaje_feedback = "✅ ¡Correcto!" if correcta == "F" else f"❌ Incorrecto. Era '{correcta}'"
                        color_feedback = SUCCESS if correcta == "F" else DANGER

                if btn_ant.collidepoint(event.pos) and indice_actual > 0:
                    indice_actual -= 1
                    mostrar_feedback = False
                if btn_menu.collidepoint(event.pos):
                    estado = "menu"
                    indice_actual = 0
                    mostrar_feedback = False
                if btn_sig.collidepoint(event.pos):
                    if indice_actual < len(preguntas_respuestas) - 1:
                        indice_actual += 1
                        mostrar_feedback = False
                    elif all(respondidas):
                        mostrar_resultado_final()
                if btn_salir.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

    pygame.display.flip()
    clock.tick(60)