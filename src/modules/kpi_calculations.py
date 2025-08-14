# <ID:KPI-ATTRITION-MODELING>
"""
KPI Calculations Module for HR Analytics Dashboard
Implements FP&A-aligned HR metrics and analytics for strategic decision making
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
import logging
import sys
import os
from scipy import stats

# Add parent directory to path for imports
current_dir = os.path.dirname(__file__)
project_root = os.path.join(current_dir, '..', '..')
sys.path.insert(0, project_root)

# <ID:KPI-LOGGING>
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# <ID:KPI-ATTRITION-RATE>
def calculate_attrition_rate(df: pd.DataFrame) -> Dict[str, float]:
    """Calculate overall and segmented attrition rates"""
    
    # Overall attrition rate
    overall_rate = (df['Attrition'] == 'Yes').mean() * 100
    
    # Attrition by department
    dept_attrition = df.groupby('Department')['Attrition'].apply(
        lambda x: (x == 'Yes').mean() * 100
    ).to_dict()
    
    # Attrition by job role
    role_attrition = df.groupby('JobRole')['Attrition'].apply(
        lambda x: (x == 'Yes').mean() * 100
    ).to_dict()
    
    # Attrition by gender
    gender_attrition = df.groupby('Gender')['Attrition'].apply(
        lambda x: (x == 'Yes').mean() * 100
    ).to_dict()
    
    return {
        'overall_rate': overall_rate,
        'by_department': dept_attrition,
        'by_job_role': role_attrition,
        'by_gender': gender_attrition
    }

# <ID:KPI-SALARY-ANALYSIS>
def calculate_salary_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate salary-related KPIs"""
    
    # Average monthly income by job role
    avg_salary_by_role = df.groupby('JobRole')['MonthlyIncome'].agg([
        'mean', 'median', 'std', 'count'
    ]).round(2).to_dict('index')
    
    # Salary distribution by department
    dept_salary_stats = df.groupby('Department')['MonthlyIncome'].agg([
        'mean', 'median', 'min', 'max'
    ]).round(2).to_dict('index')
    
    # Salary vs performance correlation
    salary_perf_corr = df['MonthlyIncome'].corr(df['PerformanceRating'])
    
    # Salary hike analysis
    avg_salary_hike = df['PercentSalaryHike'].mean()
    salary_hike_by_dept = df.groupby('Department')['PercentSalaryHike'].mean().to_dict()
    
    return {
        'avg_salary_by_role': avg_salary_by_role,
        'dept_salary_stats': dept_salary_stats,
        'salary_performance_correlation': salary_perf_corr,
        'avg_salary_hike': avg_salary_hike,
        'salary_hike_by_dept': salary_hike_by_dept
    }

# <ID:KPI-WORKLIFE-BALANCE>
def calculate_worklife_balance_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate work-life balance related KPIs"""
    
    # Attrition by work-life balance
    wlb_attrition = df.groupby('WorkLifeBalance')['Attrition'].apply(
        lambda x: (x == 'Yes').mean() * 100
    ).to_dict()
    
    # Work-life balance distribution
    wlb_distribution = df['WorkLifeBalance'].value_counts().sort_index().to_dict()
    
    # Work-life balance vs job satisfaction
    wlb_satisfaction_corr = df['WorkLifeBalance'].corr(df['JobSatisfaction'])
    
    # Work-life balance by department
    wlb_by_dept = df.groupby('Department')['WorkLifeBalance'].mean().to_dict()
    
    return {
        'attrition_by_wlb': wlb_attrition,
        'wlb_distribution': wlb_distribution,
        'wlb_satisfaction_correlation': wlb_satisfaction_corr,
        'wlb_by_department': wlb_by_dept
    }

# <ID:KPI-PERFORMANCE-SATISFACTION>
def calculate_performance_satisfaction_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate performance and satisfaction correlation metrics"""
    
    # Salary vs Performance correlation
    salary_perf_corr = df['MonthlyIncome'].corr(df['PerformanceRating'])
    
    # Tenure vs Job Satisfaction
    tenure_satisfaction_corr = df['YearsAtCompany'].corr(df['JobSatisfaction'])
    
    # Performance rating distribution
    perf_distribution = df['PerformanceRating'].value_counts().sort_index().to_dict()
    
    # Satisfaction scores by department
    satisfaction_cols = ['JobSatisfaction', 'EnvironmentSatisfaction', 'RelationshipSatisfaction']
    satisfaction_by_dept = df.groupby('Department')[satisfaction_cols].mean().to_dict('index')
    
    # Performance vs satisfaction matrix
    perf_sat_matrix = df.groupby(['PerformanceRating', 'JobSatisfaction']).size().unstack(fill_value=0)
    
    return {
        'salary_performance_correlation': salary_perf_corr,
        'tenure_satisfaction_correlation': tenure_satisfaction_corr,
        'performance_distribution': perf_distribution,
        'satisfaction_by_department': satisfaction_by_dept,
        'performance_satisfaction_matrix': perf_sat_matrix.to_dict()
    }

