from pybricks.parameters import Stop
from pybricks.tools import wait
from pybricks.pupdevices import Motor
import config # Movido arriba para eliminar lag de I/O en ejecución

class MecanismoBase:

    """Clase base para reutilizar lógica de movimiento de motores."""

    def __init__(self, motor: Motor):

        self.motor = motor


    def mover_angulo(self, grados: int, velocidad=600, wait_after=True, frenado=Stop.HOLD, margen_grados=0):

        if wait_after and margen_grados > 0:

            angulo_meta = self.motor.angle() + grados

            self.motor.run_angle(velocidad, grados, then=frenado, wait=False)

            while abs(angulo_meta - self.motor.angle()) > margen_grados:

                if self.motor.stalled():

                    break

                wait(2)

        else:

            self.motor.run_angle(velocidad, grados, then=frenado, wait=wait_after)


    def llevar_al_tope(self, direccion: str, velocidad=1000, limite_potencia=50, wait_after=True, frenado=Stop.HOLD):
        """
        Función maestra blindada para topes físicos.
        Se integró el parámetro 'frenado' en la firma para evitar TypeError.
        Incluye sanitización matemática del límite de potencia.
        """
        # 1. Asignación Vectorial Rápida
        vel_real = abs(velocidad) if direccion in ["positivo", 1] else -abs(velocidad)

        # 2. Sanitización Matemática (Evita ValueError en capas C/C++)
        limite_seguro = min(100, max(0, abs(limite_potencia)))
        
        if wait_after:
            # Ejecución síncrona: El microcontrolador absorbe el impacto
            self.motor.run_until_stalled(vel_real, then=frenado, duty_limit=limite_seguro)
            
            # --- CORTE ELÉCTRICO INYECTADO ---
            # Solo se activa si la clase hija inyecta Stop.COAST explícitamente
            if frenado == Stop.COAST:
                self.motor.dc(0)
                self.motor.stop()
        else:
            # Modo Asíncrono: Inyección de voltaje continuo
            potencia_vectorial = limite_seguro if vel_real > 0 else -limite_seguro
            self.motor.dc(potencia_vectorial)

class GarraDelantera(MecanismoBase):
    def __init__(self, motor: Motor):
        super().__init__(motor)
        self.motor.control.limits(speed=1500, acceleration=5000)

    def abrir(self, grados, velocidad=600, wait_after=True, frenado=Stop.HOLD, margen_grados=0):
        self.mover_angulo(-abs(grados), velocidad, wait_after, frenado, margen_grados)

    def cerrar(self, grados, velocidad=600, wait_after=True, frenado=Stop.HOLD, margen_grados=0):
        self.mover_angulo(abs(grados), velocidad, wait_after, frenado, margen_grados)

    def abrir_al_tope(self, velocidad=800, limite_potencia=50, wait_after=True):
        self.llevar_al_tope("negativo", velocidad, limite_potencia, wait_after)

    def cerrar_al_tope(self, velocidad=800, limite_potencia=50, wait_after=True):
        self.llevar_al_tope("positivo", velocidad, limite_potencia, wait_after)

class ElevadorDelantero(MecanismoBase):
    def mover(self, grados, velocidad=600, wait_after=True, frenado=Stop.HOLD, margen_grados=0):
        self.mover_angulo(grados, velocidad, wait_after, frenado, margen_grados)

    def subir_al_tope(self, velocidad=1000, limite_potencia=50, wait_after=True):
        self.llevar_al_tope("positivo", velocidad, limite_potencia, wait_after)

    def bajar_al_tope(self, velocidad=1000, limite_potencia=50, wait_after=True):
        self.llevar_al_tope("negativo", velocidad, limite_potencia, wait_after)

class GarraTrasera(MecanismoBase):
    def __init__(self, motor: Motor):
        super().__init__(motor)
        # Desbloqueamos los límites del firmware para aceleraciones agresivas.
        # ROBOCOP no puede perder tiempo en rampas de aceleración lentas.
        self.motor.control.limits(speed=1500, acceleration=5000)

    # --- MOVIMIENTOS RELATIVOS SEMÁNTICOS ---
    def bajar(self, grados, velocidad=600, wait_after=True, frenado=Stop.HOLD, margen_grados=0):
        """Baja la garra un número específico de grados."""
        self.mover_angulo(abs(grados), velocidad, wait_after, frenado, margen_grados)

    def subir(self, grados, velocidad=600, wait_after=True, frenado=Stop.HOLD, margen_grados=0):
        """Sube la garra un número específico de grados."""
        self.mover_angulo(-abs(grados), velocidad, wait_after, frenado, margen_grados)

    # --- RUTINAS DE TOPE FÍSICO (WRAPPERS SOLID) ---
    def bajar_al_tope(self, velocidad=800, limite_potencia=50, wait_after=True):
        """
        Desciende la garra hasta impactar con el tope físico. 
        Inyecta Stop.COAST obligatoriamente para desconectar el puente H 
        y dejar el mecanismo 100% libre y "flojito".
        """
        # Nota: Asumo que "negativo" es la dirección hacia el suelo en tu ensamble.
        self.llevar_al_tope("positivo", velocidad, limite_potencia, wait_after, frenado=Stop.COAST)

    def subir_al_tope(self, velocidad=800, limite_potencia=50, wait_after=True):
        """
        Eleva la garra hasta su tope superior. 
        Mantiene Stop.HOLD por defecto para asegurar la estructura de forma rígida en el aire.
        """
        self.llevar_al_tope("negativo", velocidad, limite_potencia, wait_after, frenado=Stop.HOLD)

    def avanzar_y_gatillar(self, chasis, distancia_total_cm, vel_chasis, distancia_trigger_cm, grados_garra, vel_garra=1000):
        # (El código asíncrono original permanece intacto)
        distancia_total_mm = distancia_total_cm * 10
        trigger_mm = abs(distancia_trigger_cm * 10)
        
        if trigger_mm > abs(distancia_total_mm):
            trigger_mm = abs(distancia_total_mm)
            
        vel_segura = min(abs(vel_chasis), 930)
        _, accel_lin, vel_giro, accel_giro = chasis.drive_base.settings()
        chasis.drive_base.settings(vel_segura, accel_lin, vel_giro, accel_giro)
        
        dist_inicial = chasis.drive_base.distance()
        chasis.drive_base.straight(distancia_total_mm, then=Stop.HOLD, wait=False)

        garra_disparada = False

        while not chasis.drive_base.done():
            recorrido_actual = abs(chasis.drive_base.distance() - dist_inicial)

            if recorrido_actual >= trigger_mm and not garra_disparada:
                self.mover(grados_garra, velocidad=vel_garra, wait_after=False, frenado=Stop.HOLD)
                garra_disparada = True
            wait(1)

        if not garra_disparada:
            self.mover(grados_garra, velocidad=vel_garra, wait_after=False, frenado=Stop.HOLD)

        chasis.drive_base.settings(config.STRAIGHT_SPEED, accel_lin, vel_giro, accel_giro)

class Mecanismos:
    def __init__(self, motor_garra_delantera: Motor, motor_elevador_del: Motor, motor_garra_trasera: Motor):
        self.garra_delantera = GarraDelantera(motor_garra_delantera)
        self.elevador_delantero = ElevadorDelantero(motor_elevador_del)
        self.garra_trasera = GarraTrasera(motor_garra_trasera)
