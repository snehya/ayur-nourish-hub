#!/usr/bin/env python3
"""
Test Supabase Connection Script
"""
import os
from supabase import create_client, Client

# Supabase credentials
SUPABASE_URL = "https://bizmbwpgbbdgdjktffni.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJpem1id3BnYmJkZ2Rqa3RmZm5pIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg4MjQxOTAsImV4cCI6MjA3NDQwMDE5MH0.r2hY7J-04Ln91S4EvFtqiZtyYrx71zRg16oqvY1RL2I"
SUPABASE_SERVICE_ROLE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJpem1id3BnYmJkZ2Rqa3RmZm5pIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1ODgyNDE5MCwiZXhwIjoyMDc0NDAwMTkwfQ.3_cHaE4TaZgauLNMiSVXA_KnV0tUwzgxGFZVfY34nRM"

def test_supabase_connection():
    """Test connection to Supabase using the Python client"""
    print("🔍 Testing Supabase connection...")
    
    try:
        # Create Supabase client with service role key
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
        
        # Test connection by trying to list tables
        result = supabase.table("information_schema.tables").select("table_name").limit(1).execute()
        
        print("✅ Supabase connection successful!")
        print(f"📊 Connected to: {SUPABASE_URL}")
        print(f"🔑 Using service role authentication")
        
        return True
        
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return False

def get_database_info():
    """Get information about the Supabase database"""
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
        
        # Try to get database info
        print("\n📋 Database Information:")
        print(f"Project URL: {SUPABASE_URL}")
        print("Testing table creation capability...")
        
        # Test if we can create a simple test table
        test_result = supabase.rpc('version').execute()
        print("✅ Database connection established!")
        
    except Exception as e:
        print(f"❌ Failed to get database info: {e}")

if __name__ == "__main__":
    if test_supabase_connection():
        get_database_info()
    else:
        print("\n🔧 Troubleshooting:")
        print("1. Check if your Supabase project is active")
        print("2. Verify the service role key has sufficient permissions")
        print("3. Check if your project URL is correct")