# <ID:KPI-TENURE-ANALYSIS>
def calculate_tenure_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate tenure-related KPIs"""
    
    # Tenure vs Job Satisfaction mapping
    tenure_satisfaction = df.groupby('YearsAtCompany')['JobSatisfaction'].agg([
        'mean', 'count'
    ]).round(2).to_dict('index')
    
    # Attrition by tenure
    tenure_attrition = df.groupby('tenure_category')['Attrition'].apply(
        lambda x: (x == 'Yes').mean() * 100
    ).to_dict()
    
    # Average tenure by department
    avg_tenure_by_dept = df.groupby('Department')['YearsAtCompany'].mean().to_dict()
    
    # Tenure vs salary correlation
    tenure_salary_corr = df['YearsAtCompany'].corr(df['MonthlyIncome'])
    
    return {
        'tenure_satisfaction_mapping': tenure_satisfaction,
        'attrition_by_tenure': tenure_attrition,
        'avg_tenure_by_department': avg_tenure_by_dept,
        'tenure_salary_correlation': tenure_salary_corr
    }

# <ID:KPI-COMPREHENSIVE-ANALYSIS>
def calculate_comprehensive_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate all KPIs in one comprehensive analysis"""
    
    kpis = {}
    
    # Basic attrition metrics
    kpis['attrition'] = calculate_attrition_rate(df)
    
    # Salary analysis
    kpis['salary'] = calculate_salary_metrics(df)
    
    # Work-life balance metrics
    kpis['worklife_balance'] = calculate_worklife_balance_metrics(df)
    
    # Performance and satisfaction metrics
    kpis['performance_satisfaction'] = calculate_performance_satisfaction_metrics(df)
    
    # Tenure analysis
    kpis['tenure'] = calculate_tenure_metrics(df)
    
    # Additional FP&A metrics
    kpis['financial_metrics'] = calculate_financial_metrics(df)
    
    # Risk indicators
    kpis['risk_indicators'] = calculate_risk_indicators(df)
    
    logger.info("Comprehensive KPI analysis completed")
    return kpis

# <ID:KPI-FINANCIAL-METRICS>
def calculate_financial_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate FP&A-focused financial metrics"""
    
    # Total payroll cost
    total_payroll = df['MonthlyIncome'].sum() * 12  # Annual
    
    # Average cost per employee
    avg_cost_per_employee = df['MonthlyIncome'].mean() * 12
    
    # Attrition cost (assuming replacement cost is 150% of annual salary)
    attrition_cost = df[df['Attrition'] == 'Yes']['MonthlyIncome'].sum() * 12 * 1.5
    
    # Salary efficiency (performance per dollar)
    df['salary_efficiency'] = df['PerformanceRating'] / (df['MonthlyIncome'] / 1000)
    avg_salary_efficiency = df['salary_efficiency'].mean()
    
    # Department cost analysis
    dept_costs = df.groupby('Department')['MonthlyIncome'].agg([
        'sum', 'mean', 'count'
    ]).round(2).to_dict('index')
    
    return {
        'total_annual_payroll': total_payroll,
        'avg_cost_per_employee': avg_cost_per_employee,
        'estimated_attrition_cost': attrition_cost,
        'avg_salary_efficiency': avg_salary_efficiency,
        'department_costs': dept_costs
    }

# <ID:KPI-RISK-INDICATORS>
def calculate_risk_indicators(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate risk indicators for HR analytics"""
    
    # High-risk employees (low satisfaction, high performance)
    high_risk = df[
        (df['JobSatisfaction'] <= 2) & 
        (df['PerformanceRating'] >= 4)
    ].shape[0]
    
    # Flight risk (high performers with low tenure)
    flight_risk = df[
        (df['PerformanceRating'] >= 4) & 
        (df['YearsAtCompany'] <= 2)
    ].shape[0]
    
    # Burnout risk (high overtime, low work-life balance)
    burnout_risk = df[
        (df['OverTime'] == 'Yes') & 
        (df['WorkLifeBalance'] <= 2)
    ].shape[0]
    
    # Retention risk score by department
    retention_risk = df.groupby('Department').apply(
        lambda x: ((x['JobSatisfaction'] <= 2).sum() / len(x)) * 100
    ).to_dict()
    
    return {
        'high_risk_employees': high_risk,
        'flight_risk_employees': flight_risk,
        'burnout_risk_employees': burnout_risk,
        'retention_risk_by_dept': retention_risk
    }

# <ID:KPI-STATISTICAL-TESTS>
def perform_statistical_tests(df: pd.DataFrame) -> Dict[str, Any]:
    """Perform statistical tests for significant differences"""
    
    results = {}
    
    # T-test: Attrition vs Non-attrition salary difference
    attrition_salary = df[df['Attrition'] == 'Yes']['MonthlyIncome']
    non_attrition_salary = df[df['Attrition'] == 'No']['MonthlyIncome']
    
    if len(attrition_salary) > 0 and len(non_attrition_salary) > 0:
        t_stat, p_value = stats.ttest_ind(attrition_salary, non_attrition_salary)
        results['salary_attrition_ttest'] = {
            't_statistic': t_stat,
            'p_value': p_value,
            'significant': p_value < 0.05
        }
    
    # Chi-square test: Department vs Attrition
    contingency_table = pd.crosstab(df['Department'], df['Attrition'])
    chi2, chi2_p_value, dof, expected = stats.chi2_contingency(contingency_table)
    results['department_attrition_chisquare'] = {
        'chi2_statistic': chi2,
        'p_value': chi2_p_value,
        'significant': chi2_p_value < 0.05
    }
    
    return results 