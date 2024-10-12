from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.employee_register import EmployeeRegisterCreate, EmployeeRegisterUpdate, EmployeeRegisterResponse
from app.services.employee_register import create_employee_register, update_employee_register, get_registers_by_employee, get_registers_by_place, delete_employee_register
from app.shared.utils import verify_token

router = APIRouter(prefix="/employee_register", tags=["employee_register"])


# Registrar una nueva entrada de un empleado
@router.post("/", response_model=EmployeeRegisterResponse,dependencies=[Depends(verify_token)])
def register_employee_entry(employee_register: EmployeeRegisterCreate, db: Session = Depends(get_db)):
    return create_employee_register(db, employee_register)

# Actualizar el registro con la salida del empleado y calcular horas trabajadas
@router.put("/{id}", response_model=EmployeeRegisterResponse,dependencies=[Depends(verify_token)])
def update_employee(id: int, employee_register_update: EmployeeRegisterUpdate, db: Session = Depends(get_db)):
    return update_employee_register(db, id, employee_register_update)

# Obtener historial de asistencia de un empleado
@router.get("/{id}", response_model=list[EmployeeRegisterResponse],dependencies=[Depends(verify_token)])
def get_employee_registers(employee_id: int, db: Session = Depends(get_db)):
    return get_registers_by_employee(db, employee_id)

# Obtener registros de asistencia en una sede
@router.get("/{place_id}", response_model=list[EmployeeRegisterResponse],dependencies=[Depends(verify_token)])
def get_place_registers(place_id: int, db: Session = Depends(get_db)):
    return get_registers_by_place(db, place_id)

# Eliminar un registro de asistencia
@router.delete("/{id}",dependencies=[Depends(verify_token)])
def delete_register(id: int, db: Session = Depends(get_db)):
    delete_employee_register(db, id)
    return {"message": "EmployeeRegister deleted successfully"}

@router.post("/register-record", response_description="register-record")
async def register_record(request: Request):
    print("register-record")
    try:
        # Create a JSONResponse object to send as a response
        response = JSONResponse(
                status_code=200,
                content={"success": 'true', "result": 1},
            )
        # Get the request body data as bytes
        databyte = await request.body()
        # Decode the bytes data as a string
        strRecord = databyte.decode("UTF-8")
        # Enviar el callback a procesar en segundo plano
        #background_tasks.add_task(save_attendance,databyte)
        #await save_attendance(strRecord)
        print(strRecord)
        return response
    # If any errors occur during the process, catch them and return a JSONResponse with an error message
    except Exception as e:
        response = JSONResponse(
            status_code=500,
            content={"success": 'false', "message": str(e)},
        )
        return response