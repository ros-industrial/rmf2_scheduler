from __future__ import annotations

import typing

import rmf2_scheduler._core.cache
import rmf2_scheduler._core.data

__all__ = ['ScheduleStream']
class ScheduleStream:
    """
    
        Stream for the schedule
        
    """
    @staticmethod
    def create_default(arg0: str) -> ScheduleStream:
        ...
    @staticmethod
    def create_simple(arg0: int, arg1: str) -> ScheduleStream:
        ...
    def read_schedule(self, arg0: rmf2_scheduler._core.cache.ScheduleCache, arg1: rmf2_scheduler._core.data.TimeWindow) -> tuple:
        ...
    @typing.overload
    def write_schedule(self, arg0: rmf2_scheduler._core.cache.ScheduleCache, arg1: rmf2_scheduler._core.data.TimeWindow) -> tuple:
        ...
    @typing.overload
    def write_schedule(self, arg0: rmf2_scheduler._core.cache.ScheduleCache, arg1: list[rmf2_scheduler._core.data.ScheduleChangeRecord]) -> tuple:
        ...
