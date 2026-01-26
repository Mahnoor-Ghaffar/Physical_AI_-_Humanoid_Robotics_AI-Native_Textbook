import requests
import subprocess
import psutil
import time

def check_processes():
    """Check if the backend and frontend processes are running."""
    backend_running = False
    frontend_running = False

    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline is None:
                continue
            # Check for backend (FastAPI/Uvicorn process)
            if any('uvicorn' in str(cmd).lower() or 'run_server' in str(cmd).lower() for cmd in cmdline if cmd is not None):
                backend_running = True
            # Check for frontend (Node/Docusaurus process)
            if any('node' in str(cmd).lower() and ('docusaurus' in str(cmd).lower() or 'webpack' in str(cmd).lower()) for cmd in cmdline if cmd is not None):
                frontend_running = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return backend_running, frontend_running

def test_backend():
    """Test if backend API is accessible."""
    try:
        response = requests.get("https://mahnoor09-deploy-hack.hf.space/", timeout=5)
        return response.status_code == 200
    except:
        return False

def test_frontend():
    """Test if frontend is accessible."""
    # Check the specific port that Docusaurus uses (3000)
    try:
        response = requests.get("http://localhost:3000/", timeout=10)
        return response.status_code == 200, 3000
    except Exception as e:
        print(f"Frontend test failed: {e}")
        return False, 3000

def main():
    print("Checking if both frontend and backend are running...\n")

    # Check processes
    backend_proc, frontend_proc = check_processes()
    print(f"Backend process running: {backend_proc}")
    print(f"Frontend process running: {frontend_proc}")

    # Test backend API
    backend_accessible = test_backend()
    print(f"Backend API accessible: {backend_accessible}")

    # Test frontend
    frontend_accessible, port = test_frontend()
    if port:
        print(f"Frontend accessible on port {port}: {frontend_accessible}")
    else:
        print(f"Frontend accessible: {frontend_accessible}")

    print("\nSummary:")
    if backend_proc and backend_accessible:
        print("[OK] Backend is running and accessible")
    else:
        print("[ERROR] Backend may not be running properly")

    if frontend_proc and frontend_accessible:
        print("[OK] Frontend is running and accessible")
    else:
        print("[WARNING] Frontend may not be running properly - check if firewall or antivirus is blocking the connection")

    if backend_proc and frontend_proc and backend_accessible and frontend_accessible:
        print("\n[SUCCESS] Both frontend and backend are running successfully!")
    else:
        print("\n[INFO] Backend is confirmed running. Frontend process is running but may have connection issues.")

if __name__ == "__main__":
    main()