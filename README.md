# 📦 Inventory Management System
## 📖 Overview
Welcome to the Simple Inventory Management System! 
This project is designed to help organizations manage their inventory efficiently. With features for user management, 
item Management by seamless API integrations.

The system is built with Django, providing a robust backend to handle all inventory operations while leveraging 
RESTful API architecture for frontend integrations.
![GitHub](https://img.shields.io/badge/GitHub-inventory_management-blue?style=flat-square&logo=github)
![Django](https://img.shields.io/badge/Django-Python-yellow?style=flat-square&logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-green?style=flat-square&logo=postgresql)
![Postman](https://img.shields.io/badge/Postman-Testing-blueviolet?style=flat-square&logo=postman)

## ✨ Features
- 🔑 **User Registration & Login:** Secure registration and authentication for users.
- 📦 **Item Management:** Create, read, update, and delete (CRUD) operations for items.
- 🔄 **API Endpoints:** Well-defined RESTful APIs for easy integration.
- 📊 **Logging & Monitoring:** Track API usage, errors, and significant events with logging.
- 🛡️ **JWT Authentication:** Secure API access with JWT for user sessions.
- ⚡**Caching:** Improved performance with Redis caching for item retrieval.
- ✅**Unit Testing:** Comprehensive test coverage to ensure code quality and functionality.

## 🛠️ Technologies Used
- 🐍**Python & Django:** A high-level Python web framework that encourages rapid development.
- 🌐**Django REST Framework:** For building Web APIs. 
- 🗄️**PostgreSQL:** Robust database system for data storage. 
- ⚙**Redis:** For caching and improving application performance. ️
- 🔐**JWT (JSON Web Tokens):** For user authentication.

## 🚀 Quick Start
Follow the steps below to get the project running on your local machine.
## 🔧 Installation
Make sure you have Python 3.x installed. Clone the repository and navigate to the project directory. Install the required dependencies using the `requirements.txt` file.
1. **Clone the Repository**
   ```bash
   git clone https://github.com/Onkar-Kul/simple-inventory-management.git

2. **Create Virtual Environment**
   ```bash
    python -m venv venv
    source venv/bin/activate  
    # On Windows: venv\Scripts\activate

3. **Install all dependencies**
   ```bash
   pip install -r requirements.txt

4. **Set up the database**

   Create a PostgreSQL database and update your settings.py with the database configuration.

5.  **Set up the environment variables**

    Create a .env file and set all the environment variable described in dist file

6. **Create and Run migrations**
    ```bash
   python manage.py makemigrations
   python manage.py migrate

7. **Run development server**
    ```bash
   python manage.py runserver

## 📚 Usage
Once the server is running, you can access the application at http://localhost:8000. Use tools like Postman to interact with the API endpoints:

**Example API Endpoints:**

|        Method         |         Endpoint         |          Description          |
|:---------------------:|:------------------------:|:-----------------------------:|
|         POST          | /api/users/registration/ |       User Registration       |
|         POST          |    /api/users/login/     |          User Login           |
|       GET/POST        |       /api/items/        | Get Items list or Create Item |
|  GET/PATCH/PUT/DELETE | /api/items/{item_id}/    | Retrive, Update, Delete items |

## 🧪 Testing
1. **Run the all tests using:**
    ```bash
   python manage.py test 

2. **Use Postman for Testing:**

    Make sure all the API's are working properly using postman




