from fastapi import HTTPException, status
from sqlmodel import select
from sqlalchemy.orm import selectinload
from app.db import SessionDep
from app.products.models import Product
from app.products.schemas import ProductCreate, ProductUpdate

class ProductService:
    no_task:str = "Product doesn't exits"
    # CREATE
    # ----------------------
    def create_product(self, item_data: ProductCreate, session: SessionDep):
        try:
            product_db = Product.model_validate(item_data.model_dump())
            session.add(product_db)
            session.commit()
            session.refresh(product_db)
            return product_db
        except Exception:
            session.rollback
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server error, create Product"
            )

    # GET ONE
    # ----------------------
    def get_product(self, item_id: int, session: SessionDep):
        statement = (
            select(Product)
            .where(Product.id == item_id)
            .options(selectinload(Product.category))  # Cargar la categoría
        )
        product_db = session.exec(statement).first()

        if not product_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=self.no_product
            )
        return product_db

    # UPDATE
    # ----------------------
    def update_product(self, item_id: int, item_data: ProductUpdate, session: SessionDep):
        product_db = session.get(Product, item_id)
        if not product_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=self.no_task
            )
        item_data_dict = item_data.model_dump(exclude_unset=True)
        product_db.sqlmodel_update(item_data_dict)
        session.add(product_db)
        session.commit()
        session.refresh(product_db)
        return product_db

    # GET ALL PLANS
    # ----------------------
    def get_products(self, session: SessionDep):
        statement = select(Product).options(selectinload(Product.category))  # Cargar categorías
        return session.exec(statement).all()

    # DELETE
    # ----------------------
    def delete_product(self, item_id: int, session: SessionDep):
        product_db = session.get(Product, item_id)
        if not product_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=self.no_task
            )
        session.delete(product_db)
        session.commit()
        
        return {"detail": "ok"}
