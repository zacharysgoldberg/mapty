# Pizza Drone

Pizza Drone simulator that uses user geolocation data input to display optimal path for delivery. Leveraging the Leaflet library for interactive map functionality and a backend API for path computation, the project provides a practical solution for visual route planning.

**Frontend in-progress**

## Features

- **Interactive Map Interface**: Users can select multiple points by clicking on the map.
- **Dynamic Route Calculation**: The application computes the shortest path connecting the selected points.
- **Real-Time Feedback**: Immediate visual and textual feedback on the computed route and distance.
- **Scalable Backend**: The backend is designed to handle multiple points and provide accurate distance calculations.

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript, Leaflet.js, jQuery
- **Backend**: Python, Flask
- **Data**: OpenStreetMap for geocoding
- **Other Tools**: Docker (for deployment), pytest (for testing)

## Algorithmic challenge

Calculating the optimal path required a custom variation of the [Held–Karp algorithm](https://en.wikipedia.org/wiki/Held%E2%80%93Karp_algorithm) to solve the Traveling Salesman Problem.
