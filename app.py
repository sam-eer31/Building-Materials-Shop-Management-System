from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta
import csv
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import os
from config import config
from sqlalchemy.exc import IntegrityError, OperationalError

app = Flask(__name__)

# Load configuration
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Language Support
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'hi': 'हिंदी',
    'ur': 'اردو'
}

DEFAULT_LANGUAGE = 'en'

# Translation dictionaries
TRANSLATIONS = {
    'en': {
        # Navigation
        'dashboard': 'Dashboard',
        'customers': 'Customers',
        'products': 'Products',
        'orders': 'Orders',
        'payments': 'Payments',
        'reports': 'Reports',
        'settings': 'Settings',
        'logout': 'Logout',
        
        # Dashboard
        'total_customers': 'Total Customers',
        'total_products': 'Total Products',
        'monthly_sales': 'Monthly Sales',
        'pending_payments': 'Pending Payments',
        'orders_received_today': 'Orders Received Today',
        'low_stock_alert': 'Low Stock Alert',
        'quick_actions': 'Quick Actions',
        'add_customer': 'Add Customer',
        'add_product': 'Add Product',
        'new_order': 'New Order',
        'view_reports': 'View Reports',
        'pending_deliveries': 'Pending Deliveries',
        'view_all_orders': 'View All Orders',
        'no_pending_deliveries': 'No pending deliveries for today and tomorrow!',
        'all_products_sufficient_stock': 'All products have sufficient stock!',
        
        # Table Headers
        'order_id': 'Order ID',
        'customer': 'Customer',
        'order_date': 'Order Date',
        'delivery_date': 'Delivery Date',
        'amount': 'Amount',
        'payment_status': 'Payment Status',
        'delivery_address': 'Delivery Address',
        'product': 'Product',
        'current_stock': 'Current Stock',
        'unit': 'Unit',
        'name': 'Name',
        'phone': 'Phone',
        'address': 'Address',
        
        # Status and Badges
        'today': 'TODAY',
        'tomorrow': 'TOMORROW',
        'other': 'OTHER',
        'not_specified': 'Not specified',
        'paid': 'Paid',
        'unpaid': 'Unpaid',
        'partial': 'Partial',
        
        # Actions and Buttons
        'view_order_details': 'View Order Details',
        'generate_invoice': 'Generate Invoice',
        'view_order': 'View Order',
        'loading_pending_deliveries': 'Loading pending deliveries...',
        'failed_to_load_deliveries': 'Failed to load pending deliveries.',
        
        # Form Labels and Placeholders
        'enter_customer_name': 'Enter customer\'s full name',
        'enter_phone_number': 'Enter phone number',
        'enter_complete_address': 'Enter complete address',
        
        # Products
        'product_inventory_management': 'Product & Inventory Management',
        'add_product': 'Add Product',
        'search_products': 'Search products...',
        'product_name': 'Product Name',
        'price_per_unit': 'Price per Unit',
        'stock_quantity': 'Stock Quantity',
        'unit': 'Unit',
        'status': 'Status',
        'low_stock': 'Low Stock',
        'medium_stock': 'Medium Stock',
        'in_stock': 'In Stock',
        'add_new_product': 'Add New Product',
        'edit_product': 'Edit Product',
        'save_product': 'Save Product',
        'update_product': 'Update Product',
        'delete_product': 'Delete Product',
        'confirm_delete_product': 'Confirm Product Deletion',
        'delete_product_warning': 'Are you sure you want to delete product',
        'product_added_successfully': 'Product added successfully!',
        'product_updated_successfully': 'Product updated successfully!',
        'product_deleted_successfully': 'Product deleted successfully!',
        'failed_to_add_product': 'Failed to add product.',
        'failed_to_update_product': 'Failed to update product.',
        'failed_to_delete_product': 'Failed to delete product.',
        
        # Orders
        'order_management': 'Order Management',
        'new_order': 'New Order',
        'search_orders': 'Search orders...',
        'order_date': 'Order Date',
        'delivery_date': 'Delivery Date',
        'total_amount': 'Total Amount',
        'payment_status': 'Payment Status',
        'delivery_address': 'Delivery Address',
        'add_new_order': 'Add New Order',
        'edit_order': 'Edit Order',
        'save_order': 'Save Order',
        'update_order': 'Update Order',
        'delete_order': 'Delete Order',
        'confirm_delete_order': 'Confirm Order Deletion',
        'delete_order_warning': 'Are you sure you want to delete order',
        'order_added_successfully': 'Order added successfully!',
        'order_updated_successfully': 'Order updated successfully!',
        'order_deleted_successfully': 'Order deleted successfully!',
        'failed_to_add_order': 'Failed to add order.',
        'failed_to_update_order': 'Failed to update order.',
        'failed_to_delete_order': 'Failed to delete order.',
        
        # Payments
        'payment_management': 'Payment Management',
        'add_payment': 'Add Payment',
        'search_payments': 'Search payments...',
        'payment_date': 'Payment Date',
        'payment_method': 'Payment Method',
        'notes': 'Notes',
        'add_new_payment': 'Add New Payment',
        'edit_payment': 'Edit Payment',
        'save_payment': 'Save Payment',
        'update_payment': 'Update Payment',
        'delete_payment': 'Delete Payment',
        'confirm_delete_payment': 'Confirm Payment Deletion',
        'delete_payment_warning': 'Are you sure you want to delete payment',
        'payment_added_successfully': 'Payment added successfully!',
        'payment_updated_successfully': 'Payment updated successfully!',
        'payment_deleted_successfully': 'Payment deleted successfully!',
        'failed_to_add_payment': 'Failed to add payment.',
        'failed_to_update_payment': 'Failed to update payment.',
        'failed_to_delete_payment': 'Failed to delete payment.',
        
        # Reports
        'reports': 'Reports',
        'sales_report': 'Sales Report',
        'inventory_report': 'Inventory Report',
        'customer_report': 'Customer Report',
        'generate_report': 'Generate Report',
        'export_report': 'Export Report',
        'date_range': 'Date Range',
        'start_date': 'Start Date',
        'end_date': 'End Date',
        'filter': 'Filter',
        'reset': 'Reset',
        
        # Payment Summary Cards
        'total_outstanding': 'Total Outstanding',
        'total_paid': 'Total Paid',
        'partial_payments': 'Partial Payments',
        'customers_with_debt': 'Customers with Debt',
        'outstanding_orders': 'Outstanding Orders',
        'all_orders_payment_status': 'All Orders & Payment Status',
        'payment_history': 'Payment History',
        'paid_amount': 'Paid Amount',
        'outstanding': 'Outstanding',
        'record_payment': 'Record Payment',
        'payment_amount': 'Payment Amount',
        'payment_method': 'Payment Method',
        'cash': 'Cash',
        'bank_transfer': 'Bank Transfer',
        'cheque': 'Cheque',
        'upi': 'UPI',
        'other': 'Other',
        'payment_notes': 'Payment Notes',
        'record_new_payment': 'Record New Payment',
        'edit_payment_record': 'Edit Payment Record',
        'confirm_delete_payment_record': 'Confirm Payment Deletion',
        'delete_payment_record_warning': 'Are you sure you want to delete this payment record',
        'payment_recorded_successfully': 'Payment recorded successfully!',
        'payment_updated_successfully': 'Payment updated successfully!',
        'payment_deleted_successfully': 'Payment deleted successfully!',
        'failed_to_record_payment': 'Failed to record payment.',
        'failed_to_update_payment_record': 'Failed to update payment record.',
        'failed_to_delete_payment_record': 'Failed to delete payment record.',
        
        # Reports
        'report_filters': 'Report Filters',
        'report_type': 'Report Type',
        'sales_report': 'Sales Report',
        'customer_report': 'Customer Report',
        'product_report': 'Product Report',
        'report_results': 'Report Results',
        'select_date_range_generate': 'Select date range and click "Generate Report" to view data',
        'total_sales': 'Total Sales',
        'total_orders': 'Total Orders',
        'unique_customers': 'Unique Customers',
        'average_order_value': 'Average Order Value',
        'quick_reports': 'Quick Reports',
        'today_sales': 'Today\'s Sales',
        'this_week_sales': 'This Week\'s Sales',
        'this_month_sales': 'This Month\'s Sales',
        'top_customers': 'Top Customers',
        'top_products': 'Top Products',
        'low_stock_products': 'Low Stock Products',
        'top_performers': 'Top Performers',
        'generate_report_see_top_performers': 'Generate a report to see top performers',
        'select_order': 'Select Order',
        'payment_id': 'Payment ID',
        
        # Order Modal
        'create_new_order': 'Create New Order',
        'select_customer': 'Select Customer',
        'delivery_date': 'Delivery Date',
        'delivery_address': 'Delivery Address',
        'order_items': 'Order Items',
        'add_item': 'Add Item',
        'product': 'Product',
        'quantity': 'Quantity',
        'price': 'Price',
        'subtotal': 'Subtotal',
        'total': 'Total',
        'save_order': 'Save Order',
        'edit_order': 'Edit Order',
        'update_order': 'Update Order',
        'confirm_delete_order': 'Confirm Order Deletion',
        'delete_order_warning': 'Are you sure you want to delete this order',
        'order_deleted_successfully': 'Order deleted successfully!',
        'failed_to_delete_order': 'Failed to delete order.',
        
        # Payment Modal
        'payment_amount': 'Payment Amount',
        'payment_date': 'Payment Date',
        'payment_notes': 'Payment Notes',
        'record_new_payment': 'Record New Payment',
        'edit_payment_record': 'Edit Payment Record',
        'update_payment': 'Update Payment',
        'confirm_delete_payment_record': 'Confirm Payment Deletion',
        'delete_payment_record_warning': 'Are you sure you want to delete this payment record',
        'payment_recorded_successfully': 'Payment recorded successfully!',
        'payment_updated_successfully': 'Payment updated successfully!',
        'payment_deleted_successfully': 'Payment deleted successfully!',
        'failed_to_record_payment': 'Failed to record payment.',
        'failed_to_update_payment_record': 'Failed to update payment record.',
        'failed_to_delete_payment_record': 'Failed to delete payment record.',
        
        # Payment Methods
        'cash': 'Cash',
        'bank_transfer': 'Bank Transfer',
        'cheque': 'Cheque',
        'upi': 'UPI',
        'other': 'Other',
        
        # Status Tags
        'paid': 'Paid',
        'unpaid': 'Unpaid',
        'partial': 'Partial',
        
        # Report Table Headers
        'rank': 'Rank',
        'customer_name': 'Customer Name',
        'product_name': 'Product Name',
        'sales_amount': 'Sales Amount',
        'order_count': 'Order Count',
        'stock_level': 'Stock Level',
        'revenue': 'Revenue',
        'profit': 'Profit',
        'margin': 'Margin',
        'please_select_dates': 'Please select both start and end dates.',
        'start_date_after_end': 'Start date cannot be after end date.',
        'generating_report': 'Generating report...',
        'loading': 'Loading...',
        
        # Empty State Messages
        'no_data_found': 'No data found',
        'no_products_found': 'No products found. Add your first product to get started.',
        'no_orders_found': 'No orders found. Create your first order to get started.',
        'no_customers_found': 'No customers found. Add your first customer to get started.',
        'no_payments_found': 'No payments found. Record your first payment to get started.',
        'no_reports_data': 'No data found for the selected date range',
        'no_outstanding_orders': 'No outstanding orders found.',
        'no_payment_history': 'No payment history found.',
        'no_pending_deliveries': 'No pending deliveries found.',
        'no_low_stock_products': 'No low stock products found.',
        
        # App Name
        'app_name': 'Building Materials Shop',
        'management_system': 'Management System',
        
        # Customer Management
        'customer_management': 'Customer Management',
        'customer_directory': 'Customer Directory',
        'search_customers': 'Search customers by name, phone, or address...',
        'total_customers_count': 'Total customers',
        'add_new_customer': 'Add New Customer',
        'edit_customer': 'Edit Customer',
        'customer_name': 'Customer Name',
        'phone_number': 'Phone Number',
        'address': 'Address',
        'save_customer': 'Save Customer',
        'update_customer': 'Update Customer',
        'delete_customer': 'Delete Customer',
        'confirm_deletion': 'Confirm Deletion',
        'delete_customer_warning': 'Are you sure you want to delete customer',
        'delete_warning': 'This action cannot be undone and will remove all associated data.',
        'export': 'Export',
        'no_customers_found': 'No customers found',
        'try_adjusting_search': 'Try adjusting your search criteria',
        
        # Common Actions
        'actions': 'Actions',
        'edit': 'Edit',
        'delete': 'Delete',
        'save': 'Save',
        'cancel': 'Cancel',
        'close': 'Close',
        'search': 'Search',
        'export_data': 'Export Data',
        'loading': 'Loading...',
        'no_data_found': 'No data found',
        
        # Messages
        'customer_added_successfully': 'Customer added successfully!',
        'customer_updated_successfully': 'Customer updated successfully!',
        'customer_deleted_successfully': 'Customer deleted successfully!',
        'failed_to_add_customer': 'Failed to add customer.',
        'failed_to_update_customer': 'Failed to update customer.',
        'failed_to_delete_customer': 'Failed to delete customer.',
        'please_fill_required_fields': 'Please fill in all required fields.',
        'server_error_occurred': 'A server error occurred. Please try again later.',
        'network_error': 'Network error. Please check your connection and try again.',
        
        # Settings
        'theme': 'Theme',
        'language': 'Language',
        'choose_theme': 'Choose between light and dark themes',
        'choose_language': 'Select your preferred language',
        'more_settings_coming': 'More settings coming soon...',
        
        # Form Labels
        'enter_customer_name': 'Enter customer\'s full name',
        'enter_phone_number': 'Enter phone number',
        'enter_complete_address': 'Enter complete address',
        'required': 'Required',
    },
    
    'hi': {
        # Navigation
        'dashboard': 'डैशबोर्ड',
        'customers': 'ग्राहक',
        'products': 'उत्पाद',
        'orders': 'ऑर्डर',
        'payments': 'भुगतान',
        'reports': 'रिपोर्ट',
        'settings': 'सेटिंग्स',
        'logout': 'लॉगआउट',
        
        # Dashboard
        'total_customers': 'कुल ग्राहक',
        'total_products': 'कुल उत्पाद',
        'monthly_sales': 'मासिक बिक्री',
        'pending_payments': 'बकाया भुगतान',
        'orders_received_today': 'आज प्राप्त ऑर्डर',
        'low_stock_alert': 'कम स्टॉक चेतावनी',
        'quick_actions': 'त्वरित कार्य',
        'add_customer': 'ग्राहक जोड़ें',
        'add_product': 'उत्पाद जोड़ें',
        'new_order': 'नया ऑर्डर',
        'view_reports': 'रिपोर्ट देखें',
        'pending_deliveries': 'बकाया डिलीवरी',
        'view_all_orders': 'सभी ऑर्डर देखें',
        'no_pending_deliveries': 'आज और कल के लिए कोई बकाया डिलीवरी नहीं!',
        'all_products_sufficient_stock': 'सभी उत्पादों में पर्याप्त स्टॉक है!',
        
        # Table Headers
        'order_id': 'ऑर्डर आईडी',
        'customer': 'ग्राहक',
        'order_date': 'ऑर्डर तिथि',
        'delivery_date': 'डिलीवरी तिथि',
        'amount': 'राशि',
        'payment_status': 'भुगतान स्थिति',
        'delivery_address': 'डिलीवरी पता',
        'product': 'उत्पाद',
        'current_stock': 'वर्तमान स्टॉक',
        'unit': 'इकाई',
        'name': 'नाम',
        'phone': 'फोन',
        'address': 'पता',
        
        # Status and Badges
        'today': 'आज',
        'tomorrow': 'कल',
        'other': 'अन्य',
        'not_specified': 'निर्दिष्ट नहीं',
        'paid': 'भुगतान किया',
        'unpaid': 'बकाया',
        'partial': 'आंशिक',
        
        # Actions and Buttons
        'view_order_details': 'ऑर्डर विवरण देखें',
        'generate_invoice': 'चालान बनाएं',
        'view_order': 'ऑर्डर देखें',
        'loading_pending_deliveries': 'बकाया डिलीवरी लोड हो रही है...',
        'failed_to_load_deliveries': 'बकाया डिलीवरी लोड करने में विफल।',
        
        # Form Labels and Placeholders
        'enter_customer_name': 'ग्राहक का पूरा नाम दर्ज करें',
        'enter_phone_number': 'फोन नंबर दर्ज करें',
        'enter_complete_address': 'पूरा पता दर्ज करें',
        
        # Products
        'product_inventory_management': 'उत्पाद और इन्वेंटरी प्रबंधन',
        'add_product': 'उत्पाद जोड़ें',
        'search_products': 'उत्पाद खोजें...',
        'product_name': 'उत्पाद का नाम',
        'price_per_unit': 'प्रति इकाई मूल्य',
        'stock_quantity': 'स्टॉक मात्रा',
        'unit': 'इकाई',
        'status': 'स्थिति',
        'low_stock': 'कम स्टॉक',
        'medium_stock': 'मध्यम स्टॉक',
        'in_stock': 'स्टॉक में',
        'add_new_product': 'नया उत्पाद जोड़ें',
        'edit_product': 'उत्पाद संपादित करें',
        'save_product': 'उत्पाद सहेजें',
        'update_product': 'उत्पाद अपडेट करें',
        'delete_product': 'उत्पाद हटाएं',
        'confirm_delete_product': 'उत्पाद हटाने की पुष्टि करें',
        'delete_product_warning': 'क्या आप वाकई उत्पाद को हटाना चाहते हैं',
        'product_added_successfully': 'उत्पाद सफलतापूर्वक जोड़ा गया!',
        'product_updated_successfully': 'उत्पाद सफलतापूर्वक अपडेट किया गया!',
        'product_deleted_successfully': 'उत्पाद सफलतापूर्वक हटा दिया गया!',
        'failed_to_add_product': 'उत्पाद जोड़ने में विफल।',
        'failed_to_update_product': 'उत्पाद अपडेट करने में विफल।',
        'failed_to_delete_product': 'उत्पाद हटाने में विफल।',
        
        # Orders
        'order_management': 'ऑर्डर प्रबंधन',
        'new_order': 'नया ऑर्डर',
        'search_orders': 'ऑर्डर खोजें...',
        'order_date': 'ऑर्डर तिथि',
        'delivery_date': 'डिलीवरी तिथि',
        'total_amount': 'कुल राशि',
        'payment_status': 'भुगतान स्थिति',
        'delivery_address': 'डिलीवरी पता',
        'add_new_order': 'नया ऑर्डर जोड़ें',
        'edit_order': 'ऑर्डर संपादित करें',
        'save_order': 'ऑर्डर सहेजें',
        'update_order': 'ऑर्डर अपडेट करें',
        'delete_order': 'ऑर्डर हटाएं',
        'confirm_delete_order': 'ऑर्डर हटाने की पुष्टि करें',
        'delete_order_warning': 'क्या आप वाकई ऑर्डर को हटाना चाहते हैं',
        'order_added_successfully': 'ऑर्डर सफलतापूर्वक जोड़ा गया!',
        'order_updated_successfully': 'ऑर्डर सफलतापूर्वक अपडेट किया गया!',
        'order_deleted_successfully': 'ऑर्डर सफलतापूर्वक हटा दिया गया!',
        'failed_to_add_order': 'ऑर्डर जोड़ने में विफल।',
        'failed_to_update_order': 'ऑर्डर अपडेट करने में विफल।',
        'failed_to_delete_order': 'ऑर्डर हटाने में विफल।',
        
        # Payments
        'payment_management': 'भुगतान प्रबंधन',
        'add_payment': 'भुगतान जोड़ें',
        'search_payments': 'भुगतान खोजें...',
        'payment_date': 'भुगतान तिथि',
        'payment_method': 'भुगतान विधि',
        'notes': 'टिप्पणियां',
        'add_new_payment': 'नया भुगतान जोड़ें',
        'edit_payment': 'भुगतान संपादित करें',
        'save_payment': 'भुगतान सहेजें',
        'update_payment': 'भुगतान अपडेट करें',
        'delete_payment': 'भुगतान हटाएं',
        'confirm_delete_payment': 'भुगतान हटाने की पुष्टि करें',
        'delete_payment_warning': 'क्या आप वाकई भुगतान को हटाना चाहते हैं',
        'payment_added_successfully': 'भुगतान सफलतापूर्वक जोड़ा गया!',
        'payment_updated_successfully': 'भुगतान सफलतापूर्वक अपडेट किया गया!',
        'payment_deleted_successfully': 'भुगतान सफलतापूर्वक हटा दिया गया!',
        'failed_to_add_payment': 'भुगतान जोड़ने में विफल।',
        'failed_to_update_payment': 'भुगतान अपडेट करने में विफल।',
        'failed_to_delete_payment': 'भुगतान हटाने में विफल।',
        
        # Reports
        'reports': 'रिपोर्ट',
        'sales_report': 'बिक्री रिपोर्ट',
        'inventory_report': 'इन्वेंटरी रिपोर्ट',
        'customer_report': 'ग्राहक रिपोर्ट',
        'generate_report': 'रिपोर्ट बनाएं',
        'export_report': 'रिपोर्ट निर्यात करें',
        'date_range': 'तिथि सीमा',
        'start_date': 'प्रारंभ तिथि',
        'end_date': 'समाप्ति तिथि',
        'filter': 'फ़िल्टर',
        'reset': 'रीसेट',
        
        # Payment Summary Cards
        'total_outstanding': 'कुल बकाया',
        'total_paid': 'कुल भुगतान',
        'partial_payments': 'आंशिक भुगतान',
        'customers_with_debt': 'ऋण वाले ग्राहक',
        'outstanding_orders': 'बकाया ऑर्डर',
        'all_orders_payment_status': 'सभी ऑर्डर और भुगतान स्थिति',
        'payment_history': 'भुगतान इतिहास',
        'paid_amount': 'भुगतान की गई राशि',
        'outstanding': 'बकाया',
        'record_payment': 'भुगतान दर्ज करें',
        'payment_amount': 'भुगतान राशि',
        'payment_method': 'भुगतान विधि',
        'cash': 'नकद',
        'bank_transfer': 'बैंक ट्रांसफर',
        'cheque': 'चेक',
        'upi': 'यूपीआई',
        'other': 'अन्य',
        'payment_notes': 'भुगतान नोट्स',
        'record_new_payment': 'नया भुगतान दर्ज करें',
        'edit_payment_record': 'भुगतान रिकॉर्ड संपादित करें',
        'confirm_delete_payment_record': 'भुगतान हटाने की पुष्टि करें',
        'delete_payment_record_warning': 'क्या आप वाकई इस भुगतान रिकॉर्ड को हटाना चाहते हैं',
        'payment_recorded_successfully': 'भुगतान सफलतापूर्वक दर्ज किया गया!',
        'payment_updated_successfully': 'भुगतान सफलतापूर्वक अपडेट किया गया!',
        'payment_deleted_successfully': 'भुगतान सफलतापूर्वक हटा दिया गया!',
        'failed_to_record_payment': 'भुगतान दर्ज करने में विफल।',
        'failed_to_update_payment_record': 'भुगतान रिकॉर्ड अपडेट करने में विफल।',
        'failed_to_delete_payment_record': 'भुगतान रिकॉर्ड हटाने में विफल।',
        
        # Reports
        'report_filters': 'रिपोर्ट फ़िल्टर',
        'report_type': 'रिपोर्ट प्रकार',
        'sales_report': 'बिक्री रिपोर्ट',
        'customer_report': 'ग्राहक रिपोर्ट',
        'product_report': 'उत्पाद रिपोर्ट',
        'report_results': 'रिपोर्ट परिणाम',
        'select_date_range_generate': 'डेटा देखने के लिए तिथि सीमा चुनें और "रिपोर्ट बनाएं" पर क्लिक करें',
        'total_sales': 'कुल बिक्री',
        'total_orders': 'कुल ऑर्डर',
        'unique_customers': 'अद्वितीय ग्राहक',
        'average_order_value': 'औसत ऑर्डर मूल्य',
        'quick_reports': 'त्वरित रिपोर्ट',
        'today_sales': 'आज की बिक्री',
        'this_week_sales': 'इस सप्ताह की बिक्री',
        'this_month_sales': 'इस महीने की बिक्री',
        'top_customers': 'शीर्ष ग्राहक',
        'top_products': 'शीर्ष उत्पाद',
        'low_stock_products': 'कम स्टॉक वाले उत्पाद',
        'top_performers': 'शीर्ष प्रदर्शनकर्ता',
        'generate_report_see_top_performers': 'शीर्ष प्रदर्शनकर्ताओं को देखने के लिए रिपोर्ट बनाएं',
        'select_order': 'ऑर्डर चुनें',
        'payment_id': 'भुगतान आईडी',
        
        # Order Modal
        'create_new_order': 'नया ऑर्डर बनाएं',
        'select_customer': 'ग्राहक चुनें',
        'delivery_date': 'डिलीवरी तिथि',
        'delivery_address': 'डिलीवरी पता',
        'order_items': 'ऑर्डर आइटम',
        'add_item': 'आइटम जोड़ें',
        'product': 'उत्पाद',
        'quantity': 'मात्रा',
        'price': 'मूल्य',
        'subtotal': 'उप-कुल',
        'total': 'कुल',
        'save_order': 'ऑर्डर सहेजें',
        'edit_order': 'ऑर्डर संपादित करें',
        'update_order': 'ऑर्डर अपडेट करें',
        'confirm_delete_order': 'ऑर्डर हटाने की पुष्टि करें',
        'delete_order_warning': 'क्या आप वाकई इस ऑर्डर को हटाना चाहते हैं',
        'order_deleted_successfully': 'ऑर्डर सफलतापूर्वक हटा दिया गया!',
        'failed_to_delete_order': 'ऑर्डर हटाने में विफल।',
        
        # Payment Modal
        'payment_amount': 'भुगतान राशि',
        'payment_date': 'भुगतान तिथि',
        'payment_notes': 'भुगतान नोट्स',
        'record_new_payment': 'नया भुगतान दर्ज करें',
        'edit_payment_record': 'भुगतान रिकॉर्ड संपादित करें',
        'update_payment': 'भुगतान अपडेट करें',
        'confirm_delete_payment_record': 'भुगतान हटाने की पुष्टि करें',
        'delete_payment_record_warning': 'क्या आप वाकई इस भुगतान रिकॉर्ड को हटाना चाहते हैं',
        'payment_recorded_successfully': 'भुगतान सफलतापूर्वक दर्ज किया गया!',
        'payment_updated_successfully': 'भुगतान सफलतापूर्वक अपडेट किया गया!',
        'payment_deleted_successfully': 'भुगतान सफलतापूर्वक हटा दिया गया!',
        'failed_to_record_payment': 'भुगतान दर्ज करने में विफल।',
        'failed_to_update_payment_record': 'भुगतान रिकॉर्ड अपडेट करने में विफल।',
        'failed_to_delete_payment_record': 'भुगतान रिकॉर्ड हटाने में विफल।',
        
        # Payment Methods
        'cash': 'नकद',
        'bank_transfer': 'बैंक ट्रांसफर',
        'cheque': 'चेक',
        'upi': 'यूपीआई',
        'other': 'अन्य',
        
        # Status Tags
        'paid': 'भुगतान किया गया',
        'unpaid': 'अभुगतान',
        'partial': 'आंशिक',
        
        # Report Table Headers
        'rank': 'रैंक',
        'customer_name': 'ग्राहक का नाम',
        'product_name': 'उत्पाद का नाम',
        'sales_amount': 'बिक्री राशि',
        'order_count': 'ऑर्डर संख्या',
        'stock_level': 'स्टॉक स्तर',
        'revenue': 'राजस्व',
        'profit': 'लाभ',
        'margin': 'मार्जिन',
        'please_select_dates': 'कृपया प्रारंभ और समाप्ति तिथि दोनों चुनें।',
        'start_date_after_end': 'प्रारंभ तिथि समाप्ति तिथि के बाद नहीं हो सकती।',
        'generating_report': 'रिपोर्ट बना रहा है...',
        'loading': 'लोड हो रहा है...',
        
        # Empty State Messages
        'no_data_found': 'कोई डेटा नहीं मिला',
        'no_products_found': 'कोई उत्पाद नहीं मिला। शुरू करने के लिए अपना पहला उत्पाद जोड़ें।',
        'no_orders_found': 'कोई ऑर्डर नहीं मिला। शुरू करने के लिए अपना पहला ऑर्डर बनाएं।',
        'no_customers_found': 'कोई ग्राहक नहीं मिला। शुरू करने के लिए अपना पहला ग्राहक जोड़ें।',
        'no_payments_found': 'कोई भुगतान नहीं मिला। शुरू करने के लिए अपना पहला भुगतान दर्ज करें।',
        'no_reports_data': 'चयनित तिथि सीमा के लिए कोई डेटा नहीं मिला',
        'no_outstanding_orders': 'कोई बकाया ऑर्डर नहीं मिला।',
        'no_payment_history': 'कोई भुगतान इतिहास नहीं मिला।',
        'no_pending_deliveries': 'कोई लंबित डिलीवरी नहीं मिली।',
        'no_low_stock_products': 'कोई कम स्टॉक उत्पाद नहीं मिला।',
        
        # App Name
        'app_name': 'बिल्डिंग मटीरियल्स शॉप',
        'management_system': 'प्रबंधन प्रणाली',
        
        # Customer Management
        'customer_management': 'ग्राहक प्रबंधन',
        'customer_directory': 'ग्राहक निर्देशिका',
        'search_customers': 'नाम, फोन या पते से ग्राहक खोजें...',
        'total_customers_count': 'कुल ग्राहक',
        'add_new_customer': 'नया ग्राहक जोड़ें',
        'edit_customer': 'ग्राहक संपादित करें',
        'customer_name': 'ग्राहक का नाम',
        'phone_number': 'फोन नंबर',
        'address': 'पता',
        'save_customer': 'ग्राहक सहेजें',
        'update_customer': 'ग्राहक अपडेट करें',
        'delete_customer': 'ग्राहक हटाएं',
        'confirm_deletion': 'हटाने की पुष्टि करें',
        'delete_customer_warning': 'क्या आप वाकई ग्राहक को हटाना चाहते हैं',
        'delete_warning': 'यह कार्य पूर्ववत नहीं किया जा सकता और सभी संबंधित डेटा हटा देगा।',
        'export': 'निर्यात',
        'no_customers_found': 'कोई ग्राहक नहीं मिला',
        'try_adjusting_search': 'अपने खोज मानदंड को समायोजित करने का प्रयास करें',
        
        # Common Actions
        'actions': 'कार्य',
        'edit': 'संपादित करें',
        'delete': 'हटाएं',
        'save': 'सहेजें',
        'cancel': 'रद्द करें',
        'close': 'बंद करें',
        'search': 'खोजें',
        'export_data': 'डेटा निर्यात करें',
        'loading': 'लोड हो रहा है...',
        'no_data_found': 'कोई डेटा नहीं मिला',
        
        # Messages
        'customer_added_successfully': 'ग्राहक सफलतापूर्वक जोड़ा गया!',
        'customer_updated_successfully': 'ग्राहक सफलतापूर्वक अपडेट किया गया!',
        'customer_deleted_successfully': 'ग्राहक सफलतापूर्वक हटा दिया गया!',
        'failed_to_add_customer': 'ग्राहक जोड़ने में विफल।',
        'failed_to_update_customer': 'ग्राहक अपडेट करने में विफल।',
        'failed_to_delete_customer': 'ग्राहक हटाने में विफल।',
        'please_fill_required_fields': 'कृपया सभी आवश्यक फ़ील्ड भरें।',
        'server_error_occurred': 'सर्वर त्रुटि हुई। कृपया बाद में पुनः प्रयास करें।',
        'network_error': 'नेटवर्क त्रुटि। कृपया अपना कनेक्शन जांचें और पुनः प्रयास करें।',
        
        # Settings
        'theme': 'थीम',
        'language': 'भाषा',
        'choose_theme': 'हल्की और गहरी थीम के बीच चुनें',
        'choose_language': 'अपनी पसंदीदा भाषा चुनें',
        'more_settings_coming': 'अधिक सेटिंग्स जल्द आ रही हैं...',
        
        # Form Labels
        'enter_customer_name': 'ग्राहक का पूरा नाम दर्ज करें',
        'enter_phone_number': 'फोन नंबर दर्ज करें',
        'enter_complete_address': 'पूरा पता दर्ज करें',
        'required': 'आवश्यक',
    },
    
    'ur': {
        # Navigation
        'dashboard': 'ڈیش بورڈ',
        'customers': 'گاہک',
        'products': 'مصنوعات',
        'orders': 'آرڈر',
        'payments': 'ادائیگی',
        'reports': 'رپورٹس',
        'settings': 'ترتیبات',
        'logout': 'لاگ آؤٹ',
        
        # Dashboard
        'total_customers': 'کل گاہک',
        'total_products': 'کل مصنوعات',
        'monthly_sales': 'ماہانہ فروخت',
        'pending_payments': 'زیر التواء ادائیگی',
        'orders_received_today': 'آج موصولہ آرڈر',
        'low_stock_alert': 'کم اسٹاک الرٹ',
        'quick_actions': 'فوری اقدامات',
        'add_customer': 'گاہک شامل کریں',
        'add_product': 'مصنوعات شامل کریں',
        'new_order': 'نیا آرڈر',
        'view_reports': 'رپورٹس دیکھیں',
        'pending_deliveries': 'زیر التواء ترسیل',
        'view_all_orders': 'تمام آرڈر دیکھیں',
        'no_pending_deliveries': 'آج اور کل کے لیے کوئی زیر التواء ترسیل نہیں!',
        'all_products_sufficient_stock': 'تمام مصنوعات میں کافی اسٹاک ہے!',
        
        # Table Headers
        'order_id': 'آرڈر آئی ڈی',
        'customer': 'گاہک',
        'order_date': 'آرڈر کی تاریخ',
        'delivery_date': 'ترسیل کی تاریخ',
        'amount': 'رقم',
        'payment_status': 'ادائیگی کی حالت',
        'delivery_address': 'ترسیل کا پتہ',
        'product': 'مصنوعات',
        'current_stock': 'موجودہ اسٹاک',
        'unit': 'یونٹ',
        'name': 'نام',
        'phone': 'فون',
        'address': 'پتہ',
        
        # Status and Badges
        'today': 'آج',
        'tomorrow': 'کل',
        'other': 'دیگر',
        'not_specified': 'متعلق نہیں',
        'paid': 'ادا شدہ',
        'unpaid': 'غیر ادا شدہ',
        'partial': 'جزوی',
        
        # Actions and Buttons
        'view_order_details': 'آرڈر کی تفصیلات دیکھیں',
        'generate_invoice': 'انوائس بنائیں',
        'view_order': 'آرڈر دیکھیں',
        'loading_pending_deliveries': 'زیر التواء ترسیل لوڈ ہو رہی ہے...',
        'failed_to_load_deliveries': 'زیر التواء ترسیل لوڈ کرنے میں ناکام۔',
        
        # Form Labels and Placeholders
        'enter_customer_name': 'گاہک کا مکمل نام درج کریں',
        'enter_phone_number': 'فون نمبر درج کریں',
        'enter_complete_address': 'مکمل پتہ درج کریں',
        
        # Products
        'product_inventory_management': 'مصنوعات اور انوینٹری کا انتظام',
        'add_product': 'مصنوعات شامل کریں',
        'search_products': 'مصنوعات تلاش کریں...',
        'product_name': 'مصنوعات کا نام',
        'price_per_unit': 'فی یونٹ قیمت',
        'stock_quantity': 'اسٹاک کی مقدار',
        'unit': 'یونٹ',
        'status': 'حیثیت',
        'low_stock': 'کم اسٹاک',
        'medium_stock': 'درمیانی اسٹاک',
        'in_stock': 'اسٹاک میں',
        'add_new_product': 'نیا مصنوعات شامل کریں',
        'edit_product': 'مصنوعات میں ترمیم کریں',
        'save_product': 'مصنوعات محفوظ کریں',
        'update_product': 'مصنوعات اپ ڈیٹ کریں',
        'delete_product': 'مصنوعات حذف کریں',
        'confirm_delete_product': 'مصنوعات حذف کرنے کی تصدیق کریں',
        'delete_product_warning': 'کیا آپ واقعی مصنوعات کو حذف کرنا چاہتے ہیں',
        'product_added_successfully': 'مصنوعات کامیابی سے شامل کر دیا گیا!',
        'product_updated_successfully': 'مصنوعات کامیابی سے اپ ڈیٹ کر دیا گیا!',
        'product_deleted_successfully': 'مصنوعات کامیابی سے حذف کر دیا گیا!',
        'failed_to_add_product': 'مصنوعات شامل کرنے میں ناکام۔',
        'failed_to_update_product': 'مصنوعات اپ ڈیٹ کرنے میں ناکام۔',
        'failed_to_delete_product': 'مصنوعات حذف کرنے میں ناکام۔',
        
        # Orders
        'order_management': 'آرڈر کا انتظام',
        'new_order': 'نیا آرڈر',
        'search_orders': 'آرڈر تلاش کریں...',
        'order_date': 'آرڈر کی تاریخ',
        'delivery_date': 'ترسیل کی تاریخ',
        'total_amount': 'کل رقم',
        'payment_status': 'ادائیگی کی حالت',
        'delivery_address': 'ترسیل کا پتہ',
        'add_new_order': 'نیا آرڈر شامل کریں',
        'edit_order': 'آرڈر میں ترمیم کریں',
        'save_order': 'آرڈر محفوظ کریں',
        'update_order': 'آرڈر اپ ڈیٹ کریں',
        'delete_order': 'آرڈر حذف کریں',
        'confirm_delete_order': 'آرڈر حذف کرنے کی تصدیق کریں',
        'delete_order_warning': 'کیا آپ واقعی آرڈر کو حذف کرنا چاہتے ہیں',
        'order_added_successfully': 'آرڈر کامیابی سے شامل کر دیا گیا!',
        'order_updated_successfully': 'آرڈر کامیابی سے اپ ڈیٹ کر دیا گیا!',
        'order_deleted_successfully': 'آرڈر کامیابی سے حذف کر دیا گیا!',
        'failed_to_add_order': 'آرڈر شامل کرنے میں ناکام۔',
        'failed_to_update_order': 'آرڈر اپ ڈیٹ کرنے میں ناکام۔',
        'failed_to_delete_order': 'آرڈر حذف کرنے میں ناکام۔',
        
        # Payments
        'payment_management': 'ادائیگی کا انتظام',
        'add_payment': 'ادائیگی شامل کریں',
        'search_payments': 'ادائیگی تلاش کریں...',
        'payment_date': 'ادائیگی کی تاریخ',
        'payment_method': 'ادائیگی کا طریقہ',
        'notes': 'نوٹس',
        'add_new_payment': 'نیا ادائیگی شامل کریں',
        'edit_payment': 'ادائیگی میں ترمیم کریں',
        'save_payment': 'ادائیگی محفوظ کریں',
        'update_payment': 'ادائیگی اپ ڈیٹ کریں',
        'delete_payment': 'ادائیگی حذف کریں',
        'confirm_delete_payment': 'ادائیگی حذف کرنے کی تصدیق کریں',
        'delete_payment_warning': 'کیا آپ واقعی ادائیگی کو حذف کرنا چاہتے ہیں',
        'payment_added_successfully': 'ادائیگی کامیابی سے شامل کر دیا گیا!',
        'payment_updated_successfully': 'ادائیگی کامیابی سے اپ ڈیٹ کر دیا گیا!',
        'payment_deleted_successfully': 'ادائیگی کامیابی سے حذف کر دیا گیا!',
        'failed_to_add_payment': 'ادائیگی شامل کرنے میں ناکام۔',
        'failed_to_update_payment': 'ادائیگی اپ ڈیٹ کرنے میں ناکام۔',
        'failed_to_delete_payment': 'ادائیگی حذف کرنے میں ناکام۔',
        
        # Reports
        'reports': 'رپورٹس',
        'sales_report': 'فروخت کی رپورٹ',
        'inventory_report': 'انوینٹری رپورٹ',
        'customer_report': 'گاہک کی رپورٹ',
        'generate_report': 'رپورٹ بنائیں',
        'export_report': 'رپورٹ برآمد کریں',
        'date_range': 'تاریخ کی حد',
        'start_date': 'شروع کی تاریخ',
        'end_date': 'ختم کی تاریخ',
        'filter': 'فلٹر',
        'reset': 'ری سیٹ',
        
        # Payment Summary Cards
        'total_outstanding': 'کل بقایا',
        'total_paid': 'کل ادا شدہ',
        'partial_payments': 'جزوی ادائیگی',
        'customers_with_debt': 'قرض والے گاہک',
        'outstanding_orders': 'بقایا آرڈر',
        'all_orders_payment_status': 'تمام آرڈر اور ادائیگی کی حالت',
        'payment_history': 'ادائیگی کی تاریخ',
        'paid_amount': 'ادا شدہ رقم',
        'outstanding': 'بقایا',
        'record_payment': 'ادائیگی درج کریں',
        'payment_amount': 'ادائیگی کی رقم',
        'payment_method': 'ادائیگی کا طریقہ',
        'cash': 'نقد',
        'bank_transfer': 'بینک ٹرانسفر',
        'cheque': 'چیک',
        'upi': 'یو پی آئی',
        'other': 'دیگر',
        'payment_notes': 'ادائیگی کے نوٹس',
        'record_new_payment': 'نیا ادائیگی درج کریں',
        'edit_payment_record': 'ادائیگی ریکارڈ میں ترمیم کریں',
        'confirm_delete_payment_record': 'ادائیگی حذف کرنے کی تصدیق کریں',
        'delete_payment_record_warning': 'کیا آپ واقعی اس ادائیگی ریکارڈ کو حذف کرنا چاہتے ہیں',
        'payment_recorded_successfully': 'ادائیگی کامیابی سے درج کر دیا گیا!',
        'payment_updated_successfully': 'ادائیگی کامیابی سے اپ ڈیٹ کر دیا گیا!',
        'payment_deleted_successfully': 'ادائیگی کامیابی سے حذف کر دیا گیا!',
        'failed_to_record_payment': 'ادائیگی درج کرنے میں ناکام۔',
        'failed_to_update_payment_record': 'ادائیگی ریکارڈ اپ ڈیٹ کرنے میں ناکام۔',
        'failed_to_delete_payment_record': 'ادائیگی ریکارڈ حذف کرنے میں ناکام۔',
        
        # Reports
        'report_filters': 'رپورٹ فلٹر',
        'report_type': 'رپورٹ کی قسم',
        'sales_report': 'فروخت کی رپورٹ',
        'customer_report': 'گاہک کی رپورٹ',
        'product_report': 'مصنوعات کی رپورٹ',
        'report_results': 'رپورٹ کے نتائج',
        'select_date_range_generate': 'ڈیٹا دیکھنے کے لیے تاریخ کی حد منتخب کریں اور "رپورٹ بنائیں" پر کلک کریں',
        'total_sales': 'کل فروخت',
        'total_orders': 'کل آرڈر',
        'unique_customers': 'منفرد گاہک',
        'average_order_value': 'اوسط آرڈر کی قیمت',
        'quick_reports': 'فوری رپورٹس',
        'today_sales': 'آج کی فروخت',
        'this_week_sales': 'اس ہفتے کی فروخت',
        'this_month_sales': 'اس مہینے کی فروخت',
        'top_customers': 'اہم گاہک',
        'top_products': 'اہم مصنوعات',
        'low_stock_products': 'کم اسٹاک والی مصنوعات',
        'top_performers': 'اہم کارکردگی',
        'generate_report_see_top_performers': 'اہم کارکردگی دیکھنے کے لیے رپورٹ بنائیں',
        'select_order': 'آرڈر منتخب کریں',
        'payment_id': 'ادائیگی آئی ڈی',
        
        # Order Modal
        'create_new_order': 'نیا آرڈر بنائیں',
        'select_customer': 'گاہک منتخب کریں',
        'delivery_date': 'ترسیل کی تاریخ',
        'delivery_address': 'ترسیل کا پتہ',
        'order_items': 'آرڈر آئٹمز',
        'add_item': 'آئٹم شامل کریں',
        'product': 'مصنوعات',
        'quantity': 'مقدار',
        'price': 'قیمت',
        'subtotal': 'ذیلی کل',
        'total': 'کل',
        'save_order': 'آرڈر محفوظ کریں',
        'edit_order': 'آرڈر میں ترمیم کریں',
        'update_order': 'آرڈر اپ ڈیٹ کریں',
        'confirm_delete_order': 'آرڈر حذف کرنے کی تصدیق کریں',
        'delete_order_warning': 'کیا آپ واقعی اس آرڈر کو حذف کرنا چاہتے ہیں',
        'order_deleted_successfully': 'آرڈر کامیابی سے حذف کر دیا گیا!',
        'failed_to_delete_order': 'آرڈر حذف کرنے میں ناکام۔',
        
        # Payment Modal
        'payment_amount': 'ادائیگی کی رقم',
        'payment_date': 'ادائیگی کی تاریخ',
        'payment_notes': 'ادائیگی کے نوٹس',
        'record_new_payment': 'نیا ادائیگی درج کریں',
        'edit_payment_record': 'ادائیگی ریکارڈ میں ترمیم کریں',
        'update_payment': 'ادائیگی اپ ڈیٹ کریں',
        'confirm_delete_payment_record': 'ادائیگی حذف کرنے کی تصدیق کریں',
        'delete_payment_record_warning': 'کیا آپ واقعی اس ادائیگی ریکارڈ کو حذف کرنا چاہتے ہیں',
        'payment_recorded_successfully': 'ادائیگی کامیابی سے درج کر دیا گیا!',
        'payment_updated_successfully': 'ادائیگی کامیابی سے اپ ڈیٹ کر دیا گیا!',
        'payment_deleted_successfully': 'ادائیگی کامیابی سے حذف کر دیا گیا!',
        'failed_to_record_payment': 'ادائیگی درج کرنے میں ناکام۔',
        'failed_to_update_payment_record': 'ادائیگی ریکارڈ اپ ڈیٹ کرنے میں ناکام۔',
        'failed_to_delete_payment_record': 'ادائیگی ریکارڈ حذف کرنے میں ناکام۔',
        
        # Payment Methods
        'cash': 'نقد',
        'bank_transfer': 'بینک ٹرانسفر',
        'cheque': 'چیک',
        'upi': 'یو پی آئی',
        'other': 'دیگر',
        
        # Status Tags
        'paid': 'ادا شدہ',
        'unpaid': 'غیر ادا شدہ',
        'partial': 'جزوی',
        
        # Report Table Headers
        'rank': 'درجہ',
        'customer_name': 'گاہک کا نام',
        'product_name': 'مصنوعات کا نام',
        'sales_amount': 'فروخت کی رقم',
        'order_count': 'آرڈر کی تعداد',
        'stock_level': 'اسٹاک کی سطح',
        'revenue': 'آمدنی',
        'profit': 'منافع',
        'margin': 'مارجن',
        'please_select_dates': 'براہ کرم شروع اور ختم کی تاریخ دونوں منتخب کریں۔',
        'start_date_after_end': 'شروع کی تاریخ ختم کی تاریخ کے بعد نہیں ہو سکتی۔',
        'generating_report': 'رپورٹ بنا رہا ہے...',
        'loading': 'لوڈ ہو رہا ہے...',
        
        # Empty State Messages
        'no_data_found': 'کوئی ڈیٹا نہیں ملا',
        'no_products_found': 'کوئی مصنوعات نہیں ملی۔ شروع کرنے کے لیے اپنی پہلی مصنوعات شامل کریں۔',
        'no_orders_found': 'کوئی آرڈر نہیں ملا۔ شروع کرنے کے لیے اپنا پہلا آرڈر بنائیں۔',
        'no_customers_found': 'کوئی گاہک نہیں ملا۔ شروع کرنے کے لیے اپنا پہلا گاہک شامل کریں۔',
        'no_payments_found': 'کوئی ادائیگی نہیں ملی۔ شروع کرنے کے لیے اپنی پہلی ادائیگی درج کریں۔',
        'no_reports_data': 'منتخب تاریخ کی حد کے لیے کوئی ڈیٹا نہیں ملا',
        'no_outstanding_orders': 'کوئی بقایا آرڈر نہیں ملا۔',
        'no_payment_history': 'کوئی ادائیگی کی تاریخ نہیں ملی۔',
        'no_pending_deliveries': 'کوئی زیر التوا ترسیل نہیں ملی۔',
        'no_low_stock_products': 'کوئی کم اسٹاک مصنوعات نہیں ملی۔',
        
        # App Name
        'app_name': 'بلڈنگ میٹیریلز شاپ',
        'management_system': 'انتظامی نظام',
        
        # Customer Management
        'customer_management': 'گاہک کا انتظام',
        'customer_directory': 'گاہک کی ڈائریکٹری',
        'search_customers': 'نام، فون یا پتے سے گاہک تلاش کریں...',
        'total_customers_count': 'کل گاہک',
        'add_new_customer': 'نیا گاہک شامل کریں',
        'edit_customer': 'گاہک میں ترمیم کریں',
        'customer_name': 'گاہک کا نام',
        'phone_number': 'فون نمبر',
        'address': 'پتہ',
        'save_customer': 'گاہک محفوظ کریں',
        'update_customer': 'گاہک اپ ڈیٹ کریں',
        'delete_customer': 'گاہک حذف کریں',
        'confirm_deletion': 'حذف کی تصدیق کریں',
        'delete_customer_warning': 'کیا آپ واقعی گاہک کو حذف کرنا چاہتے ہیں',
        'delete_warning': 'یہ عمل واپس نہیں کیا جا سکتا اور تمام متعلقہ ڈیٹا ہٹا دے گا۔',
        'export': 'برآمد کریں',
        'no_customers_found': 'کوئی گاہک نہیں ملا',
        'try_adjusting_search': 'اپنے تلاش کے معیارات کو ایڈجسٹ کرنے کی کوشش کریں',
        
        # Common Actions
        'actions': 'اقدامات',
        'edit': 'ترمیم کریں',
        'delete': 'حذف کریں',
        'save': 'محفوظ کریں',
        'cancel': 'منسوخ کریں',
        'close': 'بند کریں',
        'search': 'تلاش کریں',
        'export_data': 'ڈیٹا برآمد کریں',
        'loading': 'لوڈ ہو رہا ہے...',
        'no_data_found': 'کوئی ڈیٹا نہیں ملا',
        
        # Messages
        'customer_added_successfully': 'گاہک کامیابی سے شامل کر دیا گیا!',
        'customer_updated_successfully': 'گاہک کامیابی سے اپ ڈیٹ کر دیا گیا!',
        'customer_deleted_successfully': 'گاہک کامیابی سے حذف کر دیا گیا!',
        'failed_to_add_customer': 'گاہک شامل کرنے میں ناکام۔',
        'failed_to_update_customer': 'گاہک اپ ڈیٹ کرنے میں ناکام۔',
        'failed_to_delete_customer': 'گاہک حذف کرنے میں ناکام۔',
        'please_fill_required_fields': 'براہ کرم تمام مطلوبہ فیلڈز بھریں۔',
        'server_error_occurred': 'سرور کی خرابی ہوئی۔ براہ کرم بعد میں دوبارہ کوشش کریں۔',
        'network_error': 'نیٹ ورک کی خرابی۔ براہ کرم اپنا کنکشن چیک کریں اور دوبارہ کوشش کریں۔',
        
        # Settings
        'theme': 'تھیم',
        'language': 'زبان',
        'choose_theme': 'ہلکی اور گہری تھیم کے درمیان منتخب کریں',
        'choose_language': 'اپنی پسندیدہ زبان منتخب کریں',
        'more_settings_coming': 'مزید ترتیبات جلد آ رہی ہیں...',
        
        # Form Labels
        'enter_customer_name': 'گاہک کا مکمل نام درج کریں',
        'enter_phone_number': 'فون نمبر درج کریں',
        'enter_complete_address': 'مکمل پتہ درج کریں',
        'required': 'مطلوبہ',
    }
}

