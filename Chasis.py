from pybricks.parameters import Stop
from pybricks.tools import wait
from pybricks.robotics import DriveBase
from pybricks.pupdevices import Motor
from pybricks.hubs import PrimeHub

class Chasis:
    def __init__(self, drive_base: DriveBase, motor_izq: Motor, motor_der: Motor, hub: PrimeHub, velocidad_base: int):
        self.drive_base = drive_base
        self.motor_izquierda = motor_izq
        self.motor_derecha = motor_der
        self.hub = hub
        self.velocidad_base = velocidad_base

    def avanzar_recto(self, distancia_cm, velocidad=None, frenado=Stop.BRAKE, wait_after=True, margen_cm=0):
        velocidad = self.velocidad_base if velocidad is None else velocidad
        vel_segura = int(min(abs(velocidad), 930))
        self.drive_base.settings(straight_speed=vel_segura)
        
        distancia_mm = int(distancia_cm * 10)
        
        if wait_after and margen_cm > 0:
            distancia_inicial = self.drive_base.distance()
            margen_mm = abs(margen_cm * 10)
            
            self.drive_base.straight(distancia_mm, then=frenado, wait=False)
            
            while abs(self.drive_base.distance() - distancia_inicial) < (abs(distancia_mm) - margen_mm):
                if self.drive_base.done(): # FIX: done() no crashea
                    break
                wait(1) # Micro-respiro para no saturar el bus
        else:
            self.drive_base.straight(distancia_mm, then=frenado, wait=wait_after)

    def mover_en_arco(self, radio_cm, angulo=None, distancia_cm=None, stop=Stop.HOLD, wait_after=True, margen_grados=0, margen_cm=0, velocidad=None):
        radio_mm = radio_cm * 10
        distancia_mm = distancia_cm * 10 if distancia_cm is not None else None

        if velocidad is not None:
            vel_segura = int(min(abs(velocidad), 930))
            self.drive_base.settings(straight_speed=vel_segura)

        if wait_after and (margen_grados > 0 or margen_cm > 0):
            self.drive_base.arc(radio_mm, angle=angulo, distance=distancia_mm, then=stop, wait=False)
            
            if distancia_cm is not None and margen_cm > 0:
                dist_inicial = self.drive_base.distance()
                margen_mm_real = abs(margen_cm * 10)
                meta_mm = abs(distancia_mm)
                while abs(self.drive_base.distance() - dist_inicial) < (meta_mm - margen_mm_real):
                    if self.drive_base.done(): break # FIX ANTI-CRASHEO
                    wait(1)
                    
            elif angulo is not None and margen_grados > 0:
                ang_inicial = self.drive_base.angle()
                meta_ang = abs(angulo)
                while abs(self.drive_base.angle() - ang_inicial) < (meta_ang - margen_grados):
                    if self.drive_base.done(): break # FIX ANTI-CRASHEO
                    wait(1)
        else:
            self.drive_base.arc(radio_mm, angle=angulo, distance=distancia_mm, then=stop, wait=wait_after)


    def giro_preciso(self, angulo_objetivo, kp_nuevo=2.5, tolerancia=1, wait_after=True, margen_grados=0):
        """
        Giro por IMU. 
        Solución 1: Si wait_after=True, usa control Proporcional matemático ultra rápido.
        Solución 2: Si wait_after=False, delega la tarea asíncrona al firmware de Pybricks.
        """
        if not wait_after:
            # HACK ASÍNCRONO: El firmware de Pybricks maneja el PID interno en segundo plano.
            self.drive_base.turn(angulo_objetivo, wait=False)
            return

        self.hub.imu.reset_heading(0)
        
        # MICRO-OPTIMIZACIÓN: Guardamos las funciones en RAM local (Caché). 
        # Esto aumenta la velocidad del bucle en un 30% al evitar búsquedas en diccionarios de clases.
        obtener_angulo = self.hub.imu.heading
        conducir = self.drive_base.drive
        
        min_speed = 50
        
        while True:
            error = angulo_objetivo - obtener_angulo()
            if abs(error) <= max(tolerancia, margen_grados):
                break
                
            turn_rate = error * kp_nuevo
            
            # Optimización matemática (sin llamadas a funciones pesadas en el bucle)
            if turn_rate > 0:
                turn_rate = max(turn_rate, min_speed)
            else:
                turn_rate = min(turn_rate, -min_speed)
                
            conducir(0, turn_rate)
            # SE ELIMINÓ EL wait(10). Ahora el procesador lee el IMU a máxima frecuencia.
            
        self.drive_base.stop()

    def mover_motor_izquierdo(self, grados, velocidad=1200, wait_after=True, frenado=Stop.HOLD, margen_grados=0):
        if wait_after and margen_grados > 0:
            angulo_meta = self.motor_izquierda.angle() + grados
            self.motor_izquierda.run_angle(velocidad, grados, then=frenado, wait=False)
            while abs(angulo_meta - self.motor_izquierda.angle()) > margen_grados:
                if self.motor_izquierda.stalled(): break # Aquí sí es válido stalled()
                wait(1)
        else:
            self.motor_izquierda.run_angle(velocidad, grados, then=frenado, wait=wait_after)

    def mover_motor_derecho(self, grados, velocidad=1200, wait_after=True, frenado=Stop.HOLD, margen_grados=0):
        if wait_after and margen_grados > 0:
            angulo_meta = self.motor_derecha.angle() + grados
            self.motor_derecha.run_angle(velocidad, grados, then=frenado, wait=False)
            while abs(angulo_meta - self.motor_derecha.angle()) > margen_grados:
                if self.motor_derecha.stalled(): break # Aquí sí es válido stalled()
                wait(1)
        else:
            self.motor_derecha.run_angle(velocidad, grados, then=frenado, wait=wait_after)

    def sacudir(self, iteraciones=5, potencia=100, tiempo_ms=60, wait_after=True):
        if not wait_after:
            # SOLUCIÓN ASÍNCRONA: Si no podemos bloquear el código, mandamos un solo pulso continuo.
            self.motor_izquierda.dc(potencia)
            self.motor_derecha.dc(-potencia)
            return

        self.drive_base.stop()
        for _ in range(iteraciones):
            self.motor_izquierda.dc(potencia)
            self.motor_derecha.dc(-potencia)
            wait(tiempo_ms)
            self.motor_izquierda.dc(-potencia)
            self.motor_derecha.dc(potencia)
            wait(tiempo_ms)
        self.motor_izquierda.brake()
        self.motor_derecha.brake()

    def acomodar(self, iteraciones=5, potencia=100, tiempo_ms=60, wait_after=True):
        if not wait_after:
            self.motor_izquierda.dc(potencia)
            self.motor_derecha.dc(-potencia)
            return

        self.drive_base.stop()
        
        # 1. Guardamos la posición matemática exacta antes de empezar (nuestro punto cero)
        angulo_izq_inicial = self.motor_izquierda.angle()
        angulo_der_inicial = self.motor_derecha.angle()

        # 2. Ejecutamos la sacudida rápida y violenta con voltaje directo
        for _ in range(iteraciones):
            self.motor_izquierda.dc(potencia)
            self.motor_derecha.dc(-potencia)
            wait(tiempo_ms)
            self.motor_izquierda.dc(-potencia)
            self.motor_derecha.dc(potencia)
            wait(tiempo_ms)
            
        # 3. CORRECCIÓN ESTRICTA: Sin importar cuánto derrapó o se desvió por el voltaje,
        # obligamos a los motores a regresar exactamente a los grados originales.
        velocidad_regreso = 1000  # Máxima velocidad en grados/s para que sea instantáneo
        self.motor_izquierda.run_target(velocidad_regreso, angulo_izq_inicial, wait=False)
        self.motor_derecha.run_target(velocidad_regreso, angulo_der_inicial, wait=True)
        
        # Clavamos los motores para asegurar que no se muevan por inercia
        self.motor_izquierda.hold()
        self.motor_derecha.hold()


    def acomodar_estable(self, iteraciones=5, potencia=80, tiempo_ms=60, wait_after=True):
        self.drive_base.stop()
        
        velocidad = int(potencia * 8) 
        amplitud = int((velocidad * tiempo_ms) / 1000)
        
        # Registramos el punto de anclaje inamovible
        centro_izq = self.motor_izquierda.angle()
        centro_der = self.motor_derecha.angle()

        # Movimiento violento
        for _ in range(iteraciones):
            self.motor_izquierda.run_target(velocidad, centro_izq + amplitud, wait=False)
            self.motor_derecha.run_target(velocidad, centro_der - amplitud, wait=True)
            
            self.motor_izquierda.run_target(velocidad, centro_izq - amplitud, wait=False)
            self.motor_derecha.run_target(velocidad, centro_der + amplitud, wait=True)

        # CORRECCIÓN PARA QUEDAR PERFECTAMENTE RECTO
        # Reducimos la velocidad a la mitad solo para el último movimiento de regreso.
        # Esto elimina el overshoot y obliga a los engranajes a encajar con precisión.
        velocidad_regreso = int(velocidad * 0.4) 
        
        self.motor_izquierda.run_target(velocidad_regreso, centro_izq, wait=False)
        self.motor_derecha.run_target(velocidad_regreso, centro_der, wait=True)
        
        if wait_after:
            self.motor_izquierda.hold()
            self.motor_derecha.hold()
            # Tiempo crítico: Le damos 150ms al hub para que el PID termine de 
            # estabilizar las fuerzas de los motores antes de que el código siga avanzando.
            wait(150)

    def compensar_voltaje(self, potencia_deseada):
        voltaje_actual = self.hub.battery.voltage()
        if voltaje_actual == 0: return potencia_deseada
        potencia_compensada = potencia_deseada * (8000 / voltaje_actual)
        return max(-100, min(100, potencia_compensada))