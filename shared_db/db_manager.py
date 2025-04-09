import sqlite3
from datetime import datetime
import os
from pathlib import Path
from dotenv import load_dotenv
from django.contrib.auth.hashers import make_password, check_password

# Load environment variables
load_dotenv()

# Status options for assignments
ASSIGNMENT_STATUSES = ["Not Started", "In Progress", "Completed"]

# Database path - store in the shared_db directory
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'taskmanager.db')

class DatabaseManager:
    def __init__(self):
        self.conn = None
        self.connect()
        self.create_tables()

    def connect(self):
        try:
            self.conn = sqlite3.connect(DB_PATH)
            # Enable foreign keys
            self.conn.execute("PRAGMA foreign_keys = ON")
            # Return rows as dictionaries
            self.conn.row_factory = sqlite3.Row
        except Exception as e:
            print(f"Error connecting to database: {e}")
            raise

    def create_tables(self):
        try:
            cursor = self.conn.cursor()

            # Create auth_user table if it doesn't exist (matches Django's auth_user table)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS auth_user (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    password VARCHAR(128) NOT NULL,
                    last_login TIMESTAMP NULL,
                    is_superuser BOOLEAN NOT NULL DEFAULT 0,
                    username VARCHAR(150) NOT NULL UNIQUE,
                    first_name VARCHAR(150) NOT NULL DEFAULT '',
                    last_name VARCHAR(150) NOT NULL DEFAULT '',
                    email VARCHAR(254) NOT NULL DEFAULT '',
                    is_staff BOOLEAN NOT NULL DEFAULT 0,
                    is_active BOOLEAN NOT NULL DEFAULT 1,
                    date_joined TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create tasks_assignment table (matches Django model)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks_assignment (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(200) NOT NULL,
                    due_date DATE NOT NULL,
                    description TEXT NOT NULL DEFAULT '',
                    status VARCHAR(20) NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    creator_id INTEGER,
                    FOREIGN KEY (creator_id) REFERENCES auth_user(id) ON DELETE SET NULL
                )
            """)

            # Create tasks_assignment_assignees table (for many-to-many relationship)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks_assignment_assignees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    assignment_id INTEGER,
                    user_id INTEGER,
                    UNIQUE(assignment_id, user_id),
                    FOREIGN KEY (assignment_id) REFERENCES tasks_assignment(id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
                )
            """)

            # Create tasks_subtask table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks_subtask (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(200) NOT NULL,
                    is_completed BOOLEAN NOT NULL DEFAULT 0,
                    assignment_id INTEGER NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (assignment_id) REFERENCES tasks_assignment(id) ON DELETE CASCADE
                )
            """)

            self.conn.commit()

        except Exception as e:
            print(f"Error creating tables: {e}")
            raise

    def create_user(self, username, password, is_staff=False):
        try:
            # Generate Django-compatible password hash
            password_hash = make_password(password)

            # Current timestamp for date_joined
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO auth_user (
                    username, password, is_staff, is_superuser,
                    is_active, first_name, last_name, email, date_joined
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (username, password_hash, is_staff, False, True, '', '', '', now)
            )
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating user: {e}")
            raise

    def verify_user(self, username, password):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT id, password, is_staff FROM auth_user WHERE username = ?",
                (username,)
            )
            result = cursor.fetchone()

            if not result:
                return None

            user_id = result['id']
            password_hash = result['password']
            is_staff = result['is_staff']

            # Use Django's password verification
            if check_password(password, password_hash):
                return {
                    'user_id': user_id,
                    'is_staff': is_staff
                }

            return None
        except Exception as e:
            print(f"Error verifying user: {e}")
            raise

    def create_assignment(self, name, due_date, description, status, creator_id, assignee_ids, subtasks=None):
        try:
            cursor = self.conn.cursor()
            # Insert assignment
            cursor.execute(
                """
                INSERT INTO tasks_assignment (name, due_date, description, status, creator_id)
                VALUES (?, ?, ?, ?, ?)
                """,
                (name, due_date.strftime('%Y-%m-%d'), description, status, creator_id)
            )
            assignment_id = cursor.lastrowid

            # Insert assignees
            for user_id in assignee_ids:
                cursor.execute(
                    "INSERT INTO tasks_assignment_assignees (assignment_id, user_id) VALUES (?, ?)",
                    (assignment_id, user_id)
                )

            # Insert subtasks if provided
            if subtasks:
                for subtask in subtasks:
                    cursor.execute(
                        """
                        INSERT INTO tasks_subtask (name, is_completed, assignment_id)
                        VALUES (?, ?, ?)
                        """,
                        (subtask['name'], subtask.get('is_completed', False), assignment_id)
                    )

            self.conn.commit()
            return assignment_id
        except Exception as e:
            print(f"Error creating assignment: {e}")
            self.conn.rollback()
            raise

    def get_assignments(self, user_id, is_staff):
        try:
            cursor = self.conn.cursor()
            if is_staff:
                cursor.execute(
                    """
                    SELECT a.*, u.username as creator_name
                    FROM tasks_assignment a
                    LEFT JOIN auth_user u ON a.creator_id = u.id
                    ORDER BY a.due_date
                    """
                )
            else:
                cursor.execute(
                    """
                    SELECT a.*, u.username as creator_name
                    FROM tasks_assignment a
                    LEFT JOIN auth_user u ON a.creator_id = u.id
                    WHERE a.creator_id = ?
                    OR a.id IN (
                        SELECT assignment_id FROM tasks_assignment_assignees WHERE user_id = ?
                    )
                    ORDER BY a.due_date
                    """,
                    (user_id, user_id)
                )
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting assignments: {e}")
            raise

    def get_assignment_details(self, assignment_id):
        try:
            cursor = self.conn.cursor()
            # Get assignment details
            cursor.execute(
                """
                SELECT a.*, u.username as creator_name
                FROM tasks_assignment a
                LEFT JOIN auth_user u ON a.creator_id = u.id
                WHERE a.id = ?
                """,
                (assignment_id,)
            )
            assignment = cursor.fetchone()

            # Get assignees
            cursor.execute(
                """
                SELECT u.id, u.username
                FROM auth_user u
                JOIN tasks_assignment_assignees aa ON u.id = aa.user_id
                WHERE aa.assignment_id = ?
                """,
                (assignment_id,)
            )
            assignees = cursor.fetchall()

            return assignment, assignees
        except Exception as e:
            print(f"Error getting assignment details: {e}")
            raise

    def update_assignment_status(self, assignment_id, status):
        try:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE tasks_assignment SET status = ?, updated_at = ? WHERE id = ?",
                (status, now, assignment_id)
            )
            self.conn.commit()
        except Exception as e:
            print(f"Error updating assignment status: {e}")
            self.conn.rollback()
            raise

    def get_all_users(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, username, is_staff FROM auth_user")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting all users: {e}")
            raise

    def promote_user(self, user_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE auth_user SET is_staff = 1 WHERE id = ?",
                (user_id,)
            )
            self.conn.commit()
        except Exception as e:
            print(f"Error promoting user: {e}")
            self.conn.rollback()

    def get_subtasks(self, assignment_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                SELECT id, name, is_completed, created_at, updated_at
                FROM tasks_subtask
                WHERE assignment_id = ?
                ORDER BY created_at
                """,
                (assignment_id,)
            )
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting subtasks: {e}")
            return []

    def update_subtask(self, subtask_id, is_completed):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                UPDATE tasks_subtask
                SET is_completed = ?, updated_at = datetime('now')
                WHERE id = ?
                """,
                (is_completed, subtask_id)
            )

            # Get the assignment_id for this subtask
            cursor.execute(
                "SELECT assignment_id FROM tasks_subtask WHERE id = ?",
                (subtask_id,)
            )
            result = cursor.fetchone()
            assignment_id = result['assignment_id'] if result else None

            self.conn.commit()

            # Return the assignment_id so we can calculate completion percentage
            return assignment_id
        except Exception as e:
            print(f"Error updating subtask: {e}")
            self.conn.rollback()
            return None

    def get_completion_percentage(self, assignment_id):
        try:
            cursor = self.conn.cursor()

            # Get all subtasks for this assignment
            cursor.execute(
                "SELECT is_completed FROM tasks_subtask WHERE assignment_id = ?",
                (assignment_id,)
            )
            subtasks = cursor.fetchall()

            if subtasks:
                total = len(subtasks)
                completed = sum(1 for s in subtasks if s['is_completed'])
                return int((completed / total) * 100) if total > 0 else 0
            else:
                # If no subtasks, base on assignment status
                cursor.execute(
                    "SELECT status FROM tasks_assignment WHERE id = ?",
                    (assignment_id,)
                )
                result = cursor.fetchone()
                if result:
                    status = result['status']
                    if status == 'Completed':
                        return 100
                    elif status == 'In Progress':
                        return 50
                    else:
                        return 0
                return 0
        except Exception as e:
            print(f"Error calculating completion percentage: {e}")
            return 0

    def close(self):
        if self.conn:
            self.conn.close()