def get_language():
    """Get current language from session or default"""
    return session.get('language', DEFAULT_LANGUAGE)

def set_language(language):
    """Set language in session"""
    if language in SUPPORTED_LANGUAGES:
        session['language'] = language
        return True
    return False

def t(key, language=None):
    """Translate text based on current language"""
    if language is None:
        language = get_language()
    
    if language in TRANSLATIONS and key in TRANSLATIONS[language]:
        return TRANSLATIONS[language][key]
    
    # Fallback to English if translation not found
    if key in TRANSLATIONS['en']:
        return TRANSLATIONS['en'][key]
    
    # Return key if no translation found
    return key

# Make translation function available in templates
app.jinja_env.globals.update(t=t, get_language=get_language, SUPPORTED_LANGUAGES=SUPPORTED_LANGUAGES)

# Database Models
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships with cascade delete
    orders = db.relationship('Order', backref='customer', cascade='all, delete-orphan')

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False, default=0)
    unit = db.Column(db.String(20), default='piece')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships with cascade delete
    order_items = db.relationship('OrderItem', backref='product', cascade='all, delete-orphan')

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    order_date = db.Column(db.Date, nullable=False)
    delivery_date = db.Column(db.Date)
    delivery_address = db.Column(db.Text)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    payment_status = db.Column(db.Enum('Paid', 'Unpaid', 'Partial'), default='Unpaid')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='order', cascade='all, delete-orphan')

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.String(50), default='Cash')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
@login_required
def dashboard():
    # Get dashboard statistics
    total_customers = Customer.query.count()
    total_products = Product.query.count()
    
    # Calculate monthly sales
    first_day = date.today().replace(day=1)
    monthly_orders = Order.query.filter(Order.order_date >= first_day).all()
    monthly_sales = sum(order.total_amount for order in monthly_orders)
    
    # Get pending payments (outstanding amounts)
    pending_orders = Order.query.filter(Order.payment_status != 'Paid').all()
    pending_amount = 0
    for order in pending_orders:
        total_paid = sum(float(p.amount) for p in order.payments)
        outstanding = float(order.total_amount) - total_paid
        pending_amount += outstanding
    
    # Get orders placed today
    today = date.today()
    orders_placed_today = Order.query.filter(Order.order_date == today).count()
    
    # Get low stock products
    low_stock_products = Product.query.filter(Product.stock_quantity < 10).all()
    
    return render_template('dashboard.html', 
                         total_customers=total_customers,
                         total_products=total_products,
                         monthly_sales=monthly_sales,
                         pending_amount=pending_amount,
                         orders_placed_today=orders_placed_today,
                         low_stock_products=low_stock_products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Customer Management
@app.route('/customers')
@login_required
def customers():
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)

