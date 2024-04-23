from fastapi import HTTPException, APIRouter
from db.db import collection
from model.usuario import Usuario

router = APIRouter()

@router.post('/', response_description="Crear un nuevo usuario", response_model=Usuario)
async def create_usuario(usuario : Usuario):
    existing_user = await collection.find_one({'email': usuario.email})
    if existing_user != None:
        raise HTTPException(status_code=404, detail=f'Email {usuario.email} ya existe.')
    result = await collection.insert_one(usuario.model_dump())
    usuario._id = str(result.inserted_id)
    return usuario

@router.get('/', response_description="Listar todos los usuarios", response_model=list[Usuario])
async def read_usuarios():
    usuarios = await collection.find().to_list(100)
    for u in usuarios:
        u['_id'] = str(u['_id'])
    return usuarios

@router.get('/{email}', response_description= 'Busca un usuario por su email', response_model=Usuario)
async def find_usuario_by_email(email: str):
    usuario = await collection.find_one({'email': email})
    if usuario:
        return usuario
    raise HTTPException(status_code=404, detail=f'Usuario con email {email} no encontrado.')

@router.put('/{email}', response_description='Actualiza un usuario, buscandolo por su email', response_model=Usuario)
async def update_usuario(email: str, usuario: Usuario):
    updated_usuario = await collection.find_one_and_update({'email': email}, {'$set': usuario.model_dump()})
    if updated_usuario:
        return Usuario(**updated_usuario)
    raise HTTPException(status_code=404, detail=f'Usuario con email {email} no encontrado.')

@router.delete('/{email}', response_description='Borra un usuario por su email', response_model=Usuario)
async def delete_usario(email: str):
    deleted_usuario = await collection.find_one_and_delete({'email': email})
    if deleted_usuario:
        return deleted_usuario
    raise HTTPException(status_code=404, detail=f'Usuario con email {email} no encontrado.')
