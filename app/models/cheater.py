from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Cheater(Base):
    __tablename__ = 'cheater'

    id = Column(Integer, primary_key=True)
    added_at = Column(DateTime, default=datetime.utcnow)
    added_by = Column(String, nullable=False)
    steamId = Column(String, nullable=False)
    name = Column(String, nullable=False)
    nbr_VAC = Column(Integer, nullable=False)
    nbr_game_bans = Column(Integer, nullable=False)
    nbr_community_bans = Column(Integer, nullable=False)
    days_since_last_ban = Column(Integer, nullable=False)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Cheater(id={self.id}, added_at={self.added_at}, added_by={self.added_by}, id_steam={self.id_steam}, name={self.name}, nbr_VAC={self.nbr_VAC}, nbr_game_bans={self.nbr_game_bans}, nbr_community_bans={self.nbr_community_bans}, days_since_last_ban={self.days_since_last_ban})>'