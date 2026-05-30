from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.estante import Estante
from app.schemas.estante import EstanteCreate, EstanteResponse, EstanteUpdate


class EstanteService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def crear(self, data: EstanteCreate) -> EstanteResponse:
        estante = Estante(
            id_zona=data.id_zona,
            nombre=data.nombre,
            posicion_vertical=data.posicion_vertical,
            color_ui=data.color_ui,
        )
        self.db.add(estante)
        await self.db.flush()
        await self.db.refresh(estante)
        return EstanteResponse.model_validate(estante)

    async def listar(self, id_zona: int | None = None) -> list[EstanteResponse]:
        stmt = select(Estante)
        if id_zona is not None:
            stmt = stmt.where(Estante.id_zona == id_zona)
        stmt = stmt.order_by(Estante.posicion_vertical)
        result = await self.db.execute(stmt)
        estantes = result.scalars().all()
        return [EstanteResponse.model_validate(e) for e in estantes]

    async def obtener(self, id_estante: int) -> EstanteResponse:
        estante = await self.db.get(Estante, id_estante)
        if not estante:
            raise NotFoundError("Estante no encontrado")
        return EstanteResponse.model_validate(estante)

    async def actualizar(self, id_estante: int, data: EstanteUpdate) -> EstanteResponse:
        estante = await self.db.get(Estante, id_estante)
        if not estante:
            raise NotFoundError("Estante no encontrado")
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                setattr(estante, key, value)
        await self.db.flush()
        await self.db.refresh(estante)
        return EstanteResponse.model_validate(estante)

    async def eliminar(self, id_estante: int) -> None:
        estante = await self.db.get(Estante, id_estante)
        if not estante:
            raise NotFoundError("Estante no encontrado")
        await self.db.delete(estante)
        await self.db.flush()
