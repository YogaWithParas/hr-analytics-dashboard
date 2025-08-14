# <ID:MODULES-INIT>
"""
HR Analytics Dashboard - Modules Package
Data processing, KPI calculations, and visualization modules
"""

from .data_cleaning import run_cleaning_pipeline, load_attrition_data
from .kpi_calculations import calculate_comprehensive_kpis, perform_statistical_tests
from .visual_helpers import create_comprehensive_dashboard

__all__ = [
    'run_cleaning_pipeline',
    'load_attrition_data', 
    'calculate_comprehensive_kpis',
    'perform_statistical_tests',
    'create_comprehensive_dashboard'
] 