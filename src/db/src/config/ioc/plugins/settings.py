from db.src.custom.settings import AlembicSettings


def settings_provider() -> AlembicSettings:
    # Populated via .env
    return AlembicSettings()  # type: ignore
