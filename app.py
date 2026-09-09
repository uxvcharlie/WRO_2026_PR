from pybricks.pupdevices import ColorSensor
from pybricks.tools import wait
import config
from robot import Robot
from ArmadorMosaicos import ArmadorMosaicos
from RevisadorBateria import RevisadorBateria
from Misiones import Misiones
import gc 

# 1. Inicialización de Hardware usando el archivo config
mi_robot = Robot(
    port_izq=config.PORT_MOTOR_IZQ,
    port_der=config.PORT_MOTOR_DER,
    port_elevador_delantero=config.PORT_ELEVADOR_DELANTERO,
    port_garra_delantera=config.PORT_GARRA_DELANTERA,
    port_garra_trasera=config.PORT_GARRA_TRASERA
)

# Inicialización de Sensores
sensor = ColorSensor(config.PORT_SENSOR_FRENTE)

# 2. Controladores de alto nivel
misiones = Misiones(mi_robot, sensor)
armador = ArmadorMosaicos(mi_robot, sensor)
revisador_bateria = RevisadorBateria(mi_robot)

# 3. Flujo Principal
if __name__ == "__main__":
    if not revisador_bateria.revisar_bateria():
        print("Ejecución cancelada por batería baja.")
    else:
        #, # ZONA DE PRUEBAS: Descomenta la misión que quieras ejecutar
        # misiones.prueba_precision()

        # # misiones.pruebasIndividuales()

        misiones.pruebasuwu()

        # misiones.cemento_llana_nuevo()
        # misiones.agarrar_verdes_nuevo()
        # misiones.escanear_dejar_verde_nuevo()
        # misiones.agarrar_amarillos_nuevo()
        # misiones.agarrar_azules_nuevo()
        # misiones.agarrar_pala_nuevo()
        # misiones.dejar_amarillos_nuevo()

        # # 1. Primera Misión
        # misiones.cemento_y_llana()
        # gc.collect() # Limpiamos la RAM de las variables temporales de la misión anterior

        # # 2. Segunda Misión
        # misiones.agarrar_bloques_blancos()
        # gc.collect()

        # # 3. Tercera Misión
        # misiones.dejar_bloques_blancos()
        # gc.collect()

        # # 4. Cuarta Mision
        # misiones.agarrar_bloques_verdes()
        # gc.collect()

        # numero_mosaico = misiones.dejar_bloques_verdes_y_detectar_mosaico()
        # gc.collect()

        # # 6. Sexta Misión
        # misiones.agarrar_bloques_amarillos()
        # gc.collect()

        # # 7. Séptima Misión
        # misiones.dejar_bloques_amarillos()
        # gc.collect()

        # # 8. Octava Misión (Ataque a la pala)
        # misiones.agarrar_bloques_azules_y_pala()
        # gc.collect()

        # # 9. Novena misión 
        # armador.armar(numero_mosaico)




        """ Recorrido 'nuevo' de hacerlo sin agarrar los cementos blancos."""

        """Matrices"""

        # misiones.ejecutar_matriz_1()

        # misiones.ejecutar_matriz_2()

        # misiones.ejecutar_matriz_3()

        # misiones.ejecutar_matriz_4()

        # misiones.ejecutar_matriz_5()

        # misiones.pruebasuwu()


        # misiones.video()


