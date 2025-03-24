import uuid
from sqlalchemy.orm import Session
from app.repository import phone_repository
from app.model.phone import Phone
from app.model.db_models.phone import Phone as PhoneDB
from typing import List
from uuid import UUID, uuid4
from app.core.utils import generate_random_phone, generate_random_name

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

    def generate_phone_data(self, n: int):
        for _ in range(n):
            name = generate_random_name()
            phone_number = generate_random_phone()
            phone = PhoneDB(id=uuid.uuid4(), name=name, number=str(phone_number))
            self.db.add(phone)
        self.db.commit()

    def delete_all_phone_data(self):
        self.db.query(PhoneDB).delete()
        self.db.commit()