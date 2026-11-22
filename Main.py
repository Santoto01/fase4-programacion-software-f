# Main.py
"""
Punto de entrada interactivo por terminal para el sistema de gestión Software FJ.
Permite operar manualmente mediante menú e incluye la simulación automática de 12 casos.
"""

from Logger import configurar_logger
from Gestor import GestorSoftwareFJ
from Cliente import Cliente
from Servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from Excepciones import SoftwareFJError


def ejecutar_simulacion_automatica(gestor: GestorSoftwareFJ):
    """Ejecuta las 12 operaciones automáticas exigidas por la guía."""
    logger = gestor.logger
    logger.info("=== INICIO DE SIMULACIÓN AUTOMÁTICA (12 OPERACIONES) ===")

    # 1. Registro válido de cliente (try / except / else)
    try:
        c1 = Cliente("1098765432", "Laura Gómez", "laura.gomez@correo.com", "3104567890")
        gestor.registrar_cliente(c1)
    except SoftwareFJError as e:
        logger.error(f"Operación 1 fallida: {e}")
    else:
        logger.info("Operación 1 completada sin errores.")

    # 2. Registro válido de segundo cliente
    try:
        c2 = Cliente("1095123456", "Carlos Mendoza", "cmendoza@empresa.co", "3209876543")
        gestor.registrar_cliente(c2)
    except SoftwareFJError as e:
        logger.error(f"Operación 2 fallida: {e}")

    # 3. Registro inválido de cliente
    try:
        c_invalido = Cliente("1099000111", "Pedro", "pedrocorreo.com", "123")
        gestor.registrar_cliente(c_invalido)
    except SoftwareFJError as e:
        logger.error(f"Operación 3 capturada correctamente: {e}")

    # 4. Creación correcta de los 3 tipos de servicios
    try:
        s1 = ReservaSala("SALA-01", "Sala Juntas Norte", 80000, capacidad=12)
        s2 = AlquilerEquipo("EQ-01", "Portátil Workstation Dell", 25000, stock=3, deposito=50000)
        s3 = AsesoriaEspecializada("ASE-01", "Arquitectura Cloud", 120000, especialidad="DevOps")
        gestor.agregar_servicio(s1)
        gestor.agregar_servicio(s2)
        gestor.agregar_servicio(s3)
    except SoftwareFJError as e:
        logger.error(f"Operación 4 fallida: {e}")

    # 5. Creación incorrecta de servicio (tarifa negativa)
    try:
        s_malo = ReservaSala("SALA-ERR", "Sala Fantasma", -50000, capacidad=5)
        gestor.agregar_servicio(s_malo)
    except SoftwareFJError as e:
        logger.error(f"Operación 5 capturada correctamente: {e}")

    # 6. Servicio sin stock disponible
    try:
        s_agotado = AlquilerEquipo("EQ-02", "Proyector 4K", 30000, stock=0)
        gestor.agregar_servicio(s_agotado)
        gestor.crear_reserva("RES-001", "1098765432", "EQ-02", 3)
    except SoftwareFJError as e:
        logger.error(f"Operación 6 capturada correctamente (Causa: {e.__cause__}): {e}")

    # 7. Reserva exitosa + Confirmación + Procesamiento
    try:
        r1 = gestor.crear_reserva("RES-002", "1098765432", "SALA-01", 5)
        r1.confirmar()
        total_r1 = r1.procesar()
    except SoftwareFJError as e:
        logger.error(f"Operación 7 fallida: {e}")
    else:
        logger.info(f"Operación 7 exitosa -> Total pagado por {r1.id}: ${total_r1:,.2f}")

    # 8. Reserva fallida por cliente inexistente
    try:
        gestor.crear_reserva("RES-003", "9999999999", "ASE-01", 2)
    except SoftwareFJError as e:
        logger.error(f"Operación 8 capturada correctamente (Causa original: {e.__cause__}): {e}")

    # 9. Reserva fallida por duración inválida
    try:
        gestor.crear_reserva("RES-004", "1095123456", "EQ-01", 1)
    except SoftwareFJError as e:
        logger.error(f"Operación 9 capturada correctamente (Causa: {e.__cause__}): {e}")

    # 10. Sobrecarga de métodos y error de cálculo inconsistente
    try:
        r2 = gestor.crear_reserva("RES-005", "1095123456", "ASE-01", 4)
        total_desc = r2.calcular_total(porcentaje_iva=0.19, descuento=50000)
        logger.info(f"Operación 10a (Sobrecarga válida) -> Total con descuento: ${total_desc:,.2f}")
        r2.calcular_total(porcentaje_iva=0.19, descuento=9000000)
    except SoftwareFJError as e:
        logger.error(f"Operación 10b capturada correctamente: {e}")

    # 11. Operación no permitida sobre estado de reserva (try / except / finally)
    try:
        r2.cancelar()
        r2.confirmar()
    except SoftwareFJError as e:
        logger.error(f"Operación 11 capturada correctamente: {e}")
    finally:
        logger.info(f"Operación 11 finally -> Estado final de {r2.id}: {r2.estado}")

    # 12. Reserva exitosa con tarifa especial (exento de IVA + urgencia)
    try:
        r3 = gestor.crear_reserva("RES-006", "1098765432", "EQ-01", 4)
        r3.confirmar()
        total_esp = r3.calcular_total(porcentaje_iva=0.0, descuento=0.0, recargo_urgencia=20000)
        logger.info(f"Operación 12 exitosa -> Total tarifa especial {r3.id}: ${total_esp:,.2f}")
    except SoftwareFJError as e:
        logger.error(f"Operación 12 fallida: {e}")

    logger.info("=== FIN DE SIMULACIÓN AUTOMÁTICA ===")


