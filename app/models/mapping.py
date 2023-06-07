from sqlalchemy import Column, String

from app.models.base import Base,db


# 单纯存储key，value信息
class Mapping(Base):
    __tablename__ = 'mapping'

    key = Column(String(300), primary_key=True)
    value = Column(String(100))


    @property
    def id(self):
        return self.key

    @classmethod
    def delete_by_id(cls, id_):
        with db.auto_commit():
            cls.query.filter_by(key=id_).delete()

    @classmethod
    def get_by_id(cls, id_):
        res = cls.query.get(id_)
        return res if res else None

    @classmethod
    def set_token(cls, key, value:bool = True):
        val = 'true' if value else 'false'
        cls.create(key=key, value=val)
