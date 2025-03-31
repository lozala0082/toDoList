# Task Management System

A desktop application for managing tasks and assignments with role-based access control (Admin/Assigner vs. Regular User/Assignee).

## Features

- User Authentication (Login/Register)
- Role-based Access Control
  - Admin/Assigner: Create, edit, delete assignments, manage users
  - Regular User/Assignee: View and update assignment status
- Assignment Management
  - Create new assignments
  - View assignment details
  - Update assignment status
  - Assign tasks to multiple users
- User Management (Admin only)
  - View all users
  - Promote users to admin role

## Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd task-management-system
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a PostgreSQL database:
```sql
CREATE DATABASE task_management;
```

5. Update the database configuration in `config.py`:
```python
DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'task_management',
    'user': 'your_username',
    'password': 'your_password'
}
```

## Usage

1. Run the application:
```bash
python main.py
```

2. Register a new user (first user will be a regular user)
3. Login with your credentials
4. For the first admin user, you'll need to manually update the database:
```sql
UPDATE users SET is_admin = TRUE WHERE username = 'your_username';
```

## Security Features

- Password hashing using bcrypt
- SQL injection prevention using parameterized queries
- Role-based access control
- Secure password storage

## Error Handling

The application includes comprehensive error handling for:
- Database connection issues
- Invalid user input
- Authentication failures
- Database operation failures

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 