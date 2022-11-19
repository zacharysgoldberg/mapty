# Pizza Drone

Pizza Drone simulator that uses user geolocation data input to display optimal path for delivery. Implemented JQuery/AJAX for fetching location data to FastAPI routes and temporarily storing it in Redis database using Redis-OM.

**Frontend in-progress**

## Features

* Implemented OpenStreetMap API
* Path finding animation

## Algorithmic challenge

Calculating the optimal path required a custom variation of the [Held–Karp algorithm](https://en.wikipedia.org/wiki/Held%E2%80%93Karp_algorithm) to solve the Traveling Salesman Problem.
