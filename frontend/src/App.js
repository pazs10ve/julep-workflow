import React, { useState, useEffect, useCallback } from 'react';

const API_BASE_URL = 'http://localhost:8000'; // Your FastAPI backend URL

function App() {
  const [city, setCity] = useState('');
  const [taskId, setTaskId] = useState(null);
  const [tourStatus, setTourStatus] = useState(null);
  const [tourResult, setTourResult] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const pollInterval = 3000; // Poll every 3 seconds

  const handleFetchStatus = useCallback(async (currentTaskId) => {
    if (!currentTaskId) return;

    try {
      const response = await fetch(`${API_BASE_URL}/tour/status/${currentTaskId}`);
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setTourStatus(data.status);
      setError(data.error || null);

      if (data.status === 'completed') {
        setTourResult(data.result);
        setTaskId(null); // Stop polling
        setIsLoading(false);
      } else if (data.status === 'failed') {
        setError(data.error || 'Tour generation failed.');
        setTaskId(null); // Stop polling
        setIsLoading(false);
      }
    } catch (err) {
      console.error('Failed to fetch status:', err);
      setError(err.message);
      setTaskId(null); // Stop polling on error
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    let intervalId;
    if (taskId && (tourStatus === 'pending' || tourStatus === 'processing')) {
      intervalId = setInterval(() => {
        handleFetchStatus(taskId);
      }, pollInterval);
    }
    return () => clearInterval(intervalId);
  }, [taskId, tourStatus, handleFetchStatus, pollInterval]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!city.trim()) {
      setError('City name cannot be empty.');
      return;
    }

    setIsLoading(true);
    setError(null);
    setTourResult(null);
    setTourStatus(null);
    setTaskId(null);

    try {
      const response = await fetch(`${API_BASE_URL}/tour/async`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ city }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setTaskId(data.task_id);
      setTourStatus('pending'); // Initial status
      // Start polling by triggering useEffect
    } catch (err) {
      console.error('Failed to create tour:', err);
      setError(err.message);
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Foodie Tour Planner</h1>
      </header>

      <form onSubmit={handleSubmit} className="tour-form">
        <input
          type="text"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          placeholder="Enter city name"
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Planning...' : 'Plan My Tour'}
        </button>
      </form>

      {error && (
        <div className="status-section error-message">
          <p>Error: {error}</p>
        </div>
      )}

      {taskId && tourStatus && (tourStatus === 'pending' || tourStatus === 'processing') && (
        <div className="status-section loading-message">
          <p>Status: {tourStatus} (Task ID: {taskId})</p>
          <p>Checking for updates...</p>
        </div>
      )}

      {tourResult && (
        <div className="results-section">
          <h3>Tour for {tourResult.city}</h3>
          <p><strong>Weather:</strong> {tourResult.weather.description}, {tourResult.weather.temperature}°C</p>
          <p><strong>Suggested Dining:</strong> {tourResult.dining_type}</p>
          <p><strong>Recommended Dishes:</strong> {tourResult.dishes.join(', ')}</p>
          <h4>Restaurants:</h4>
          {tourResult.restaurants && tourResult.restaurants.length > 0 ? (
            <ul className="restaurant-list">
              {tourResult.restaurants.map((resto, index) => (
                <li key={index}>
                  <strong>{resto.name}</strong> ({resto.cuisine})
                  {resto.rating && <span> - Rating: {resto.rating}</span>}
                  {resto.address && <p><em>{resto.address}</em></p>}
                  {resto.specialties && resto.specialties.length > 0 && (
                    <p>Specialties: {resto.specialties.join(', ')}</p>
                  )}
                </li>
              ))}
            </ul>
          ) : (
            <p>No specific restaurants listed for this plan.</p>
          )}
          <h4>Tour Narrative:</h4>
          <pre>{tourResult.tour_narrative}</pre>
          <p><small>Created at: {new Date(tourResult.created_at).toLocaleString()}</small></p>
        </div>
      )}
    </div>
  );
}

export default App;
