# Pizza Drone

Pizza Drone map that uses user geolocation data to display selected delivery route on OpenStreetMap API. Frontend complete, FastAPI backend in-progress, including OAuth 2.0.

## Algorithmic challenge

To calculate the optimal path for the drone to follow and return to store requires a variation of the Traveling Salesman Problem. Currently utilizing "Greedy" algorithm to accomplish this with the help of google or-tools library.
