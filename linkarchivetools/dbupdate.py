from pathlib import Path
from sqlalchemy import (
    create_engine,
)

from linkarchive.models.definitions import create_tables


class DbUpdate():
    def __init__(self, db=None, engine=None):
        self.db=db
        self.engine=engine

    def create(self):
        path = Path(args.db)
        if not path.exists():
            path.touch()

        engine = create_engine(f"sqlite:///{args.db}")
        if engine:
            create_tables(engine)


def parse():
    parser = argparse.ArgumentParser(description="Data update program")
    parser.add_argument("--db", default="places.db", help="DB to be updated")

    parser.add_argument("--create", action="store_true", help="Creates missing table")

    parser.add_argument("-v", "--verbosity", help="Verbosity level")

    args = parser.parse_args()

    return parser, args


def main():
    parser, args = parse()

    if args.create:
        update = DbUpdate()
        update.create()
