from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Sync database tables for the webapp without recreating existing tables'

    def handle(self, *args, **options):
        # Create missing tables but skip tables that already exist
        
        with connection.cursor() as cursor:
            # Check if django_session table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='django_session';")
            if not cursor.fetchone():
                self.stdout.write(self.style.SUCCESS('Creating django_session table...'))
                cursor.execute('''
                    CREATE TABLE django_session (
                        session_key varchar(40) NOT NULL PRIMARY KEY,
                        session_data text NOT NULL,
                        expire_date datetime NOT NULL
                    )
                ''')
                cursor.execute('CREATE INDEX django_session_expire_date ON django_session (expire_date)')
            
            # Check if django_admin_log table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='django_admin_log';")
            if not cursor.fetchone():
                self.stdout.write(self.style.SUCCESS('Creating django_admin_log table...'))
                cursor.execute('''
                    CREATE TABLE django_admin_log (
                        id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                        action_time datetime NOT NULL,
                        object_id text NULL,
                        object_repr varchar(200) NOT NULL,
                        action_flag smallint unsigned NOT NULL,
                        change_message text NOT NULL,
                        content_type_id integer NULL REFERENCES django_content_type (id),
                        user_id integer NOT NULL REFERENCES auth_user (id)
                    )
                ''')
            
            # Check if django_content_type table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='django_content_type';")
            if not cursor.fetchone():
                self.stdout.write(self.style.SUCCESS('Creating django_content_type table...'))
                cursor.execute('''
                    CREATE TABLE django_content_type (
                        id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                        app_label varchar(100) NOT NULL,
                        model varchar(100) NOT NULL,
                        UNIQUE (app_label, model)
                    )
                ''')
            
            # Create django_migrations table if it doesn't exist
            cursor.execute("CREATE TABLE IF NOT EXISTS django_migrations (id INTEGER PRIMARY KEY AUTOINCREMENT, app VARCHAR(255) NOT NULL, name VARCHAR(255) NOT NULL, applied DATETIME NOT NULL)")
            
            # Insert migration records for all apps
            migrations = [
                ('contenttypes', '0001_initial'),
                ('contenttypes', '0002_remove_content_type_name'),
                ('auth', '0001_initial'),
                ('auth', '0002_alter_permission_name_max_length'),
                ('auth', '0003_alter_user_email_max_length'),
                ('auth', '0004_alter_user_username_opts'),
                ('auth', '0005_alter_user_last_login_null'),
                ('auth', '0006_require_contenttypes_0002'),
                ('auth', '0007_alter_validators_add_error_messages'),
                ('auth', '0008_alter_user_username_max_length'),
                ('auth', '0009_alter_user_last_name_max_length'),
                ('auth', '0010_alter_group_name_max_length'),
                ('auth', '0011_update_proxy_permissions'),
                ('auth', '0012_alter_user_first_name_max_length'),
                ('admin', '0001_initial'),
                ('admin', '0002_logentry_remove_auto_add'),
                ('admin', '0003_logentry_add_action_flag_choices'),
                ('sessions', '0001_initial'),
                ('tasks', '0001_initial'),
            ]
            
            for app, name in migrations:
                # Check if migration is already recorded
                cursor.execute("SELECT id FROM django_migrations WHERE app = %s AND name = %s", [app, name])
                if not cursor.fetchone():
                    cursor.execute(
                        "INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, datetime('now'))",
                        [app, name]
                    )
                    self.stdout.write(f"Marked migration {app}.{name} as applied")
            
        self.stdout.write(self.style.SUCCESS('Database synchronized successfully!')) 