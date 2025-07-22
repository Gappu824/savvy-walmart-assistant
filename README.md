# Walmart Savvy: AI-Powered Meal Planning Assistant

**Savvy** is a proactive, AI-powered grocery planning assistant that
transforms weekly meal decisions into a seamless, personalized process.
Integrated into the Walmart shopping ecosystem, it uses your pantry,
taste profile, and intelligent parsing to recommend meals, minimize food
waste, and auto-fill shopping lists.

https://github.com/user-attachments/assets/f564a863-3938-4c89-bff2-486d47416dbd



------------------------------------------------------------------------

## 🧠 Problem Statement

-   **Overwhelming mental load** from daily meal planning
-   **Redundant shopping** due to lack of pantry visibility
-   **Wasted groceries** and missed offers
-   **Lack of personalization** in current meal-planning apps

------------------------------------------------------------------------

## 🚀 Core Features

-   **AI-Powered Query Understanding:** Uses a fine-tuned
    TinyLlama-1.1B-Chat model to extract ingredients, diets, and recipe
    types from natural language queries.
-   **Real-Time Pantry Sync:** Pantry tracked per user with optional
    expiry dates. Add/delete items from the app or backend.
-   **Smart Shopping List:** Compares your chosen recipe with pantry
    items and adds only the missing ingredients -- with substitutions
    for Great Value products.
-   **Taste Profiles:** Customize dietary preferences, household size,
    and health goals.
-   **Microservices Architecture:** Modular FastAPI-based services
    containerized via Docker Compose.

------------------------------------------------------------------------

## 🏗 Architecture

    Frontend (React Native / Expo)
       ↓
    local_server.py (API Gateway)
       ↓
    [ user_service | recommendation_service | community_service ]
       ↓
    [ TinyLlama + Spoonacular API + Postgres DB ]

------------------------------------------------------------------------

## 📦 Installation

### 🔧 Prerequisites

-   Python 3.10
-   Node.js 18+ and npm
-   Expo CLI (`npm install -g expo-cli`)
-   Docker (optional, for full stack)

### 💻 Running the Project

#### **Backend**

    cd backend
    python -m venv venv
    source venv/bin/activate   # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    python local_server.py

#### **Docker Multi-Service Setup**

    docker-compose up --build

#### **Frontend (Expo App)**

    cd frontend
    npm install
    npx expo start

Scan the QR code shown in the terminal using the Expo Go app on your
phone.

------------------------------------------------------------------------

## 📚 API Endpoints

-   `POST /recommend` --- Get recommended recipes
-   `GET /pantry/{user_id}` --- View pantry items
-   `POST /pantry/{user_id}` --- Add an item to pantry
-   `DELETE /pantry/item/{item_id}` --- Remove pantry item
-   `GET /smart-cart/{user_id}/{recipe_id}` --- List missing ingredients
-   `POST /shopping-list/{user_id}/{recipe_id}` --- Add to shopping list
-   `GET /shopping-list/{user_id}` --- View full list

------------------------------------------------------------------------

## 🧠 Model & AI Integration

-   **Base Model:** TinyLlama-1.1B-Chat-v1.0
-   **Adapter:** PEFT (LoRA adapter for personalization)
-   **Fallback Strategy:** AI parse → Pantry-boosted parse → Raw
    fallback
-   **External API:** Spoonacular used to enrich natural language output

------------------------------------------------------------------------

## 🔍 Known Issues & Improvements

> Based on review of
> [Gappu824/savvy-walmart-assistant](https://github.com/Gappu824/savvy-walmart-assistant){target="_blank"}

1.  **Missing .env file**: API keys hard-coded --- should be securely
    loaded using `os.getenv()`.
2.  **No .gitignore**: Sensitive and build files should be excluded from
    Git commits.
3.  **Incomplete Model Card**: Model and adapter details require
    completion.
4.  **API Key Leakage**: Visible inside `local_server.py` and `main.py`.
5.  **No Testing & CI:** No formal tests (e.g., with `pytest`) or GitHub
    Actions workflow.
6.  **Lack of Error Handling**: Community/user services need error
    tracing and validation.
7.  **Hardcoded User ID**: Authentication not yet implemented.

------------------------------------------------------------------------

## 🛠 To Do

-   \[ \] Create and reference a `.env`
-   \[ \] Update and add a `.gitignore`
-   \[ \] Secure API keys in all services
-   \[ \] Add backend and integration tests
-   \[ \] Implement continuous integration (CI)
-   \[ \] Finalize Model Card and attach in repo
-   \[ \] Add onboarding UX for new users

------------------------------------------------------------------------

## 📄 License

MIT License --- © 2024 Walmart Savvy Hackathon Team
