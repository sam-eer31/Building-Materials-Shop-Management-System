# 🏗️ Building Materials Shop Management System

A comprehensive, modern web-based management system designed specifically for building materials shops and construction supply businesses. Built with Flask, featuring a responsive UI, multi-language support, and complete business operations management.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.2-purple.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 🎯 Core Business Management
- **Customer Management**: Complete customer database with contact information and order history
- **Product & Inventory Management**: Track products, prices, stock levels, and low stock alerts
- **Order Management**: Create, edit, and track orders with delivery scheduling
- **Payment Tracking**: Comprehensive payment management with multiple payment methods
- **Invoice Generation**: Professional PDF invoice generation for orders

### 📊 Analytics & Reporting
- **Dashboard Analytics**: Real-time business metrics and KPIs
- **Sales Reports**: Detailed sales analysis with date range filtering
- **Inventory Reports**: Stock level monitoring and alerts
- **Customer Reports**: Customer performance and order history analysis
- **Export Functionality**: CSV export for all reports

### 🌐 Multi-Language Support
- **English** (Default)
- **हिंदी** (Hindi)
- **اردو** (Urdu)
- Easy language switching with persistent preferences

### 🎨 Modern User Interface
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Dark/Light Theme**: Toggle between themes for comfortable viewing
- **Modern UI/UX**: Clean, intuitive interface built with Bootstrap 5
- **Real-time Updates**: Dynamic content loading without page refreshes
- **Interactive Elements**: Modals, tooltips, and smooth animations

### 🔐 Security & Authentication
- **User Authentication**: Secure login system with password hashing
- **Session Management**: Configurable session timeouts
- **Data Validation**: Comprehensive input validation and sanitization
- **SQL Injection Protection**: Parameterized queries and ORM usage

## 🚀 Quick Start

### Setup (Recommended)
**⚠️ IMPORTANT**: You must install and set up MySQL BEFORE using the automated setup.

**For Windows users**: 
1. **Install MySQL** (see Database Setup section below)
2. **Set up the database** using the provided schema (see Database Setup section below)
3. **Double-click the `start.bat` file** to automatically:
   - Create virtual environment
   - Install all dependencies
   - Launch the application

**For other platforms**: Follow the manual installation steps below.

### Manual Installation

