Backend for Ruiru PCEA SACCO Portal (local dev).

Run locally:

pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload

API endpoints:
- GET / -> status
- GET /api/v1/members/search?q=... -> search
- GET /api/v1/members/{member_no} -> member
- GET /api/v1/dashboard/summary -> portfolio summary
