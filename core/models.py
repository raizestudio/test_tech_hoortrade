from enum import Enum


class DataSource(Enum):
    ADMIN = "admin"
    CMD = "cmd"
    API = "api"
    TMDB = "tmdb"

    @classmethod
    def choices(cls):
        return [(tag.name, tag.value) for tag in cls]
