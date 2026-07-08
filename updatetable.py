from sqlalchemy import create_engine

from linkarchivetools.model.definitions import create_tables


def main():
    file_name = "example/db.db"
    engine = create_engine(f"sqlite:///{file_name}")
    create_tables(engine)

main()