@app.route('/api/customers', methods=['GET', 'POST'])
@login_required
def api_customers():
    if request.method == 'POST':
        data = request.get_json()
        
        # Validate data
        if not all(key in data for key in ['name', 'phone', 'address']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        customer = Customer(
            name=data['name'],
            phone=data['phone'],
            address=data['address']
        )
        
        try:
            db.session.add(customer)
            db.session.commit()
            return jsonify({'message': 'Customer added successfully', 'id': customer.id})
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'error': f'Customer with this phone number or username already exists: {e}'}), 409
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    customers = Customer.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'phone': c.phone,
        'address': c.address
    } for c in customers])

@app.route('/api/customers/<int:customer_id>/check-orders')
@login_required
def check_customer_orders(customer_id):
    """Check if a customer has any related orders before deletion"""
    try:
        order_count = Order.query.filter_by(customer_id=customer_id).count()
        return jsonify({'order_count': order_count})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/customers/<int:customer_id>', methods=['PUT', 'DELETE'])
@login_required
def api_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    
    if request.method == 'PUT':
        data = request.get_json()
        
        customer.name = data.get('name', customer.name)
        customer.phone = data.get('phone', customer.phone)
        customer.address = data.get('address', customer.address)
        
        try:
            db.session.commit()
            return jsonify({'message': 'Customer updated successfully'})
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'error': f'Customer with this phone number or username already exists: {e}'}), 409
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'DELETE':
        try:
            # Check if customer has any orders
            order_count = Order.query.filter_by(customer_id=customer.id).count()
            
            if order_count > 0:
                # Customer has orders, delete them first
                orders_to_delete = Order.query.filter_by(customer_id=customer.id).all()
                for order in orders_to_delete:
                    # Delete payments and order items first
                    for payment in order.payments:
                        db.session.delete(payment)
                    for item in order.items:
                        db.session.delete(item)
                    db.session.delete(order)
            
            db.session.delete(customer)
            db.session.commit()
            
            if order_count > 0:
                return jsonify({'message': f'Customer and {order_count} associated order(s) deleted successfully'})
            else:
                return jsonify({'message': 'Customer deleted successfully'})
                
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'error': f'Cannot delete customer due to database constraints: {str(e)}'}), 409
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to delete customer: {str(e)}'}), 500

