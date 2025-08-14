# <ID:DASHBOARD-UI-MAIN>
"""
Main Streamlit Dashboard for HR Analytics
FP&A-aligned HR insights using IBM Employee Attrition dataset
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
import os
from datetime import datetime
import base64
import traceback

# Add project root to path for imports
current_dir = os.path.dirname(__file__)
project_root = os.path.join(current_dir, '..')
sys.path.insert(0, project_root)

# Import modules
try:
    from src.modules.data_cleaning import run_cleaning_pipeline, load_attrition_data
    from src.modules.kpi_calculations import calculate_comprehensive_kpis, perform_statistical_tests
    from src.modules.visual_helpers import create_comprehensive_dashboard
    from src.config.schema import validate_employee_data
    st.success("✅ All modules imported successfully!")
except Exception as e:
    st.error(f"❌ Import error: {e}")
    st.stop()

# <ID:DASHBOARD-CONFIG>
st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better responsive layout and comfortable viewing
st.markdown("""
<style>
    /* Main container improvements */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Better spacing for headers */
    h1, h2, h3 {
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Improved KPI cards */
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    
    /* Better chart containers */
    .stPlotlyChart {
        margin: 1rem 0;
    }
    
    /* Responsive sidebar */
    .css-1d391kg {
        min-width: 300px;
    }
    
    /* Better tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 0.5rem 0.5rem 0 0;
        gap: 1rem;
        padding-top: 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
    }
    
    /* Improved spacing between elements */
    .element-container {
        margin-bottom: 1.5rem;
    }
    
    /* Better file uploader styling */
    .stFileUploader {
        margin-bottom: 1rem;
    }
    
    /* Responsive columns */
    @media (max-width: 1200px) {
        .stTabs [data-baseweb="tab-list"] {
            flex-direction: column;
        }
    }
</style>
""", unsafe_allow_html=True)

# <ID:DASHBOARD-SIDEBAR>
def create_sidebar():
    """Create sidebar with filters and controls"""
    
    st.sidebar.header("📊 HR Analytics Dashboard")
    st.sidebar.markdown("---")
    
    # File upload section
    st.sidebar.subheader("📁 Data Upload")
    uploaded_file = st.sidebar.file_uploader(
        "Upload HR Data (CSV)",
        type=['csv'],
        help="Upload IBM Employee Attrition dataset or similar HR data"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔍 Data Filters")
    
    # Department filter
    st.sidebar.markdown("**Department**")
    departments = st.sidebar.multiselect(
        "Select departments",
        options=['All', 'Sales', 'Research & Development', 'Human Resources'],
        default=['All'],
        label_visibility="collapsed"
    )
    
    # Gender filter
    st.sidebar.markdown("**Gender**")
    genders = st.sidebar.multiselect(
        "Select genders",
        options=['All', 'Male', 'Female'],
        default=['All'],
        label_visibility="collapsed"
    )
    
    # Job Role filter
    st.sidebar.markdown("**Job Role**")
    job_roles = st.sidebar.multiselect(
        "Select job roles",
        options=['All', 'Sales Executive', 'Research Scientist', 'Laboratory Technician', 
                'Manufacturing Director', 'Healthcare Representative', 'Manager', 
                'Sales Representative', 'Research Director', 'Human Resources'],
        default=['All'],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Range Filters")
    
    # Age range filter
    st.sidebar.markdown("**Age Range**")
    age_range = st.sidebar.slider(
        "Select age range",
        min_value=18,
        max_value=80,
        value=(18, 80),
        label_visibility="collapsed"
    )
    
    # Tenure range filter
    st.sidebar.markdown("**Years at Company**")
    tenure_range = st.sidebar.slider(
        "Select tenure range",
        min_value=0,
        max_value=20,
        value=(0, 20),
        label_visibility="collapsed"
    )
    
    # Add some spacing at the bottom
    st.sidebar.markdown("---")
    st.sidebar.markdown("**💡 Tip:** Use filters to focus on specific employee segments")
    
    return {
        'uploaded_file': uploaded_file,
        'departments': departments,
        'genders': genders,
        'job_roles': job_roles,
        'age_range': age_range,
        'tenure_range': tenure_range
    }

# <ID:DASHBOARD-DATA-LOADING>
def load_and_process_data(uploaded_file):
    """Load and process the uploaded data"""
    
    if uploaded_file is not None:
        try:
            # Load data through cleaning pipeline
            df, cleaning_stats = run_cleaning_pipeline(uploaded_file)
            st.success(f"✅ Data loaded and cleaned successfully! {len(df)} records found.")
            st.info(f"📊 Cleaning stats: {cleaning_stats['duplicates_removed']} duplicates removed")
            return df
        except Exception as e:
            st.error(f"❌ Error loading data: {str(e)}")
            return None
    else:
        # Load sample data if no file uploaded
        try:
            sample_file = os.path.join("..", "data", "WA_Fn-UseC_-HR-Employee-Attrition.csv")
            if os.path.exists(sample_file):
                df, cleaning_stats = run_cleaning_pipeline(sample_file)
                st.info("📊 Using sample IBM Employee Attrition dataset")
                st.info(f"📊 Cleaning stats: {cleaning_stats['duplicates_removed']} duplicates removed")
                return df
            else:
                st.warning("⚠️ Please upload a CSV file or ensure sample data is available")
                return None
        except Exception as e:
            st.error(f"❌ Error loading sample data: {str(e)}")
            return None

# <ID:DASHBOARD-FILTERING>
def apply_filters(df, filters):
    """Apply filters to the dataset"""
    
    if df is None:
        return None
    
    filtered_df = df.copy()
    
    # Department filter
    if 'All' not in filters['departments']:
        filtered_df = filtered_df[filtered_df['Department'].isin(filters['departments'])]
    
    # Gender filter
    if 'All' not in filters['genders']:
        filtered_df = filtered_df[filtered_df['Gender'].isin(filters['genders'])]
    
    # Job Role filter
    if 'All' not in filters['job_roles']:
        filtered_df = filtered_df[filtered_df['JobRole'].isin(filters['job_roles'])]
    
    # Age range filter
    filtered_df = filtered_df[
        (filtered_df['Age'] >= filters['age_range'][0]) & 
        (filtered_df['Age'] <= filters['age_range'][1])
    ]
    
    # Tenure range filter
    filtered_df = filtered_df[
        (filtered_df['YearsAtCompany'] >= filters['tenure_range'][0]) & 
        (filtered_df['YearsAtCompany'] <= filters['tenure_range'][1])
    ]
    
    return filtered_df

# <ID:DASHBOARD-KPI-CARDS>
def display_kpi_cards(kpis):
    """Display KPI cards at the top of the dashboard"""
    
    st.header("📈 Key Performance Indicators")
    st.markdown("---")
    
    # Create responsive columns for KPI cards
    # Use different column layouts based on screen size
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 1.5rem; border-radius: 0.5rem; border-left: 4px solid #28a745; margin-bottom: 1rem;">
            <h4 style="margin: 0; color: #495057;">Overall Attrition Rate</h4>
            <h2 style="margin: 0.5rem 0; color: #28a745;">{:.1f}%</h2>
        </div>
        """.format(kpis['attrition']['overall_rate']), unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 1.5rem; border-radius: 0.5rem; border-left: 4px solid #007bff; margin-bottom: 1rem;">
            <h4 style="margin: 0; color: #495057;">Average Monthly Salary</h4>
            <h2 style="margin: 0.5rem 0; color: #007bff;">${:,.0f}</h2>
        </div>
        """.format(kpis['salary']['dept_salary_stats']['Sales']['mean']), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 1.5rem; border-radius: 0.5rem; border-left: 4px solid #ffc107; margin-bottom: 1rem;">
            <h4 style="margin: 0; color: #495057;">Annual Payroll Cost</h4>
            <h2 style="margin: 0.5rem 0; color: #ffc107;">${:,.0f}</h2>
        </div>
        """.format(kpis['financial_metrics']['total_annual_payroll']), unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 1.5rem; border-radius: 0.5rem; border-left: 4px solid #dc3545; margin-bottom: 1rem;">
            <h4 style="margin: 0; color: #495057;">Attrition Cost</h4>
            <h2 style="margin: 0.5rem 0; color: #dc3545;">${:,.0f}</h2>
        </div>
        """.format(kpis['financial_metrics']['estimated_attrition_cost']), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 1.5rem; border-radius: 0.5rem; border-left: 4px solid #6f42c1; margin-bottom: 1rem;">
            <h4 style="margin: 0; color: #495057;">High-Risk Employees</h4>
            <h2 style="margin: 0.5rem 0; color: #6f42c1;">{}</h2>
        </div>
        """.format(kpis['risk_indicators']['high_risk_employees']), unsafe_allow_html=True)
        
        # Add a summary metric
        total_employees = kpis.get('summary_stats', {}).get('total_employees', 'N/A')
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 1.5rem; border-radius: 0.5rem; border-left: 4px solid #17a2b8; margin-bottom: 1rem;">
            <h4 style="margin: 0; color: #495057;">Total Employees</h4>
            <h2 style="margin: 0.5rem 0; color: #17a2b8;">{}</h2>
        </div>
        """.format(total_employees), unsafe_allow_html=True)
    
    st.markdown("---")

# <ID:DASHBOARD-CHARTS>
def display_charts(dashboard_data):
    """Display all charts and visualizations"""
    
    st.header("📊 Analytics Dashboard")
    st.markdown("---")
    
    # Create tabs for different chart categories with better styling
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏢 Attrition Analysis", 
        "💰 Salary Analysis", 
        "⚖️ Work-Life Balance", 
        "📈 Tenure Analysis",
        "📋 Summary Statistics"
    ])
    
    with tab1:
        st.subheader("🏢 Attrition Analysis")
        st.markdown("---")
        
        # First row - two charts side by side
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("**Attrition Rate Overview**")
            st.plotly_chart(dashboard_data['attrition_charts']['attrition_gauge'], 
                           use_container_width=True, height=400)
        
        with col2:
            st.markdown("**Attrition by Department**")
            st.plotly_chart(dashboard_data['attrition_charts']['attrition_by_dept'], 
                           use_container_width=True, height=400)
        
        # Second row - full width chart
        st.markdown("**Attrition by Job Role**")
        st.plotly_chart(dashboard_data['attrition_charts']['attrition_by_role'], 
                       use_container_width=True, height=500)
    
    with tab2:
        st.subheader("💰 Salary Analysis")
        st.markdown("---")
        
        # First row - two charts side by side
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("**Salary by Job Role**")
            st.plotly_chart(dashboard_data['salary_charts']['salary_by_role'], 
                           use_container_width=True, height=400)
        
        with col2:
            st.markdown("**Salary Distribution**")
            st.plotly_chart(dashboard_data['salary_charts']['salary_distribution'], 
                           use_container_width=True, height=400)
        
        # Second row - full width chart
        st.markdown("**Salary vs Performance Correlation**")
        st.plotly_chart(dashboard_data['salary_charts']['salary_performance_scatter'], 
                       use_container_width=True, height=500)
    
    with tab3:
        st.subheader("⚖️ Work-Life Balance Analysis")
        st.markdown("---")
        
        # First row - two charts side by side
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("**Attrition by Work-Life Balance**")
            st.plotly_chart(dashboard_data['worklife_charts']['attrition_by_wlb'], 
                           use_container_width=True, height=400)
        
        with col2:
            st.markdown("**Work-Life Balance Distribution**")
            st.plotly_chart(dashboard_data['worklife_charts']['wlb_distribution'], 
                           use_container_width=True, height=400)
        
        # Second row - full width chart
        st.markdown("**Work-Life Balance vs Satisfaction**")
        st.plotly_chart(dashboard_data['worklife_charts']['wlb_satisfaction_scatter'], 
                       use_container_width=True, height=500)
    
    with tab4:
        st.subheader("📈 Tenure Analysis")
        st.markdown("---")
        
        # First row - two charts side by side
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("**Tenure vs Satisfaction**")
            st.plotly_chart(dashboard_data['tenure_charts']['tenure_satisfaction'], 
                           use_container_width=True, height=400)
        
        with col2:
            st.markdown("**Attrition by Tenure**")
            st.plotly_chart(dashboard_data['tenure_charts']['attrition_by_tenure'], 
                           use_container_width=True, height=400)
        
        # Second row - full width chart
        st.markdown("**Tenure vs Salary Relationship**")
        st.plotly_chart(dashboard_data['tenure_charts']['tenure_salary_scatter'], 
                       use_container_width=True, height=500)
    
    with tab5:
        st.subheader("📋 Summary Statistics")
        st.markdown("---")
        
        # Create a more organized summary layout
        col1, col2, col3 = st.columns([1, 1, 1])
        stats = dashboard_data['summary_stats']
        
        with col1:
            st.markdown("""
            <div style="background-color: #e3f2fd; padding: 1.5rem; border-radius: 0.5rem; text-align: center;">
                <h3 style="margin: 0; color: #1976d2;">Total Employees</h3>
                <h1 style="margin: 0.5rem 0; color: #1976d2;">{}</h1>
            </div>
            """.format(stats['total_employees']), unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background-color: #e8f5e8; padding: 1.5rem; border-radius: 0.5rem; text-align: center; margin-top: 1rem;">
                <h3 style="margin: 0; color: #388e3c;">Departments</h3>
                <h1 style="margin: 0.5rem 0; color: #388e3c;">{}</h1>
            </div>
            """.format(stats['departments']), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background-color: #fff3e0; padding: 1.5rem; border-radius: 0.5rem; text-align: center;">
                <h3 style="margin: 0; color: #f57c00;">Attrition Count</h3>
                <h1 style="margin: 0.5rem 0; color: #f57c00;">{}</h1>
            </div>
            """.format(stats['attrition_count']), unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background-color: #fce4ec; padding: 1.5rem; border-radius: 0.5rem; text-align: center; margin-top: 1rem;">
                <h3 style="margin: 0; color: #c2185b;">Job Roles</h3>
                <h1 style="margin: 0.5rem 0; color: #c2185b;">{}</h1>
            </div>
            """.format(stats['job_roles']), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background-color: #f3e5f5; padding: 1.5rem; border-radius: 0.5rem; text-align: center;">
                <h3 style="margin: 0; color: #7b1fa2;">Average Age</h3>
                <h1 style="margin: 0.5rem 0; color: #7b1fa2;">{:.1f}</h1>
            </div>
            """.format(stats['avg_age']), unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background-color: #e0f2f1; padding: 1.5rem; border-radius: 0.5rem; text-align: center; margin-top: 1rem;">
                <h3 style="margin: 0; color: #00796b;">Average Tenure</h3>
                <h1 style="margin: 0.5rem 0; color: #00796b;">{:.1f}</h1>
            </div>
            """.format(stats['avg_tenure']), unsafe_allow_html=True)

