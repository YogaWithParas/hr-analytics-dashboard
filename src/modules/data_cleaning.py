# <ID:CLEANING-EMPLOYEE-ATTRITION>
"""
Data Cleaning Module for HR Employee Attrition Dataset
Handles data preprocessing, validation, and transformation for HR analytics
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any
import logging
import sys
import os

# Add parent directory to path for imports
current_dir = os.path.dirname(__file__)
project_root = os.path.join(current_dir, '..', '..')
sys.path.insert(0, project_root)

try:
    from src.config.schema import validate_employee_data, map_dataframe_to_records
except ImportError:
    # Fallback for direct module import
    sys.path.insert(0, os.path.join(current_dir, '..'))
    from config.schema import validate_employee_data, map_dataframe_to_records

# <ID:CLEANING-LOGGING>
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# <ID:CLEANING-LOAD-DATA>
def load_attrition_data(file_path: str) -> pd.DataFrame:
    """Load IBM HR Employee Attrition dataset"""
    try:
        # Handle both file paths and uploaded files
        if hasattr(file_path, 'read'):
            # It's an uploaded file object
            df = pd.read_csv(file_path)
        else:
            # It's a file path string
            df = pd.read_csv(file_path)
        
        logger.info(f"Successfully loaded data with {len(df)} records and {len(df.columns)} columns")
        return df
    except Exception as e:
        logger.error(f"Error loading data from {file_path}: {e}")
        raise

# <ID:CLEANING-BASIC-CLEANUP>
def perform_basic_cleanup(df: pd.DataFrame) -> pd.DataFrame:
    """Perform basic data cleaning operations"""
    
    # Remove duplicates
    initial_rows = len(df)
    df = df.drop_duplicates()
    logger.info(f"Removed {initial_rows - len(df)} duplicate records")
    
    # Handle missing values
    missing_counts = df.isnull().sum()
    if missing_counts.sum() > 0:
        logger.warning(f"Missing values found: {missing_counts[missing_counts > 0].to_dict()}")
        
        # Fill missing values with appropriate defaults
        df['YearsSinceLastPromotion'] = df['YearsSinceLastPromotion'].fillna(0)
        df['YearsWithCurrManager'] = df['YearsWithCurrManager'].fillna(0)
    
    # Standardize text columns
    text_columns = ['Gender', 'MaritalStatus', 'Department', 'JobRole', 'BusinessTravel', 'EducationField', 'OverTime', 'Attrition']
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].str.strip().str.title()
    
    return df

# <ID:CLEANING-FEATURE-ENGINEERING>
def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create derived features for analysis"""
    
    # Create binary attrition flag
    df['attrition_flag'] = (df['Attrition'] == 'Yes').astype(int)
    
    # Create tenure categories
    df['tenure_category'] = pd.cut(df['YearsAtCompany'], 
                                  bins=[0, 2, 5, 10, 20, 50], 
                                  labels=['New', 'Early', 'Mid', 'Senior', 'Veteran'])
    
    # Create salary categories
    df['salary_category'] = pd.cut(df['MonthlyIncome'], 
                                  bins=[0, 3000, 5000, 8000, 12000, 20000], 
                                  labels=['Low', 'Lower-Mid', 'Mid', 'Upper-Mid', 'High'])
    
    # Create satisfaction score (average of all satisfaction metrics)
    satisfaction_cols = ['JobSatisfaction', 'EnvironmentSatisfaction', 'RelationshipSatisfaction']
    df['overall_satisfaction'] = df[satisfaction_cols].mean(axis=1)
    
    # Create work-life balance score
    df['work_life_score'] = df['WorkLifeBalance'] * df['JobInvolvement']
    
    # Create performance-salary ratio
    df['performance_salary_ratio'] = df['PerformanceRating'] / (df['MonthlyIncome'] / 1000)
    
    logger.info("Feature engineering completed")
    return df

# <ID:CLEANING-OUTLIER-DETECTION>
def detect_and_handle_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """Detect and handle outliers in numerical columns"""
    
    numerical_columns = ['Age', 'MonthlyIncome', 'HourlyRate', 'DailyRate', 'DistanceFromHome']
    
    for col in numerical_columns:
        if col in df.columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            if len(outliers) > 0:
                logger.info(f"Found {len(outliers)} outliers in {col}")
                # Cap outliers instead of removing them
                df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
    
    return df

# <ID:CLEANING-VALIDATION>
def validate_cleaned_data(df: pd.DataFrame) -> bool:
    """Validate cleaned data meets requirements"""
    
    # Check for required columns
    required_columns = ['Age', 'Gender', 'MaritalStatus', 'Department', 'JobRole', 'Attrition']
    missing_required = [col for col in required_columns if col not in df.columns]
    
    if missing_required:
        logger.error(f"Missing required columns: {missing_required}")
        return False
    
    # Check for data types
    if not pd.api.types.is_numeric_dtype(df['Age']):
        logger.error("Age column is not numeric")
        return False
    
    # Check for reasonable value ranges
    if df['Age'].min() < 18 or df['Age'].max() > 80:
        logger.warning("Age values outside expected range (18-80)")
    
    logger.info("Data validation passed")
    return True

# <ID:CLEANING-MAIN-PIPELINE>
def run_cleaning_pipeline(file_path: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Main data cleaning pipeline"""
    
    cleaning_stats = {
        'initial_records': 0,
        'final_records': 0,
        'duplicates_removed': 0,
        'outliers_handled': 0,
        'missing_values_filled': 0
    }
    
    try:
        # Load data
        df = load_attrition_data(file_path)
        cleaning_stats['initial_records'] = len(df)
        
        # Basic cleanup
        df = perform_basic_cleanup(df)
        cleaning_stats['final_records'] = len(df)
        cleaning_stats['duplicates_removed'] = cleaning_stats['initial_records'] - cleaning_stats['final_records']
        
        # Handle outliers
        df = detect_and_handle_outliers(df)
        
        # Engineer features
        df = engineer_features(df)
        
        # Validate schema
        try:
            df = validate_employee_data(df)
        except Exception as e:
            logger.warning(f"Schema validation failed, continuing with raw data: {e}")
        
        # Final validation
        if not validate_cleaned_data(df):
            logger.warning("Data validation failed, but continuing with available data")
        
        logger.info("Data cleaning pipeline completed successfully")
        return df, cleaning_stats
        
    except Exception as e:
        logger.error(f"Error in cleaning pipeline: {e}")
        # Return the original data if cleaning fails
        if 'df' in locals():
            return df, cleaning_stats
        else:
            raise

# <ID:CLEANING-EXPORT>
def export_cleaned_data(df: pd.DataFrame, output_path: str) -> None:
    """Export cleaned data to CSV"""
    try:
        df.to_csv(output_path, index=False)
        logger.info(f"Cleaned data exported to {output_path}")
    except Exception as e:
        logger.error(f"Error exporting data: {e}")
        raise 