# Product Management
@app.route('/products')
@login_required
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/api/products', methods=['GET', 'POST'])
@login_required
def api_products():
    if request.method == 'POST':
        data = request.get_json()
        
        if not all(key in data for key in ['name', 'price', 'stock_quantity']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        product = Product(
            name=data['name'],
            price=data['price'],
            stock_quantity=data['stock_quantity'],
            unit=data.get('unit', 'piece')
        )
        
        try:
            db.session.add(product)
            db.session.commit()
            return jsonify({'message': 'Product added successfully', 'id': product.id})
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'error': f'Product with this name already exists: {e}'}), 409
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'price': float(p.price),
        'stock_quantity': p.stock_quantity,
        'unit': p.unit
    } for p in products])

@app.route('/api/products/<int:product_id>/check-orders')
@login_required
def check_product_orders(product_id):
    """Check if a product has any related order items before deletion"""
    try:
        order_item_count = OrderItem.query.filter_by(product_id=product_id).count()
        return jsonify({'order_item_count': order_item_count})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['PUT', 'DELETE'])
@login_required
def api_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'PUT':
        data = request.get_json()
        
        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        product.stock_quantity = data.get('stock_quantity', product.stock_quantity)
        product.unit = data.get('unit', product.unit)
        
        try:
            db.session.commit()
            return jsonify({'message': 'Product updated successfully'})
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'error': f'Product with this name already exists: {e}'}), 409
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'DELETE':
        try:
            # Check if product has any order items
            order_item_count = OrderItem.query.filter_by(product_id=product.id).count()
            
            if order_item_count > 0:
                # Product has order items, delete them first
                order_items_to_delete = OrderItem.query.filter_by(product_id=product.id).all()
                for item in order_items_to_delete:
                    db.session.delete(item)
            
            db.session.delete(product)
            db.session.commit()
            
            if order_item_count > 0:
                return jsonify({'message': f'Product and {order_item_count} associated order item(s) deleted successfully'})
            else:
                return jsonify({'message': 'Product deleted successfully'})
                
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'error': f'Cannot delete product due to database constraints: {str(e)}'}), 409
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to delete product: {str(e)}'}), 500

