"""Activity query compiler: ActivityQueryPlan → parameterized SQL.

Pure function, no model anywhere near it. The plan is the entire surface
the model can influence; everything below this line is code — which is
the answer to "the model never writes SQL" made testable.
"""

from __future__ import annotations

from datetime import timedelta

from second_brain.domain.contracts import ActivityQueryPlan


def compile_activity_query(plan: ActivityQueryPlan) -> tuple[str, list[object]]:
    clauses: list[str] = []
    params: list[object] = []

    if plan.since is not None:
        clauses.append("created_at >= ?")
        params.append(plan.since.isoformat())
    if plan.until is not None:
        # Inclusive end date: strictly before the next day.
        clauses.append("created_at < ?")
        params.append((plan.until + timedelta(days=1)).isoformat())

    # tags/entities are stored as JSON arrays; a quoted-substring LIKE is
    # exact enough for controlled vocabularies. OR within a list, AND
    # between lists. Tags were lowercased at write time.
    for values, column, fold in ((plan.tags, "tags", True), (plan.entities, "entities", False)):
        if values:
            clauses.append("(" + " OR ".join([f"{column} LIKE ?"] * len(values)) + ")")
            params.extend(f'%"{v.strip().lower() if fold else v.strip()}"%' for v in values)

    if plan.types:
        placeholders = ", ".join(["?"] * len(plan.types))
        clauses.append(f"type IN ({placeholders})")
        params.extend(t.value for t in plan.types)

    where = " AND ".join(clauses) if clauses else "1=1"
    sql = f"SELECT id FROM notes WHERE {where} ORDER BY created_at DESC LIMIT ?"  # noqa: S608 — every value is bound
    params.append(plan.limit)
    return sql, params
