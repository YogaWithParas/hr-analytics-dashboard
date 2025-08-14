# 🏢 HR Analytics Dashboard - FP&A-Aligned HR Insights

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Professional HR Analytics Dashboard** providing FP&A-aligned insights using IBM Employee Attrition dataset with advanced analytics, predictive modeling, and interactive visualizations.

## 🎯 **Project Overview**

This HR Analytics Dashboard is designed to provide **executive-level insights** into employee attrition, compensation analysis, work-life balance metrics, and tenure patterns. Built with modern data science practices, it offers actionable insights for HR professionals and business leaders.

### ✨ **Key Features**

- 📊 **Interactive Dashboard** with real-time filtering and analysis
- 🎯 **KPI Metrics** including attrition rates, salary analysis, and risk indicators
- 📈 **Advanced Visualizations** using Plotly for professional presentations
- 🔍 **Data Filtering** by department, role, age, and tenure
- 📋 **Comprehensive Reports** across multiple HR dimensions
- 🚀 **Responsive Design** optimized for all screen sizes

## 🏗️ **Architecture & Technology Stack**

### **Frontend & UI**
- **Streamlit** - Modern web application framework
- **Plotly** - Interactive, publication-quality charts
- **Custom CSS** - Professional styling and responsive design

### **Backend & Data Processing**
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **Scikit-learn** - Statistical analysis and modeling
- **Pydantic** - Data validation and settings management

### **Data Sources**
- **IBM Employee Attrition Dataset** (included)
- **CSV Upload Support** for custom HR data
- **Real-time Data Processing** pipeline

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.8+
- pip package manager

### **Installation**

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/hr-analytics-dashboard.git
   cd hr-analytics-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard**
   ```bash
   cd dashboard
   streamlit run streamlit_app.py
   ```

4. **Access the dashboard**
   - Open your browser and go to: `http://localhost:8501`
   - The dashboard will automatically load with sample data

## 📊 **Dashboard Features**

### **🏢 Attrition Analysis**
- Overall attrition rate with trend analysis
- Department-wise attrition patterns
- Job role attrition insights
- Risk assessment and prediction

### **💰 Salary Analysis**
- Compensation benchmarking by role
- Salary distribution analysis
- Performance-salary correlation
- Cost optimization insights

### **⚖️ Work-Life Balance**
- Work-life balance metrics
- Satisfaction correlation analysis
- Attrition impact assessment
- Employee engagement insights

### **📈 Tenure Analysis**
- Tenure patterns and trends
- Satisfaction vs. tenure correlation
- Retention risk assessment
- Career progression insights

### **📋 Summary Statistics**
- Comprehensive employee metrics
- Department overview
- Role distribution
- Demographic insights

## 🔧 **Configuration & Customization**

### **Data Upload**
- Support for CSV files
- Automatic data validation
- Custom data schema support
- Real-time data processing

### **Filtering Options**
- **Department**: Sales, R&D, HR
- **Gender**: Male, Female
- **Job Role**: 10+ predefined roles
- **Age Range**: 18-80 years
- **Tenure**: 0-20+ years

### **Export Capabilities**
- Chart downloads (PNG, SVG)
- Data export (CSV, Excel)
- Report generation
- KPI summaries

## 📁 **Project Structure**

```
hr-analytics-dashboard/
├── dashboard/
│   └── streamlit_app.py          # Main Streamlit application
├── src/
│   ├── modules/
│   │   ├── data_cleaning.py      # Data processing pipeline
│   │   ├── kpi_calculations.py   # KPI computation engine
│   │   └── visual_helpers.py     # Chart generation utilities
│   ├── config/
│   │   └── schema.py             # Data validation schemas
│   └── db/                       # Database utilities
├── data/
│   └── WA_Fn-UseC_-HR-Employee-Attrition.csv  # Sample dataset
├── notebooks/                     # Jupyter notebooks for analysis
├── docs/                         # Documentation
├── requirements.txt               # Python dependencies
└── README.md                     # This file
```

## 🎨 **Screenshots & Demo**

### **Main Dashboard**
![Main Dashboard](docs/images/main-dashboard.png)

### **KPI Overview**
![KPI Cards](docs/images/kpi-cards.png)

### **Interactive Charts**
![Interactive Charts](docs/images/interactive-charts.png)

## 📈 **Business Value**

### **For HR Professionals**
- **Data-Driven Decisions**: Make informed HR decisions based on analytics
- **Risk Mitigation**: Identify and address retention risks proactively
- **Cost Optimization**: Optimize compensation and benefits strategies
- **Performance Insights**: Understand factors affecting employee satisfaction

### **For Business Leaders**
- **Strategic Planning**: Align HR strategy with business objectives
- **ROI Analysis**: Measure the impact of HR initiatives
- **Competitive Advantage**: Benchmark against industry standards
- **Predictive Insights**: Forecast future HR challenges and opportunities

## 🔒 **Security & Privacy**

- **Local Processing**: All data processing happens locally
- **No External APIs**: No data sent to third-party services
- **Configurable Security**: Role-based access control support
- **Data Encryption**: Support for encrypted data sources

## 🚀 **Deployment Options**

### **Local Development**
- Run directly on your machine
- Perfect for development and testing
- Full control over data and environment

### **Cloud Deployment**
- **Streamlit Cloud**: One-click deployment
- **AWS/GCP/Azure**: Containerized deployment
- **Docker**: Containerized application
- **Heroku**: Platform-as-a-Service deployment

### **Enterprise Integration**
- **SSO Integration**: Single Sign-On support
- **LDAP/Active Directory**: Enterprise authentication
- **Database Integration**: Connect to existing HR systems
- **API Endpoints**: RESTful API for custom integrations

## 📚 **Documentation**

- **User Guide**: Complete dashboard usage instructions
- **API Reference**: Technical documentation for developers
- **Deployment Guide**: Step-by-step deployment instructions
- **Troubleshooting**: Common issues and solutions

## 🤝 **Contributing**

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### **Development Setup**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 **Team & Support**

- **Lead Developer**: [Your Name]
- **Data Science**: [Team Members]
- **UI/UX Design**: [Design Team]
- **Support**: [support@yourcompany.com]

## 🌟 **Acknowledgments**

- **IBM** for the Employee Attrition dataset
- **Streamlit** for the amazing web framework
- **Plotly** for interactive visualizations
- **Open Source Community** for the supporting libraries

## 📞 **Contact & Demo**

- **Website**: [yourcompany.com](https://yourcompany.com)
- **Email**: [contact@yourcompany.com](mailto:contact@yourcompany.com)
- **LinkedIn**: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- **Demo Request**: [Schedule a demo](https://calendly.com/yourcompany/demo)

---

<div align="center">

**Built with ❤️ for better HR decision making**

[![GitHub stars](https://img.shields.io/github/stars/yourusername/hr-analytics-dashboard.svg?style=social&label=Star)](https://github.com/yourusername/hr-analytics-dashboard)
[![GitHub forks](https://img.shields.io/gadge/github/forks/yourusername/hr-analytics-dashboard.svg?style=social&label=Fork)](https://github.com/yourusername/hr-analytics-dashboard)

</div> 