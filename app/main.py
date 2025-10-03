from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os
from .scheduler import start_scheduler
from .storage import load_snapshot
from .settings import settings
from .tasks import ingest_today
from .formatting import get_spread_class, get_total_class, get_winprob_class

# Create FastAPI application
app = FastAPI(
    title="NCAA D1 Predictor",
    description="Daily NCAA Men's D1 games analysis with multiple data sources",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware для разработки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Start scheduler on application startup
@app.on_event("startup")
async def startup_event():
    """Application startup initialization"""
    print("Starting NCAA D1 Predictor...")
    start_scheduler()
    print("Application started successfully!")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown"""
    print("Shutting down NCAA D1 Predictor...")

# Main page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Main page with predictions table"""
    try:
        snap = await load_snapshot()
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "snap": snap,
            "get_spread_class": get_spread_class,
            "get_total_class": get_total_class,
            "get_winprob_class": get_winprob_class
        })
    except Exception as e:
        print(f"Error loading snapshot: {e}")
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "snap": None
        })

# API for manual data refresh
@app.post("/admin/refresh", response_class=PlainTextResponse)
async def manual_refresh(token: str):
    """Manual data refresh (token required)"""
    if token != settings.ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    try:
        await ingest_today()
        return "Data refresh completed successfully"
    except Exception as e:
        print(f"Manual refresh error: {e}")
        raise HTTPException(status_code=500, detail=f"Refresh failed: {str(e)}")

# API to get data in JSON format
@app.get("/api/data")
async def get_data():
    """API endpoint to get data in JSON format"""
    try:
        snap = await load_snapshot()
        if not snap:
            raise HTTPException(status_code=404, detail="No data available")
        
        return {
            "status": snap.status,
            "date": snap.etDate,
            "games": [game.model_dump() for game in snap.rows]
        }
    except Exception as e:
        print(f"API data error: {e}")
        raise HTTPException(status_code=500, detail=f"Error loading data: {str(e)}")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Application health check"""
    try:
        snap = await load_snapshot()
        return {
            "status": "healthy",
            "data_available": snap is not None,
            "data_status": snap.status if snap else "no_data",
            "games_count": len(snap.rows) if snap else 0
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

# Statistics endpoint
@app.get("/api/stats")
async def get_stats():
    """Data statistics"""
    try:
        snap = await load_snapshot()
        if not snap:
            return {"error": "No data available"}
        
        # Count data sources
        source_counts = {}
        for game in snap.rows:
            for source in ["kenpom", "bart", "massey", "hasla", "odds"]:
                metrics = getattr(game, source)
                if metrics and any([
                    metrics.spread is not None,
                    metrics.total is not None,
                    metrics.winProbHome is not None,
                    metrics.moneylineHome is not None
                ]):
                    source_counts[source] = source_counts.get(source, 0) + 1
        
        return {
            "total_games": len(snap.rows),
            "data_status": snap.status,
            "date": snap.etDate,
            "source_coverage": source_counts,
            "games_with_avg_spread": len([g for g in snap.rows if g.avgSpread is not None]),
            "games_with_avg_total": len([g for g in snap.rows if g.avgTotal is not None]),
            "games_with_avg_winprob": len([g for g in snap.rows if g.avgWinProbHome is not None])
        }
    except Exception as e:
        print(f"Stats error: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating stats: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
