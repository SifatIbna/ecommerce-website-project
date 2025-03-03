$(document).ready(function(){
// Contact Form

    var contactForm = $(".contact-form")
    var contactFormMethod = contactForm.attr("method")
    var contactFormEndPoint = contactForm.attr("action")

    function displaySubmit(submitBtn, defaultText, doSubmit){
        if (doSubmit){
        submitBtn.addClass("disabled")
        submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Sending...")

        } else {
        submitBtn.removeClass("disabled")
        submitBtn.html(defaultText)
        }
    }

    contactForm.submit(function(event){
        event.preventDefault()
        var contactFormData = contactForm.serialize()
        var contactFormSubmitBtn = contactForm.find("[type='submit']")
        var contactFormSubmitTxt  =contactFormSubmitBtn.text()

        var thisForm = $(this)
        displaySubmit(contactFormSubmitBtn, "", true)
        
        $.ajax({
        method : contactFormMethod,
        url : contactFormEndPoint,
        data: contactFormData,
        success:function(data){
            //console.log("Success")

            thisForm[0].reset()
            $.alert({
            title: "Success!",
            content: "Thank you for your submission!",
            theme: "modern",
            })

            setTimeout(function(){
            displaySubmit(contactFormSubmitBtn,contactFormSubmitTxt,false)
            },500)
        },
        error: function(error){
            console.log(error.responseJSON)
            var jsonData = error.responseJSON
            var msg = ""

            $.each(jsonData, function(key,value){
            msg += key + ": "+ value[0].message +"<br/>"
            })
            $.alert({
            title: "Oops!",
            content: msg,
            theme: "modern",
            })
            console.log("Error")
            console.log(error)
            setTimeout(function(){
            displaySubmit(contactFormSubmitBtn,contactFormSubmitTxt,false)
            },500)
        }
        })
    })

    // Search call

    /* var searchForm = $(".search-form")
    var searchInput = searchForm.find("[name='q']")
    var typingTimer;
    var typingInterval = 500;
    var searchBtn = searchForm.find("[type='submit']")

    searchInput.keyup(function(event){
        clearTimeout(typingInterval)

        typingTime = setTimeout(performSearch,typingInterval)
    })

    searchInput.keydown(function(event){
        clearTimeout(typingTimer)
        typingTime = setTimeout(performSearch,typingInterval)

    })

    function doSearch(){
        searchBtn.addClass("disabled")
        searchBtn.html("<i class='fa fa-spin fa-spinner'></i> Searching...")
    }

    function performSearch(){
        doSearch()
        var query = searchInput.val()
        window.location.href='/search/?q=' +query

        setTimeout(function(){
        },1500)

    } */


    // cart and cart update

    var productForm = $(".form-product-ajax")

    productForm.submit(function(event){
        event.preventDefault()
        //console.log("Form is not sending")

        var thisForm = $(this)

        var actionEndpoint = thisForm.attr("action");
        
        var httpMethod = thisForm.attr("method");
        var formData = thisForm.serialize();

        $.ajax({
        url : actionEndpoint,
        method: httpMethod,
        data: formData,
        success : function(data) {
            //console.log(data)
            var submitSpan = thisForm.find(".submit-span")

            if (data.added){
            submitSpan.html("In cart <button type='submit' class='btn btn-link'> Remove? </button>")
            }

            else {
            submitSpan.html("<button type='submit' class='btn btn-success'> Add to cart  </button>")
            }
            //console.log(submitSpan.html())

            var navbarCount = $(".navbar-cart-count")
            navbarCount.text(data.cartItem)
            //console.log(navbarCount)
        },

        error :function(errorData){
            $.alert({
            title: "Oops!",
            content: "An error occured",
            theme: "modern",
            })
            console.log("Error")
            console.log(errorData)
        }
        })

    })

})