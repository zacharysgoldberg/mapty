# Pizza Drone

Pizza Drone that uses user geolocation data to display selected delivery route on GPS map. Implemented JQuery/AJAX for fetching location data to FastAPI routes and temporarily stored in Redis database using Redis-OM.

**Frontend in-progress**

## Features

* Implemented OpenStreetMap API
* Path finding animation

## Algorithmic challenge

Calculating the optimal path required a custom variation of the [Held–Karp algorithm](https://en.wikipedia.org/wiki/Held%E2%80%93Karp_algorithm) to solve the Traveling Salesman Problem.
