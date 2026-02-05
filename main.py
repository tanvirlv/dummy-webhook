from fastapi import FastAPI, Request, Query, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import json
import os
from datetime import datetime
import uvicorn

# Initialize FastAPI
app = FastAPI(
    title="Dummy API Logger",
    description="Logs all incoming requests for testing webhooks and API calls",
    version="1.0.0"
)

# CORS - Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Color codes for pretty console output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def log_request(method: str, path: str, headers: dict, query_params: dict, body: any, client_ip: str):
    """Pretty print request details"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("\n" + "="*80)
    print(f"{Colors.BOLD}{Colors.GREEN}[{timestamp}] NEW REQUEST{Colors.END}")
    print("="*80)
    
    # Method and Path
    print(f"{Colors.CYAN}Method:{Colors.END} {Colors.BOLD}{method}{Colors.END}")
    print(f"{Colors.CYAN}Path:{Colors.END} {path}")
    print(f"{Colors.CYAN}Client IP:{Colors.END} {client_ip}")
    
    # Headers
    if headers:
        print(f"\n{Colors.YELLOW}📋 HEADERS:{Colors.END}")
        for key, value in headers.items():
            print(f"  {Colors.BLUE}{key}:{Colors.END} {value}")
    
    # Query Parameters
    if query_params:
        print(f"\n{Colors.YELLOW}🔍 QUERY PARAMS:{Colors.END}")
        for key, value in query_params.items():
            print(f"  {Colors.BLUE}{key}:{Colors.END} {value}")
    
    # Body
    if body:
        print(f"\n{Colors.YELLOW}📦 BODY:{Colors.END}")
        if isinstance(body, (dict, list)):
            print(json.dumps(body, indent=2))
        else:
            print(f"  {body}")
    
    print("="*80 + "\n")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "status": "success",
        "service": "Dummy API Logger",
        "message": "Send requests to any endpoint and check the console logs!",
        "examples": {
            "GET": "/webhook?param1=value1&param2=value2",
            "POST": "/webhook (with JSON body)",
            "ANY": "/any/path/you/want"
        }
    }

@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
async def catch_all(
    request: Request,
    full_path: str
):
    """Catch all requests to any endpoint"""
    
    # Get client IP
    client_ip = request.client.host if request.client else "unknown"
    
    # Get headers (filter out some noisy ones if you want)
    headers = dict(request.headers)
    
    # Get query parameters
    query_params = dict(request.query_params)
    
    # Get body
    body = None
    try:
        # Try to parse as JSON
        body = await request.json()
    except:
        try:
            # Try to get as form data
            body = await request.form()
            body = dict(body)
        except:
            try:
                # Try to get as plain text
                body_bytes = await request.body()
                if body_bytes:
                    body = body_bytes.decode('utf-8')
            except:
                body = None
    
    # Log the request
    log_request(
        method=request.method,
        path=f"/{full_path}",
        headers=headers,
        query_params=query_params,
        body=body,
        client_ip=client_ip
    )
    
    # Return success response
    return {
        "status": "received",
        "message": "Request logged successfully",
        "data": {
            "method": request.method,
            "path": f"/{full_path}",
            "timestamp": datetime.now().isoformat(),
            "client_ip": client_ip,
            "headers_count": len(headers),
            "query_params": query_params,
            "body_received": body is not None
        }
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8001))  # Different port from main.py
    print(f"""
{Colors.BOLD}{Colors.GREEN}
╔═══════════════════════════════════════════════════════════╗
║          🔍 DUMMY API LOGGER STARTED 🔍                   ║
╚═══════════════════════════════════════════════════════════╝
{Colors.END}
{Colors.CYAN}📡 Server running on: http://0.0.0.0:{port}{Colors.END}
{Colors.YELLOW}📝 All requests will be logged below...{Colors.END}
{Colors.GREEN}✅ Ready to receive webhooks and API calls!{Colors.END}
""")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="warning"  # Reduce uvicorn's own logs to focus on our custom logs
    )
