'use strict';

class Orders {
  today = new Date();
  time =
    this.today.getHours() +
    ':' +
    this.today.getMinutes() +
    ':' +
    this.today.getSeconds();
  // id = (Date.now() + '').slice(-10);
  clicks = 0;

  constructor(coords) {
    this.coords = coords; // {lat, long}
    // this.distance = distance; // km
    // this.duration = duration; // min
  }

  _setDescription(time) {
    // prettier-ignore
    const months = [
      'January', 
      'February', 
      'March', 
      'April', 
      'May',
      'June', 
      'July', 
      'August', 
      'September', 
      'October', 
      'November', 
      'December'
    ];

    this.description = `${this.type[0].toUpperCase()}${this.type.slice(1)} at ${
      this.time
    }`;
  }

  click() {
    this.clicks++;
  }
}

class Base extends Orders {
  type = 'base';

  constructor(coords) {
    super(coords);
    // let d = this.calcMaxRange(this.coords);
    // min/km
    // this.maxRange = this.coords;
    // return this;
    this._setDescription(this.time);
  }
}

class Order extends Orders {
  type = 'order';

  constructor(coords) {
    super(coords);
    // this.elevationGain = elevationGain;
    // this.calcSpeed();
    this._setDescription(this.time);
  }

  // calcSpeed() {
  //   // km/h
  //   this.speed = this.distance / (this.duration / 60);
  //   return this;
  // }
}

// const run1 = new Running([39, -12], 5.2, 24, 178);
// const cycling1 = new Cycling([39, -12], 27, 95, 523);
// console.log(run1, cycling1);

///////////////////////////////////////////
// APPLICATION ARCHITECTURE
const form = document.querySelector('.form');
const containerOrders = document.querySelector('.orders');
const inputType = document.querySelector('.form__input--type');
// const inputDistance = document.querySelector('.form__input--distance');
// const inputDuration = document.querySelector('.form__input--duration');
// const inputCadence = document.querySelector('.form__input--cadence');
// const inputElevation = document.querySelector('.form__input--elevation');

class App {
  #map;
  #mapZoomLevel = 13;
  #mapEvent;
  #orders = [];

  constructor() {
    // Get user's position
    this._getPosition();

    // Get data from local storage
    this._getLocalStorage();

    // Attach event handlers
    form.addEventListener('submit', this._newOrder.bind(this)); // must always bind this keyword when calling local methods/functions inside of classes
    inputType.addEventListener('change', this._calcMaxRange.bind(this));
    containerOrders.addEventListener('click', this._moveToPopup.bind(this));
  }

  _getPosition() {
    if (navigator.geolocation)
      navigator.geolocation.getCurrentPosition(
        this._loadMap.bind(this),
        function () {
          alert('Could not get your position');
        }
      );
  }

  _getBase() {
    for (let i = 0; i < this.#orders.length; i++) {
      if (this.#orders[i].type === 'base') {
        return this.#orders[i].coords;
      }
    }
  }

  _calcMaxRange(coords1, coords2) {
    coords1 = this.#mapEvent.latlng;
    coords2 = this._getBase();
    var earthRadius = 6371;
    var dLat = this.deg2rad(coords2[0] - coords1.lat);
    var dLon = this.deg2rad(coords2[1] - coords1.lng);
    var a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(this.deg2rad(coords1.lat)) *
        Math.cos(this.deg2rad(coords2[0])) *
        Math.sin(dLon / 2) *
        Math.sin(dLon / 2);
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    var d = earthRadius * c; // Distance in km
    console.log(d);
    return d;
  }

  deg2rad(deg) {
    return deg * (Math.PI / 180);
  }

