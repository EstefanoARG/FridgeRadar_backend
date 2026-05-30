from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.estante import EstanteCreate, EstanteResponse, EstanteUpdate
from app.services.estante_service import EstanteService

router = APIRouter()


@router.get("/", response_model=list[EstanteResponse])
async def listar_estantes(
    id_zona: int | None = Query(None, description="Filtrar por zona"),
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = EstanteService(db)
    return await service.listar(id_zona=id_zona)


@router.post("/", response_model=EstanteResponse, status_code=status.HTTP_201_CREATED)
async def crear_estante(
    data: EstanteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = EstanteService(db)
    return await service.crear(data)


@router.get("/{id_estante}", response_model=EstanteResponse)
async def obtener_estante(
    id_estante: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = EstanteService(db)
    return await service.obtener(id_estante)


@router.patch("/{id_estante}", response_model=EstanteResponse)
async def actualizar_estante(
    id_estante: int,
    data: EstanteUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = EstanteService(db)
    return await service.actualizar(id_estante=id_estante, data=data)


@router.delete("/{id_estante}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_estante(
    id_estante: int,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    service = EstanteService(db)
    await service.eliminar(id_estante=id_estante)
