$(document).ready(function(){

  var stripeFormModule = $(".string-payment-form")
  var stripeFormModulePubKey = stripeFormModule.attr("data-token")
  var stripeFormModuleURL = stripeFormModule.attr("next_url")


  var stripeTemplate = $.templates("#stripeTemplate")
  var stripeTemplateDataContext = {
    publish_key : stripeFormModulePubKey,
    next_url : stripeFormModuleURL,
  }

  var stripeTemplateHtml = stripeTemplate.render(stripeTemplateDataContext)
  stripeFormModule.html(stripeTemplateHtml)


  var paymentForm = $(".payment-form")

  if (paymentForm.length > 1) {
    alert("Only one payment is allowed per page")
    paymentForm.css('display','none')
  }

  else if(paymentForm.length == 1) {

    var pubId = paymentForm.attr("data-token")
    var next_url = paymentForm.attr("data-next-url")

    var stripe = Stripe(pubId);

    // Create an ins tance of Elements.
    var elements = stripe.elements();

    // Custom styling can be passed to options when creating an Element.
    // (Note that this demo uses a wider set of styles than the guide below.)
    var style = {
      base: {
        color: '#32325d',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
          color: '#aab7c4'
        }
      },
      invalid: {
        color: '#fa755a',
        iconColor: '#fa755a'
      }
    };

    // Create an instance of the card Element.
    var card = elements.create('card', {style: style});

    // Add an instance of the card Element into the `card-element` <div>.
    card.mount('#card-element');

    // Handle real-time validation errors from the card Element.
    card.on('change', function(event) {
      var displayError = document.getElementById('card-errors');
      if (event.error) {
        displayError.textContent = event.error.message;
      } else {
        displayError.textContent = '';
      }
    });

    // Handle form submission.
    var form = document.getElementById('payment-form');
    form.addEventListener('submit', function(event) {
      event.preventDefault();

      stripe.createToken(card).then(function(result) {
        if (result.error) {
          // Inform the user if there was an error.
          var errorElement = document.getElementById('card-errors');
          errorElement.textContent = result.error.message;
        } else {
          // Send the token to your server.
          stripeTokenHandler(result.token,next_url);
        }
      });
    });

    // Submit the form with the token ID.
    function stripeTokenHandler2(token) {
      // Insert the token ID into the form so it gets submitted to the server
      var form = document.getElementById('payment-form');
      var hiddenInput = document.createElement('input');
      hiddenInput.setAttribute('type', 'hidden');
      hiddenInput.setAttribute('name', 'stripeToken');
      hiddenInput.setAttribute('value', token.id);
      form.appendChild(hiddenInput);

      // Submit the form
      form.submit();
    }
    function redirectToNext(next_url,time) {
      if (next_url){
        setTImeout(function(){
          window.location.href = next_url
        },time)
      }
    }

    function stripeTokenHandler(token,next_url) {
        // console.log(token.id)
        // console.log(next_url);
        var paymentMethodEndPoint = '/billing/payment-method/create/'
        data  = {
          'token': token.id,
        }
        $.ajax({
          data : data,
          url  : paymentMethodEndPoint,
          method : "POST",
          success : function(data){
            //console.log(data)
            var successMsg = data.message || "Success ! Your card was added"
            card.clear()
            console.log(next_url)
            if(next_url) {
              successMsg = successMsg + "<br/><br/><i class='fa fa-spin fa-spiner'/> Redirecting ... "
            }

            if($.alert){
              $.alert(successMsg)
            } else {
              alert(successMsg)
            }

            redirectToNext(next_url,1500)
          },
          error : function(error){
            console.log(error)
          }
        })
    }


  }

})
