from pybricks.parameters import Stop, Color
from pybricks.pupdevices import ColorSensor
from pybricks.tools import wait
import config
from robot import Robot

class Misiones:
    def __init__(self, robot: Robot, sensor: ColorSensor):
        self.robot = robot
        self.sensor = sensor

    def _identificar_combinacion(self, sensor: ColorSensor, distancia_si_verde):
        color_principal = sensor.color()
        if color_principal not in config.MOSAICOS:
            return -1
        decision = config.MOSAICOS[color_principal]
        if type(decision) is dict:
            self.robot.chasis.avanzar_recto(distancia_si_verde)
            color_anterior = sensor.color()
            if color_anterior not in decision: return -1
            return decision[color_anterior]
        return decision


    def pruebasuwu(self):
    
        self.robot.chasis.avanzar_recto(20)
        self.robot.navegacion.giro_preciso_pd(-45)
        self.robot.chasis.avanzar_recto(45)
        self.robot.chasis.mover_motor_izquierdo(350)
        self.robot.chasis.mover_motor_derecho(500)




    def cemento_llana_nuevo(self):
        
        # 1. ARRANQUE FLUIDO
        self.robot.chasis.mover_en_arco(radio_cm=14, distancia_cm=20.5, stop=Stop.NONE, margen_cm=3, velocidad=config.STRAIGHT_SPEED)

        # 2. SEGUIDOR BLINDADO
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=89, lado="derecha", tiempo_acomodo_ms=0)
        self.robot.navegacion.giro_preciso_pd(-90)

        # ¡ACCIÓN SIMULTÁNEA! Garra a máxima velocidad (1500) mientras retrocede
        self.robot.mecanismos.garra_trasera.mover(grados=170, velocidad=250, wait_after=False, frenado=Stop.HOLD)
        self.robot.chasis.avanzar_recto(-7, velocidad=1000, frenado=Stop.BRAKE, margen_cm=0)

        self.robot.navegacion.giro_preciso_pd(80)
        self.robot.chasis.avanzar_recto(-26, velocidad=1300, frenado=Stop.NONE, margen_cm=4)
        self.robot.chasis.mover_en_arco(-230, distancia_cm=34, stop=Stop.NONE, margen_cm=1, velocidad=930)

        # ¡ACCIÓN SIMULTÁNEA! Mueve chasis asíncrono y entra al seguidor
        self.robot.chasis.mover_motor_izquierdo(165, wait_after=False)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=46, lado="derecha", tiempo_acomodo_ms=0)
        
        self.robot.navegacion.giro_preciso_pd(-90)

    def agarrar_verdes_nuevo(self):
        self.robot.mecanismos.garra_trasera.avanzar_y_gatillar(chasis=self.robot.chasis, distancia_total_cm=43, vel_chasis=1000, distancia_trigger_cm=15, grados_garra=-168, vel_garra=1500)
        self.robot.navegacion.giro_preciso_pd(90)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=27)
        self.robot.navegacion.giro_preciso_pd(180)
        # 5. RECOLECCIÓN LETAL SIMULTÁNEA (Embestimos a velocidad 1000, no a 150)
        self.robot.mecanismos.garra_trasera.mover(172, velocidad=240, wait_after=False, frenado= Stop.HOLD)
        self.robot.chasis.avanzar_recto(-15, velocidad=1000, frenado=Stop.HOLD)
        self.robot.navegacion.seguidor_linea_color(self.sensor, 100,Color.GREEN, lado="izquierda",tiempo_acomodo_ms=0, distancia_cm=90)

    def escanear_dejar_verde_nuevo(self):
        self.robot.chasis.mover_motor_izquierdo(75)
        self.robot.chasis.avanzar_recto(16)

        mosaico = self._identificar_combinacion(self.sensor, 5)
        print(f"Mosaico detectado: {mosaico}" if mosaico != -1 else "Error en escaneo")
        
        if (mosaico == 1 or mosaico == 2):
            self.robot.chasis.avanzar_recto(-5, velocidad=1000)
            
        self.robot.chasis.avanzar_recto(-36, velocidad=1000)
        self.robot.navegacion.giro_preciso_pd(-180)
        
        # ACCIÓN SIMULTÁNEA 
        self.robot.chasis.avanzar_recto(-20, velocidad=500)

        return mosaico 


    "Recorrido nuevo para no dejar los bloques blancos"


    def agarrar_amarillos_nuevo(self):
        self.robot.mecanismos.elevador_delantero.subir_al_tope(wait_after=False)
        self.robot.mecanismos.garra_delantera.abrir_al_tope(wait_after=False)
        self.robot.mecanismos.garra_trasera.mover(-170, velocidad=820, wait_after=False)
        self.robot.navegacion.seguidor_linea_color(self.sensor,100 ,Color.GREEN, tiempo_acomodo_ms=0, distancia_cm=80)
        self.robot.chasis.mover_motor_derecho(75)
        self.robot.chasis.avanzar_recto(10)
        self.robot.navegacion.giro_preciso_pd(-90)
        self.robot.chasis.avanzar_recto(25)
        self.robot.navegacion.giro_preciso_pd(-90)

    def agarrar_azules_nuevo(self):
        self.robot.chasis.avanzar_recto(17)
        self.robot.navegacion.giro_preciso_pd(-90)
        self.robot.chasis.avanzar_recto(49)
        self.robot.navegacion.giro_preciso_pd(90)
        self.robot.mecanismos.garra_trasera.mover(172, velocidad=240, wait_after=False, frenado= Stop.HOLD)
        self.robot.chasis.avanzar_recto(-17, velocidad=1000, frenado=Stop.HOLD, wait_after=False)
        self.robot.mecanismos.garra_delantera.cerrar(grados=550)


    
    def agarrar_pala_nuevo(self):
        self.robot.chasis.avanzar_recto(10)
        self.robot.navegacion.giro_preciso_pd(-30)
        self.robot.mecanismos.elevador_delantero.mover(grados=-530,wait_after=False)
        self.robot.chasis.avanzar_recto(50)
        self.robot.mecanismos.garra_delantera.cerrar_al_tope()
        self.robot.mecanismos.elevador_delantero.mover(50, wait_after=False)
        self.robot.chasis.avanzar_recto(-9)
        self.robot.chasis.mover_motor_izquierdo(250)

    def dejar_amarillos_nuevo(self):
        self.robot.chasis.avanzar_recto(45)
        self.robot.mecanismos.elevador_delantero.subir_al_tope(wait_after=False)
        self.robot.mecanismos.garra_delantera.abrir(150)
        self.robot.navegacion.giro_preciso_pd(90)
        self.robot.chasis.avanzar_recto(28)
        self.robot.chasis.avanzar_recto(-25)


        
        



    "Fin del recorrido nuevo"
        
 
    # --- MISIONES DE COMPETENCIA OPTIMIZADAS (MODO ASÍNCRONO) ---
    def cemento_y_llana(self):
        # 1. ARRANQUE FLUIDO
        self.robot.chasis.mover_en_arco(radio_cm=14, distancia_cm=20.5, stop=Stop.NONE, margen_cm=3, velocidad=config.STRAIGHT_SPEED)

        # 2. SEGUIDOR BLINDADO
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=89, lado="derecha", tiempo_acomodo_ms=0)
        self.robot.navegacion.giro_preciso_pd(-90)

        # ¡ACCIÓN SIMULTÁNEA! Garra a máxima velocidad (1500) mientras retrocede
        self.robot.mecanismos.garra_trasera.mover(grados=170, velocidad=250, wait_after=False, frenado=Stop.HOLD)
        self.robot.chasis.avanzar_recto(-7, velocidad=1000, frenado=Stop.BRAKE, margen_cm=0)

        self.robot.navegacion.giro_preciso_pd(80)
        self.robot.chasis.avanzar_recto(-26, velocidad=1300, frenado=Stop.NONE, margen_cm=4)
        self.robot.chasis.mover_en_arco(-230, distancia_cm=34, stop=Stop.NONE, margen_cm=1, velocidad=930)

        # ¡ACCIÓN SIMULTÁNEA! Mueve chasis asíncrono y entra al seguidor
        self.robot.chasis.mover_motor_izquierdo(165, wait_after=False)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=51, lado="derecha", tiempo_acomodo_ms=0)
        
        self.robot.navegacion.giro_preciso_pd(90)
        

    def agarrar_bloques_blancos(self):
        # 1. ARRANQUE ASÍNCRONO EXPLOSIVO
        self.robot.mecanismos.garra_trasera.mover(-170, velocidad=1500, wait_after=False)
        self.robot.chasis.avanzar_recto(-5, frenado=Stop.HOLD)

        # Encadenamiento fluido
        self.robot.chasis.mover_en_arco(-12, distancia_cm=16, stop=Stop.NONE, margen_cm=2, velocidad=930)
        
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=19, lado="izquierda", tiempo_acomodo_ms=0, kp=1.2, kd=3.5)
        
    
        self.robot.navegacion.giro_preciso_pd(180)
        
        # 5. RECOLECCIÓN LETAL SIMULTÁNEA (Embestimos a velocidad 1000, no a 150)
        self.robot.mecanismos.garra_trasera.mover(172, velocidad=240, wait_after=False, frenado= Stop.HOLD)
        self.robot.chasis.avanzar_recto(-20, velocidad=1000, frenado=Stop.HOLD)

    def dejar_bloques_blancos(self):
        self.robot.chasis.motor_derecha.hold() 
        self.robot.chasis.mover_motor_izquierdo(400, velocidad=1000, frenado=Stop.HOLD)
        
        self.robot.chasis.drive_base.settings(straight_speed=930, straight_acceleration=1500, turn_rate=config.TURN_RATE, turn_acceleration=config.STRAIGHT_ACCEL)
        
        self.robot.chasis.avanzar_recto(54, velocidad=930, frenado=Stop.HOLD)
        
        self.robot.chasis.drive_base.settings(straight_speed=config.STRAIGHT_SPEED, straight_acceleration=config.STRAIGHT_ACCEL, turn_rate=config.TURN_RATE, turn_acceleration=config.STRAIGHT_ACCEL)
        
        self.robot.navegacion.giro_preciso_pd(-55)

        self.robot.navegacion.seguidor_linea_color(self.sensor, 100, Color.GREEN, lado="derecha",distancia_cm=60)
        
        self.robot.chasis.mover_motor_derecho(75, velocidad=800, frenado=Stop.HOLD)        
               
        self.robot.navegacion.giro_preciso_pd(235.5, max_speed=700)       
        
        # 7. ENTREGA LETAL SIMULTÁNEA
        self.robot.mecanismos.garra_trasera.mover(-170, velocidad=100, wait_after=False)
        self.robot.chasis.avanzar_recto(-18, velocidad=1000, frenado=Stop.HOLD)

    def agarrar_bloques_verdes(self):
        self.robot.chasis.avanzar_recto(14, velocidad=1000, frenado=Stop.BRAKE)
        self.robot.chasis.motor_izquierda.hold()
        self.robot.chasis.mover_motor_derecho(370, velocidad=1300, margen_grados=30)
        
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=42, lado="izquierda", tiempo_acomodo_ms=0, kp=1.2, kd=3.5)
        self.robot.navegacion.giro_preciso_pd(180)
        
        # ACCIÓN SIMULTÁNEA MIENTRAS ENTRA
        self.robot.mecanismos.garra_trasera.mover(171, velocidad=200, frenado=Stop.COAST, wait_after=False)
        self.robot.chasis.avanzar_recto(-25, velocidad=1000)

    def dejar_bloques_verdes_y_detectar_mosaico(self):
        self.robot.navegacion.seguidor_linea_color(self.sensor, 100, Color.GREEN, lado="derecha", tiempo_acomodo_ms=200, distancia_cm=95)
        self.robot.chasis.mover_motor_derecho(75)
        self.robot.chasis.avanzar_recto(16)

        mosaico = self._identificar_combinacion(self.sensor, 5)
        print(f"Mosaico detectado: {mosaico}" if mosaico != -1 else "Error en escaneo")
        
        if (mosaico == 1 or mosaico == 2):
            self.robot.chasis.avanzar_recto(-5, velocidad=1000)
            
        self.robot.chasis.avanzar_recto(-34, velocidad=1000)
        self.robot.navegacion.giro_preciso_pd(180)
        
        # ACCIÓN SIMULTÁNEA 
        self.robot.chasis.avanzar_recto(-20, velocidad=500)
        return mosaico 

    def agarrar_bloques_amarillos(self):
        self.robot.mecanismos.garra_trasera.mover(-170, velocidad=60, wait_after=False )
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, 100, distancia_cm= 12, lado="izquierda")
        self.robot.navegacion.giro_preciso_pd(-45)
        self.robot.chasis.avanzar_recto(31, velocidad=1000)
        self.robot.navegacion.giro_preciso_pd(45)

        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=18, tiempo_acomodo_ms=0) # Eliminamos el acomodo para no perder tiempo
        self.robot.navegacion.giro_preciso_pd(-180)
        
        # ACCIÓN SIMULTÁNEA
        self.robot.mecanismos.garra_trasera.mover(170, velocidad=240, wait_after=False, frenado=Stop.COAST)
        self.robot.chasis.avanzar_recto(-19, velocidad=1000)

    def dejar_bloques_amarillos(self):
        self.robot.navegacion.giro_preciso_pd(-60)
        self.robot.chasis.avanzar_recto(distancia_cm=76, velocidad=1000)
        self.robot.navegacion.giro_preciso_pd(60)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=65, lado="izquierda")
        self.robot.navegacion.giro_preciso_pd(-90)
        
        # ACCIÓN SIMULTÁNEA
        self.robot.chasis.avanzar_recto(distancia_cm=-17, velocidad=1000)

    def agarrar_bloques_azules_y_pala(self):
        self.robot.mecanismos.garra_trasera.mover(-170, velocidad=200, wait_after=False)

        self.robot.chasis.avanzar_recto(distancia_cm=16.2, velocidad=1000)
        self.robot.navegacion.giro_preciso_pd(-90)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=51)
        self.robot.navegacion.giro_preciso_pd(-35)
        
        # ACCIÓN SIMULTÁNEA 1
        self.robot.mecanismos.garra_trasera.mover(160, velocidad=300, wait_after=False)
        self.robot.chasis.avanzar_recto(distancia_cm=-13, velocidad=1000)
        
        # Gatillazo perfecto al vuelo (le agregamos vel_garra=1500 para que sea violento)
        self.robot.mecanismos.garra_trasera.avanzar_y_gatillar(chasis=self.robot.chasis, distancia_total_cm=35, vel_chasis=1000, distancia_trigger_cm=14, grados_garra=-168, vel_garra=1500)
        
        self.robot.navegacion.giro_preciso_pd(35)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor,  velocidad_max=100, distancia_cm=16, tiempo_acomodo_ms=0)
        self.robot.navegacion.giro_preciso_pd(-180)
        
        # ACCIÓN SIMULTÁNEA 2
        self.robot.mecanismos.garra_trasera.mover(170, velocidad=240, wait_after=False)
        self.robot.chasis.avanzar_recto(-22, velocidad=1000)
        
        self.robot.navegacion.giro_preciso_pd(-30)
        self.robot.chasis.avanzar_recto(distancia_cm=34.5, velocidad=950)
        self.robot.navegacion.giro_preciso_pd(30, margen_grados=10)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=155, lado="izquierda")  
        self.robot.chasis.avanzar_recto(distancia_cm=-21)
        self.robot.navegacion.giro_preciso_pd(90)
        self.robot.mecanismos.garra_trasera.mover(-170)

    def pruebas_matrizAmarilloBlancoVerde(self):
        self.robot.mecanismos.garra_delantera.abrir_al_tope(wait_after=False)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=110, distancia_cm=15, tiempo_acomodo_ms=0)
        self.robot.mecanismos.elevador_delantero.mover(-400, velocidad=1000, wait_after= False)
        self.robot.navegacion.giro_preciso_pd(-90)
        self.robot.chasis.avanzar_recto(15)
        self.robot.mecanismos.garra_delantera.cerrar(800, wait_after=False)
        self.robot.mecanismos.elevador_delantero.mover(200)
        self.robot.chasis.avanzar_recto(-13)
        self.robot.navegacion.giro_preciso_pd(90.5)
        self.robot.chasis.mover_motor_izquierdo(200)
        self.robot.chasis.mover_motor_derecho(200)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=40)
        self.robot.navegacion.giro_preciso_pd(-90)
  
    def ejecutar_matriz_4(self):

        #Acomoda su elevador y garra delantera
        self.robot.mecanismos.elevador_delantero.subir_al_tope(wait_after=False)
        self.robot.mecanismos.garra_delantera.abrir_al_tope(wait_after=False)

        """Intentar hacer el recorrido con la garra abajo para llevar los cementos azules seria un dolor de cabeza, debido a que la friccion generada de esta 
        hace que el funcionamiento del robot sea distinto mayormente en los giros"""
        # self.robot.mecanismos.garra_trasera.bajar_al_tope()

        #Camino a los 4 primeros bloques azules
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=39)
        self.robot.navegacion.giro_preciso_pd(-90)

        #Agarra los 4 azules
        self.robot.mecanismos.elevador_delantero.mover(-510, velocidad=500, wait_after=False)

        self.robot.chasis.avanzar_recto(distancia_cm=24, velocidad=2000)

        #Camino al amarillo

        self.robot.chasis.avanzar_recto(-24)
        self.robot.navegacion.giro_preciso_pd(-90)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=21, lado="izquierda", tiempo_acomodo_ms=0)
        self.robot.mecanismos.garra_delantera.cerrar(490, velocidad=500,wait_after=False)
   
        self.robot.navegacion.giro_preciso_pd(90)

        #Agarra un bloque amarillo
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(velocidad=30, wait_after=False)
        self.robot.chasis.avanzar_recto(10.8)
        self.robot.chasis.avanzar_recto(-10.8)

        #Camino al bloque verdecito jeje
        self.robot.navegacion.giro_preciso_pd(90)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=41, tiempo_acomodo_ms=50)
        self.robot.navegacion.giro_preciso_pd(-90)
        self.robot.mecanismos.garra_delantera.abrir(grados=100, wait_after=False)

        #Agarra el bloque verde alaverga
        self.robot.navegacion.chasis.avanzar_recto(9.5)
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(velocidad=1000)
        self.robot.chasis.avanzar_recto(-5)
        self.robot.navegacion.giro_preciso_pd(-80)
        self.robot.chasis.mover_motor_derecho(grados=800)

        #Sigue la linea hacia el mosaico 
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=14,tiempo_acomodo_ms=0)

        #Abre la garra para dejar los 4 bloques azules
        self.robot.mecanismos.garra_delantera.abrir(300, wait_after=False)


        #Levanta la garra para meter los 6 bloques
        self.robot.mecanismos.elevador_delantero.mover(400, velocidad=900, wait_after=False)
        self.robot.chasis.avanzar_recto(-15)
        self.robot.mecanismos.elevador_delantero.mover(-380)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=90, distancia_cm=25, tiempo_acomodo_ms=0)

        #Aprieta la garra y agarra los 6 bloques
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(limite_potencia=100)
        self.robot.mecanismos.elevador_delantero.mover(300, wait_after=False)
        
        self.robot.chasis.mover_motor_derecho(30)
        self.robot.chasis.mover_motor_izquierdo(30)

        #Se mete a la matriz a dejar los 6 bloques
        self.robot.chasis.avanzar_recto(25, wait_after=False)
        self.robot.mecanismos.elevador_delantero.mover(-260)

        #Tira los bloques a la matriz y acomoda los bloques 
        self.robot.mecanismos.garra_delantera.abrir(160, velocidad=2000)

        #avance y retroceso para acomodar los bloques
        self.robot.chasis.avanzar_recto(2)
        self.robot.chasis.avanzar_recto(-4)

        #acomodos que gira a la izquierda y derecha para terminar de acomodar los 6 bloques 
        self.robot.chasis.acomodar_estable(iteraciones=3,tiempo_ms=60)    
        self.robot.mecanismos.garra_delantera.abrir(50, wait_after=False)

        #termina de acomodar
        self.robot.mecanismos.elevador_delantero.mover(-100)
        self.robot.chasis.acomodar_estable(iteraciones=3 ,tiempo_ms=40)

        #levanta la garra para que no choque con las barreras al rededor de la matriz
        self.robot.mecanismos.elevador_delantero.subir_al_tope(wait_after= False)
        self.robot.mecanismos.garra_delantera.abrir_al_tope(wait_after=False)

        # Camino al resto de los bloques
        self.robot.chasis.avanzar_recto(-12)
        self.robot.navegacion.giro_preciso_pd(-178)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=39, lado="derecha",tiempo_acomodo_ms=0)
        self.robot.navegacion.giro_preciso_pd(-90)
        self.robot.chasis.avanzar_recto(9.5)
        self.robot.navegacion.giro_preciso_pd(90)

        #Se mete a agarrar los dos bloques azules
        self.robot.mecanismos.elevador_delantero.mover(-495, velocidad=300, wait_after=False)
        self.robot.chasis.avanzar_recto(31)
        self.robot.chasis.avanzar_recto(-31)


        #Camino a los 3 bloques amarillos
        self.robot.navegacion.giro_preciso_pd(-90)

        self.robot.chasis.avanzar_recto(16) 
        self.robot.navegacion.giro_preciso_pd(90)
        self.robot.mecanismos.garra_delantera.abrir(110, wait_after=False)
        self.robot.chasis.avanzar_recto(10)

        #Agarra el primer bloque amarillo 
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(velocidad=1000)
        self.robot.mecanismos.elevador_delantero.mover(300)
        self.robot.mecanismos.elevador_delantero.mover(-320, velocidad=500, wait_after=False)
        self.robot.chasis.avanzar_recto(16)
        self.robot.chasis.avanzar_recto(-26)

        #Camino al bloque verde 
        self.robot.navegacion.giro_preciso_pd(90)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=30, tiempo_acomodo_ms=100)


        #Se mete a agarrar el ultimo bloque verde
        self.robot.navegacion.giro_preciso_pd(-90)
        self.robot.mecanismos.garra_delantera.abrir(grados=110, wait_after=False)

        #Agarra el SEGUNDO bloque verde alaverga
        self.robot.navegacion.chasis.avanzar_recto(13.5)
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(velocidad=1000, limite_potencia=100, wait_after=False)
        self.robot.chasis.avanzar_recto(distancia_cm=-9.5)
        self.robot.navegacion.giro_preciso_pd(-120)
        self.robot.chasis.mover_motor_derecho(grados=500)

        #Sigue la linea hacia el mosaico 
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=14, tiempo_acomodo_ms=0)

        #Abre la garra para dejar los 2 amarillos, 3 azules y un verde
        self.robot.mecanismos.garra_delantera.abrir(300, wait_after=False)


        #Levanta la garra para meter los 6 bloques
        self.robot.mecanismos.elevador_delantero.mover(400, velocidad=900, wait_after=False)
        self.robot.chasis.avanzar_recto(-15)
        self.robot.mecanismos.elevador_delantero.mover(-380)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=90, distancia_cm=25, tiempo_acomodo_ms=0)

        #Aprieta la garra y agarra los 6 bloques
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(limite_potencia=100)
        self.robot.mecanismos.elevador_delantero.mover(300)

        self.robot.chasis.mover_motor_derecho(30)
        self.robot.chasis.mover_motor_izquierdo(30)

        #Se mete a la matriz a dejar los 6 bloques
        self.robot.chasis.avanzar_recto(13)
        self.robot.mecanismos.elevador_delantero.mover(-260)

        #Tira los bloques a la matriz y acomoda los bloques 
        self.robot.mecanismos.garra_delantera.abrir(160, velocidad=2000)

        #avance y retroceso para acomodar los bloques
        self.robot.chasis.avanzar_recto(2)  
        self.robot.chasis.avanzar_recto(-4)

        #acomodos que gira a la izquierda y derecha para terminar de acomodar los 6 bloques 
        self.robot.chasis.acomodar_estable(iteraciones=3, potencia=50,tiempo_ms=60)    
        self.robot.mecanismos.garra_delantera.abrir(50, wait_after=False)

        #termina de acomodar
        self.robot.mecanismos.elevador_delantero.mover(-100)
        self.robot.chasis.acomodar_estable(iteraciones=3 ,tiempo_ms=40)


    # =====================================================================
    # MATRICES NUEVAS (1, 2, 3 y 5)
    #
    # Numeracion: la del repositorio de referencia (Hexagon Force).
    #   1 = VERDE, 2 = AMARILLO, 3 = AZUL, 4 = BLANCO
    # Los patrones MATRIZ_1..MATRIZ_5 son los mismos en ambos repositorios
    # (se verifico con la composicion de ejecutar_matriz_4: 6 Az + 4 Am + 2 V).
    #
    # OJO: config.MOSAICOS de este repo usa otra correspondencia color->numero
    # (Azul=3, Amarillo=4, Blanco=5). NO se modifico config.py.
    #
    # Todas arrancan desde la MISMA posicion que ejecutar_matriz_4().
    # Las distancias son las validadas de ESTE repositorio; del repositorio
    # de referencia se tomo unicamente el ORDEN y la SECUENCIA de acciones.
    # =====================================================================

    def ejecutar_matriz_1(self):
        # MATRIZ_1 -> 6 Azul + 6 Verde
        #   [Az, Az, V,  Az]
        #   [V,  V,  V,  V ]
        #   [Az, Az, V,  Az]
        #
        # Recorrido copiado paso a paso de matriz1.py de la referencia.
        # ATENCION: en ese archivo solo los 10 primeros pasos son codigo activo.
        # Todo lo que sigue a la marca SIN VALIDAR estaba comentado alla dentro
        # de un bloque ''' ''' y nunca se ejecuto en pista.

        #Acomoda su elevador y garra delantera
        self.robot.mecanismos.elevador_delantero.subir_al_tope(wait_after=False)

        #ref: mover_garra(-130) -> abrir la garra
        self.robot.mecanismos.garra_delantera.abrir_al_tope(wait_after=False)

        # ---------------- PARTE ACTIVA DE LA REFERENCIA ----------------

        #ref: seguir_linea(30, "derecha")
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=30, lado="derecha")

        #ref: girar(-92)
        self.robot.navegacion.giro_preciso_pd(-92)

        #ref: avanzar(8.75) -> entra a los 2 primeros verdes
        #REQUIERE PRUEBA FISICA: profundidad de entrada
        self.robot.chasis.avanzar_recto(8.75)

        #ref: mover_garra_delantera(286) -> bajar elevador (aqui ya agarro los 2 verdes)
        #Conversion: -286 * 2.2222 = -636. Se usa -510, el descenso validado de este repo.
        #REQUIERE PRUEBA FISICA: altura de descenso
        self.robot.mecanismos.elevador_delantero.mover(-510, velocidad=500)

        #ref: retroceder(8)
        self.robot.chasis.avanzar_recto(-8)

        #ref: girar(-91)
        self.robot.navegacion.giro_preciso_pd(-91)

        #ref: avanzar(17)  -> avance RECTO, no seguidor de linea
        self.robot.chasis.avanzar_recto(17)

        #ref: girar(73.05) -> angulo geometrico real, NO es un 90 con sesgo
        self.robot.navegacion.giro_preciso_pd(73.05)

        #ref: esperar(300)
        wait(300)

        # ---------------- SIN VALIDAR: estaba comentado en la referencia ----------------

        #ref: mover_garra_delantera(-140) -> subir elevador | conversion +140*2.2222 = +311
        self.robot.mecanismos.elevador_delantero.mover(311)
        #ref: avanzar(13.75)
        self.robot.chasis.avanzar_recto(13.75)
        #ref: mover_garra_delantera(140) -> bajar elevador (aqui ya agarro los 2 azules)
        #REQUIERE PRUEBA FISICA
        self.robot.mecanismos.elevador_delantero.mover(-311)

        #ref: retroceder(9) / girar(89) / avanzar(4.5) / girar(-86)
        self.robot.chasis.avanzar_recto(-9)
        self.robot.navegacion.giro_preciso_pd(89)
        self.robot.chasis.avanzar_recto(4.5)
        self.robot.navegacion.giro_preciso_pd(-86)

        #ref: mover_garra(100) / avanzar(16) / mover_garra(50) -> cerrar, entrar, apretar
        #REQUIERE PRUEBA FISICA: agarre de los 2 bloques del centro
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(velocidad=1000, limite_potencia=100)
        self.robot.chasis.avanzar_recto(16)
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(velocidad=1000, limite_potencia=100)

        #ref: retroceder(10) / giro_izquierda(-92) -> pivote sobre la rueda IZQUIERDA
        #Conversion: 92 * 5.714 = 526 grados de motor
        self.robot.chasis.avanzar_recto(-10)
        self.robot.chasis.mover_motor_izquierdo(-526)

        #ref: mover_garra(-130) abrir / mover_garra_delantera(-140) subir
        self.robot.mecanismos.garra_delantera.abrir(300, wait_after=False)
        self.robot.mecanismos.elevador_delantero.mover(311)

        #ref: retroceder(10) / mover_garra_delantera(140) bajar / avanzar(15) / mover_garra(100) cerrar
        self.robot.chasis.avanzar_recto(-10)
        self.robot.mecanismos.elevador_delantero.mover(-311)
        self.robot.chasis.avanzar_recto(15)
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(velocidad=1000, limite_potencia=100)

        #ref: giro_derecha(-90) -> pivote sobre la rueda DERECHA | 90 * 5.714 = 514
        #Queda enfrente de la linea de la matriz
        self.robot.chasis.mover_motor_derecho(-514)

        #ref: seguir_linea(20) / avanzar(10)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=20, lado="derecha")
        self.robot.chasis.avanzar_recto(10)

        #ref: mover_garra_delantera(-140) subir / avanzar(15) / mover_garra_delantera(100) bajar
        #ref: mover_garra(-130) abrir / mover_garra_delantera(-100) subir  -> deja los bloques
        #REQUIERE PRUEBA FISICA: TODA la colocacion en la matriz
        self.robot.mecanismos.elevador_delantero.mover(311)
        self.robot.chasis.avanzar_recto(15)
        self.robot.mecanismos.elevador_delantero.mover(-222)
        self.robot.mecanismos.garra_delantera.abrir(160, velocidad=2000)
        self.robot.mecanismos.elevador_delantero.mover(222)

        #ref: retroceder(40) / girar(90) / avanzar(10) / girar(-90)
        self.robot.chasis.avanzar_recto(-40)
        self.robot.navegacion.giro_preciso_pd(90)
        self.robot.chasis.avanzar_recto(10)
        self.robot.navegacion.giro_preciso_pd(-90)

        #ref: mover_garra_delantera(-140) subir / avanzar(15) / mover_garra_delantera(140) bajar
        #Aqui ya agarro los otros 2 bloques de la matriz
        #REQUIERE PRUEBA FISICA
        self.robot.mecanismos.elevador_delantero.mover(311)
        self.robot.chasis.avanzar_recto(15)
        self.robot.mecanismos.elevador_delantero.mover(-311)

        #ref: retroceder(15) / giro_derecha(90) / avanzar(15) / girar(-90)
        self.robot.chasis.avanzar_recto(-15)
        self.robot.chasis.mover_motor_derecho(514)
        self.robot.chasis.avanzar_recto(15)
        self.robot.navegacion.giro_preciso_pd(-90)

    def ejecutar_matriz_2(self):
        # MATRIZ_2 -> 6 Azul + 6 Amarillo
        #   [Az, Am, Az, Az]
        #   [Am, Am, Am, Am]
        #   [Az, Am, Az, Az]
        #
        # Recorrido copiado paso a paso de MATRIZ2.py de la referencia
        # (version del 2026-07-14, la mas reciente). La parte final de ese
        # archivo tambien estaba comentada y se marca como SIN VALIDAR.

        #Acomoda su elevador y garra delantera
        self.robot.mecanismos.elevador_delantero.subir_al_tope(wait_after=False)
        self.robot.mecanismos.garra_delantera.abrir_al_tope(wait_after=False)

        #ref: seguir_linea_extremo(31, "derecha")
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=31, lado="derecha")
        wait(300)

        #ref: girar(-77) -> angulo real, NO es un -90
        self.robot.navegacion.giro_preciso_pd(-90)

        #ref: mover_garra(300, 90) -> abrir garra
        self.robot.mecanismos.garra_delantera.abrir(300, wait_after=False)

        #ref: seguir_linea_extremo(7, "derecha", velocidad_max=60)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=60, distancia_cm=7, lado="derecha")

        #ref: mover_recto(14)
        self.robot.chasis.avanzar_recto(14)

        #ref: mover_garra_delantera(600, 290) -> bajar elevador | captura el primer grupo
        #Conversion: -290 * 2.2222 = -644. Se usa -510, el descenso validado de este repo.
        #REQUIERE PRUEBA FISICA: altura de descenso y captura del grupo
        self.robot.mecanismos.elevador_delantero.mover(-510, velocidad=500)
        wait(200)

        #ref: retroceder(22) / girar(-83)
        self.robot.chasis.avanzar_recto(-22)
        self.robot.navegacion.giro_preciso_pd(-83)

        #ref: seguir_linea_extremo(11, "izquierda", velocidad_max=60)  <- borde IZQUIERDO
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=60, distancia_cm=11, lado="izquierda")

        #ref: girar(80)
        self.robot.navegacion.giro_preciso_pd(80)

        #ref: mover_garra_delantera(600, -25) subir | conversion +25*2.2222 = +56
        self.robot.mecanismos.elevador_delantero.mover(56)
        #ref: mover_garra(300, -49) -> cerrar garra
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(velocidad=1000, limite_potencia=100)

        #ref: mover_recto(14) / mover_garra_delantera(600, 15) bajar / mover_garra(300,-31) cerrar
        #REQUIERE PRUEBA FISICA: agarre incremental con la garra ya cargada
        self.robot.chasis.avanzar_recto(14)
        self.robot.mecanismos.elevador_delantero.mover(-33)
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(velocidad=1000, limite_potencia=100)

        #ref: retroceder(14) / girar(80)
        self.robot.chasis.avanzar_recto(-14)
        self.robot.navegacion.giro_preciso_pd(80)

        #ref: seguir_linea_extremo(12, "derecha") / girar(80) / seguir_linea_extremo(10, "derecha")
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=12, lado="derecha")
        self.robot.navegacion.giro_preciso_pd(80)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=80, distancia_cm=10, lado="derecha")

        #ref: mover_garra(300,80) abrir / mover_garra_delantera(600,-90) subir | +90*2.2222 = +200
        self.robot.mecanismos.garra_delantera.abrir(110, wait_after=False)
        self.robot.mecanismos.elevador_delantero.mover(200)

        #ref: retroceder(13) / mover_garra_delantera(600, 95) bajar | -95*2.2222 = -211
        self.robot.chasis.avanzar_recto(-13)
        self.robot.mecanismos.elevador_delantero.mover(-211)

        #ref: seguir_linea_extremo(13, "derecha") / mover_garra(500,-50) cerrar
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=13, lado="derecha")
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(velocidad=1000, limite_potencia=100)

        #ref: mover_garra_delantera(600, -150) subir | +150*2.2222 = +333
        self.robot.mecanismos.elevador_delantero.mover(333)

        #ref: seguir_linea_hasta_color(Color.BLUE, "derecha") -> aproximacion al marco
        #REQUIERE PRUEBA FISICA: deteccion del azul del marco
        self.robot.navegacion.seguidor_linea_color(self.sensor, 100, Color.BLUE, lado="derecha", tiempo_acomodo_ms=0)
        wait(400)

        #ref: girar(-3) -> correccion fina
        self.robot.navegacion.giro_preciso_pd(-3)

        #ref: mover_recto(13.5)
        self.robot.chasis.avanzar_recto(13.5)

        #ref: mover_garra_delantera(400, 70) bajar | -70*2.2222 = -156
        #ref: mover_garra_rapida(10, abrir=True) -> suelta los bloques en la matriz
        #REQUIERE PRUEBA FISICA: altura de colocacion y soltado
        self.robot.mecanismos.elevador_delantero.mover(-156)
        self.robot.mecanismos.garra_delantera.abrir(160, velocidad=2000)

        # ---------------- SIN VALIDAR: estaba comentado en la referencia ----------------

        #ref: mover_garra_delantera(400,-100) subir | +100*2.2222 = +222
        self.robot.mecanismos.elevador_delantero.mover(222)
        #ref: retroceder(13) / girar(180)
        self.robot.chasis.avanzar_recto(-13)
        self.robot.navegacion.giro_preciso_pd(180)

        #ref: seguir_linea_extremo(16,"derecha") / girar(-80) / mover_recto(2) / girar(80)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=16, lado="derecha")
        self.robot.navegacion.giro_preciso_pd(-80)
        self.robot.chasis.avanzar_recto(2)
        self.robot.navegacion.giro_preciso_pd(80)

        #ref: seguir_linea_extremo(12,"derecha",50) / mover_garra(300,90) abrir / mover_recto(19)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=50, distancia_cm=12, lado="derecha")
        self.robot.mecanismos.garra_delantera.abrir(110, wait_after=False)
        self.robot.chasis.avanzar_recto(19)

        #ref: mover_garra_delantera(400,180) bajar | -180*2.2222 = -400
        #REQUIERE PRUEBA FISICA
        self.robot.mecanismos.elevador_delantero.mover(-400)

        #ref: retroceder(26) / girar(-80) / seguir_linea_extremo(16,"derecha",50) / girar(80)
        self.robot.chasis.avanzar_recto(-26)
        self.robot.navegacion.giro_preciso_pd(-80)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=50, distancia_cm=16, lado="derecha")
        self.robot.navegacion.giro_preciso_pd(80)

        #ref: mover_recto(10) / mover_garra_delantera(400,-10) subir / mover_garra(300,-120) cerrar
        self.robot.chasis.avanzar_recto(10)
        self.robot.mecanismos.elevador_delantero.mover(22)
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(velocidad=1000, limite_potencia=100)

        #ref: retroceder(10) / girar(-80) / mover_garra(300,120) abrir / retroceder(2) / girar(80)
        self.robot.chasis.avanzar_recto(-10)
        self.robot.navegacion.giro_preciso_pd(-80)
        self.robot.mecanismos.garra_delantera.abrir(110, wait_after=False)
        self.robot.chasis.avanzar_recto(-2)
        self.robot.navegacion.giro_preciso_pd(80)

        #ref: seguir_linea_extremo(16,"derecha",50) / mover_recto(19)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=50, distancia_cm=16, lado="derecha")
        self.robot.chasis.avanzar_recto(19)

        #ref: mover_garra_delantera(400,10) bajar / mover_garra(300,-120) cerrar / retroceder(27)
        #REQUIERE PRUEBA FISICA: colocacion final
        self.robot.mecanismos.elevador_delantero.mover(-22)
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(velocidad=1000, limite_potencia=100)
        self.robot.chasis.avanzar_recto(-27)

    def ejecutar_matriz_3(self):
        # MATRIZ_3 -> 4 Verde + 4 Blanco + 4 Amarillo
        #   [V,  V,  V,  V ]
        #   [B,  B,  B,  B ]
        #   [Am, Am, Am, Am]
        #
        # Recorrido copiado paso a paso de matriz3.py de la referencia.
        # Es la unica matriz de la que existe recorrido COMPLETO y ejecutado
        # (alla vive a nivel de modulo, no dentro de la funcion).
        #
        # Estrategia de la referencia: agarra un grupo, lo SUELTA acomodado
        # sobre la linea, y al final empuja todo junto dentro del marco con un
        # avance largo y lento. NO es la estrategia de "meter y soltar" de la
        # matriz 4 de este repo.

        #Acomoda su elevador y garra delantera
        self.robot.mecanismos.elevador_delantero.subir_al_tope(wait_after=False)
        self.robot.mecanismos.garra_delantera.abrir_al_tope(wait_after=False)

        # ---------------- SECCION VERDES ----------------

        #ref: seguir_linea_extremo(45.5, "derecha")
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=45.5, lado="derecha")

        #ref: girar_modo_bestia_elite(-90)
        self.robot.navegacion.giro_preciso_pd(-90)

        #ref: mover_garra_rapida(39, abrir=True) / mover_garra_delantera(850, 276) bajar
        #Conversion del elevador: -276*2.2222 = -613. Se usa -510, el validado de este repo.
        #REQUIERE PRUEBA FISICA: altura de descenso
        self.robot.mecanismos.garra_delantera.abrir(110, wait_after=False)
        self.robot.mecanismos.elevador_delantero.mover(-510, velocidad=500)

        #ref: mover_recto_supremo(12) / mover_garra_rapida(-38, abrir=False) -> toma los 4 verdes
        #REQUIERE PRUEBA FISICA: profundidad de entrada y agarre de 4 bloques
        self.robot.chasis.avanzar_recto(12)
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(velocidad=1000, limite_potencia=100)

        #ref: mover_recto_supremo(-8.5) / girar_modo_bestia_elite(-90)
        self.robot.chasis.avanzar_recto(-8.5)
        self.robot.navegacion.giro_preciso_pd(-90)

        #ref: mover_garra_rapida(50, abrir=True) / mover_garra_delantera(850,-285) subir
        #Suelta los verdes acomodados
        #REQUIERE PRUEBA FISICA: soltado y acomodo de los verdes
        self.robot.mecanismos.garra_delantera.abrir(160, velocidad=2000)
        self.robot.mecanismos.elevador_delantero.subir_al_tope(wait_after=False)

        #ref: esperar(100) / mover_recto_supremo(-3) / esperar(100)
        wait(100)
        self.robot.chasis.avanzar_recto(-3)
        wait(100)

        #ref: seguir_linea_extremo(33.2, "derecha") -> acomoda los verdes
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=33.2, lado="derecha")

        # ---------------- SECCION AMARILLOS ----------------

        #ref: girar_modo_bestia_elite(92)
        self.robot.navegacion.giro_preciso_pd(92)

        #ref: mover_garra_rapida(12, abrir=True) / mover_garra_delantera(850,285) bajar
        self.robot.mecanismos.garra_delantera.abrir(110, wait_after=False)
        self.robot.mecanismos.elevador_delantero.mover(-510, velocidad=500)

        #ref: mover_recto_supremo(11) / mover_garra_rapida(-38, abrir=False) -> toma los 4 amarillos
        #REQUIERE PRUEBA FISICA
        self.robot.chasis.avanzar_recto(11)
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(velocidad=1000, limite_potencia=100)

        #ref: mover_recto_supremo(-15.5) / girar_modo_bestia_elite(92) / esperar(100)
        self.robot.chasis.avanzar_recto(-15.5)
        self.robot.navegacion.giro_preciso_pd(92)
        wait(100)

        #ref: mover_recto_supremo(-16.8) / mover_garra_rapida(50, abrir=True) / subir elevador
        #REQUIERE PRUEBA FISICA: soltado y acomodo de los amarillos
        self.robot.chasis.avanzar_recto(-16.8)
        self.robot.mecanismos.garra_delantera.abrir(160, velocidad=2000)
        self.robot.mecanismos.elevador_delantero.subir_al_tope(wait_after=False)

        #ref: seguir_linea_extremo(55.3, "izquierda")  <- borde IZQUIERDO
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=55.3, lado="izquierda")

        # ---------------- SECCION BLANCOS ----------------
        # ATENCION: este repositorio NO tiene ningun valor validado para
        # manipular bloques BLANCOS con la garra delantera.

        #ref: mover_garra_delantera(850,285) bajar / mover_recto_supremo(2)
        self.robot.mecanismos.elevador_delantero.mover(-510, velocidad=500)
        self.robot.chasis.avanzar_recto(2)

        #ref: girar_modo_bestia_elite(-92)
        self.robot.navegacion.giro_preciso_pd(-92)

        #ref: mover_garra_rapida(13, abrir=True) / mover_recto_supremo(13)
        #ref: mover_garra_rapida(-43, abrir=False) / mover_garra_delantera(850,-10) subir poco
        #REQUIERE PRUEBA FISICA: TODO este bloque (no hay valores validados para blancos)
        self.robot.mecanismos.garra_delantera.abrir(110, wait_after=False)
        self.robot.chasis.avanzar_recto(13)
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(velocidad=1000, limite_potencia=100)
        self.robot.mecanismos.elevador_delantero.mover(22)

        #ref: mover_recto_supremo(-14) / esperar(300) / girar_modo_bestia_elite(-96.3)
        self.robot.chasis.avanzar_recto(-14)
        wait(300)
        self.robot.navegacion.giro_preciso_pd(-96.3)

        #ref: mover_garra_rapida(45, abrir=True) / mover_garra_delantera(850,-290) subir
        self.robot.mecanismos.garra_delantera.abrir(160, velocidad=2000)
        self.robot.mecanismos.elevador_delantero.subir_al_tope(wait_after=False)

        #ref: mover_recto_supremo(-25)
        self.robot.chasis.avanzar_recto(-25)

        #ref: mover_garra_rapida(53, abrir=True) / mover_garra_delantera(850,291) bajar
        self.robot.mecanismos.garra_delantera.abrir_al_tope(wait_after=False)
        self.robot.mecanismos.elevador_delantero.mover(-510, velocidad=500)
        wait(300)

        # ---------------- ACOMODO FINAL POR EMPUJE ----------------

        #ref: mover_recto_supremo(40, velocidad_max=700, kp_gyro=0) -> empuje lento
        #Empuja los 12 bloques dentro del marco. Velocidad baja a proposito.
        #REQUIERE PRUEBA FISICA: este empuje define la puntuacion de toda la matriz
        self.robot.chasis.avanzar_recto(40, velocidad=200)

        #ref: esperar(100) / mover_recto_supremo(-1)
        wait(100)
        self.robot.chasis.avanzar_recto(-1)

        #ref: mover_garra_rapida(-55, abrir=False) / mover_garra_delantera(850,-25) bajar | -25*2.2222 = -56
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(velocidad=1000, limite_potencia=100)
        self.robot.mecanismos.elevador_delantero.mover(-56)

        #ref: girar_modo_bestia_elite(-91)
        self.robot.navegacion.giro_preciso_pd(-91)

        #ref: seguir_linea_extremo(20, "izquierda", velocidad_max=90)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=90, distancia_cm=20, lado="izquierda")

        #ref: mover_garra_delantera(850,-70) subir | +70*2.2222 = +156 / mover_recto(30)
        self.robot.mecanismos.elevador_delantero.mover(156)
        self.robot.chasis.avanzar_recto(30)

    def ejecutar_matriz_5(self):
        # MATRIZ_5 -> 6 Amarillo + 6 Azul (patron asimetrico)
        #   [Am, Az, Am, Az]
        #   [Am, Am, Am, Az]
        #   [Az, Am, Az, Az]
        #
        # ======================================================================
        # ATENCION: matriz5.py NO EXISTE en el repositorio de referencia.
        # Se reviso el archivo en los 51 commits del repo y siempre fue "pass".
        # ESTE RECORRIDO NO TIENE FUENTE. Es una copia de la topologia de
        # ejecutar_matriz_2(), porque la MATRIZ_2 tiene exactamente la misma
        # composicion (6 Am + 6 Az) y por lo tanto la recoleccion deberia ser
        # la misma. Lo unico que cambia es el ARREGLO dentro del marco, que
        # depende del orden de carga en la garra y NO PUEDE DETERMINARSE con
        # el codigo disponible.
        #
        # Probar ejecutar_matriz_2() primero. Lo que funcione alli, traerlo aqui.
        # ======================================================================

        #Acomoda su elevador y garra delantera
        self.robot.mecanismos.elevador_delantero.subir_al_tope(wait_after=False)
        self.robot.mecanismos.garra_delantera.abrir_al_tope(wait_after=False)

        #Topologia de la matriz 2: seguidor 31 derecha
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=31, lado="derecha")
        wait(300)
        self.robot.navegacion.giro_preciso_pd(-90)

        #Abre la garra y se acerca al primer grupo
        self.robot.mecanismos.garra_delantera.abrir(300, wait_after=False)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=60, distancia_cm=7, lado="derecha")
        self.robot.chasis.avanzar_recto(14)

        #Baja el elevador y captura el primer grupo
        #REQUIERE PRUEBA FISICA: altura de descenso y captura del grupo
        self.robot.mecanismos.elevador_delantero.mover(-510, velocidad=500)
        wait(200)

        #Sale y encadena hacia el segundo grupo
        self.robot.chasis.avanzar_recto(-22)
        self.robot.navegacion.giro_preciso_pd(-83)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=60, distancia_cm=11, lado="izquierda")
        self.robot.navegacion.giro_preciso_pd(80)

        #Agarre incremental
        #REQUIERE PRUEBA FISICA: agarre con la garra ya cargada
        self.robot.mecanismos.elevador_delantero.mover(56)
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(velocidad=1000, limite_potencia=100)
        self.robot.chasis.avanzar_recto(14)
        self.robot.mecanismos.elevador_delantero.mover(-33)
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(velocidad=1000, limite_potencia=100)

        #Encadena hacia el tercer grupo
        self.robot.chasis.avanzar_recto(-14)
        self.robot.navegacion.giro_preciso_pd(80)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=12, lado="derecha")
        self.robot.navegacion.giro_preciso_pd(80)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=80, distancia_cm=10, lado="derecha")

        #Reacomodo de la carga
        #REQUIERE PRUEBA FISICA
        self.robot.mecanismos.garra_delantera.abrir(110, wait_after=False)
        self.robot.mecanismos.elevador_delantero.mover(200)
        self.robot.chasis.avanzar_recto(-13)
        self.robot.mecanismos.elevador_delantero.mover(-211)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=13, lado="derecha")
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(velocidad=1000, limite_potencia=100)
        self.robot.mecanismos.elevador_delantero.mover(333)

        #Aproximacion al marco buscando el azul
        #REQUIERE PRUEBA FISICA: deteccion del azul del marco
        self.robot.navegacion.seguidor_linea_color(self.sensor, 100, Color.BLUE, lado="derecha", tiempo_acomodo_ms=0)
        wait(400)
        self.robot.navegacion.giro_preciso_pd(-3)
        self.robot.chasis.avanzar_recto(13.5)

        #Coloca los bloques
        #REQUIERE PRUEBA FISICA: altura de colocacion y ARREGLO ASIMETRICO
        self.robot.mecanismos.elevador_delantero.mover(-156)
        self.robot.mecanismos.garra_delantera.abrir(160, velocidad=2000)
