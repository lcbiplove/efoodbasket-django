function resetForm(formElement) {
    var frm_elements = formElement.elements;
    
    for (i = 0; i < frm_elements.length; i++)
    {
        field_type = frm_elements[i].type.toLowerCase();
        switch (field_type)
        {
        case "text":
        case "password":
        case "textarea":
        case "hidden":
            frm_elements[i].value = "";
            break;
        case "radio":
        case "checkbox":
            if (frm_elements[i].checked)
            {
                frm_elements[i].checked = false;
            }
            break;
        case "select-one":
        case "select-multi":
            frm_elements[i].selectedIndex = -1;
            break;
        default:
            break;
        }
    }
}

window.addEventListener("load", function () {
    var filterForm = document.getElementById("filter-form");
    var sortBySelect = document.getElementById("search-sortBy");
    var filterRowRating = document.querySelectorAll(".filter-row-rating");

    var filterBtn = document.querySelector(".filter-btn");
    var resetBtn = document.querySelector(".filter-reset-btn");

    var minPrice = document.getElementById("minPrice");
    var maxPrice = document.getElementById("maxPrice");

    var element = document.getElementById('myRangeSlider');
    var options = {
        isDate: false,
        min: 0,
        max: 200,
        step: 1,
        start: +minPrice.value,
        end: +maxPrice.value,
        overlap: false
    };

    var mySlider = new Slider(element, options);

    mySlider.subscribe('moving', function(data) {
        minPrice.value = data.left.toFixed(0);
        maxPrice.value = data.right.toFixed(0);
    });

    filterBtn.onclick = function () {
        var urlParams = new URLSearchParams(window.location.search);

        urlParams.set('minPrice', minPrice.value);
        urlParams.set('maxPrice', maxPrice.value);
        window.location.search = urlParams.toString();
    }
    
    resetBtn.onclick = function () {
        var urlParams = new URLSearchParams(window.location.search);

        urlParams.delete('minPrice');
        urlParams.delete('maxPrice');
        urlParams.delete('rating');
        window.location.search = urlParams.toString();
    }

    if(sortBySelect){
        sortBySelect.onchange = function () {
            var urlParams = new URLSearchParams(window.location.search);
            var elem = (typeof this.selectedIndex === "undefined" ? window.event.srcElement : this);
            var value = elem.value || elem.options[elem.selectedIndex].value;
    
            urlParams.set('orderBy', value);
            window.location.search = urlParams.toString();
        }
    }
    
    filterRowRating.forEach(function(item){
        item.onclick = function (e) {
            e.preventDefault();

            var ratingAbove = item.getAttribute("href");

            var urlParams = new URLSearchParams(window.location.search);
            urlParams.set('rating', ratingAbove);
            window.location.search = urlParams.toString();
        }
    });
})