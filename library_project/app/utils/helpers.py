from datetime import datetime


def format_datetime(dt: datetime) -> str:
    if dt is None:
        return None
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def paginate(query, skip: int = 0, limit: int = 10):
    return query.offset(skip).limit(limit).all()
