#!/usr/bin/env python3
"""
Extract Database Connection Info from Supabase
"""
import psycopg2
import os

# Try different possible database passwords based on your project reference
project_ref = "bizmbwpgbbdgdjktffni"
possible_passwords = [
    "7ZLxHWMTzWVzBXiQ",  # Common default
    "password",
    "postgres",
]

# Database connection parameters
host = f"db.{project_ref}.supabase.co"
port = "5432"
dbname = "postgres"
user = "postgres"

def test_connection(password):
    """Test PostgreSQL connection with given password"""
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
            sslmode="require"
        )
        
        # Test the connection
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        print(f"✅ Connection successful with password: {password}")
        print(f"📊 PostgreSQL Version: {version[0]}")
        return True
        
    except Exception as e:
        print(f"❌ Failed with password '{password}': {e}")
        return False

def main():
    print(f"🔍 Testing connection to: {host}")
    print(f"📍 Database: {dbname}, User: {user}")
    print()
    
    for password in possible_passwords:
        if test_connection(password):
            print(f"\n🎯 Use this password in Django settings: '{password}'")
            print(f"\n📝 Database Configuration:")
            print(f"HOST: {host}")
            print(f"PORT: {port}")
            print(f"NAME: {dbname}")
            print(f"USER: {user}")
            print(f"PASSWORD: {password}")
            break
    else:
        print("\n❌ None of the passwords worked.")
        print("Please check your Supabase project settings for the correct database password.")

if __name__ == "__main__":
    main()