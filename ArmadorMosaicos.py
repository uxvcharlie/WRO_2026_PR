from pybricks.parameters import Color, Stop
from robot import Robot

class ArmadorMosaicos:
    def __init__(self, robot_instancia: Robot, sensor):
        self.robot = robot_instancia
        self.sensor = sensor
        
        # --- PATRÓN ESTRATEGIA (Diccionario de Rutinas) ---
        # Mapea el número de mosaico con la función que debe ejecutar.
        # Si las reglas cambian, solo agregas el nuevo mosaico aquí.
        self.rutinas = {
            1: self._armar_verde_verde,
            2: self._armar_verde_amarillo,
            3: self._armar_azul,
            4: self._armar_amarillo,
            5: self._armar_blanco
        }

    def armar(self, numero_mosaico: int):
        """Método principal que decide qué rutina ejecutar dinámicamente."""
        # Intenta obtener la rutina del diccionario. Si el número no existe, usa la 1 por defecto.
        rutina_a_ejecutar = self.rutinas.get(numero_mosaico, self._armar_verde_verde)
        
        print(f"Ejecutando rutina de armado para mosaico: {numero_mosaico}")
        rutina_a_ejecutar()

    # --- RUTINAS PRIVADAS ---
    def _armar_verde_verde(self):
        # Mandar la garra central abajo si no lo está
        self.robot.mecanismos.garra_trasera.llevar_al_tope("negativo")
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(velocidad=1000, limite_potencia=100)
        
        # Acomodo para agarrar dos azules y dos verdes
        self.robot.navegacion.seguidor_linea_distancia_desacelerado(self.sensor, 100, 52, margen_cm=5, tiempo_acomodo_ms=500)
        self.robot.chasis.giro_preciso(-87)
        
        # Entrada
        self.robot.mecanismos.garra_delantera.abrir(170, velocidad=1000, wait_after=False)
        self.robot.chasis.avanzar_recto(13, velocidad=1000, margen_cm=3)
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(velocidad=1000, limite_potencia=100)
        self.robot.chasis.avanzar_recto(-5)
        self.robot.mecanismos.garra_delantera.abrir(170, velocidad=1000, wait_after=True, margen_grados=100)
        self.robot.chasis.avanzar_recto(10, velocidad=1000)
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(velocidad=1000, limite_potencia=100)
        self.robot.chasis.avanzar_recto(-25, velocidad=1000)
        self.robot.mecanismos.garra_delantera.abrir(100, velocidad=1000, margen_grados=20)
        self.robot.chasis.avanzar_recto(6)
        self.robot.chasis.avanzar_recto(-3.5)
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(velocidad=1000, limite_potencia=100)

        self.robot.chasis.giro_preciso(200, margen_grados=20)
        self.robot.chasis.avanzar_recto(5, 1000, frenado=Stop.NONE)
        self.robot.navegacion.seguidor_linea_color(self.sensor, 100, Color.BLUE, lado="izquierda", tiempo_acomodo_ms=0, distancia_cm=20)
        
        # Subida de garra
        self.robot.mecanismos.garra_trasera.llevar_al_tope("positivo", velocidad=400, limite_potencia=100)
        
        # Acomodo para que queden en su lugar
        self.robot.chasis.mover_en_arco(-9, distancia_cm=3.6, stop=Stop.COAST, velocidad=930)
        self.robot.chasis.mover_en_arco(9.5, distancia_cm=2, stop=Stop.NONE, velocidad=930)
        self.robot.chasis.avanzar_recto(7)
        self.robot.chasis.mover_motor_izquierdo(30)
        
        # Soltar
        self.robot.mecanismos.garra_trasera.mover(-110)
        self.robot.mecanismos.garra_delantera.abrir(grados=50, velocidad=400) 
        self.robot.chasis.sacudir(iteraciones=3, potencia=60, tiempo_ms=100)
        self.robot.mecanismos.garra_delantera.abrir_al_tope(velocidad=1200, limite_potencia=100) 
        self.robot.chasis.sacudir(iteraciones=2, potencia=60, tiempo_ms=100)      
        
        # Acomodo para buscar los otros
        self.robot.chasis.avanzar_recto(-30) # Retroceso limpio
        self.robot.mecanismos.garra_trasera.llevar_al_tope("negativo", limite_potencia=100)
        self.robot.chasis.giro_preciso(155)
        self.robot.chasis.avanzar_recto(28)
        self.robot.chasis.mover_motor_izquierdo(120)
        
        # Entrar
        self.robot.chasis.avanzar_recto(12)
        self.robot.chasis.avanzar_recto(10, velocidad=1000)
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(velocidad=1000, limite_potencia=100)
        self.robot.chasis.avanzar_recto(-5)
        self.robot.mecanismos.garra_delantera.abrir(170, velocidad=1000)
        self.robot.chasis.avanzar_recto(10, velocidad=1000)
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(velocidad=1000, limite_potencia=100)
        self.robot.chasis.avanzar_recto(-25)
        self.robot.mecanismos.garra_delantera.abrir(100, velocidad=1000, margen_grados=20)
        self.robot.chasis.avanzar_recto(7)
        self.robot.chasis.avanzar_recto(-3.5)
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(velocidad=1000, limite_potencia=100)
        
        # Agarrar / Buscar seguidor
        self.robot.chasis.giro_preciso(80)
        self.robot.chasis.avanzar_recto(32) 
        self.robot.chasis.mover_motor_izquierdo(150)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, 80, 20)
        self.robot.mecanismos.garra_trasera.llevar_al_tope("positivo", limite_potencia=100)
        self.robot.chasis.mover_en_arco(9, distancia_cm=3.8, stop=Stop.COAST, velocidad=930)
        self.robot.chasis.mover_en_arco(-9, distancia_cm=3.8, stop=Stop.BRAKE, velocidad=930)
        self.robot.chasis.avanzar_recto(14)
        self.robot.mecanismos.garra_trasera.llevar_al_tope("negativo", limite_potencia=100)
        self.robot.mecanismos.garra_trasera.mover(90)
        
        self.robot.mecanismos.garra_delantera.abrir(grados=50, velocidad=400) 
        self.robot.mecanismos.garra_trasera.llevar_al_tope("negativo", limite_potencia=100)
        self.robot.chasis.sacudir(iteraciones=4, potencia=60, tiempo_ms=100)
        self.robot.mecanismos.garra_delantera.abrir_al_tope(velocidad=1200, limite_potencia=100) 
        self.robot.mecanismos.garra_trasera.llevar_al_tope(direccion="positivo", limite_potencia=100)
        self.robot.chasis.avanzar_recto(-30) 

        # Acá se pretende agarrar los bloques azul y verde y dejarlos en la fila de atrás
        self.robot.chasis.giro_preciso(180)
        self.robot.chasis.avanzar_recto(40)
        self.robot.mecanismos.garra_delantera.abrir_al_tope(170, limite_potencia=100)
        self.robot.chasis.avanzar_recto(20)
        self.robot.mecanismos.garra_delantera.cerrar_al_tope()
        self.robot.chasis.avanzar_recto(-10)
        self.robot.mecanismos.garra_delantera.abrir(170, 1000)
        self.robot.chasis.avanzar_recto(10)
        self.robot.chasis.avanzar_recto(-5)
        self.robot.mecanismos.garra_delantera.cerrar_al_tope()
        
        # Acá retroceder y girar para agarrar los otros dos verdes
        self.robot.chasis.avanzar_recto(-10)
        self.robot.chasis.giro_preciso(90)
        self.robot.chasis.avanzar_recto(-15)
        self.robot.chasis.mover_motor_derecho(180, 1000)
        self.robot.chasis.avanzar_recto(10)
        self.robot.chasis.mover_motor_izquierdo(180, 1000)
        self.robot.mecanismos.garra_delantera.abrir(170, 1000)
        self.robot.chasis.avanzar_recto(10)
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(1000, 100)

        # Acá agarra los 2 bloques restantes con la garra de atras
        self.robot.chasis.avanzar_recto(-30)
        self.robot.chasis.giro_preciso(180)
        self.robot.mecanismos.garra_trasera.llevar_al_tope(direccion="positivo", limite_potencia=100)
        self.robot.chasis.avanzar_recto(-30)
        self.robot.mecanismos.garra_trasera.llevar_al_tope(direccion="negativo", limite_potencia=100)

        # Acá irlo a dejar al mosaico desde el espacio de los verdes
        self.robot.chasis.avanzar_recto(30)
        self.robot.chasis.giro_preciso(90)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, 1000, 200)
        self.robot.chasis.giro_preciso(-90)
        self.robot.chasis.avanzar_recto(30)
        self.robot.navegacion.seguidor_linea_color(self.sensor, 1000, Color.GREEN, distancia_cm=40)

        # Acá el robot hp se acomoda para quedar recto con los colores
        self.robot.mecanismos.garra_trasera.llevar_al_tope("positivo", velocidad=400, limite_potencia=100)
        self.robot.chasis.mover_motor_derecho(180, 1000)
        self.robot.chasis.avanzar_recto(3)
        self.robot.chasis.mover_motor_izquierdo(180, 1000)

        # Acá los deja
        self.robot.mecanismos.garra_trasera.mover(-110)
        self.robot.mecanismos.garra_delantera.abrir(grados=50, velocidad=400) 
        self.robot.chasis.sacudir(iteraciones=3, potencia=60, tiempo_ms=100)
        self.robot.mecanismos.garra_delantera.abrir_al_tope(velocidad=1200, limite_potencia=100) 
        self.robot.chasis.sacudir(iteraciones=2, potencia=60, tiempo_ms=100)   

    def _armar_verde_amarillo(self):

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
        self.robot.chasis.avanzar_recto(10.5)
        self.robot.chasis.avanzar_recto(-10.5)

        #Camino al bloque verdecito jeje
        self.robot.navegacion.giro_preciso_pd(90)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=41, tiempo_acomodo_ms=50)
        self.robot.navegacion.giro_preciso_pd(-90)
        self.robot.mecanismos.garra_delantera.abrir(grados=110, wait_after=False)

        #Agarra el bloque verde alaverga
        self.robot.navegacion.chasis.avanzar_recto(9.3)
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(velocidad=1000)
        self.robot.chasis.avanzar_recto(-5)
        self.robot.navegacion.giro_preciso_pd(-80)
        self.robot.chasis.mover_motor_derecho(grados=780)

        #Sigue la linea hacia el mosaico 
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=100, distancia_cm=14, tiempo_acomodo_ms=0)

        #Abre la garra para dejar los 4 bloques azules
        self.robot.mecanismos.garra_delantera.abrir(300, wait_after=False)


        #Levanta la garra para meter los 6 bloques
        self.robot.mecanismos.elevador_delantero.mover(400, velocidad=900, wait_after=False)
        self.robot.chasis.avanzar_recto(-15)
        self.robot.mecanismos.elevador_delantero.mover(-380)
        self.robot.navegacion.seguidor_linea_distancia(self.sensor, velocidad_max=90, distancia_cm=25, tiempo_acomodo_ms=0)

        #Aprieta la garra y agarra los 6 bloques
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(limite_potencia=100)
        self.robot.mecanismos.elevador_delantero.mover(300)

        #Se mete a la matriz a dejar los 6 bloques
        self.robot.chasis.avanzar_recto(25)
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

        self.robot.chasis.avanzar_recto(15.5) 
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

        #Agarra el bloque verde alaverga
        self.robot.navegacion.chasis.avanzar_recto(9.5)
        self.robot.mecanismos.garra_delantera.cerrar_al_tope(velocidad=1000, limite_potencia=100, wait_after=False)
        self.robot.chasis.avanzar_recto(distancia_cm=-5.5)
        self.robot.navegacion.giro_preciso_pd(-150)
        self.robot.chasis.mover_motor_derecho(grados=250)

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

        #Se mete a la matriz a dejar los 6 bloques
        self.robot.chasis.avanzar_recto(25)
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


    def _armar_azul(self):
        self.robot.chasis.avanzar_recto(10)

    def _armar_amarillo(self):
        pass

    def _armar_blanco(self):
        pass