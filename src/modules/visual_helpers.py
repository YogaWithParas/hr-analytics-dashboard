# <ID:VISUAL-HELPERS>
"""
Visual Helpers Module for HR Analytics Dashboard
Provides chart creation and visualization functions for Streamlit dashboard
"""

import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import logging
import sys
import os

# Add parent directory to path for imports
current_dir = os.path.dirname(__file__)
project_root = os.path.join(current_dir, '..', '..')
sys.path.insert(0, project_root)

# <ID:VISUAL-LOGGING>
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# <ID:VISUAL-ATTRITION-CHARTS>
def create_attrition_charts(df: pd.DataFrame, kpis: Dict[str, Any]) -> Dict[str, go.Figure]:
    """Create attrition-related visualizations"""
    
    charts = {}
    
    # Overall attrition rate gauge
    overall_rate = kpis['attrition']['overall_rate']
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=overall_rate,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Overall Attrition Rate (%)"},
        gauge={
            'axis': {'range': [None, 50]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 10], 'color': "lightgreen"},
                {'range': [10, 20], 'color': "yellow"},
                {'range': [20, 50], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 20
            }
        }
    ))
    fig_gauge.update_layout(height=300)
    charts['attrition_gauge'] = fig_gauge
    
    # Attrition by department
    dept_data = pd.DataFrame(list(kpis['attrition']['by_department'].items()), 
                            columns=['Department', 'Attrition_Rate'])
    fig_dept = px.bar(dept_data, x='Department', y='Attrition_Rate',
                      title='Attrition Rate by Department',
                      color='Attrition_Rate',
                      color_continuous_scale='RdYlGn_r')
    charts['attrition_by_dept'] = fig_dept
    
    # Attrition by job role
    role_data = pd.DataFrame(list(kpis['attrition']['by_job_role'].items()),
                            columns=['JobRole', 'Attrition_Rate'])
    fig_role = px.bar(role_data, x='JobRole', y='Attrition_Rate',
                      title='Attrition Rate by Job Role',
                      color='Attrition_Rate',
                      color_continuous_scale='RdYlGn_r')
    charts['attrition_by_role'] = fig_role
    
    return charts

# <ID:VISUAL-SALARY-CHARTS>
def create_salary_charts(df: pd.DataFrame, kpis: Dict[str, Any]) -> Dict[str, go.Figure]:
    """Create salary-related visualizations"""
    
    charts = {}
    
    # Average monthly income by job role
    salary_data = pd.DataFrame.from_dict(kpis['salary']['avg_salary_by_role'], orient='index')
    salary_data.reset_index(inplace=True)
    salary_data.rename(columns={'index': 'JobRole'}, inplace=True)
    
    fig_salary_role = px.bar(salary_data, x='JobRole', y='mean',
                             title='Average Monthly Income by Job Role',
                             color='mean',
                             color_continuous_scale='Blues')
    charts['salary_by_role'] = fig_salary_role
    
    # Salary vs Performance correlation
    fig_scatter = px.scatter(df, x='MonthlyIncome', y='PerformanceRating',
                            color='Attrition', size='YearsAtCompany',
                            title='Salary vs Performance Rating',
                            hover_data=['JobRole', 'Department'])
    charts['salary_performance_scatter'] = fig_scatter
    
    # Salary distribution by department
    fig_box = px.box(df, x='Department', y='MonthlyIncome',
                     title='Salary Distribution by Department',
                     color='Department')
    charts['salary_distribution'] = fig_box
    
    return charts

# <ID:VISUAL-WORKLIFE-CHARTS>
def create_worklife_charts(df: pd.DataFrame, kpis: Dict[str, Any]) -> Dict[str, go.Figure]:
    """Create work-life balance visualizations"""
    
    charts = {}
    
    # Attrition by work-life balance
    wlb_data = pd.DataFrame(list(kpis['worklife_balance']['attrition_by_wlb'].items()),
                           columns=['WorkLifeBalance', 'Attrition_Rate'])
    fig_wlb = px.bar(wlb_data, x='WorkLifeBalance', y='Attrition_Rate',
                      title='Attrition Rate by Work-Life Balance',
                      color='Attrition_Rate',
                      color_continuous_scale='RdYlGn_r')
    charts['attrition_by_wlb'] = fig_wlb
    
    # Work-life balance distribution
    wlb_dist = pd.DataFrame(list(kpis['worklife_balance']['wlb_distribution'].items()),
                           columns=['WorkLifeBalance', 'Count'])
    fig_dist = px.pie(wlb_dist, values='Count', names='WorkLifeBalance',
                      title='Work-Life Balance Distribution')
    charts['wlb_distribution'] = fig_dist
    
    # Work-life balance vs job satisfaction
    fig_scatter = px.scatter(df, x='WorkLifeBalance', y='JobSatisfaction',
                            color='Attrition', size='YearsAtCompany',
                            title='Work-Life Balance vs Job Satisfaction')
    charts['wlb_satisfaction_scatter'] = fig_scatter
    
    return charts

