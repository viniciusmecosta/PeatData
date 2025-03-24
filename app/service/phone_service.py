# app/service/phone_service.py
from sqlalchemy.orm import Session
from app.repository import phone_repository
from app.model.phone import Phone
from typing import List
from uuid import UUID, uuid4

class PhoneService:
    """Serviço para operações relacionadas a telefones."""
    def __init__(self, db: Session):
        """Inicializa o serviço com uma sessão do banco de dados."""
        self.db = db

    def add_phone(self, name: str, number: str):
        """Adiciona um novo telefone."""
        phone_data = Phone(id=uuid4(), name=name, number=number)
        return phone_repository.create_phone(self.db, phone_data)

    def get_phone(self, phone_id: UUID):
        """Obtém um telefone pelo ID."""
        return phone_repository.get_phone(self.db, phone_id)

    def update_phone(self, phone_id: UUID, phone: Phone):
        """Atualiza um telefone existente."""
        return phone_repository.update_phone(self.db, phone_id, phone)

    def delete_phone(self, phone_id: UUID):
        """Exclui um telefone pelo ID."""
        return phone_repository.delete_phone(self.db, phone_id)

    def get_all_phones(self) -> List[Phone]:
        """Obtém todos os telefones."""
        return phone_repository.get_all_phones(self.db)