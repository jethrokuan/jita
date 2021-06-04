from sqlalchemy import *

engine = create_engine('sqlite:///jita.db')

metadata = MetaData()

songs_table = Table('songs', metadata,
                    Column('id', String(60), primary_key=True),
                    Column('artist', String(16), nullable=False),
                    Column('title', String(60), nullable=False),
                    Column('hashes', Integer, nullable=False),
)

fingerprints_table = Table('fingerprints', metadata,
                           Column('hash', String(60)),
                           Column('song_id', String(60), ForeignKey("songs.id"), nullable=False),
                           Column('offset', Integer, nullable=False),
)

tabs_table = Table('tabs', metadata,
                   Column('song_id', String(60), ForeignKey("songs.id"), nullable=False),
                   Column('tab', Text),
                   Column('difficulty', String(60), nullable=True),
                   Column('tuning', String(60)),
                   Column('tuning_value', String(60)),
                   Column('capo', Integer, nullable=True))

Index('fingerprints_hash', fingerprints_table.c.hash)
Index('fingerprints_song_id', fingerprints_table.c.song_id)
Index('tabs_song_id', tabs_table.c.song_id)

metadata.create_all(engine, checkfirst=True)
