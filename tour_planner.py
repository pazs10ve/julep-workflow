from julep import Julep
import yaml
import time
import os
from typing import Dict, Any, List

class TourPlanner:
    def __init__(self):
        self.client = Julep(api_key=os.getenv('JULEP_API_KEY'))
        self.agent = self._create_agent()
        self.tour_task = self._create_tour_task()
    
    def _create_agent(self):
        """Create the tour planning agent"""
        try:
            agent = self.client.agents.create(
                name="Foodie Tour Planner",
                model="gpt-4o",
                about="A creative tour planner that crafts delightful foodie experiences."
            )
            print(f"Agent created successfully with ID: {agent.id}")
            return agent
        except Exception as e:
            print(f"Failed to create agent: {e}")
            raise
    
    def _create_tour_task(self):
        """Create task to plan a foodie tour"""
        task_definition = {
            "name": "Create Foodie Tour",
            "description": "Create a delightful one-day foodie tour narrative",
            "main": [
                {
                    "prompt": [
                        {
                            "role": "system",
                            "content": """You are a creative foodie tour planner. Create a one-day foodie tour plan for a given city. Use the provided city, weather, dining preference, and restaurant list. Format the response with clear headers (## Breakfast, ## Lunch, ## Dinner) and consider the weather conditions in the narrative."""
                        }
                    ]
                }
            ]
        }
        
        try:
            task = self.client.tasks.create(
                agent_id=self.agent.id,
                **task_definition
            )
            print(f"Task created successfully with ID: {task.id}")
            return task
        except Exception as e:
            print(f"Failed to create task: {e}")
            raise
    
    def create_tour(self, city: str, weather_data: Dict[str, Any], 
                   dining_type: str, restaurants: List[str]) -> str:
        """Create a foodie tour narrative"""
        try:
            user_message = f"""Create a delightful one-day foodie tour for {city}.

Tour Details:
- Weather: {weather_data['description']} ({weather_data['temperature']}°C)
- Dining preference: {dining_type}
- Featured restaurants: {', '.join(restaurants)}

Please create brief but engaging narratives for breakfast, lunch, and dinner that consider the weather conditions. Format your response with clear meal headers (## Breakfast, ## Lunch, ## Dinner)."""

            execution = self.client.executions.create(
                task_id=self.tour_task.id,
                input={
                    "user_message": user_message
                }
            )
            
            print(f"Execution created with ID: {execution.id}")
            result = self._wait_for_completion(execution.id)
            
            if result.status == "succeeded" and hasattr(result, 'output') and result.output:
                # Extract the content from the chat.completion response
                if isinstance(result.output, dict) and 'choices' in result.output:
                    content = result.output['choices'][0]['message']['content']
                    # Check if the response contains the expected headers
                    if "## Breakfast" in content and "## Lunch" in content and "## Dinner" in content:
                        return content
                    else:
                        print("Response does not contain expected narrative structure. Using fallback.")
                        return self._create_fallback_tour(city, weather_data, dining_type, restaurants)
                else:
                    print("Unexpected output structure. Using fallback.")
                    return self._create_fallback_tour(city, weather_data, dining_type, restaurants)
            else:
                print(f"Execution failed or timed out. Status: {result.status}")
                if hasattr(result, 'error') and result.error:
                    print(f"Error details: {result.error}")
                print(f"Full result: {result}")
                return self._create_fallback_tour(city, weather_data, dining_type, restaurants)
                
        except Exception as e:
            print(f"Exception occurred: {e}")
            return self._create_fallback_tour(city, weather_data, dining_type, restaurants)
    
    def _create_fallback_tour(self, city: str, weather_data: Dict[str, Any], 
                            dining_type: str, restaurants: List[str]) -> str:
        """Create a simple fallback tour when API fails"""
        weather_desc = weather_data['description']
        temp = weather_data['temperature']
        
        tour = f"""## Your Foodie Tour of {city}

**Weather**: {weather_desc} ({temp}°C)
**Dining Style**: {dining_type}

## Breakfast
Start your day at {restaurants[0] if restaurants else 'a local café'} for a delightful morning meal. The {weather_desc} weather makes it perfect for {"outdoor seating" if dining_type == "outdoor" and temp > 15 else "a cozy indoor experience"}.

## Lunch  
For lunch, head to {restaurants[1] if len(restaurants) > 1 else 'a traditional restaurant'} to experience authentic local flavors. {"Enjoy the pleasant weather on their terrace" if dining_type == "outdoor" and temp > 15 else "Savor the warmth inside while watching the world go by"}.

## Dinner
End your culinary adventure at {restaurants[2] if len(restaurants) > 2 else 'a renowned dinner spot'} for an unforgettable evening meal. The perfect way to conclude your foodie exploration of {city}!

*Bon appétit!*"""
        
        return tour
    
    def _wait_for_completion(self, execution_id: str):
        """Wait for task execution to complete"""
        max_attempts = 30
        attempts = 0
        
        while attempts < max_attempts:
            result = self.client.executions.get(execution_id)
            if result.status in ['succeeded', 'failed']:
                return result
            time.sleep(1)
            attempts += 1
        
        return type('Result', (), {'status': 'timeout', 'output': None})()

# Example usage
if __name__ == "__main__":
    tour_planner = TourPlanner()
    
    city = "Chandigarh"
    weather_data = {
        'temperature': 18,
        'description': 'partly cloudy',
        'feels_like': 16,
        'humidity': 65
    }
    dining_type = "outdoor"
    restaurants = [
        "Croissant - Du Pain et des Idées",
        "Coq au Vin - L'Ami Jean", 
        "Crème Brûlée - Le Comptoir du Relais"
    ]
    
    tour = tour_planner.create_tour(city, weather_data, dining_type, restaurants)
    print(f"Foodie Tour for {city}:\n{tour}")