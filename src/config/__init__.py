# <ID:CONFIG-INIT>
"""
HR Analytics Dashboard - Config Package
Schema definitions and configuration modules
"""

from .schema import validate_employee_data, map_dataframe_to_records, EmployeeRecord

__all__ = [
    'validate_employee_data',
    'map_dataframe_to_records', 
    'EmployeeRecord'
] 