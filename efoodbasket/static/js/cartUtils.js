var MAX_QUANTITY_VALUE = 20;

/**
 * Check for each buttons and disable them if necessary
 * 
 * @param {*} quantityValue 
 * @param {*} subtractQuantityBtn 
 * @param {*} addQuantityBtn 
 */
 var checkDisableBtns = function(quantityValue, subtractQuantityBtn, addQuantityBtn, totalQuantity) {
    if(quantityValue <= 1){
        subtractQuantityBtn.classList.add("disabled");
    } else {
        subtractQuantityBtn.classList.remove("disabled");
    }

    if(totalQuantity >= MAX_QUANTITY_VALUE){
        addQuantityBtn.classList.add("disabled");
    } else {
        addQuantityBtn.classList.remove("disabled");
    }
}

/**
 * Returns total price from array of obj
 * 
 * @param {*} myProductData 
 * @returns int total price
 */
var getSubTotal = function (myProductData) {
    var new_total = 0;
    myProductData.forEach(function(elem){
        new_total += elem.total;
    });
    return new_total;
}

/**
 * Check if proceed button should be disabled
 * 
 * @param {*} proceedBtn 
 * @param {*} totalQuantity 
 * @param {*} allAddBtns 
 */
var checkProceedBtnDisable = function (proceedBtn, totalQuantity, allAddBtns) {
    if(totalQuantity >= MAX_QUANTITY_VALUE+1){
        proceedBtn.classList.add("disabled");
    } 
    else if(totalQuantity >= MAX_QUANTITY_VALUE) {
        allAddBtns.forEach(function (item) {
            item.classList.add("disabled"); 
         });
    }
    else {
        proceedBtn.classList.remove("disabled");
    }
}


/**
 * Returns slot value in string with time from number
 * 
 * @param {*} slotNum 
 * @returns slot value
 */
var getSlotValueFromNumber = function (slotNum) {
    var slot = {
        "1": "9:00 - 11:00",
        "2": "12:00 - 14:00",
        "3": "15:00 - 17:00",
    }
    return slot[slotNum];
}

/**
 * Check if proceed to payment button should be clickabled based on
 * slot number and slot day
 * 
 * @param {*} slotNum 
 * @param {*} slotDay 
 * @param {*} proceedBtn 
 */
var checkProceedToPaymentBtn = function (slotNum, slotDay, proceedBtn) {
    if(slotNum && slotDay){
        proceedBtn.classList.remove("disabled");
    } else {
        proceedBtn.classList.add("disabled");
    }
}