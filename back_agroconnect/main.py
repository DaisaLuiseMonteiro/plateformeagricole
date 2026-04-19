from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importation des routes de l'application
from app.routes.user import router as user_router
from app.routes.produit import router as produit_router
from app.routes.notification import router as notification_router
from app.routes.commande import router as commande_router
from app.routes.production import router as production_router

app = FastAPI(
    title="Plateforme de Gestion Agricole API",
    description="API pour la plateforme de gestion agricole",
    version="1.0.0"
)

# Configuration CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://plateformeagricole.vercel.app",
    "https://plateformeagricole-coc8qixax.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins + ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route pour la racine "/"
@app.get("/")
async def root():
    return {
        "message": "Bienvenue sur l'API de la Plateforme de Gestion Agricole",
        "author": "Daisa",
        "email": "daisa@gmil.com",
        "status": "Running"
    }

# Inclusion des routes
app.include_router(user_router)
app.include_router(produit_router)
app.include_router(notification_router)
app.include_router(commande_router)
app.include_router(production_router)
