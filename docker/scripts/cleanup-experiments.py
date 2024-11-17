import os
from typing import List

from sqlalchemy import MetaData, Table, create_engine, delete, select
from sqlalchemy.orm import Session


def get_tables(engine):
    """Create Table objects with autoload for all required tables."""
    metadata = MetaData()

    return {
        "experiments": Table("experiments", metadata, autoload_with=engine),
        "experiment_tags": Table("experiment_tags", metadata, autoload_with=engine),
        "runs": Table("runs", metadata, autoload_with=engine),
        "latest_metrics": Table("latest_metrics", metadata, autoload_with=engine),
        "metrics": Table("metrics", metadata, autoload_with=engine),
        "tags": Table("tags", metadata, autoload_with=engine),
        "params": Table("params", metadata, autoload_with=engine),
    }


def get_deleted_experiment_ids(session: Session, tables: dict) -> List[int]:
    """Get IDs of experiments marked as deleted."""
    query = select(tables["experiments"].c.experiment_id).where(tables["experiments"].c.lifecycle_stage == "deleted")
    return [row[0] for row in session.execute(query)]


def get_affected_run_uuids(session: Session, tables: dict, experiment_ids: List[int]) -> List[str]:
    """Get run UUIDs associated with given experiment IDs."""
    query = select(tables["runs"].c.run_uuid).where(tables["runs"].c.experiment_id.in_(experiment_ids))
    return [row[0] for row in session.execute(query)]


def delete_related_records(session: Session, tables: dict, experiment_ids: List[int], run_uuids: List[str]) -> None:
    """Delete all related records in dependent tables."""
    deletions = [
        delete(tables["experiment_tags"]).where(tables["experiment_tags"].c.experiment_id.in_(experiment_ids)),
        delete(tables["latest_metrics"]).where(tables["latest_metrics"].c.run_uuid.in_(run_uuids)),
        delete(tables["metrics"]).where(tables["metrics"].c.run_uuid.in_(run_uuids)),
        delete(tables["tags"]).where(tables["tags"].c.run_uuid.in_(run_uuids)),
        delete(tables["params"]).where(tables["params"].c.run_uuid.in_(run_uuids)),
        delete(tables["runs"]).where(tables["runs"].c.experiment_id.in_(experiment_ids)),
        delete(tables["experiments"]).where(tables["experiments"].c.lifecycle_stage == "deleted"),
    ]

    for deletion in deletions:
        session.execute(deletion)


def clean_deleted_experiments(db_url: str) -> None:
    """Clean deleted experiments and related records."""
    engine = create_engine(db_url)
    tables = get_tables(engine)

    with Session(engine) as session:
        experiment_ids = get_deleted_experiment_ids(session, tables)
        run_uuids = get_affected_run_uuids(session, tables, experiment_ids)
        delete_related_records(session, tables, experiment_ids, run_uuids)
        session.commit()


if __name__ == "__main__":
    database_url = os.environ["POSTGRES_URL"]
    clean_deleted_experiments(database_url)
