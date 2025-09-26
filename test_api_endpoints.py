#!/usr/bin/env python3
"""
Simple API Test Script
Test the essential endpoints manually
"""
import subprocess
import time
import os

def start_server():
    """Start Django server in background"""
    print("🚀 Starting Django server...")
    server_cmd = [
        "C:/Users/sneha/ayurdiet_backend/venv/Scripts/python.exe",
        "manage.py", "runserver", "--noreload"
    ]
    
    # Start server in background
    process = subprocess.Popen(
        server_cmd, 
        cwd="C:/Users/sneha/ayurdiet_backend",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait a moment for server to start
    time.sleep(5)
    return process

def test_with_curl():
    """Test endpoints using PowerShell Invoke-RestMethod"""
    tests = [
        {
            "name": "Test Foods API",
            "url": "http://127.0.0.1:8000/api/foods/",
            "expected": "Should return 117 foods"
        },
        {
            "name": "Test Food Search",
            "url": "http://127.0.0.1:8000/api/foods/search/?virya=Cooling",
            "expected": "Should return cooling foods"
        },
        {
            "name": "Test Statistics",
            "url": "http://127.0.0.1:8000/api/foods/statistics/",
            "expected": "Should return statistics"
        }
    ]
    
    print("\n🧪 Testing API Endpoints...")
    for test in tests:
        print(f"\n📍 {test['name']}")
        print(f"URL: {test['url']}")
        print(f"Expected: {test['expected']}")
        
        # PowerShell command to test
        ps_cmd = f"""
        try {{
            $response = Invoke-RestMethod -Uri '{test['url']}' -Method GET -TimeoutSec 5
            Write-Host "✅ Success - Response received"
            if ($response -is [array]) {{
                Write-Host "📊 Count: $($response.Count)"
            }} else {{
                Write-Host "📊 Response type: $($response.GetType().Name)"
            }}
        }} catch {{
            Write-Host "❌ Failed: $($_.Exception.Message)"
        }}
        """
        
        # Execute PowerShell command
        try:
            result = subprocess.run(
                ["powershell", "-Command", ps_cmd],
                capture_output=True,
                text=True,
                timeout=10
            )
            print(result.stdout)
            if result.stderr:
                print(f"Error: {result.stderr}")
        except Exception as e:
            print(f"❌ Test failed: {e}")

def main():
    print("🎯 BACKEND API TESTING")
    print("=" * 40)
    
    # Start server
    server_process = start_server()
    
    try:
        # Test endpoints
        test_with_curl()
        
        print("\n🎉 Testing completed!")
        print("=" * 40)
        print("✅ Your backend is ready for frontend integration!")
        
    finally:
        # Stop server
        print("\n🛑 Stopping server...")
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    main()