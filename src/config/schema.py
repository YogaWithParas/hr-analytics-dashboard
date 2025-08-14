# <ID:SCHEMA-EMPLOYEE-RECORD>
"""
Employee Record Schema for HR Analytics Dashboard
Defines data structures and validation rules for employee data processing
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime
import pandas as pd

@dataclass
class EmployeeRecord:
    """Employee record schema for HR analytics"""
    
    # Basic Information
    employee_id: int
    age: int
    gender: str
    marital_status: str
    
    # Job Information
    department: str
    job_role: str
    job_level: int
    years_at_company: int
    years_in_current_role: int
    years_since_last_promotion: int
    years_with_curr_manager: int
    
    # Compensation & Performance
    monthly_income: float
    hourly_rate: float
    daily_rate: float
    percent_salary_hike: float
    performance_rating: int
    
    # Work Environment
    work_life_balance: int
    job_involvement: int
    job_satisfaction: int
    environment_satisfaction: int
    relationship_satisfaction: int
    
    # Business Travel & Education
    business_travel: str
    education: int
    education_field: str
    
    # Distance & Overtime
    distance_from_home: int
    overtime: str
    
    # Target Variable
    attrition: str
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EmployeeRecord':
        """Create EmployeeRecord from dictionary"""
        return cls(**data)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert EmployeeRecord to dictionary"""
        return {
            'employee_id': self.employee_id,
            'age': self.age,
            'gender': self.gender,
            'marital_status': self.marital_status,
            'department': self.department,
            'job_role': self.job_role,
            'job_level': self.job_level,
            'years_at_company': self.years_at_company,
            'years_in_current_role': self.years_in_current_role,
            'years_since_last_promotion': self.years_since_last_promotion,
            'years_with_curr_manager': self.years_with_curr_manager,
            'monthly_income': self.monthly_income,
            'hourly_rate': self.hourly_rate,
            'daily_rate': self.daily_rate,
            'percent_salary_hike': self.percent_salary_hike,
            'performance_rating': self.performance_rating,
            'work_life_balance': self.work_life_balance,
            'job_involvement': self.job_involvement,
            'job_satisfaction': self.job_satisfaction,
            'environment_satisfaction': self.environment_satisfaction,
            'relationship_satisfaction': self.relationship_satisfaction,
            'business_travel': self.business_travel,
            'education': self.education,
            'education_field': self.education_field,
            'distance_from_home': self.distance_from_home,
            'overtime': self.overtime,
            'attrition': self.attrition
        }

# <ID:SCHEMA-VALIDATION>
def validate_employee_data(df: pd.DataFrame) -> pd.DataFrame:
    """Validate and clean employee data according to schema"""
    
    # Required columns
    required_columns = [
        'Age', 'Gender', 'MaritalStatus', 'Department', 'JobRole', 'JobLevel',
        'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion',
        'YearsWithCurrManager', 'MonthlyIncome', 'HourlyRate', 'DailyRate',
        'PercentSalaryHike', 'PerformanceRating', 'WorkLifeBalance',
        'JobInvolvement', 'JobSatisfaction', 'EnvironmentSatisfaction',
        'RelationshipSatisfaction', 'BusinessTravel', 'Education',
        'EducationField', 'DistanceFromHome', 'OverTime', 'Attrition'
    ]
    
    # Check for required columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # Data type validations
    numeric_columns = ['Age', 'JobLevel', 'YearsAtCompany', 'YearsInCurrentRole',
                      'YearsSinceLastPromotion', 'YearsWithCurrManager',
                      'MonthlyIncome', 'HourlyRate', 'DailyRate', 'PercentSalaryHike',
                      'PerformanceRating', 'WorkLifeBalance', 'JobInvolvement',
                      'JobSatisfaction', 'EnvironmentSatisfaction', 'RelationshipSatisfaction',
                      'Education', 'DistanceFromHome']
    
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

# <ID:SCHEMA-MAPPING>
def map_dataframe_to_records(df: pd.DataFrame) -> list[EmployeeRecord]:
    """Map DataFrame to list of EmployeeRecord objects"""
    records = []
    
    for _, row in df.iterrows():
        try:
            record = EmployeeRecord(
                employee_id=row.get('EmployeeID', len(records) + 1),
                age=row['Age'],
                gender=row['Gender'],
                marital_status=row['MaritalStatus'],
                department=row['Department'],
                job_role=row['JobRole'],
                job_level=row['JobLevel'],
                years_at_company=row['YearsAtCompany'],
                years_in_current_role=row['YearsInCurrentRole'],
                years_since_last_promotion=row['YearsSinceLastPromotion'],
                years_with_curr_manager=row['YearsWithCurrManager'],
                monthly_income=row['MonthlyIncome'],
                hourly_rate=row['HourlyRate'],
                daily_rate=row['DailyRate'],
                percent_salary_hike=row['PercentSalaryHike'],
                performance_rating=row['PerformanceRating'],
                work_life_balance=row['WorkLifeBalance'],
                job_involvement=row['JobInvolvement'],
                job_satisfaction=row['JobSatisfaction'],
                environment_satisfaction=row['EnvironmentSatisfaction'],
                relationship_satisfaction=row['RelationshipSatisfaction'],
                business_travel=row['BusinessTravel'],
                education=row['Education'],
                education_field=row['EducationField'],
                distance_from_home=row['DistanceFromHome'],
                overtime=row['OverTime'],
                attrition=row['Attrition']
            )
            records.append(record)
        except Exception as e:
            print(f"Error creating record for row {len(records) + 1}: {e}")
            continue
    
    return records 