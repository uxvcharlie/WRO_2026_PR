"""
AdaptadorMecanico.py

Utilidades de conversion mecanica entre el robot de referencia
(Hexagon Force / WRO_2026_Robotica) y ESTE robot.

IMPORTANTE
----------
Este modulo NO se importa en ninguna parte del proyecto y NINGUNA de sus
funciones se usa dentro de ejecutar_matriz_1/2/3/5. Existe solo como
herramienta de calculo para futuras adaptaciones de recorrido.

Los grados de ejecutar_matriz_4() NO fueron convertidos con estas funciones:
esos valores estan validados en pista y se dejaron intactos.
"""

# ============================================================
# CONSTANTES FISICAS
# ============================================================

# Relaciones de transmision declaradas
RELACION_ELEVADOR_REFERENCIA = 2.25
RELACION_ELEVADOR_PROPIO = 5.0

RELACION_GARRA_DELANTERA_REFERENCIA = 1.5
RELACION_GARRA_DELANTERA_PROPIO = 1.5

# Medidas del chasis (espejo de config.py, duplicadas a proposito para que
# este modulo sea autonomo y no arrastre dependencias al Hub)
DIAMETRO_RUEDA_MM = 56
SEPARACION_RUEDAS_MM = 160


# ============================================================
# ELEVADOR
# ============================================================

def convertir_grados_elevador(grados_referencia):
    """
    Convierte grados de elevador del robot de referencia a grados de ESTE robot.

    Que hace
        Aplica dos correcciones a la vez:
          1) Factor de relacion 5 / 2.25 = 2.2222
          2) Inversion de signo, porque los criterios estan al reves:
                referencia -> positivo = BAJAR
                este robot -> positivo = SUBIR

        grados_propios = -grados_referencia * (5 / 2.25)

    Por que se creo
        Todos los recorridos del repo de referencia expresan el elevador en
        grados de un mecanismo con relacion 2.25. Reutilizarlos tal cual
        provoca un recorrido 2.22 veces mas corto y en el sentido contrario.

    Donde podria usarse despues
        Al portar cualquier recorrido nuevo del repo de referencia, para
        obtener un valor de arranque antes de calibrarlo en pista.

    Ejemplos de referencia (bajar al piso):
        276 -> -613 | 285 -> -633 | 290 -> -644 | 291 -> -647

    ADVERTENCIA: el resultado NO esta validado fisicamente. En este repo el
    descenso al piso validado es -510 (matriz 4) y -690 (_armar_verde_amarillo).
    Usar el valor calculado solo como punto de partida.
    """
    factor = RELACION_ELEVADOR_PROPIO / RELACION_ELEVADOR_REFERENCIA
    return -grados_referencia * factor


# ============================================================
# GARRA DELANTERA
# ============================================================

def convertir_grados_garra_delantera(grados_referencia):
    """
    Convierte grados de garra delantera de la referencia a los de este robot.

    Que hace
        Ambas garras tienen relacion 1.5, asi que el factor es 1.0 y la
        funcion devuelve el mismo valor. El criterio de signo tambien coincide
        (negativo = abrir, positivo = cerrar).

    Por que se creo
        Para dejar explicito y documentado que aqui NO hace falta conversion
        de relacion, y evitar que alguien "corrija" estos grados por error.

    Donde podria usarse despues
        Como paso explicito en un futuro portador automatico de recorridos.

    ADVERTENCIA IMPORTANTE
        Que la relacion sea igual NO significa que los grados sean
        intercambiables. La geometria de las pinzas es distinta:
            referencia -> recorridos observados de 12 a 95 grados
            este robot -> recorridos observados de 50 a 800 grados
        Para agarrar, preferir siempre cerrar_al_tope() / abrir_al_tope(),
        que van por corriente y no dependen de la geometria.
    """
    factor = RELACION_GARRA_DELANTERA_PROPIO / RELACION_GARRA_DELANTERA_REFERENCIA
    return grados_referencia * factor


