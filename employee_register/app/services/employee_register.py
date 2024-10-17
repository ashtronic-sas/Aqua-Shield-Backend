from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.employee_register import EmployeeRegister, Employee, EmployeePlace
from app.schemas.employee_register import EmployeeRegisterCreate, EmployeeRegisterUpdate
from app.shared.utils import calculate_hours_worked
from datetime import datetime

# Registrar una nueva entrada
def create_employee_register(db: Session, employee_register: EmployeeRegisterCreate):
    db_employee_register = EmployeeRegister(**employee_register.dict())
    db.add(db_employee_register)
    db.commit()
    db.refresh(db_employee_register)
    return db_employee_register

# Actualizar el registro con la salida y calcular horas trabajadas
def update_employee_register(db: Session, register_id: int, update_data: EmployeeRegisterUpdate):
    db_register = db.query(EmployeeRegister).filter(EmployeeRegister.id == register_id).first()
    if not db_register:
        raise HTTPException(status_code=404, detail="EmployeeRegister not found")

    if update_data.exit_time:
        db_register.exit_time = update_data.exit_time
        db_register.hours_worked = calculate_hours_worked(db_register.entry_time, db_register.exit_time)

    db.commit()
    db.refresh(db_register)
    return db_register

# Obtener registros por empleado
def get_registers_by_employee(db: Session, employee_id: int):
    print("se entro aquí")
    return db.query(EmployeeRegister).filter(EmployeeRegister.employee_id == employee_id).all()

# Obtener registros por sede
def get_registers_by_place(db: Session, place_id: int):
    return db.query(EmployeeRegister).filter(EmployeeRegister.place_id == place_id).all()

# Obtener registros por cedula
def get_registers_by_cedula(db: Session, cedula_employee: str):
    return db.query(EmployeeRegister).filter(EmployeeRegister.cedula_employee == cedula_employee).all()

# Eliminar un registro
def delete_employee_register(db: Session, register_id: int):
    db_register = db.query(EmployeeRegister).filter(EmployeeRegister.id == register_id).first()
    if not db_register:
        raise HTTPException(status_code=404, detail="EmployeeRegister not found")
    
    db.delete(db_register)
    db.commit()

def parse_timestamp(time: str) -> str:
    # Convertir el timestamp a segundos si está en milisegundos
    timestamp_seconds = int(time) / 1000

    # Convertir a un objeto datetime
    date_time = datetime.fromtimestamp(timestamp_seconds)

    # Formatear la fecha y hora
    formatted_date_time = date_time.strftime('%Y-%m-%d %H:%M:%S')

    return formatted_date_time

def parse_parameters(db: Session,url_params):

    try:
        # Divide la cadena en pares clave-valor
        parameters = url_params.split('&')

        # Crea un diccionario con los pares clave-valor
        parameters_dict = {}

        for param in parameters:
            # Divide cada parámetro en clave y valor
            key_value = param.split('=')
            if len(key_value) == 2:
                key, value = key_value
                # Agrega la clave y el valor al diccionario
                parameters_dict[key] = value
            else:
                print(f"El parámetro '{param}' no tiene un valor asignado.")
        

        cedula = parameters_dict["personId"]
        id_employee = db.query(Employee).filter(Employee.document == cedula).first()

        datetime=parse_timestamp(parameters_dict["time"])
        

        print("employee_id:",id_employee.id)
        print("Entry_time:",datetime)
        print("cedula_employee:",cedula)
        print("photo_employee:",parameters_dict["imgBase64"])

        db_employee_register = EmployeeRegister(employee_id=id_employee.id, cedula_employee=cedula, photo_employee=parameters_dict["imgBase64"], entry_time=datetime)
        db.add(db_employee_register)
        db.commit()
        db.refresh(db_employee_register)
        

        #db_employee_register = (employee_id=employee_place.employee_id, place_id=employee_place.place_id, entry_time=datetime)
        #db.add(db_employee_register)
        #db.commit()
        #db.refresh(db_employee_register)
        

        #print("name:", parameters_dict["name"])
        #print("personId:", parameters_dict["personId"])
        #print("time:", parameters_dict["time"])

        #for key, value in parameters_dict.items():
        #    print(f"{key}: {value}")

    except Exception as e:
        print(f"Se produjo un error al analizar los parámetros: {e}")

""" Parámetros: 98717046
firstUpload: true
personId: 98717046
name: Jonathan
openDoor: 1
deviceKey: DC6294098CE0
type: face_0
ip: 192.168.78.171
time: 1728906481128
imgType: 1
imgBase64: """