# <ID:VISUAL-TENURE-CHARTS>
def create_tenure_charts(df: pd.DataFrame, kpis: Dict[str, Any]) -> Dict[str, go.Figure]:
    """Create tenure-related visualizations"""
    
    charts = {}
    
    # Tenure vs Job Satisfaction
    tenure_sat_data = pd.DataFrame.from_dict(kpis['tenure']['tenure_satisfaction_mapping'], 
                                           orient='index')
    tenure_sat_data.reset_index(inplace=True)
    tenure_sat_data.rename(columns={'index': 'YearsAtCompany'}, inplace=True)
    
    fig_tenure_sat = px.line(tenure_sat_data, x='YearsAtCompany', y='mean',
                             title='Job Satisfaction vs Years at Company',
                             markers=True)
    charts['tenure_satisfaction'] = fig_tenure_sat
    
    # Attrition by tenure category
    tenure_attrition_data = pd.DataFrame(list(kpis['tenure']['attrition_by_tenure'].items()),
                                       columns=['TenureCategory', 'Attrition_Rate'])
    fig_tenure_attrition = px.bar(tenure_attrition_data, x='TenureCategory', y='Attrition_Rate',
                                  title='Attrition Rate by Tenure Category',
                                  color='Attrition_Rate',
                                  color_continuous_scale='RdYlGn_r')
    charts['attrition_by_tenure'] = fig_tenure_attrition
    
    # Tenure vs Salary correlation
    fig_scatter = px.scatter(df, x='YearsAtCompany', y='MonthlyIncome',
                            color='Attrition', size='PerformanceRating',
                            title='Tenure vs Salary',
                            hover_data=['JobRole', 'Department'])
    charts['tenure_salary_scatter'] = fig_scatter
    
    return charts

# <ID:VISUAL-KPI-CARDS>
def create_kpi_cards(kpis: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Create KPI card data for dashboard"""
    
    cards = {}
    
    # Overall attrition rate
    cards['overall_attrition'] = {
        'value': f"{kpis['attrition']['overall_rate']:.1f}%",
        'label': 'Overall Attrition Rate',
        'color': 'red' if kpis['attrition']['overall_rate'] > 20 else 'green'
    }
    
    # Average salary
    avg_salary = kpis['salary']['dept_salary_stats']['Sales']['mean']
    cards['avg_salary'] = {
        'value': f"${avg_salary:,.0f}",
        'label': 'Average Monthly Salary',
        'color': 'blue'
    }
    
    # Total payroll cost
    total_payroll = kpis['financial_metrics']['total_annual_payroll']
    cards['total_payroll'] = {
        'value': f"${total_payroll:,.0f}",
        'label': 'Annual Payroll Cost',
        'color': 'purple'
    }
    
    # Attrition cost
    attrition_cost = kpis['financial_metrics']['estimated_attrition_cost']
    cards['attrition_cost'] = {
        'value': f"${attrition_cost:,.0f}",
        'label': 'Estimated Attrition Cost',
        'color': 'orange'
    }
    
    # High-risk employees
    high_risk = kpis['risk_indicators']['high_risk_employees']
    cards['high_risk'] = {
        'value': str(high_risk),
        'label': 'High-Risk Employees',
        'color': 'red'
    }
    
    return cards

# <ID:VISUAL-COMPREHENSIVE-DASHBOARD>
def create_comprehensive_dashboard(df: pd.DataFrame, kpis: Dict[str, Any]) -> Dict[str, Any]:
    """Create all visualizations for comprehensive dashboard"""
    
    dashboard = {}
    
    # Create all chart categories
    dashboard['attrition_charts'] = create_attrition_charts(df, kpis)
    dashboard['salary_charts'] = create_salary_charts(df, kpis)
    dashboard['worklife_charts'] = create_worklife_charts(df, kpis)
    dashboard['tenure_charts'] = create_tenure_charts(df, kpis)
    dashboard['kpi_cards'] = create_kpi_cards(kpis)
    
    # Create summary statistics
    dashboard['summary_stats'] = {
        'total_employees': len(df),
        'attrition_count': (df['Attrition'] == 'Yes').sum(),
        'departments': df['Department'].nunique(),
        'job_roles': df['JobRole'].nunique(),
        'avg_age': df['Age'].mean(),
        'avg_tenure': df['YearsAtCompany'].mean()
    }
    
    logger.info("Comprehensive dashboard visualizations created")
    return dashboard

# <ID:VISUAL-EXPORT-FUNCTIONS>
def export_chart_as_image(fig: go.Figure, filename: str, format: str = 'png') -> None:
    """Export chart as image file"""
    try:
        fig.write_image(f"dashboard/exports/{filename}.{format}")
        logger.info(f"Chart exported as {filename}.{format}")
    except Exception as e:
        logger.error(f"Error exporting chart: {e}")

def create_pdf_report(dashboard_data: Dict[str, Any], filename: str) -> None:
    """Create PDF report with all dashboard visualizations"""
    # This would integrate with a PDF library like reportlab or weasyprint
    logger.info(f"PDF report creation placeholder for {filename}")
    # Implementation would go here for actual PDF generation 