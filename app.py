from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import asyncio
import uuid
import uvicorn
from datetime import datetime
from dotenv import load_dotenv
from weather_service import WeatherService
from cuisine_agent import CuisineAgent
from tour_planner import TourPlanner

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Foodie Tour API",
    description="API for creating personalized foodie tours in different cities",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class CityRequest(BaseModel):
    city: str = Field(..., description="Name of the city for the foodie tour")

class MultipleCitiesRequest(BaseModel):
    cities: List[str] = Field(..., description="List of cities for foodie tours")

class WeatherData(BaseModel):
    temperature: float
    description: str
    humidity: Optional[int] = None
    wind_speed: Optional[float] = None

class Restaurant(BaseModel):
    name: str
    cuisine: str
    rating: Optional[float] = None
    address: Optional[str] = None
    specialties: Optional[List[str]] = None

class FoodieTourResponse(BaseModel):
    city: str
    weather: Dict[str, Any]
    dining_type: str
    dishes: List[str]
    restaurants: List[Dict[str, Any]]
    tour_narrative: str
    created_at: datetime

class TourStatus(BaseModel):
    task_id: str
    status: str  # "pending", "processing", "completed", "failed"
    progress: Optional[int] = None
    result: Optional[FoodieTourResponse] = None
    error: Optional[str] = None

# In-memory storage for async tasks (use Redis in production)
task_storage: Dict[str, TourStatus] = {}

class FoodieTourWorkflow:
    def __init__(self):
        self.weather_service = WeatherService()
        self.cuisine_agent = CuisineAgent()
        self.tour_planner = TourPlanner()
    
    async def create_foodie_tour(self, city: str) -> Dict[str, Any]:
        """Create a complete foodie tour for a city (async version)"""
        try:
            # Simulate async operations
            await asyncio.sleep(0.1)  # Small delay to simulate processing
            
            # 1. Get weather and dining suggestion
            weather_data = self.weather_service.get_weather(city)
            dining_type = self.weather_service.suggest_dining_type(weather_data)
            
            await asyncio.sleep(0.1)
            
            # 2. Get local dishes
            dishes = self.cuisine_agent.get_local_dishes(city)
            
            await asyncio.sleep(0.1)
            
            # 3. Find restaurants
            restaurants = self.cuisine_agent.find_restaurants(city, dishes)
            
            await asyncio.sleep(0.1)
            
            # 4. Create tour narrative
            tour_narrative = self.tour_planner.create_tour(
                city, weather_data, dining_type, restaurants
            )
            
            return {
                'city': city,
                'weather': weather_data,
                'dining_type': dining_type,
                'dishes': dishes,
                'restaurants': restaurants,
                'tour_narrative': tour_narrative,
                'created_at': datetime.now()
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating tour for {city}: {str(e)}")

# Initialize workflow
workflow = FoodieTourWorkflow()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Foodie Tour API is running!",
        "version": "1.0.0",
        "endpoints": {
            "single_tour": "/tour",
            "multiple_tours": "/tours",
            "async_tour": "/tour/async",
            "task_status": "/tour/status/{task_id}"
        }
    }

@app.post("/tour", response_model=FoodieTourResponse)
async def create_single_tour(request: CityRequest):
    """Create a foodie tour for a single city"""
    try:
        result = await workflow.create_foodie_tour(request.city)
        return FoodieTourResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tours")
async def create_multiple_tours(request: MultipleCitiesRequest):
    """Create foodie tours for multiple cities"""
    results = []
    errors = []
    
    for city in request.cities:
        try:
            result = await workflow.create_foodie_tour(city)
            results.append(FoodieTourResponse(**result))
        except Exception as e:
            errors.append({"city": city, "error": str(e)})
    
    return {
        "results": results,
        "errors": errors,
        "total_requested": len(request.cities),
        "successful": len(results),
        "failed": len(errors)
    }

async def process_tour_async(task_id: str, city: str):
    """Background task to process tour creation"""
    try:
        # Update status to processing
        task_storage[task_id].status = "processing"
        task_storage[task_id].progress = 10
        
        # Create the tour
        result = await workflow.create_foodie_tour(city)
        
        # Update status to completed
        task_storage[task_id].status = "completed"
        task_storage[task_id].progress = 100
        task_storage[task_id].result = FoodieTourResponse(**result)
        
    except Exception as e:
        task_storage[task_id].status = "failed"
        task_storage[task_id].error = str(e)

@app.post("/tour/async")
async def create_tour_async(request: CityRequest, background_tasks: BackgroundTasks):
    """Create a foodie tour asynchronously and return task ID"""
    task_id = str(uuid.uuid4())
    
    # Initialize task status
    task_storage[task_id] = TourStatus(
        task_id=task_id,
        status="pending",
        progress=0
    )
    
    # Add background task
    background_tasks.add_task(process_tour_async, task_id, request.city)
    
    return {
        "task_id": task_id,
        "message": f"Tour creation started for {request.city}",
        "status_url": f"/tour/status/{task_id}"
    }

@app.get("/tour/status/{task_id}", response_model=TourStatus)
async def get_tour_status(task_id: str):
    """Get the status of an async tour creation task"""
    if task_id not in task_storage:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task_storage[task_id]

@app.get("/cities/popular")
async def get_popular_cities():
    """Get a list of popular cities for foodie tours"""
    return {
        "popular_cities": [
            "Chicago", "Paris", "Mumbai", "Tokyo", "Bangkok", 
            "Istanbul", "Rome", "Barcelona", "New York", "London",
            "Melbourne", "Singapore", "Hong Kong", "Seoul", "Mexico City"
        ]
    }

@app.get("/tour/{city}/preview")
async def get_city_preview(city: str):
    """Get a preview of what a foodie tour might include for a city"""
    try:
        # Get basic info without creating full tour
        weather_data = workflow.weather_service.get_weather(city)
        dishes = workflow.cuisine_agent.get_local_dishes(city)
        
        return {
            "city": city,
            "current_weather": weather_data,
            "popular_dishes": dishes[:5],  # Top 5 dishes
            "estimated_restaurants": "8-12",
            "tour_duration": "4-6 hours"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting preview for {city}: {str(e)}")

@app.delete("/tour/status/{task_id}")
async def delete_task(task_id: str):
    """Delete a completed or failed task from storage"""
    if task_id not in task_storage:
        raise HTTPException(status_code=404, detail="Task not found")
    
    del task_storage[task_id]
    return {"message": f"Task {task_id} deleted successfully"}

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "error": True,
        "message": exc.detail,
        "status_code": exc.status_code
    }

if __name__ == "__main__":
    uvicorn.run(
        "app:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )



# uvicorn app:app --reload