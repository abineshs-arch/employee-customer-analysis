def clean_names(names: list) -> list:
    return list(map(lambda s: s.strip().title(), names))


def active_records(records: list) -> list:
    stayed = ("No", "no", 0, "0", False)
    return list(filter(lambda r: r.get("status") in stayed, records))


def high_salary(records: list, limit: int = 10000) -> list:
    return [r for r in records if r["salary"] > limit]


def sort_by_salary(records: list) -> list:
    return sorted(records, key=lambda r: r["salary"], reverse=True)


def total_by(records: list, *columns: str) -> dict:
    return {c: sum(r[c] for r in records) for c in columns}


def filter_records(records: list, **kwargs) -> list:
    result = []
    for r in records:
        if all(r.get(k) == v for k, v in kwargs.items()):
            result.append(r)
    return result


def count_until(records: list, target: int) -> int:
    i = 0
    total = 0
    while i < len(records):
        total += records[i]["salary"]
        if total >= target:
            break
        i += 1
    return i


def first_valid(records: list, min_salary: int = 0):
    for r in records:
        if r["salary"] is None:
            continue
        if r["salary"] >= min_salary:
            return r
    return None


def unique_roles(records: list) -> set:
    return {r["designation"] for r in records}


def salary_range(records: list) -> tuple:
    values = [r["salary"] for r in records]
    return (min(values), max(values))