# Order Management
@app.route('/orders')
@login_required
def orders():
    orders = Order.query.all()
    customers = Customer.query.all()
    products = Product.query.all()
    return render_template('orders.html', orders=orders, customers=customers, products=products)

@app.route('/api/orders', methods=['GET', 'POST'])
@login_required
def api_orders():
    if request.method == 'POST':
        data = request.get_json()
        
        if not all(key in data for key in ['customer_id', 'order_date', 'items']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create order
        order = Order(
            customer_id=data['customer_id'],
            order_date=datetime.strptime(data['order_date'], '%Y-%m-%d').date(),
            delivery_date=datetime.strptime(data['delivery_date'], '%Y-%m-%d').date() if data.get('delivery_date') else None,
            delivery_address=data.get('delivery_address', ''),
            payment_status=data.get('payment_status', 'Unpaid')
        )
        
        total_amount = 0
        
        try:
            db.session.add(order)
            db.session.flush()  # Get the order ID
            
            # Add order items
            for item_data in data['items']:
                product = Product.query.get(item_data['product_id'])
                if not product:
                    raise Exception(f"Product {item_data['product_id']} not found")
                
                if product.stock_quantity < item_data['quantity']:
                    raise Exception(f"Insufficient stock for {product.name}")
                
                # Update stock
                product.stock_quantity -= item_data['quantity']
                
                # Create order item
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item_data['product_id'],
                    quantity=item_data['quantity'],
                    price=product.price
                )
                
                db.session.add(order_item)
                total_amount += float(product.price) * item_data['quantity']
            
            order.total_amount = total_amount
            
            # If order is marked as Paid or Partial, create a payment record
            if data.get('payment_status') in ['Paid', 'Partial']:
                payment_amount = data.get('payment_amount', 0)
                if payment_amount > 0:
                    # Create descriptive notes for payment
                    if data.get('payment_status') == 'Paid':
                        notes = f"Full payment of ${payment_amount:.2f} recorded when order was created"
                    else:
                        outstanding = total_amount - payment_amount
                        notes = f"Partial payment of ${payment_amount:.2f} recorded when order was created (Outstanding: ${outstanding:.2f})"
                    
                    payment = Payment(
                        order_id=order.id,
                        amount=payment_amount,
                        payment_date=datetime.strptime(data['order_date'], '%Y-%m-%d').date(),
                        payment_method=data.get('payment_method', 'Cash'),
                        notes=notes
                    )
                    db.session.add(payment)
            
            db.session.commit()
            
            return jsonify({'message': 'Order created successfully', 'id': order.id})
            
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'error': f'Order with this customer and date already exists: {e}'}), 409
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    orders = Order.query.all()
    return jsonify([{
        'id': o.id,
        'customer_name': o.customer.name,
        'order_date': o.order_date.strftime('%Y-%m-%d'),
        'delivery_date': o.delivery_date.strftime('%Y-%m-%d') if o.delivery_date else None,
        'total_amount': float(o.total_amount),
        'payment_status': o.payment_status,
        'paid_amount': sum(float(p.amount) for p in o.payments),
        'items': [{
            'product_name': item.product.name,
            'quantity': item.quantity,
            'price': float(item.price)
        } for item in o.items]
    } for o in orders])