  _loadMap(position) {
    const { latitude } = position.coords;
    const { longitude } = position.coords;
    // console.log(latitude, longitude);
    console.log(`https://www.google.com/maps/@${latitude},${longitude}`);

    const coords = [latitude, longitude];

    this.#map = L.map('map').setView(coords, this.#mapZoomLevel); // (coordinates, zoom level)
    // console.log(map);

    L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(this.#map);

    // Handling clicks on map
    this.#map.on('click', this._showForm.bind(this));

    this.#orders.forEach(order => {
      this._renderOrderMarker(order);
    });
  }

  _showForm(mapE) {
    this.#mapEvent = mapE;
    form.classList.remove('hidden');
    // inputType.focus();
    // inputDistance.focus();
  }

  _hideForm() {
    // // Empty inputs
    // inputDistance.value =
    //   inputDuration.value =
    //   inputCadence.value =
    //   inputElevation.value =
    //     '';

    form.style.display = 'none';
    form.classList.add('hidden');
    setTimeout(() => (form.style.display = 'grid'), 1000);
  }

  // _toggleElevationField() {
  //   inputElevation.closest('.form__row').classList.toggle('form__row--hidden');
  //   inputCadence.closest('.form__row').classList.toggle('form__row--hidden');
  // }

  _newOrder(e) {
    // const validInputs = (...inputs) =>
    //   inputs.every(inp => Number.isFinite(inp));
    // const allPositive = (...inputs) => inputs.every(inp => inp > 0);

    e.preventDefault();
    // console.log(this);

    // Get data from form
    const type = inputType.value;
    // const distance = +inputDistance.value; // + converts to number:(Number())
    // const duration = +inputDuration.value;
    const { lat, lng } = this.#mapEvent.latlng;

    let order;

    // If workout running, create running object
    if (type == 'Base') {
      // const cadence = +inputCadence.value;

      // // Check if data is valid
      // if (
      //   // !Number.isFinite(distance) ||
      //   // !Number.isFinite(duration) ||
      //   // !Number.isFinite(cadence)
      //   !validInputs(distance, duration, cadence) ||
      //   !allPositive(distance, duration, cadence)
      // )
      //   return alert('Inputs have to be positive numbers');

      order = new Base([lat, lng]);
    }

    // If workout is order, create order object
    if (type == 'Order') {
      // const elevation = +inputElevation.value;

      // if (
      //   !validInputs(distance, duration, elevation) ||
      //   !allPositive(distance, duration)
      // )
      //   return alert('Inputs have to be positive numbers');

      order = new Order([lat, lng]);
    }

    // Add new object to order array
    this.#orders.push(order);

    // Render order on map as marker
    this._renderOrderMarker(order);

    // Render order on list
    this._renderOrder(order);

    // Hide form + Clear input fields
    this._hideForm();

    // Set local storage to all orders
    this._setLocalStorage();
  }

  _renderOrderMarker(order) {
    L.marker(order.coords)
      .addTo(this.#map)
      .bindPopup(
        L.popup({
          maxWidth: 250,
          minWidth: 100,
          autoClose: false,
          closeOnClick: false,
          className: `${order.type}-popup`,
        })
      )
      .setPopupContent(
        `${order.type === 'base' ? '🏃‍♂️' : '🚴‍♀️'} ${order.description}`
      )
      .openPopup();
  }

  // some DOM manipulation
  _renderOrder(order) {
    let html = `
    <form
    <li class="order order--${order.type}" data-id="${order.id}">
      <h2 class="order__title">${order.description}</h2>
      <div class="order__details">
        <span class="order__icon">${
          order.type === 'base' ? '🏃‍♂️' : '🚴‍♀️'
        }</span></div>
        <button onclick="window.location.href='/orders/delete-order/{{order.pk}}'" type="button">Delete</button>`;

    // if (order.type === 'base')
    //   html += `
    //     <div class="order__details">
    //         <span class="order__icon">⚡️</span>
    //         <span class="order__value">${order.pace.toFixed(1)}</span>
    //         <span class="order__unit">min/km</span>
    //       </div>
    //       <div class="order__details">
    //         <span class="order__icon">🦶🏼</span>
    //         <span class="order__value">${order.cadence}</span>
    //         <span class="order__unit">spm</span>
    //       </div>
    //       </li>`;

    // if (order.type === 'order')
    //   html += `
    //     <div class="order__details">
    //         <span class="order__icon">⚡️</span>
    //         <span class="order__value">${order.speed.toFixed(1)}</span>
    //         <span class="order__unit">km/h</span>
    //       </div>
    //       <div class="order__details">
    //         <span class="order__icon">⛰</span>
    //         <span class="order__value">${order.elevationGain}</span>
    //         <span class="order__unit">m</span>
    //       </div>
    //       </li>
    // `;

    form.insertAdjacentHTML('afterend', html);
  }

  _moveToPopup(e) {
    const orderEl = e.target.closest('.order');
    if (!orderEl) return;

    const order = this.#orders.find(order => order.id == orderEl.dataset.id);

    this.#map.setView(order.coords, this.#mapZoomLevel, {
      animate: true,
      pan: {
        duration: 1,
      },
    });

    // using the public interface
    // order.click();
  }

  _setLocalStorage() {
    localStorage.setItem('orders', JSON.stringify(this.#orders));
  }

  _getLocalStorage() {
    const data = JSON.parse(localStorage.getItem('orders'));

    if (!data) return;

    this.#orders = data;

    this.#orders.forEach(order => {
      this._renderOrder(order);
    });
  }

  // Reset
  reset() {
    localStorage.removeItem('orders');
    location.reload();
  }

  // Delete a order
  removeOrder() {}

  // Sort orders
  // sortOrders() {
  //   this.#orders.sort((a, b) => b.distance - a.distance);
  //   console.log(this.#orders);
  // }

  // Edit a order
}

const app = new App();
