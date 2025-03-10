
from fastapi import APIRouter, status

from app.db import SessionDep
from app.products_brand.models import ProductBrand
from app.products_brand.schemas import ProductBrandCreate, ProductBrandUpdate
from app.products_brand.service import ProductBrandService

router = APIRouter()
service = ProductBrandService()


# CREATE - Crear una nueva marca
# ----------------------
@router.post("/", response_model=ProductBrand, status_code=status.HTTP_201_CREATED)
async def create_product_brand(
    product_brand_data: ProductBrandCreate,
    session: SessionDep
    ):
    return service.create_product_brand(product_brand_data, session)
# GET ONE - Obtener una marca por ID
# ----------------------
@router.get("/{product_brand_id}", response_model=ProductBrand)
async def get_product_brand(
    product_brand_id: int,
    session: SessionDep
):
    return service.get_product_brand(product_brand_id,session)

# UPDATE - Actualizar una marca existente
# ----------------------
@router.patch("/{product_brand_id}", response_model=ProductBrand, status_code=status.HTTP_201_CREATED)
async def update_product_brand(
    product_brand_id: int,
    product_brand_data: ProductBrandUpdate,
    session: SessionDep
):
    
    return service.update_product_brand(product_brand_id, product_brand_data, session)

# GET ALL BRAND - Obtener todas las marcas
# ----------------------
@router.get("/", response_model=list[ProductBrand])
async def get_product_brands(
    session: SessionDep
):
    return service.get_product_brands(session)

# DELETE - Eliminar una marca
# ----------------------
@router.delete("/{product_brand_id}")
async def delete_product_brand(
    product_brand_id: int,
    session: SessionDep,
):
    return service.delete_product_brand(product_brand_id, session)