@app.route('/api/orders/<int:order_id>', methods=['PUT', 'DELETE'])
@login_required
def api_order(order_id):
    order = Order.query.get_or_404(order_id)
    
    if request.method == 'PUT':
        data = request.get_json()
        
        if 'payment_status' in data:
            old_status = order.payment_status
            order.payment_status = data['payment_status']
            
            # If status changed to Paid or Partial and there are no existing payments, create one
            if data['payment_status'] in ['Paid', 'Partial'] and old_status not in ['Paid', 'Partial']:
                existing_payments = Payment.query.filter_by(order_id=order.id).count()
                if existing_payments == 0:
                    payment_amount = data.get('payment_amount', 0)
                    if data['payment_status'] == 'Paid':
                        payment_amount = float(order.total_amount)
                    elif data['payment_status'] == 'Partial' and payment_amount == 0:
                        # For partial without amount, use 50% of total as default
                        payment_amount = float(order.total_amount) * 0.5
                    
                    # Create descriptive notes for payment
                    if data['payment_status'] == 'Paid':
                        notes = f"Full payment of ${payment_amount:.2f} recorded when order status changed to Paid"
                    else:
                        outstanding = float(order.total_amount) - payment_amount
                        notes = f"Partial payment of ${payment_amount:.2f} recorded when order status changed to Partial (Outstanding: ${outstanding:.2f})"
                    
                    payment = Payment(
                        order_id=order.id,
                        amount=payment_amount,
                        payment_date=date.today(),
                        payment_method=data.get('payment_method', 'Cash'),
                        notes=notes
                    )
                    db.session.add(payment)
        
        try:
            db.session.commit()
            return jsonify({'message': 'Order updated successfully'})
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'error': f'Order with this customer and date already exists: {e}'}), 409
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'DELETE':
        try:
            # First, explicitly delete all payments associated with this order
            # to avoid foreign key constraint issues
            payments_to_delete = Payment.query.filter_by(order_id=order.id).all()
            payment_count = len(payments_to_delete)
            for payment in payments_to_delete:
                db.session.delete(payment)
            
            # Restore stock quantities
            item_count = len(order.items)
            for item in order.items:
                product = Product.query.get(item.product_id)
                if product:
                    product.stock_quantity += item.quantity
            
            # Now delete the order
            db.session.delete(order)
            db.session.commit()
            
            message = f'Order deleted successfully'
            if payment_count > 0:
                message += f' ({payment_count} payment record(s) also deleted)'
            if item_count > 0:
                message += f' (Stock quantities restored for {item_count} product(s))'
                
            return jsonify({'message': message})
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'error': f'Cannot delete order due to database constraints: {str(e)}'}), 409
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to delete order: {str(e)}'}), 500

