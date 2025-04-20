from datetime import date, timedelta

from dateutil.relativedelta import relativedelta


def validate_dates(start_date: date, end_date: date):
    """
    start_date から数えて「1か月後の前日」までを有効とする。

    >>> validate_dates(date(2024, 3, 20), date(2024, 4, 19))  # OK
    >>> validate_dates(date(2024, 3, 20), date(2024, 4, 20))  # NG
    Traceback (most recent call last):
        ...
    ValueError: 開始日から1ヶ月後の前日までに終了日を設定してください。
    """
    limit_date = start_date + relativedelta(months=1) - timedelta(days=1)
    if end_date > limit_date:
        raise ValueError("開始日と終了日の間隔は1ヶ月未満にしてください。")


def validate_greater_equal(value: int, threshold: int) -> int:
    """
    value が threshold 以上であることを検証する。
    条件を満たさない場合は ValueError を投げる。
    """
    if value < threshold:
        raise ValueError(f"{threshold} 以上である必要があります")
    return value
