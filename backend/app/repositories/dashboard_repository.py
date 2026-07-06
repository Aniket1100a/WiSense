from datetime import datetime
from typing import Dict, List, Optional

from sqlalchemy import Date, cast, func, select
from sqlalchemy.orm import Session

from app.models.sensor import Sensor, SensorStatusEnum
from app.models.signalsample import SignalSample


class DashboardRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_device_status_counts(self) -> Dict[str, int]:
        stmt = select(Sensor.status, func.count()).group_by(Sensor.status)
        counts = {status.value: 0 for status in SensorStatusEnum}
        for status_value, count in self.session.execute(stmt):
            counts[status_value] = count
        return counts

    def get_active_rooms_count(self) -> int:
        stmt = select(func.count(func.distinct(Sensor.room_id))).where(
            Sensor.room_id != None,
            Sensor.is_active == True,
        )
        return self.session.scalar(stmt) or 0

    def get_provider_counts(self) -> List[Dict[str, int]]:
        stmt = select(Sensor.provider, func.count()).group_by(Sensor.provider)
        results = []
        for provider, count in self.session.execute(stmt):
            results.append({"provider": provider, "count": count})
        return results

    def get_avg_signal_rssi(self) -> Optional[float]:
        stmt = select(func.avg(SignalSample.rssi)).where(SignalSample.rssi != None)
        avg_value = self.session.scalar(stmt)
        return float(avg_value) if avg_value is not None else None

    def get_signal_history(self, days: int = 14) -> List[Dict[str, Optional[float]]]:
        date_column = cast(SignalSample.timestamp, Date)
        stmt = (
            select(
                date_column.label("day"),
                func.avg(SignalSample.rssi).label("avg_rssi"),
                func.count().label("count"),
            )
            .where(SignalSample.rssi != None)
            .group_by(date_column)
            .order_by(date_column.desc())
            .limit(days)
        )
        rows = self.session.execute(stmt).all()
        return [
            {
                "day": row[0].isoformat() if row[0] else None,
                "avg_rssi": float(row[1]) if row[1] is not None else None,
                "count": int(row[2]),
            }
            for row in rows
        ]

    def get_sensor_health_counts(self) -> Dict[str, int]:
        return self.get_device_status_counts()
