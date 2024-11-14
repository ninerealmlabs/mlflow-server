# %%
import os

import sqlalchemy

# %%
DB = os.getenv(...)

# %% [markdown]
# ```sql
# /*
# Clean up deleted experiments & associated data/metadata

# -- Database: dtsc-mlflow
# */

# DELETE FROM experiment_tags WHERE experiment_id in (
#     SELECT experiment_id FROM experiments where lifecycle_stage='deleted'
#     )
# DELETE FROM latest_metrics WHERE run_uuid in (
#     SELECT run_uuid FROM runs WHERE experiment_id in (
#         SELECT experiment_id FROM experiments where lifecycle_stage='deleted'
#     )
# )
# DELETE FROM metrics WHERE run_uuid in (
#     SELECT run_uuid FROM runs WHERE experiment_id in (
#         SELECT experiment_id FROM experiments where lifecycle_stage='deleted'
#     )
# )
# DELETE FROM params WHERE run_uuid in (
#     SELECT run_uuid FROM runs where experiment_id in (
#         SELECT experiment_id FROM experiments where lifecycle_stage='deleted'
#     )
# )
# DELETE FROM tags WHERE run_uuid in (
#     SELECT run_uuid FROM runs WHERE experiment_id in (
#         SELECT experiment_id FROM experiments where lifecycle_stage='deleted'
#     )
# )

# -- needed for latest_metrics, metrics, params, tags; delete 2nd to last
# DELETE FROM runs WHERE experiment_id in (
#     SELECT experiment_id FROM experiments where lifecycle_stage='deleted'
# )

# -- needed for subqueries; delete last
# DELETE FROM experiments where lifecycle_stage='deleted'
# ```
