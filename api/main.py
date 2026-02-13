from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.predict import router as predict_router
from api.routes.hotspots import router as hotspots_router
from api.routes.alerts import router as alerts_router
from api.routes.auth import router as auth_router

app = FastAPI(
    title="Accident Severity Prediction API",
    description="Backend API for accident severity prediction, hotspots, alerts, and announcements",
    version="1.0.0"
)

# -------------------------------------------------
# ✅ CORS CONFIGURATION (VERY IMPORTANT)
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://localhost:5173",          # ✅ Vite
        "http://127.0.0.1:5173"           # ✅ Vite
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# ✅ API ROUTERS
# -------------------------------------------------
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(predict_router, prefix="/predict", tags=["Prediction"])
app.include_router(hotspots_router, prefix="/hotspots", tags=["Hotspots"])
app.include_router(alerts_router, prefix="/alerts", tags=["Alerts"])

# -------------------------------------------------
# ✅ ROOT CHECK (Health Test)
# -------------------------------------------------
@app.get("/", tags=["Health"])
def root():
    return {
        "status": "Backend is running successfully",
        "message": "FastAPI backend connected and ready"
    }