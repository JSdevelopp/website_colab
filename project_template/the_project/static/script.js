document.addEventListener('DOMContentLoaded', function () {
  console.log(document.getElementById('addressChoice1'));
  console.log(document.querySelector('.radio-container'));
  const radios = document.querySelectorAll("input[name='addressChoice']");
  const billingAddressForm = document.getElementById('billingAddressForm');
  console.log('billingAddressForm:', billingAddressForm);

  const form = document.querySelector('form');
  const saveAndContinueButtonAddress = document.getElementById(
    'saveAndContinueButtonForAddress'
  );
  const saveAndContinueButtonPayment = document.getElementById(
    'saveAndContinueButtonPayment'
  );
  const paymentSection = document.querySelector('.paymentSection');
  const cardExpiry = document.getElementById('cardExpiry');
  const processOrderButton = document.getElementById('processOrderButton');
  const backToAddressButton = document.getElementById('backToAddressButton');

  // Initialization: Hide process order btn first on load
  hideElement(processOrderButton);
  hideElement(backToAddressButton); // hide back btn

  let isAddressValidated = false;
  let isPaymentValidated = false;

  // Helper Functions

  function showElement(element) {
    console.log('Showing element:', element);
    if (element) {
      element.style.display = 'block';
      element.classList.remove('d-none');
      setTimeout(() => {
        element.classList.add('show'); // Add the sliding effect after 3 seconds
      }, 1000);
    }
  }

  function hideElement(element) {
    console.log('Hiding element:', element);
    if (element) {
      element.classList.add('d-none');
      element.classList.remove('show'); // Reverse the sliding effect
      setTimeout(() => {
        element.style.display = 'none'; // Hide the element
      }, 300);
    }
  }

  function isRadioGroupChecked(name) {
    return !!document.querySelector(`input[name="${name}"]:checked`);
  }

  function areAllRequiredFieldsFilled(fields) {
    let allFieldsFilled = true;

    fields.forEach((id) => {
      let el = document.getElementById(id);

      if (!el) {
        console.error(`Element with ID ${id} not found!`);
        return; // continue to the next iteration
      }

      // Clear previous highlights
      el.classList.remove('missing-field');

      if (el.type === 'radio') {
        const isChecked = isRadioGroupChecked(el.name);
        console.log('Found a radio:', el.name, 'Is it checked?', isChecked);

        // if the radio group is not checked
        if (!isChecked) {
          el.closest('.radio-container').classList.add('missing-field');
          allFieldsFilled = false;
        }
      } else if (!el.value.trim()) {
        el.classList.add('missing-field');
        allFieldsFilled = false;
      }
    });

    return allFieldsFilled;
  }

  function areAllPaymentFieldsFilled() {
    const paymentFields = [
      'CardNumberInput',
      'CardNameInput',
      'cardExpiry',
      'CardCVVInput',
      // ... Add other fields if necessary
    ];
    return areAllRequiredFieldsFilled(paymentFields);
  }

  // Event Handlers

  // radios.forEach((radio) => {
  //   radio.addEventListener('change', function () {
  //     if (this.value === 'different') {
  //       showElement(billingAddressForm);
  //       clearBillingFields();
  //     } else {
  //       hideElement(billingAddressForm);
  //       copyShippingAddressToBilling();
  //     }
  //   });
  // });

  radios.forEach((radio) => {
    radio.addEventListener('change', function () {
      console.log('Radio changed:', this.value); // Log to console
      if (this.value === 'different') {
        showElement(billingAddressForm);
        clearBillingFields();
      } else {
        hideElement(billingAddressForm);
        copyShippingAddressToBilling();
      }
    });
  });

  // WORK IN PROGRESS - Bug where inputs needs all forms to be completed first but us actually filled out already (Maybe not getting the input id correctly?)
  saveAndContinueButtonAddress.addEventListener('click', function () {
    const addressFields = [
      'FirstNameInput',
      'LastNameInput',
      'AddressInput',
      'CityInput',
      'StateDropdown',
      'ZipCodeInput',
      'EmailInput',
      // ... Add other fields if necessary
    ];

    if (areAllRequiredFieldsFilled(addressFields)) {
      hideElement(form);
      showElement(paymentSection);
      showElement(backToAddressButton); // show back button after btn continue
      isAddressValidated = true;
      checkIfAllSectionsValidated();
    } else {
      alert('Please fill all required fields.');
    }
  });

  // Back button option if users want to edit their address form
  backToAddressButton.addEventListener('click', function () {
    hideElement(paymentSection);
    showElement(form);
    isPaymentValidated = false; // Reset the payment validation flag
    hideElement(backToAddressButton);
    checkIfAllSectionsValidated(); // Check if we should display the process button
  });

  // Save and continue payment button
  saveAndContinueButtonPayment.addEventListener('click', function () {
    if (areAllPaymentFieldsFilled()) {
      isPaymentValidated = true;
      checkIfAllSectionsValidated();
    } else {
      alert('Please fill out all payment details.');
    }
  });

  // Card expiration function to add "/" after 'MM' on cvv input field
  cardExpiry.addEventListener('input', function () {
    if (this.value.length === 2 && !this.value.includes('/')) {
      this.value += '/';
    }
  });

  // Additional utility functions

  function clearBillingFields() {
    console.log('Clearing billing fields');
    const billingFields = [
      'BillingAddressInput',
      'BillingAptInput',
      'BillingCityInput',
      'BillingStateDropdown',
      'BillingZipCodeInput',
      // ... Add other fields if necessary
    ];
    billingFields.forEach((id) => {
      let el = document.getElementById(id);
      if (el) {
        el.value = '';
      }
    });
  }

  function copyShippingAddressToBilling() {
    console.log('Copying shipping address to billing');
    const mappings = {
      ShippingAddressInput: 'BillingAddressInput',
      ShippingAptInput: 'BillingAptInput',
      ShippingCityInput: 'BillingCityInput',
      ShippingStateDropdown: 'BillingStateDropdown',
      ShippingZipCodeInput: 'BillingZipCodeInput',
    };
    for (let [shippingId, billingId] of Object.entries(mappings)) {
      let billingEl = document.getElementById(billingId);
      let shippingEl = document.getElementById(shippingId);
      if (billingEl && shippingEl) {
        billingEl.value = shippingEl.value;
      }
    }
  }

  function checkIfAllSectionsValidated() {
    if (isAddressValidated && isPaymentValidated) {
      showElement(processOrderButton);
    } else {
      hideElement(processOrderButton);
    }
  }
  // billingAddressForm.style.display = 'block';

  // Coupon function - Uses type in a custom redeemable code into input and then checks and send to the server. If coupon matches, usually it gives a custom discount on shipping or prices of the book

  function applyCoupon() {
    // get the value from the input
    const couponCode = document.getElementById('couponCode').value.trim();

    // for simplicity, let's just do a basic check if the coupon code has been entered
    if (!couponCode) {
      alert('Please enter a coupon code.');
      return;
    }

    // here, you'd typically send the coupon code to the server to check if it's valid,
    // and get the discount amount or percentage. For this example, we'll just log it:
    console.log(`Applying coupon: ${couponCode}`);

    // Reset the coupon code input for future use
    document.getElementById('couponCode').value = '';

    // Notify the user - in a real-world application you'd show a more meaningful message,
    // possibly with the discount amount or percentage
    alert('Coupon applied successfully!');
  }
});