def menu_interactivo():
    """Despliega el menú en consola para ingresar y consultar datos manualmente."""
    logger = configurar_logger("sistema_fj.log")
    gestor = GestorSoftwareFJ(logger)

    while True:
        print("\n" + "=" * 50)
        print("   SISTEMA DE GESTIÓN - SOFTWARE FJ")
        print("=" * 50)
        print("1. Registrar nuevo cliente")
        print("2. Agregar nuevo servicio")
        print("3. Crear una reserva")
        print("4. Gestionar estado de reserva (Confirmar / Cancelar / Procesar)")
        print("5. Listar clientes, servicios y reservas actuales")
        print("6. Ejecutar simulación automática)")
        print("0. Salir")
        print("=" * 50)

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            print("\n--- REGISTRAR CLIENTE ---")
            try:
                doc = input("Documento de identidad: ")
                nombre = input("Nombre completo: ")
                correo = input("Correo electrónico: ")
                telefono = input("Teléfono (solo números): ")
                cliente = Cliente(doc, nombre, correo, telefono)
                gestor.registrar_cliente(cliente)
            except SoftwareFJError as e:
                logger.error(f"Error al registrar cliente: {e}")

        elif opcion == "2":
            print("\n--- AGREGAR SERVICIO ---")
            print("Tipos: [1] Reserva de Sala  |  [2] Alquiler de Equipo  |  [3] Asesoría Especializada")
            tipo = input("Elija el tipo de servicio (1-3): ").strip()
            try:
                codigo = input("Código del servicio (ej. SALA-02): ")
                nombre = input("Nombre del servicio: ")
                tarifa = float(input("Tarifa por hora ($): "))

                if tipo == "1":
                    capacidad = int(input("Capacidad de personas: "))
                    servicio = ReservaSala(codigo, nombre, tarifa, capacidad)
                elif tipo == "2":
                    stock = int(input("Cantidad en stock: "))
                    deposito = float(input("Valor del depósito ($): "))
                    servicio = AlquilerEquipo(codigo, nombre, tarifa, stock, deposito)
                elif tipo == "3":
                    especialidad = input("Área de especialidad: ")
                    servicio = AsesoriaEspecializada(codigo, nombre, tarifa, especialidad)
                else:
                    print("Tipo de servicio no válido.")
                    continue

                gestor.agregar_servicio(servicio)
            except ValueError as e:
                logger.error(f"Error de formato numérico al crear servicio: {e}")
            except SoftwareFJError as e:
                logger.error(f"Error al agregar servicio: {e}")

        elif opcion == "3":
            print("\n--- CREAR RESERVA ---")
            try:
                cod_res = input("Código de la reserva (ej. RES-010): ")
                doc_cli = input("Documento del cliente: ")
                cod_ser = input("Código del servicio: ")
                horas = float(input("Duración en horas: "))
                gestor.crear_reserva(cod_res, doc_cli, cod_ser, horas)
            except ValueError as e:
                logger.error(f"La duración debe ser un número válido: {e}")
            except SoftwareFJError as e:
                logger.error(f"Error al crear reserva: {e}")

        elif opcion == "4":
            print("\n--- GESTIONAR ESTADO DE RESERVA ---")
            cod_res = input("Ingrese el código de la reserva: ").strip()
            reserva = next((r for r in gestor.reservas if r.id == cod_res), None)
            if not reserva:
                logger.error(f"No se encontró la reserva '{cod_res}'.")
                continue

            print(f"Reserva encontrada -> {reserva.obtener_resumen()}")
            print("Acciones: [1] Confirmar  |  [2] Cancelar  |  [3] Procesar y cobrar")
            accion = input("Seleccione acción: ").strip()

            try:
                if accion == "1":
                    reserva.confirmar()
                    logger.info(f"Reserva {reserva.id} confirmada.")
                elif accion == "2":
                    reserva.cancelar()
                    logger.info(f"Reserva {reserva.id} cancelada.")
                elif accion == "3":
                    desc = float(input("Descuento en pesos (0 si no aplica): "))
                    urgencia = float(input("Recargo por urgencia en pesos (0 si no aplica): "))
                    total = reserva.calcular_total(porcentaje_iva=0.19, descuento=desc, recargo_urgencia=urgencia)
                    reserva.procesar()
                    logger.info(f"Reserva {reserva.id} procesada. Total cobrado (con IVA 19%): ${total:,.2f}")
                else:
                    print("Acción no válida.")
            except ValueError as e:
                logger.error(f"Valor numérico inválido: {e}")
            except SoftwareFJError as e:
                logger.error(f"Operación fallida en reserva {reserva.id}: {e}")

        elif opcion == "5":
            print("\n--- CLIENTES REGISTRADOS ---")
            for c in gestor.clientes:
                print(" •", c.obtener_resumen())
            if not gestor.clientes:
                print(" (Sin clientes)")

            print("\n--- SERVICIOS DISPONIBLES ---")
            for s in gestor.servicios:
                print(" •", s.describir())
            if not gestor.servicios:
                print(" (Sin servicios)")

            print("\n--- RESERVAS REGISTRADAS ---")
            for r in gestor.reservas:
                print(" •", r.obtener_resumen())
            if not gestor.reservas:
                print(" (Sin reservas)")

        elif opcion == "6":
            ejecutar_simulacion_automatica(gestor)

        elif opcion == "0":
            logger.info("Sistema finalizado por el usuario.")
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    menu_interactivo()