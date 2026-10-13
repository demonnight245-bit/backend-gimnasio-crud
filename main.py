from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

# Inicialización de la aplicación FastAPI
app = FastAPI(
    title="Rabanitos Gym - ADSO",
    description="API RESTful completa con operaciones CRUD para auditoría de servicios web",
    version="2.0.0"
)

# Modelo de Datos con Pydantic para validación automática
class Membresia(BaseModel):
    id: int
    codigo_usuario: str
    tipo_plan: str
    valor_pagado: float
    estado_activo: bool = True

# Modelo auxiliar para la actualización parcial o total
class MembresiaUpdate(BaseModel):
    codigo_usuario: str
    tipo_plan: str
    valor_pagado: int
    estado_activo: bool

# Base de datos simulada en memoria
db_membresia: List[Membresia] = [
    Membresia(id=1, codigo_usuario="1021393520", tipo_plan="Mensual", valor_pagado=55000.00, estado_activo=True),
    Membresia(id=2, codigo_usuario="1028482163", tipo_plan="Anual", valor_pagado=600000.00, estado_activo=True),
    Membresia(id=3, codigo_usuario="1000595136", tipo_plan="Mensual", valor_pagado=55000.00, estado_activo=False)
]

# -------------------------------------------------------------
# ENDPOINTS / RUTAS DE LA API (CRUD COMPLETO)
# -------------------------------------------------------------

# 1. READ ALL (Obtener todos los Membresias)
@app.get("/api/v1/membresias", response_model=List[Membresia], status_code=status.HTTP_200_OK)
def obtener_todas_las_Membresias():
    return db_membresia

# 2. READ ONE (Obtener un Membresia específico por ID)
@app.get("/api/v1/membresias/{membresia_id}", response_model=Membresia, status_code=status.HTTP_200_OK)
def obtener_membresia_por_id(membresia_id: int):
    for membresia in db_membresia:
        if membresia.id == membresia_id:
            return membresia
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"El Membresia con ID {membresia_id} no existe en el sistema de Rabanitos Gym."
    )

# 3. CREATE (Registrar un nuevo Membresia)
@app.post("/api/v1/membresias", response_model=Membresia, status_code=status.HTTP_201_CREATED)
def crear_nueva_membresia(membresia: Membresia):
    # Validar si el ID ya existe
    for m in db_membresia:
        if m.id == membresia.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error de registro: Ya existe un Membresia con el ID {membresia.id}."
            )
    db_membresia.append(membresia)
    return membresia

# 4. UPDATE (Actualizar un Membresia existente - Método PUT)
@app.put("/api/v1/membresias/{membresia_id}", response_model=Membresia, status_code=status.HTTP_200_OK)
def actualizar_membresia(membresia_id: int, datos_actualizados: MembresiaUpdate):
    for index, membresia in enumerate(db_membresia):
        if membresia.id == membresia_id:
            membresia_modificada = Membresia(
                id=membresia_id,
                codigo_usuario=datos_actualizados.codigo_usuario,
                tipo_plan=datos_actualizados.tipo_plan,
                valor_pagado=datos_actualizados.valor_pagado,
                estado_activo=datos_actualizados.estado_activo
            )
            db_membresia[index] = membresia_modificada
            return membresia_modificada

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No es posible actualizar. El Membresia con ID {membresia_id} no fue encontrado."
    )

# 5. DELETE (Eliminar un Membresia de la biblioteca)
@app.delete("/api/v1/membresias/{membresia_id}", status_code=status.HTTP_200_OK)
def eliminar_membresia(membresia_id: int):
    for index, membresia in enumerate(db_membresia):
        if membresia.id == membresia_id:
            db_membresia.pop(index)
            return {"mensaje": f"El Membresia con ID {membresia_id} fue eliminado exitosamente."}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No es posible eliminar. El Membresia con ID {membresia_id} no existe."
    )