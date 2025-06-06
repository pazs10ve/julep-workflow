import os
from dotenv import load_dotenv
from weather_service import WeatherService
from cuisine_agent import CuisineAgent
from tour_planner import TourPlanner
from typing import Dict, List, Any

class FoodieTourWorkflow:
    def __init__(self):
        load_dotenv()
        self.weather_service = WeatherService()
        self.cuisine_agent = CuisineAgent()
        self.tour_planner = TourPlanner()
    
    def create_foodie_tour(self, city: str) -> Dict[str, Any]:
        """Create a complete foodie tour for a city"""
        print(f"\n🍽️  Creating foodie tour for {city}...")
        
        # 1. Get weather and dining suggestion
        print("☀️  Checking weather...")
        weather_data = self.weather_service.get_weather(city)
        dining_type = self.weather_service.suggest_dining_type(weather_data)
        print(f"Weather: {weather_data['description']} ({weather_data['temperature']}°C)")
        print(f"Dining suggestion: {dining_type}")
        
        # 2. Get local dishes
        print("🥘  Finding iconic local dishes...")
        dishes = self.cuisine_agent.get_local_dishes(city)
        print(f"Local dishes: {', '.join(dishes)}")
        
        # 3. Find restaurants
        print("🏪  Finding top-rated restaurants...")
        restaurants = self.cuisine_agent.find_restaurants(city, dishes)
        print(f"Restaurants found: {len(restaurants)}")
        
        # 4. Create tour narrative
        print("📝  Creating tour narrative...")
        tour_narrative = self.tour_planner.create_tour(
            city, weather_data, dining_type, restaurants
        )
        
        return {
            'city': city,
            'weather': weather_data,
            'dining_type': dining_type,
            'dishes': dishes,
            'restaurants': restaurants,
            'tour_narrative': tour_narrative
        }
    
    def run_workflow(self, cities: List[str]):
        """Run the complete workflow for multiple cities"""
        print("🚀 Starting Foodie Tour Workflow")
        print("=" * 50)
        
        results = []
        for city in cities:
            try:
                result = self.create_foodie_tour(city)
                results.append(result)
                
                # Display results
                print(f"\n📍 FOODIE TOUR FOR {city.upper()}")
                print("-" * 30)
                print(result['tour_narrative'])
                print("\n" + "=" * 50)
                
            except Exception as e:
                print(f"❌ Error processing {city}: {e}")
        
        return results

# Example usage and main execution
if __name__ == "__main__":
    # List of cities to create foodie tours for
    cities = ["Paris", "Tokyo", "New York"]
    
    # Create and run workflow
    workflow = FoodieTourWorkflow()
    results = workflow.run_workflow(cities)
    
    print(f"\n✅ Completed foodie tours for {len(results)} cities!")