### Prerequisites
- **Python 3.8 or higher** - Download from [python.org](https://python.org)
- **MySQL 8.0 or higher** - Download from [mysql.com](https://mysql.com) or use XAMPP/WAMP

### Database Setup
**Important**: You must set up the MySQL database before running the application.

#### Step 1: Install MySQL
- **Windows**: Download MySQL Installer from [mysql.com](https://dev.mysql.com/downloads/installer/)
- **macOS**: Use Homebrew: `brew install mysql`
- **Linux**: `sudo apt-get install mysql-server` (Ubuntu/Debian) or `sudo yum install mysql-server` (CentOS/RHEL)

#### Step 2: Start MySQL Service
- **Windows**: MySQL service should start automatically after installation
- **macOS**: `brew services start mysql`
- **Linux**: `sudo systemctl start mysql`

#### Step 3: Create Database and Tables
Run the provided schema file:
```bash
mysql -u your_username -p < schema.sql
```
Or manually execute the SQL commands in `schema.sql` file.

#### Step 4: Update Database Credentials
Edit `config.py` and update the database connection:
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://your_username:your_password@localhost/building_materials_shop'
```
Replace `your_username` and `your_password` with your actual MySQL credentials.

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sam-eer31/Building-Materials-Shop-Management-System
   cd Building-Materials-Shop-Management-System
   ```

2. **Configure the application**
   - Edit `config.py` to update database connection details
   - Update the `SQLALCHEMY_DATABASE_URI` with your MySQL credentials:
     ```python
     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://your_username:your_password@localhost/building_materials_shop'
     ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the application**
   ```bash
   python app.py
   ```
   The application will connect to the database, create any missing tables, and automatically create a default admin user if it doesn't exist.

5. **Access the application**
   - Open your browser and go to `http://localhost:5000`
   - Login with default credentials:
     - **Username**: `admin`
     - **Password**: `admin123`

## 📁 Project Structure

```
Building-Materials-Shop-Management-System/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── schema.sql           # Complete database schema with sample data
├── start.bat            # Windows startup script (auto-setup)
├── templates/           # HTML templates
│   ├── base.html        # Base template with navigation
│   ├── dashboard.html   # Dashboard page
│   ├── customers.html   # Customer management
│   ├── products.html    # Product management
│   ├── orders.html      # Order management
│   ├── payments.html    # Payment management
│   ├── reports.html     # Reports and analytics
│   └── login.html       # Login page
└── venv/               # Virtual environment (created automatically)
```

## 🗄️ Database Schema

The system uses a relational database with the following main entities:

- **Users**: Authentication and user management
- **Customers**: Customer information and contact details
- **Products**: Product catalog with pricing and inventory
- **Orders**: Order management with delivery scheduling
- **Order Items**: Individual items within orders
- **Payments**: Payment tracking and history

### Sample Data
The `schema.sql` file includes:
- Sample products (cement, bricks, sand, steel rods, etc.)
- Sample customers (construction companies)

**Note**: The default admin user (username: `admin`, password: `admin123`) is automatically created when you first run the application.

## 🎛️ Configuration

### Environment Variables
- `FLASK_ENV`: Set to `development`, `production`, or `testing`
- `SECRET_KEY`: Secret key for session management
- `DATABASE_URL`: MySQL database connection string

### Database Configuration
Update the database connection in `config.py`:
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/building_materials_shop'
```

## 🔧 API Endpoints

### Authentication
- `POST /login` - User authentication
- `GET /logout` - User logout

### Customer Management
- `GET /customers` - View all customers
- `GET /api/customers` - Get customer data (JSON)
- `POST /api/customers` - Create new customer
- `PUT /api/customers/<id>` - Update customer
- `DELETE /api/customers/<id>` - Delete customer

### Product Management
- `GET /products` - View all products
- `GET /api/products` - Get product data (JSON)
- `POST /api/products` - Create new product
- `PUT /api/products/<id>` - Update product
- `DELETE /api/products/<id>` - Delete product

### Order Management
- `GET /orders` - View all orders
- `GET /api/orders` - Get order data (JSON)
- `POST /api/orders` - Create new order
- `PUT /api/orders/<id>` - Update order
- `DELETE /api/orders/<id>` - Delete order

### Payment Management
- `GET /payments` - View all payments
- `GET /api/payments` - Get payment data (JSON)
- `POST /api/payments` - Record new payment

### Reports & Analytics
- `GET /reports` - Reports dashboard
- `GET /api/reports/sales` - Sales report data
- `GET /api/reports/export-csv` - Export reports to CSV
- `GET /invoice/<order_id>` - Generate PDF invoice

## 🎨 Customization

### Adding New Languages
1. Add language code to `SUPPORTED_LANGUAGES` in `app.py`
2. Add translations to the `TRANSLATIONS` dictionary
3. Update language selection UI in templates

### Customizing Themes
Modify CSS variables in `templates/base.html`:
```css
:root {
    --primary-color: #your-color;
    --secondary-color: #your-color;
    /* ... other variables */
}
```

### Adding New Features
The modular structure makes it easy to add new features:
1. Create new database models in `app.py`
2. Add corresponding API endpoints
3. Create HTML templates
4. Update navigation in `base.html`

## 🚀 Deployment

### Production Deployment
1. Set `FLASK_ENV=production` in environment variables
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Set up a reverse proxy (Nginx, Apache)
4. Configure SSL certificates
5. Set up database backups

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add comments for complex logic
- Update documentation for new features
- Test thoroughly before submitting

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Flask** - The web framework for Python
- **Bootstrap** - Frontend framework for responsive design
- **Font Awesome** - Icons and visual elements
- **ReportLab** - PDF generation capabilities
- **SQLAlchemy** - Database ORM and management

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/sam-eer31/Building-Materials-Shop-Management-System/issues) page
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce



---

**Made with ❤️ for building materials businesses worldwide**

*This project helps construction supply businesses streamline their operations, manage inventory, track orders, and grow their business efficiently.*