# ============================================================
# PIVOTE SOBRE UNA RUEDA
# ============================================================

def convertir_giro_a_grados_motor(grados_chasis):
    """
    Convierte un giro de chasis sobre una rueda fija a grados de motor.

    Que hace
        En el repo de referencia, giro_izquierda(deg) / giro_derecha(deg)
        reciben grados de CHASIS. En este repo,
        chasis.mover_motor_izquierdo(g) / mover_motor_derecho(g)
        reciben grados de MOTOR.

        Al pivotar sobre una rueda, la rueda movil recorre un arco de radio
        igual a la separacion entre ruedas:

            grados_motor = grados_chasis * (2 * SEPARACION_RUEDAS / DIAMETRO_RUEDA)
                         = grados_chasis * (2 * 160 / 56)
                         = grados_chasis * 5.714

    Por que se creo
        Sin esta conversion, copiar un giro_derecha(90) como
        mover_motor_derecho(90) produce un giro de apenas ~15.7 grados.

    Donde podria usarse despues
        Al portar los pivotes de matriz1.py y de retos_principales.py.

    Verificacion contra valores validados de este repo:
        mover_motor_derecho(780)   -> 136.5 grados de chasis
        mover_motor_derecho(370)   ->  64.7 grados
        mover_motor_izquierdo(400) ->  70.0 grados
        mover_motor_izquierdo(75)  ->  13.1 grados
    """
    factor = (2.0 * SEPARACION_RUEDAS_MM) / DIAMETRO_RUEDA_MM
    return grados_chasis * factor


def convertir_grados_motor_a_giro(grados_motor):
    """
    Inversa de convertir_giro_a_grados_motor().

    Que hace
        Traduce los grados de motor de un pivote ya calibrado en este repo al
        angulo de chasis equivalente.

    Por que se creo
        Para poder leer los pivotes existentes (780, 370, 400, 75...) en
        grados de chasis y compararlos con los del repo de referencia.

    Donde podria usarse despues
        En diagnostico y documentacion de recorridos, o para decidir si un
        pivote conviene reemplazarlo por un giro_preciso_pd equivalente.
    """
    factor = (2.0 * SEPARACION_RUEDAS_MM) / DIAMETRO_RUEDA_MM
    return grados_motor / factor


# ============================================================
# NUMERACION DE MATRICES
# ============================================================

# Correspondencia color -> numero de matriz del repositorio de REFERENCIA.
# Se deja aqui, y NO en config.py, para no tocar la configuracion existente.
# config.MOSAICOS de este repo usa otra correspondencia (Azul=3, Amarillo=4,
# Blanco=5) y se dejo intacta.
COLOR_A_MATRIZ_REFERENCIA = {
    "GREEN": 1,
    "YELLOW": 2,
    "BLUE": 3,
    "WHITE": 4,
}


def matriz_desde_nombre_color(nombre_color):
    """
    Devuelve el numero de matriz segun la numeracion del repo de referencia.

    Que hace
        Traduce el nombre de un color detectado ("GREEN", "YELLOW", "BLUE",
        "WHITE") al numero de matriz 1..4. Devuelve -1 si no reconoce el color.

    Por que se creo
        Las matrices nuevas (1, 2, 3 y 5) estan escritas con la numeracion del
        repo de referencia, que NO coincide con config.MOSAICOS. Esta funcion
        deja disponible esa correspondencia sin modificar config.py.

    Donde podria usarse despues
        En un enrutador de matrices (equivalente a ArmadorMosaicos.armar) que
        decida que ejecutar_matriz_N() llamar a partir del color leido.

    NOTA: la numeracion de referencia no asigna ningun color a la matriz 5,
    asi que ejecutar_matriz_5() no puede seleccionarse por color con este mapa.
    """
    return COLOR_A_MATRIZ_REFERENCIA.get(nombre_color, -1)
