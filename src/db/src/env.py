import typing as t
import importlib

from logging.config import fileConfig
from plug_in import Hosted

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.sql.schema import SchemaItem, MetaData

from db.src.config.ioc import configure_ioc
from db.src.custom.ioc import ioc_router
from db.src.custom.settings import AlembicSettings

configure_ioc()


@ioc_router.manage()
def deployment_only_mode(settings: AlembicSettings = Hosted()) -> bool:
    return settings.DEPLOYMENT_ONLY


@ioc_router.manage()
def get_db_url_for_alembic(settings: AlembicSettings = Hosted()) -> str:
    return settings.get_db_url()


@ioc_router.manage()
def get_target_metadata(settings: AlembicSettings = Hosted()) -> MetaData:
    meta_module = importlib.import_module(settings.META_PATH)
    return getattr(meta_module, settings.META_NAME)


# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option("sqlalchemy.url", get_db_url_for_alembic())

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

if not deployment_only_mode():
    target_metadata = get_target_metadata()
else:
    target_metadata = MetaData()


@ioc_router.manage()
def include_name(
    name: str | None,
    type_: t.Literal[
        "schema",
        "table",
        "column",
        "index",
        "unique_constraint",
        "foreign_key_constraint",
    ],
    parent_names: t.MutableMapping[
        t.Literal[
            "schema_name",
            "table_name",
            "schema_qualified_table_name",
        ],
        str | None,
    ],
    settings: AlembicSettings = Hosted(),
) -> bool:
    if type_ == "schema":
        return name in [settings.SCHEMA_NAME]
    else:
        return True


@ioc_router.manage()
def include_object(
    object_: SchemaItem,
    name: str | None,
    type_: t.Literal[
        "schema",
        "table",
        "column",
        "index",
        "unique_constraint",
        "foreign_key_constraint",
    ],
    reflected: bool,
    compare_to: SchemaItem | None,
    settings: AlembicSettings = Hosted(),
) -> bool:
    if type_ == "table" and object_.schema != settings.SCHEMA_NAME:  # type: ignore
        return False
    else:
        return True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            include_schemas=True,
            # include_name=include_name,
            include_object=include_object,
            # version_table_schema=os.getenv("SCHEMA_NAME"),
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
