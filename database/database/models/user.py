from database.database import Base
from database.database.mixins import TimestampMixin
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Boolean


class User(Base, TimestampMixin):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    password = Column(Unicode(255), nullable=False)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    full_name = Column(String, nullable=True, unique=False)
    is_admin = Column(Boolean, default=False)
    credits = Column(Float, default=400)

    referral = relationship("Referral", back_populates="user")


class Referral(Base, TimestampMixin):
    __tablename__ = "referral"

    referral_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    count_referral = Column(BigInteger, nullable=False, default=0)
    user_id = Column(BigInteger, ForeignKey('users.id'))

    user = relationship("User", back_populates="referral")


