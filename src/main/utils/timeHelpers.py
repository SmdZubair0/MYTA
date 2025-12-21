from datetime import date

def dates_overlap(start1, start2, end1 = None, end2 = None) -> bool:
    end1 = end1 or date.today()
    end2 = end2 or date.today()
    return start1 <= end2 and start2 <= end1

def parse_year_month(value: str | None) -> date | None:
    if not value:
        return None
    year, month = map(int, value.split("-"))
    return date(year, month, 1)