# <ID:DASHBOARD-MAIN>
def main():
    """Main dashboard function"""
    
    # Main title with better styling
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 1rem; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0; font-size: 3rem;">🏢 HR Analytics Dashboard</h1>
        <p style="color: white; margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">FP&A-aligned HR insights using IBM Employee Attrition dataset</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create sidebar
    filters = create_sidebar()
    
    # Load and process data
    with st.spinner("🔄 Loading and processing data..."):
        df = load_and_process_data(filters['uploaded_file'])
    
    if df is not None:
        # Apply filters
        with st.spinner("🔍 Applying filters..."):
            filtered_df = apply_filters(df, filters)
        
        if filtered_df is not None and len(filtered_df) > 0:
            # Display data summary
            st.success(f"✅ Data loaded successfully! {len(filtered_df)} records after filtering.")
            
            # Calculate KPIs
            with st.spinner("📊 Calculating KPIs..."):
                kpis = calculate_comprehensive_kpis(filtered_df)
            
            # Create dashboard visualizations
            with st.spinner("🎨 Creating visualizations..."):
                dashboard_data = create_comprehensive_dashboard(filtered_df, kpis)
            
            # Display KPI cards
            display_kpi_cards(kpis)
            
            # Display charts
            display_charts(dashboard_data)
            
        else:
            st.warning("⚠️ No data matches the selected filters. Please adjust your filter criteria.")
            st.info("💡 Try expanding your filter ranges or removing some filter constraints.")
    else:
        st.info("📊 Please upload a CSV file to begin analysis")
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 2rem; border-radius: 0.5rem; text-align: center; border: 2px dashed #dee2e6;">
            <h3 style="color: #6c757d; margin-bottom: 1rem;">No Data Available</h3>
            <p style="color: #6c757d; margin: 0;">Upload a CSV file using the sidebar to start analyzing your HR data.</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 