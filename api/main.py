from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api.routes import router

app = FastAPI(
	title="RAG Service API",
	description="API For indexing documents and querying a RAG system",
	version="1.0.0"
)

# Add CORS Middleware
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)

# Include routes
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
	return {
		"message": "RAG Service API"
	}

@app.get("/health")
async def health_check():
	return {
		"status": "healthy"
	}

if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8000)