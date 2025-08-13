# Building Materials Shop Management System

A comprehensive business management system designed specifically for building materials shops. This system helps manage customers, products, inventory, orders, payments, and provides detailed reporting capabilities.

## 🏗️ Features

### Core Management
- **Customer Management**: Add, edit, delete, and search customers with contact information
- **Product & Inventory Management**: Manage products with pricing, stock quantities, and low stock alerts
- **Order Management**: Create orders with multiple products, track delivery dates, and manage payment status
- **Payment Tracking**: Record payments, track outstanding amounts, and manage payment history
- **Billing**: Generate professional PDF invoices for each order

### Reporting & Analytics
- **Sales Reports**: Generate detailed sales reports by date range
- **Customer Analytics**: Track customer spending and payment history
- **Product Performance**: Monitor product sales and stock levels
- **CSV Export**: Export reports to CSV format for external analysis
- **Dashboard**: Real-time overview of business metrics

### User Experience
- **Responsive Design**: Mobile-friendly interface that works on all devices
- **Modern UI**: Clean, intuitive interface with Bootstrap 5 styling
- **Real-time Updates**: Live data updates without page refreshes
- **Search & Filter**: Quick search and filtering across all modules

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript, Bootstrap 5
- **Backend**: Python 3.8+, Flask framework
- **Database**: MySQL 8.0+
- **Authentication**: Session-based login system
- **PDF Generation**: ReportLab for invoice generation
- **Dependencies**: See `requirements.txt`

## 📋 Prerequisites

Before running this system, ensure you have:

- **Python 3.8 or higher**
- **MySQL 8.0 or higher**
- **pip** (Python package installer)
- **Git** (for cloning the repository)

## 🚀 Installation & Setup

### Step 1: Clone the Repository
```bash
git clone [<repository-url>](https://github.com/sam-eer31/Building-Materials-Shop-Management-System)
cd building-materials-shop
```

### Step 2: Set Up Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Database Setup
1. **Start MySQL Server**
   ```bash
   # Windows (if using XAMPP/WAMP)
   # Start MySQL service from control panel
   
   # macOS (if using Homebrew)
   brew services start mysql
   
   # Linux
   sudo systemctl start mysql
   ```

2. **Create Database**
   ```bash
   mysql -u root -p
   ```
   
   In MySQL console:
   ```sql
   CREATE DATABASE building_materials_shop;
   USE building_materials_shop;
   source schema.sql;
   exit;
   ```

3. **Update Database Configuration**
   Edit `app.py` and update the database connection string:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/building_materials_shop'
   ```
   Replace `username` and `password` with your MySQL credentials.

### Step 5: Run the Application
```bash
python app.py
```

The application will be available at: `http://localhost:5000`

### Step 6: Login
- **Username**: `admin`
- **Password**: `admin123`

⚠️ **Important**: Change the default password after first login!

## 📊 Database Schema

The system uses the following database tables:

- **`users`**: User authentication and management
- **`customers`**: Customer information and contact details
- **`products`**: Product catalog with pricing and stock levels
- **`orders`**: Order headers with customer and delivery information
- **`order_items`**: Individual items within each order
- **`payments`**: Payment records and history

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:
```env
FLASK_SECRET_KEY=your-secret-key-here
DB_USERNAME=your_db_username
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_NAME=building_materials_shop
```

### Database Connection
Update the database connection in `app.py`:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
```

## 📱 Usage Guide

### Dashboard
- View business overview with key metrics
- Monitor low stock alerts
- Quick access to common actions

### Customer Management
1. **Add Customer**: Click "Add Customer" button
2. **Edit Customer**: Click edit icon on customer row
3. **Delete Customer**: Click delete icon (with confirmation)
4. **Search**: Use search bar to find specific customers

### Product Management
1. **Add Product**: Click "Add Product" button
2. **Set Stock Levels**: Configure initial stock quantities
3. **Monitor Inventory**: View low stock alerts on dashboard
4. **Update Prices**: Edit product information as needed

### Order Management
1. **Create Order**: Click "New Order" button
2. **Select Customer**: Choose from existing customers
3. **Add Products**: Select products and quantities
4. **Set Delivery**: Specify delivery date and address
5. **Generate Invoice**: Create PDF invoice for customer

### Payment Tracking
1. **Record Payments**: Click "Record Payment" button
2. **Select Order**: Choose order to apply payment
3. **Enter Amount**: Specify payment amount and method
4. **Track Outstanding**: Monitor remaining balances

### Reports
1. **Set Date Range**: Choose start and end dates
2. **Generate Report**: Click "Generate Report" button
3. **Export Data**: Download CSV for external analysis
4. **Quick Reports**: Use preset time periods

## 🔒 Security Features

- **Session-based Authentication**: Secure login system
- **SQL Injection Protection**: Parameterized queries
- **XSS Protection**: Input sanitization
- **CSRF Protection**: Form token validation
- **Password Hashing**: Secure password storage

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. **Use WSGI Server**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

2. **Environment Variables**:
   ```bash
   export FLASK_ENV=production
   export FLASK_SECRET_KEY=your-production-secret-key
   ```

3. **Database**: Use production MySQL server with proper security

4. **Reverse Proxy**: Configure Nginx or Apache for production

## 📁 Project Structure

```
building-materials-shop/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── schema.sql            # Database schema
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── login.html        # Login page
│   ├── dashboard.html    # Dashboard
│   ├── customers.html    # Customer management
│   ├── products.html     # Product management
│   ├── orders.html       # Order management
│   ├── payments.html     # Payment tracking
│   └── reports.html      # Reporting system
└── static/               # Static files (CSS, JS, images)
```

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify MySQL is running
   - Check database credentials
   - Ensure database exists

2. **Import Errors**
   - Activate virtual environment
   - Install requirements: `pip install -r requirements.txt`

3. **Port Already in Use**
   - Change port in `app.py`: `app.run(port=5001)`
   - Kill existing process: `netstat -ano | findstr :5000`

4. **Permission Denied**
   - Check file permissions
   - Run as administrator (Windows)
   - Use `sudo` (Linux/macOS)

### Logs
Check console output for error messages and debugging information.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the documentation

## 🔄 Updates

To update the system:
1. Pull latest changes: `git pull origin main`
2. Update dependencies: `pip install -r requirements.txt`
3. Restart the application

## 📈 Future Enhancements

- **Multi-language Support**: Internationalization
- **Advanced Analytics**: Charts and graphs
- **Email Notifications**: Automated alerts
- **Mobile App**: Native mobile application
- **API Integration**: Third-party service integration
- **Backup System**: Automated database backups

---

**Built with ❤️ for building materials businesses**

*This system is designed to be simple yet powerful, helping you manage your building materials shop efficiently and grow your business.*