# Payment Management
@app.route('/payments')
@login_required
def payments():
    payments = Payment.query.all()
    orders = Order.query.all()
    return render_template('payments.html', payments=payments, orders=orders)

@app.route('/api/payments', methods=['GET', 'POST'])
@login_required
def api_payments():
    if request.method == 'GET':
        # Return all payments with order and customer details
        payments = Payment.query.all()
        return jsonify([{
            'id': p.id,
            'order_id': p.order_id,
            'customer_name': p.order.customer.name,
            'payment_date': p.payment_date.strftime('%Y-%m-%d'),
            'amount': float(p.amount),
            'payment_method': p.payment_method,
            'notes': p.notes
        } for p in payments])
    
    elif request.method == 'POST':
        data = request.get_json()
        
        if not all(key in data for key in ['order_id', 'amount', 'payment_date']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        payment = Payment(
            order_id=data['order_id'],
            amount=data['amount'],
            payment_date=datetime.strptime(data['payment_date'], '%Y-%m-%d').date(),
            payment_method=data.get('payment_method', 'Cash'),
            notes=data.get('notes', '')
        )
        
        try:
            db.session.add(payment)
            
            # Update order payment status
            order = Order.query.get(data['order_id'])
            if order:
                total_paid = sum(float(p.amount) for p in order.payments) + float(data['amount'])
                if total_paid >= float(order.total_amount):
                    order.payment_status = 'Paid'
                elif total_paid > 0:
                    order.payment_status = 'Partial'
            
            db.session.commit()
            return jsonify({'message': 'Payment recorded successfully'})
            
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'error': f'Payment with this order and date already exists: {e}'}), 409
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500



