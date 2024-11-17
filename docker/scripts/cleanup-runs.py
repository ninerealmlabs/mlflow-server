import os
from typing import List

from sqlalchemy import MetaData, Table, create_engine, delete, select
from sqlalchemy.orm import Session


def get_tables(engine):
    """Create Table objects with autoload for all required tables."""
    metadata = MetaData()

    return {
        "runs": Table("runs", metadata, autoload_with=engine),
        "latest_metrics": Table("latest_metrics", metadata, autoload_with=engine),
        "metrics": Table("metrics", metadata, autoload_with=engine),
        "tags": Table("tags", metadata, autoload_with=engine),
        "params": Table("params", metadata, autoload_with=engine),
    }


def get_deleted_run_uuids(session: Session, tables: dict) -> List[int]:
    """Get IDs of runs marked as deleted."""
    query = select(tables["runs"].c.run_uuid).where(tables["runs"].c.lifecycle_stage == "deleted")
    return [row[0] for row in session.execute(query)]


def delete_related_records(session: Session, tables: dict, run_uuids: List[str]) -> None:
    """Delete all related records in dependent tables."""
    deletions = [
        delete(tables["latest_metrics"]).where(tables["latest_metrics"].c.run_uuid.in_(run_uuids)),
        delete(tables["metrics"]).where(tables["metrics"].c.run_uuid.in_(run_uuids)),
        delete(tables["tags"]).where(tables["tags"].c.run_uuid.in_(run_uuids)),
        delete(tables["params"]).where(tables["params"].c.run_uuid.in_(run_uuids)),
        delete(tables["runs"]).where(tables["runs"].c.lifecycle_stage == "deleted"),
    ]

    for deletion in deletions:
        session.execute(deletion)


def clean_deleted_runs(db_url: str) -> None:
    """Clean deleted experiments and related records."""
    engine = create_engine(db_url)
    tables = get_tables(engine)

    with Session(engine) as session:
        run_uuids = get_deleted_run_uuids(session, tables)
        delete_related_records(session, tables, run_uuids)
        session.commit()


if __name__ == "__main__":
    database_url = os.environ["POSTGRES_URL"]
    clean_deleted_runs(database_url)
