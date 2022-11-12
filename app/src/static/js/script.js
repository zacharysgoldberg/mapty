'use strict';

class Orders {
  date = new Date();
  time =
    this.date.getHours() +
    ':' +
    this.date.getMinutes() +
    ':' +
    this.date.getSeconds();
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

    this.description = `${this.inputType[0].toUpperCase()}${this.inputType.slice(
      1
    )} at ${this.time}`;
  }

  click() {
    this.clicks++;
  }
}

class Base extends Orders {
  inputType = 'base';

  constructor(coords) {
    super(coords);
    // let d = this.calcMaxRange(this.coords);
    // min/km
    // this.maxRange = this.coords;
    // return this;
    // this._setDescription(this.time);
  }
}

class Order extends Orders {
  inputType = 'order';

  constructor(coords) {
    super(coords);
    // this.elevationGain = elevationGain;
    // this.calcSpeed();
    // this._setDescription(this.time);
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
const input = document.querySelector('.form__input--type');
const submitOrders = document.querySelector('.form__input');
// const inputDistance = document.querySelector('.form__input--distance');
// const inputDuration = document.querySelector('.form__input--duration');
// const inputCadence = document.querySelector('.form__input--cadence');
// const inputElevation = document.querySelector('.form__input--elevation');

class App {
  #map;
  #mapZoomLevel = 13;
  #mapEvent;
  orders = [];

  constructor() {
    // Get user's position
    this._getPosition();

    // Get data from local storage
    this._getLocalStorage();

    // Attach event handlers
    form.addEventListener('submit', this._newOrder.bind(this)); // must always bind this keyword when calling local methods/functions inside of classes
    input.addEventListener('change', this._calcMaxRange.bind(this));
    containerOrders.addEventListener('submit', this._moveToPopup.bind(this));
    // submitOrders.addEventListener('click', this._setRedisStorage.bind(this));
    this._setRedisStorage(this.orders);
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
    for (let i = 0; i < this.orders.length; i++) {
      if (this.orders[i].inputType === 'base') {
        return this.orders[i].coords;
      }
    }
  }
  // To calculate max range for orders from base location
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

  _setRedisStorage(orders) {
    $('#add_button').click(function () {
      console.log(orders);
      $.ajax({
        url: '/orders/add-order',
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({ orders: orders }),
      });
      // $('.hiddenField').val(JSON.stringify(this.orders));
    });
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

    this.orders.forEach(order => {
      this._renderOrderMarker(order);
    });
  }

  _showForm(mapE) {
    this.#mapEvent = mapE;
    form.classList.remove('hidden');
    // input.focus();
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
    const inputType = input.value;
    // const distance = +inputDistance.value; // + converts to number:(Number())
    // const duration = +inputDuration.value;
    const { lat, lng } = this.#mapEvent.latlng;

    let order;

    // If workout running, create running object

    if (inputType == 'Base' && !this.orders.some(e => e.inputType == 'base')) {
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

    // Catch edge case in the event user tries to add another base
    else if (
      inputType == 'Base' &&
      this.orders.some(e => e.inputType == 'base')
    ) {
      return alert('Only one Base may be submitted');
    }

    // If workout is order, create order object
    else if (inputType == 'Order') {
      // const elevation = +inputElevation.value;

      // if (
      //   !validInputs(distance, duration, elevation) ||
      //   !allPositive(distance, duration)
      // )
      //   return alert('Inputs have to be positive numbers');

      order = new Order([lat, lng]);
    }

    // Add new object to order array
    this.orders.push(order);

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
          className: `${order.inputType}-popup`,
        })
      )
      .setPopupContent(
        `${order.inputType === 'base' ? '🏃‍♂️' : '🚴‍♀️'} ${order.description}`
      )
      .openPopup();
  }

  // some DOM manipulation
  _renderOrder(order) {
    let html = `
    <form
    <li class="order order--${order.inputType}" data-id="${order.id}">
      <h2 class="order__title">${order.description}</h2>
      <div class="order__details">
        <span class="order__icon">${
          order.inputType === 'base' ? '🏃‍♂️' : '🚴‍♀️'
        }</span></div>
        <button onclick="window.location.href='/orders/delete-order/{{order.pk}}'" type="button">Delete</button>`;

    form.insertAdjacentHTML('afterend', html);
  }

  _moveToPopup(e) {
    const orderEl = e.target.closest('.order');
    if (!orderEl) return;

    const order = this.orders.find(order => order.id == orderEl.dataset.id);

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
    localStorage.setItem('orders', JSON.stringify(this.orders));
  }

  _getLocalStorage() {
    const data = JSON.parse(localStorage.getItem('orders'));

    if (!data) return;

    this.orders = data;

    this.orders.forEach(order => {
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
  //   this.orders.sort((a, b) => b.distance - a.distance);
  //   console.log(this.orders);
  // }

  // Edit a order
}

const app = new App();