# Reports
@app.route('/reports')
@login_required
def reports():
    return render_template('reports.html')

@app.route('/api/dashboard/pending-deliveries')
@login_required
def pending_deliveries():
    today = date.today()
    tomorrow = today + timedelta(days=1)
    
    # Get orders with delivery dates for today and tomorrow
    pending_deliveries = Order.query.filter(
        Order.delivery_date.in_([today, tomorrow])
    ).order_by(Order.delivery_date, Order.id).all()
    
    return jsonify([{
        'id': order.id,
        'customer_name': order.customer.name,
        'order_date': order.order_date.strftime('%Y-%m-%d'),
        'delivery_date': order.delivery_date.strftime('%Y-%m-%d') if order.delivery_date else None,
        'total_amount': float(order.total_amount),
        'payment_status': order.payment_status,
        'delivery_address': order.delivery_address
    } for order in pending_deliveries])

@app.route('/api/reports/sales')
@login_required
def sales_report():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if start_date and end_date:
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        orders = Order.query.filter(Order.order_date.between(start, end)).all()
    else:
        # Default to current month
        first_day = date.today().replace(day=1)
        orders = Order.query.filter(Order.order_date >= first_day).all()
    
    report_data = []
    for order in orders:
        for item in order.items:
            report_data.append({
                'order_id': order.id,
                'date': order.order_date.strftime('%Y-%m-%d'),
                'customer': order.customer.name,
                'product': item.product.name,
                'quantity': item.quantity,
                'price': float(item.price),
                'total': float(item.price) * item.quantity,
                'payment_status': order.payment_status
            })
    
    return jsonify(report_data)

@app.route('/api/reports/export-csv')
@login_required
def export_csv():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if start_date and end_date:
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        orders = Order.query.filter(Order.order_date.between(start, end)).all()
    else:
        first_day = date.today().replace(day=1)
        orders = Order.query.filter(Order.order_date >= first_day).all()
    
    # Create CSV
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Order ID', 'Date', 'Customer', 'Product', 'Quantity', 'Price', 'Total', 'Payment Status'])
    
    for order in orders:
        for item in order.items:
            writer.writerow([
                order.id,
                order.order_date.strftime('%Y-%m-%d'),
                order.customer.name,
                item.product.name,
                item.quantity,
                float(item.price),
                float(item.price) * item.quantity,
                order.payment_status
            ])
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'sales_report_{date.today().strftime("%Y%m%d")}.csv'
    )

# Invoice Generation
@app.route('/invoice/<int:order_id>')
@login_required
def generate_invoice(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Create PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1  # Center
    )
    
    # Create a bold style for labels
    bold_style = ParagraphStyle(
        'BoldLabel',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Helvetica-Bold'
    )
    
    # Header
    elements.append(Paragraph("BUILDING MATERIALS SHOP", title_style))
    elements.append(Paragraph("123 Construction Street, City, Country", styles['Normal']))
    elements.append(Paragraph("Phone: +1234567890 | Email: info@shop.com", styles['Normal']))
    elements.append(Spacer(1, 20))
    
    # Invoice details
    elements.append(Paragraph(f"INVOICE #{order.id}", styles['Heading2']))
    elements.append(Paragraph(f"Date: {order.order_date.strftime('%B %d, %Y')}", styles['Normal']))
    elements.append(Paragraph(f"Customer: {order.customer.name}", styles['Normal']))
    elements.append(Paragraph(f"Address: {order.customer.address}", styles['Normal']))
    elements.append(Paragraph(f"Phone: {order.customer.phone}", styles['Normal']))
    if order.delivery_address:
        elements.append(Paragraph(f"Delivery Address: {order.delivery_address}", styles['Normal']))
    if order.delivery_date:
        elements.append(Paragraph(f"Delivery Date: {order.delivery_date.strftime('%B %d, %Y')}", styles['Normal']))
    
    elements.append(Spacer(1, 20))
    
    # Items table
    table_data = [['Product', 'Quantity', 'Unit Price', 'Total']]
    for item in order.items:
        table_data.append([
            item.product.name,
            str(item.quantity),
            f"${float(item.price):.2f}",
            f"${float(item.price) * item.quantity:.2f}"
        ])
    
    # Add total row
    table_data.append(['', '', 'TOTAL', f"${float(order.total_amount):.2f}"])
    
    table = Table(table_data, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        # Make the TOTAL row bold and give it a different background
        ('FONTNAME', (2, -1), (3, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (2, -1), (3, -1), 12),
        ('BACKGROUND', (2, -1), (3, -1), colors.lightblue),
        ('TEXTCOLOR', (2, -1), (3, -1), colors.black)
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 20))
    
    # Payment status
    elements.append(Paragraph(f"Payment Status: {order.payment_status}", styles['Normal']))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'invoice_{order.id}.pdf'
    )

# Search functionality
@app.route('/api/search')
@login_required
def search():
    query = request.args.get('q', '')
    search_type = request.args.get('type', 'orders')
    
    if search_type == 'customers':
        results = Customer.query.filter(Customer.name.ilike(f'%{query}%')).all()
        return jsonify([{
            'id': c.id,
            'name': c.name,
            'phone': c.phone,
            'address': c.address
        } for c in results])
    
    elif search_type == 'products':
        results = Product.query.filter(Product.name.ilike(f'%{query}%')).all()
        return jsonify([{
            'id': p.id,
            'name': p.name,
            'price': float(p.price),
            'stock_quantity': p.stock_quantity
        } for p in results])
    
    else:  # orders
        results = Order.query.join(Customer).filter(Customer.name.ilike(f'%{query}%')).all()
        return jsonify([{
            'id': o.id,
            'customer_name': o.customer.name,
            'order_date': o.order_date.strftime('%Y-%m-%d'),
            'total_amount': float(o.total_amount),
            'payment_status': o.payment_status
        } for o in results])

# Database recreation route (for development/testing)
@app.route('/recreate-db')
@login_required
def recreate_database():
    """Recreate the database with new models (WARNING: This will delete all data!)"""
    try:
        # Drop all tables
        db.drop_all()
        # Create all tables
        db.create_all()
        
        # Create a default admin user
        admin_user = User(
            username='admin',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(admin_user)
        db.session.commit()
        
        return jsonify({'message': 'Database recreated successfully! Default admin user created (username: admin, password: admin123)'})
    except Exception as e:
        return jsonify({'error': f'Failed to recreate database: {str(e)}'}), 500

# Language change route
@app.route('/api/language', methods=['POST'])
@login_required
def change_language():
    data = request.get_json()
    language = data.get('language')
    
    if set_language(language):
        return jsonify({'success': True, 'message': 'Language changed successfully'})
    else:
        return jsonify({'success': False, 'message': 'Invalid language'}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
