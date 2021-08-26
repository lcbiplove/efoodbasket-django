window.addEventListener("load", function () {
  var mainCartCountNavElem = document.querySelectorAll(".main-cart-count");
  /* All progress bar and main wrappers */
  var shoppingWrapper = document.getElementById("shopping-cart");
  var collectionWrapper = document.getElementById("collection-slot");
  var paymentWrapper = document.getElementById("payment");
  var orderSuccessWrapper = document.getElementById("order-success");

  var progressCollection = document.getElementById("progress-bar-collection");
  var progressPayment = document.getElementById("progress-bar-payment");
  var progressSuccess = document.getElementById("progress-bar-success");

  /* Shopping Cart */
  var cartItemCountSelectElem = document.getElementById("cart-items-selected");
  var checkAllCheckbox = document.getElementById("checkAllCheckbox");
  var cartTotalElements = document.querySelectorAll(".cart-total-price");
  var subTotalElement = document.getElementById("cart-sub-total");
  var discountElement = document.getElementById("cart-discount");
  var proceedBtn = document.getElementById("proceed-btn");
  var mainDeleteBtn = document.getElementById("main-delete");
  var subtotalItemElems = document.querySelectorAll(".subtotal-items");
  var voucherBtn = document.getElementById("voucher-btn");

  var total = +document
    .getElementById("cart-summary")
    .getAttribute("data-cart-grand-total");
  var subTotal = +document
    .getElementById("cart-summary")
    .getAttribute("data-cart-sub-total");
  var discount =
    +document
      .getElementById("cart-summary")
      .getAttribute("data-cart-discount") || 0;
  var voucherId = null;
  var voucherCode = null;

  var allCheckboxes = document.querySelectorAll(".each-checkbox");
  var allQuantities = document.querySelectorAll(".each-quantity");
  var allTotals = document.querySelectorAll(".each-total");
  var allSubtractBtns = document.querySelectorAll(".each-subtract");
  var allAddBtns = document.querySelectorAll(".each-add");
  var allDeleteBtns = document.querySelectorAll(".each-delete");

  var myProductData = [];

  /* End shopping cart */

  /* Start collection slot */
  var allCollectionDays = document.querySelectorAll(".each-collection-day");
  var collectionSlotContainer = document.getElementById(
    "collection-slot-container"
  );

  var summaryDayElements = document.querySelectorAll(".summary-day");
  var summarySlotElements = document.querySelectorAll(".summary-slot");

  var proceedCollectionBtn = document.getElementById("proceed-slot-btn");
  var backCollectionBtn = document.getElementById("back-collection");

  var collection_slot_id;
  var slotDay;
  var collection_date;
  var collection_time;

  var collectionSlotData = {};
  var collectionDisplayData = {};

  /* End collection slot */

  /* Collect all initial data and make array of objects */
  allCheckboxes.forEach(function (item) {
    var obj = {};
    obj.id = item.getAttribute("data-product-id");
    obj.price = +item.getAttribute("data-product-price");
    obj.total = +item.getAttribute("data-product-total");
    obj.quantity = +item.getAttribute("data-product-quantity");
    obj.discount = +item.getAttribute("data-product-discount");
    myProductData.push(obj);
  });

  var getTotalQuantity = function () {
    var totalQuantity = 0;
    myProductData.forEach(function (item) {
      totalQuantity += item.quantity;
    });
    return totalQuantity;
  };

  myProductData.forEach(function (item, index) {
    checkDisableBtns(
      item.quantity,
      allSubtractBtns[index],
      allAddBtns[index],
      getTotalQuantity()
    );
  });

  var updateAllData = function (new_quantity, index) {
    myProductData[index].quantity = new_quantity;
    allQuantities[index].innerHTML = new_quantity;

    var item_price = myProductData[index].price;
    var total_without_discount = new_quantity * item_price;
    myProductData[index].total =
      total_without_discount -
      (total_without_discount * myProductData[index].discount) / 100;

    subTotal = getSubTotal(myProductData);
    total = subTotal - (subTotal * discount) / 100;

    allTotals[index].innerHTML =
      "&pound;" + myProductData[index].total.toFixed(2);
    subTotalElement.innerHTML = "&pound;" + subTotal.toFixed(2);
    cartTotalElements.forEach(function (elem) {
      elem.innerHTML = "&pound;" + total.toFixed(2);
    });
    subtotalItemElems.forEach(function (elem) {
      elem.innerHTML = getTotalQuantity();
    });
    cartItemCountSelectElem.innerHTML = getTotalQuantity();
    mainCartCountNavElem.forEach(function(item){
        item.innerHTML = getTotalQuantity();
    });  
  };

  var updateAllElems = function () {
    this.getValidIndex = function () {
      for (var index = 0; index < myProductData.length; index++) {
        var element = myProductData[index];
        if(element) {
          return index;
        }
      }
      return false;
    }
    
    var index = getValidIndex();
    var quantity = myProductData[index].quantity
    updateAllData(quantity, index);
  }

  var getSelectedItems = function () {
    var selected_ids = [];
    allCheckboxes.forEach(function (item, index) {
      if (item.checked === true) {
        if(myProductData[index]){
          var id = myProductData[index].id;
          selected_ids.push(id);
        }
      }
    });
    return selected_ids;
  };

  updateAllElems();

  var onAddSuccess = function(response, new_quantity, index){
    hideBigLoader();
    updateAllData(new_quantity, index);

    checkDisableBtns(new_quantity, allSubtractBtns[index], allAddBtns[index]);

    checkProceedBtnDisable(proceedBtn, getTotalQuantity(), allAddBtns);
  }

  allAddBtns.forEach(function (item, index) {
    item.onclick = function () {
      var new_quantity = myProductData[index].quantity + 1;
      var product_id = myProductData[index].id;

      var data = new FormData();
      data.append("product_id", product_id);
      data.append("quantity", new_quantity);
      data.append("replace", true);
      ajax("POST", "/ajax/cart/add/", data, function (response) {
        onAddSuccess(response, new_quantity, index);
      });
    };
  });

  allSubtractBtns.forEach(function (item, index) {
    item.onclick = function () {
      var new_quantity = myProductData[index].quantity - 1;
      var product_id = myProductData[index].id;
      
      var data = new FormData();
      data.append("product_id", product_id);
      data.append("quantity", new_quantity);
      data.append("replace", true);
      ajax("POST", "/ajax/cart/add/", data, function (response) {
        onAddSuccess(response, new_quantity, index);
      });
    };
  });

  checkAllCheckbox.onclick = function () {
    allCheckboxes.forEach(function (item) {
      if (checkAllCheckbox.checked === true) {
        item.checked = true;
      } else {
        item.checked = false;
      }
    });
  };

  mainDeleteBtn.onclick = function () {
    var product_ids_array = getSelectedItems();
    if(product_ids_array.length > 0){
      showBigLoader();
      var product_ids = product_ids_array.join();

      var data = new FormData();
      data.append("product_ids", product_ids);

      ajax("POST", "/ajax/cart/delete-multiple/", data, function (response) {
        hideBigLoader();

        checkAllCheckbox.checked = false;

        if(product_ids_array.length == getTotalQuantity()) {
          window.location.reload();
          return;
        }

        myProductData.forEach((elem, index) => {
          var product_id = elem.id;
          if(product_ids_array.includes(product_id)){
            updateAllData(0, index);

            var row = document.querySelector(".card-col-big[data-product-id='"+product_id+"']");
            row.style = "opacity: 0.1; transition: opacity 1s; pointer-events: none;";
            setTimeout(function () {
              row.remove();
              delete myProductData[index];
            }, 1000);
          }
        });
        window.location.reload();
      });
    }
  };

  var onEachDeleteSuccess = function (response, index, product_id) {
    hideBigLoader();
    updateAllData(0, index);
    if(!updateAllElems()){
      window.location.reload();
    }
    var row = document.querySelector(".card-col-big[data-product-id='"+product_id+"']");
    row.style = "opacity: 0.1; transition: opacity 1s; pointer-events: none;";
    setTimeout(function () {
      row.remove();
      delete myProductData[index];
    }, 1000);
  }

  allDeleteBtns.forEach(function (item, index) {
    item.onclick = function () {
      var product_id = myProductData[index].id;
      
      var data = new FormData();
      data.append("product_id", product_id);
      ajax("POST", "/ajax/cart/delete/", data, function (response) {
        onEachDeleteSuccess(response, index, product_id);
      });
    };
  });

  voucherBtn.onclick = function () {
    var inpt = document.getElementById("voucher-inpt");
    
    var data = new FormData();
    data.append("code", inpt.value);
    ajax("POST", "/ajax/cart/voucher/", data, function (response) {
      var result = JSON.parse(response);
      inpt.value = "";
      showJsMessage(result.message, result.type);

      if(result.type == "success") {
        discount = +result.data.DISCOUNT;
        voucherId = +result.data.VOUCHER_ID;
        voucherCode = result.data.CODE;
        discountElement.innerHTML = result.data.DISCOUNT + "%";

        updateAllElems();
      } 
    });
  }

  proceedBtn.onclick = function () {
    shoppingWrapper.style.transform = "translateX(-100%)";
    collectionWrapper.style.transform = "translateX(-100%)";
    progressCollection.classList.add("active");
  };

  /* Collection Slot */

  allCollectionDays.forEach(function (item) {
    if (!item.classList.contains("disabled")) {
      var slotsArray = item.getAttribute("data-available-slot").split(",");
      slotsDisp = item.getAttribute("data-slot-display").split(",");
     
      collectionSlotData["" + item.getAttribute("data-collection-day") + ""] = slotsArray;

      var slotsDispArray = [];
      slotsArray.forEach((element,ind) => {
        slotsDispArray[element] = slotsDisp[ind];
      });
      collectionDisplayData[""+item.getAttribute("data-collection-day")+""] = slotsDispArray;
    }
  });

  var slotItemClickedHandler = function () {
    collection_slot_id = this.collection_slot_id;

    var allCollectionSlots = document.querySelectorAll(".each-collection-slot");
    allCollectionSlots.forEach(function (elem) {
      elem.classList.remove("active");
    });
    this.classList.add("active");

    summarySlotElements.forEach(function (elem) {
      collection_time = collectionDisplayData[slotDay][collection_slot_id];
      elem.innerHTML = collection_time;
    });

    checkProceedToPaymentBtn(collection_slot_id, slotDay, proceedCollectionBtn);
  };

  allCollectionDays.forEach(function (item) {
    item.onclick = function () {
      collectionSlotContainer.innerHTML =
        '<div id="slot-upper-pad"><div class="collection-separator"></div><div class="collection-title-wrapper"><div class="collection-title-key"><span class="iconify" data-icon="bi:clock"data-inline="false"></span>Collection Slot</div><div class="collection-title-value">Time</div></div></div><div id="slot-items"></div>';

      var slotItemsDiv = document.getElementById("slot-items");
      slotItemsDiv.innerHTML = "";
      collectionSlotContainer.style.height = "0";

      slotDay = item.getAttribute("data-collection-day");
      collection_date = item.getAttribute("data-collection-date");
      collection_slot_id = null;

      allCollectionDays.forEach(function (elem) {
        elem.classList.remove("active");
      });
      item.classList.add("active");

      summaryDayElements.forEach(function (elem) {
        elem.innerHTML = slotDay;
      });

      var createEachSlotRow = function (collection_slot_id) {
        var slotItem = document.createElement("div");
        slotItem.collection_slot_id = collection_slot_id;
        slotItem.className = "slot-item each-collection-slot";
        slotItem.setAttribute("data-slot-number", collection_slot_id);

        var slotKey = document.createElement("div");
        slotKey.className = "slot-key";
        slotKey.innerHTML =
          '<span class="iconify" data-icon="gridicons:product" data-inline="false"></span><span> Collection Slot ' +
          collection_slot_id +
          "</span>";
        slotItem.append(slotKey);

        var slotValue = document.createElement("div");
        slotValue.className = "slot-value";
        
        slotValue.innerHTML = collectionDisplayData[slotDay][collection_slot_id];
        slotItem.append(slotValue);

        slotItemsDiv.append(slotItem);

        slotItem.onclick = slotItemClickedHandler.bind(slotItem);
      };

      var availableSots = collectionSlotData["" + slotDay + ""];

      availableSots.forEach(function (elem) {
        createEachSlotRow(elem);
      });

      var upperDiv = document.getElementById("slot-upper-pad");

      collectionSlotContainer.style.height =
        2 * upperDiv.offsetHeight + slotItemsDiv.offsetHeight + "px";

      checkProceedToPaymentBtn(collection_slot_id, slotDay, proceedCollectionBtn);
    };
  });

  proceedCollectionBtn.onclick = function () {
    collectionWrapper.style.transform = "translateX(-200%)";
    paymentWrapper.style.transform = "translateX(-200%)";
    progressPayment.classList.add("active");
  };

  backCollectionBtn.onclick = function () {
    shoppingWrapper.style.transform = "translateX(0px)";
    collectionWrapper.style.transform = "translateX(0px)";
    progressCollection.classList.remove("active");
  };

  /* Payment */
  var backPaymentBtn = document.getElementById("back-payment");
  var paypalBtn = document.getElementById("paypal-btn");
  var checkPaymentTerms = document.getElementById("checkPaymentTerms");

  var checkForPaymentTerms = function () {
    if (checkPaymentTerms.checked) {
      paypalBtn.classList.remove("disabled");
    } else {
      paypalBtn.classList.add("disabled");
    }
  };

  checkForPaymentTerms();

  checkPaymentTerms.onclick = function () {
    checkForPaymentTerms();
  };

  backPaymentBtn.onclick = function () {
    collectionWrapper.style.transform = "translateX(-100%)";
    paymentWrapper.style.transform = "translateX(-100%)";
    progressPayment.classList.remove("active");
  };

  var onPaymentSuccess = function (response) {
    hideBigLoader();

    var orderResultContainer = document.getElementById("order-result-main-container");
    var billContainer = document.getElementById("bill-container-id");
    var orderSuccessDiscount = document.getElementById("order-success-discount");
    var orderSuccessSubtotal = document.getElementById("order-success-subtotal");
    var orderSuccessTotal = document.getElementById("order-success-total");
    var orderSuccessVoucherCode = document.getElementById("order-success-voucher-code");
    var orderSuccessTotalItems = document.getElementById("order-success-total-items");
    var orderSuccessCollectionDay = document.getElementById("order-success-collection-day");
    var orderSuccessCollectionTime = document.getElementById("order-success-collection-time");

    mainCartCountNavElem.forEach(function(item){
        item.innerHTML = 0;
    }); 

    var result = JSON.parse(response);

    var orderItems = result.orderProduct;

    function zeroPad(num, places) {
      var zero = places - num.toString().length + 1;
      return Array(+(zero > 0 && zero)).join("0") + num;
    }
    billContainer.innerHTML = "#"+zeroPad(result.order.ORDER_ID, 10);

    orderItems.forEach(function (item) {
      var price = +item.price;
      var total_price = item.quantity * item.price * (100-item.discount)/100;
      var order_row = `<div class='success-card-row'> <div class='success-img-wrapper'> <img class='success-prod-img' src='${item.image}' alt='product-order' /> </div> <div class='success-body'> <div class='success-body-row'> <div class='success-prod-title'>${item.product_name}</div> <div class='success-prod-price-quantity'> ${item.quantity} x &pound;${price.toFixed(2)} </div> </div> <div class='success-body-row'> <div class='light-text'>${item.discount > 0 ? (item.discount + "% off") : ""}</div> <div class='success-prod-price-quantity'> = &pound;${total_price.toFixed(2)} </div> </div> </div> </div>`;
      orderResultContainer.innerHTML += order_row;
    });

    orderSuccessDiscount.innerHTML = discount + "%";
    orderSuccessSubtotal.innerHTML = "&pound;" + subTotal.toFixed(2);
    orderSuccessTotalItems.innerHTML = orderItems.length;
    orderSuccessTotal.innerHTML = "&pound;" + total.toFixed(2);
    orderSuccessCollectionTime.innerHTML = collection_time;

    if(voucherId) {
      orderSuccessVoucherCode.innerHTML = voucherCode;
    }
    
    var slotDayArray = slotDay.split("NEXT ");
    var slotDayBeauty = slotDay;

    if(slotDayArray.length != 1) {
      slotDayBeauty = slotDayArray[1];
    }
    slotDayBeauty = slotDayBeauty.toLowerCase();
    
    slotDayBeauty = slotDayBeauty.charAt(0).toUpperCase() + slotDayBeauty.slice(1);

    orderSuccessCollectionDay.innerHTML = slotDayBeauty + " ("+ result.collectionDate +")";


    paymentWrapper.style.transform = "translateX(-300%)";
    orderSuccessWrapper.style.transform = "translateX(-300%)";
    progressSuccess.classList.add("active");
  }


  /* Paypal */
  paypal
    .Buttons({
      style: {
        layout: "horizontal",
        tagline: "false",
        label: "pay",
        height: 50,
      },
      createOrder: function (data, actions) {
        return actions.order.create({
          purchase_units: [
            {
              amount: {
                value: total.toFixed(2),
              },
            },
          ],
        });
      },
      onApprove: function (data, actions) {
        return actions.order.capture().then(function(details) {
          showBigLoader();
          var payerID = data.payerID;
          var orderID = data.orderID;
          var amount = total.toFixed(2);

          var sendData = new FormData();
          sendData.append('amount', amount);
          sendData.append('paypal_payer_id', payerID);
          sendData.append('paypal_order_id', orderID);
          sendData.append('collection_date', collection_date);
          sendData.append('collection_slot_id', collection_slot_id);
          sendData.append('voucher_id', voucherId);

          ajax("POST", "/ajax/cart/payment/", sendData, onPaymentSuccess);
        });

      },
    })
    .render("#paypal-btn");
});
