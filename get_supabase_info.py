#!/usr/bin/env python3
"""
Test connection using Supabase connection pooler approach
"""
import psycopg2

def test_pooler_connection():
    """Test connection using connection pooler"""
    project_ref = "bizmbwpgbbdgdjktffni"
    
    # Try with connection pooler (sometimes works without explicit password)
    connection_strings = [
        f"postgresql://postgres.{project_ref}:PASSWORD@aws-0-us-east-1.pooler.supabase.com:5432/postgres",
        f"postgresql://postgres:[YOUR_PASSWORD]@db.{project_ref}.supabase.co:5432/postgres",
    ]
    
    print("🔍 Possible connection formats:")
    for i, conn_str in enumerate(connection_strings, 1):
        print(f"{i}. {conn_str}")
    
    print("\n📋 To get your actual password:")
    print("1. Go to: https://supabase.com/dashboard/project/bizmbwpgbbdgdjktffni")
    print("2. Settings → Database")
    print("3. Copy the connection string or reset password")
    print("4. Look for something like: postgresql://postgres:YOUR_PASSWORD@...")

if __name__ == "__main__":
    test_pooler_connection()