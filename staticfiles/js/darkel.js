
// Example POST method implementation:
/*async function postData(url = '', data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, *same-origin, omit
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    redirect: 'follow', // manual, *follow, error
    referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    body: JSON.stringify(data) // body data type must match "Content-Type" header

  });
  return response.json();// parses JSON response into native JavaScript objects

}*/


function postData(url = '', data = {}) {

   var res;
   $.ajax({
      url: 'confirm-login',
      type: 'POST',
      data: data,
      success: function (response) {
         res = response
      }
   })

   return res;
}


async function getData(url = '') {
   // Default options are marked with *

   const response = await fetch(url, {
      method: 'GET',
      mode: 'cors',
      cache: 'no-cache',
      credentials: 'same-origin',
      headers: {
         'Content-Type': 'application/json',
         'Accept': 'application/json'
      },
      redirect: 'follow',
      referrerPolicy: 'no-referrer'
   });

   return response.json()

}


function showAlert(type, paramObject) {

   let typeClass = '';

   const validTypes = ['error', 'success', 'warning', 'info'];
   if (validTypes.includes(type.toLowerCase())) {
      typeClass = type === 'error' ? 'danger' : type;
      $('#alert-modal .modal-header').addClass(`bg-${typeClass.toLowerCase()}`);
   } else {
      throw new Error('Type is invalid, allowed types are: danger, success, warning');
   }

   const validSizes = ['sm', 'md', 'lg', 'xl'];
   if (paramObject.hasOwnProperty('size')) {
      if (validSizes.includes(paramObject.size.toLowerCase())) {

         $('#alert-modal .modal-dialog').addClass(`modal-${paramObject.size.toLowerCase()}`);
      } else {
         throw new Error('Size is invalid, allowed sizes are: sm, md, lg, xl, xxl');
      }

   }

   let modalTitle = '';
   if (paramObject.hasOwnProperty('title')) {
      modalTitle = paramObject.title;
   } else {
      switch (type) {
         case 'error':
            modalTitle = 'Error'
            break;

         case 'success':
            modalTitle = 'Success'
            break;

         case 'warning':
            modalTitle = 'Warning'
            break;

         case 'info':
            modalTitle = 'Information'
            break;

         default:
            break;
      }
   }

   $('#alert-modal .modal-title').html(modalTitle);

   if (paramObject.hasOwnProperty('message')) {
      $('#alert-modal .modal-body p').html(paramObject.message);
   } else {
      throw new Error('message string is required for alert to show');
   }

   $('#alert-modal').modal({
      backdrop: 'static'
   });

   if (paramObject.hasOwnProperty('onClose')) {
      $('#alert-modal').on('hidden.bs.modal', function (e) {
         paramObject.onClose();
      });
   }

}

const Toast = Swal.mixin({
   toast: true,
   position: 'top-end',
   showConfirmButton: false,
   timer: 3000
});


//success/info/error/warning/question

function showToast(type, message) {
   Toast.fire({
      icon: type,
      title: message,
   })
};

function showLoading() {

   Swal.fire({
      showConfirmButton: false,
      toast: true,
      timer: 100000,
      customClass: {
         container: 'my-swal'
      },
      onOpen: () => {
         Swal.showLoading()
      },
   })
}


function showBtnLoading(btnId) {

   btnText = "<i class='fas fa-spinner fa-spin'></i>";

   $(`${btnId}`)
      .attr("disabled", "true")
      .html(`${btnText}`);

}

function returnBtn(btnId, btnText) {

   $(`${btnId}`)
      .removeAttr("disabled")
      .html(`${btnText}`);
}

function extractFormData(form) {
   try {
      const formData = new FormData(form);
      let dataToSubmit = {};

      for (let data of formData.entries()) {
         dataToSubmit[data[0]] = data[1].trim();
      }
      return dataToSubmit;

   } catch (error) {
      throw error;
   }

}


function reloadPage() {
   setTimeout(() => {
      location.reload(true);
   }, 3000);
}


inputFields = document.querySelectorAll('form input,select,textarea');

inputFields.forEach(element => {
   element.addEventListener('change', function (e) {
      this.classList.remove('is-invalid');
   })
});


function formatMoney(amount, decimalCount = 2, decimal = ".", thousands = ",") {
   try {
      decimalCount = Math.abs(decimalCount);
      decimalCount = isNaN(decimalCount) ? 2 : decimalCount;

      const negativeSign = amount < 0 ? "-" : "";

      let i = parseInt(amount = Math.abs(Number(amount) || 0).toFixed(decimalCount)).toString();
      let j = (i.length > 3) ? i.length % 3 : 0;

      return negativeSign + (j ? i.substr(0, j) + thousands : '') + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" +
         thousands) + (decimalCount ? decimal + Math.abs(amount - i).toFixed(decimalCount).slice(2) : "");
   } catch (e) {
      console.log(e)
   }
};

function googleTranslateElementInit() {
   new google.translate.TranslateElement({
      pageLanguage: "en"
   },
      "google_translate_element"
   );
}


function changeLanguageByButtonClick() {

   var language = document.getElementById("language").value;

   var selectField = document.querySelector(
      "#google_translate_element select"
   );

   for (var i = 0; i < selectField.children.length; i++) {
      var option = selectField.children[i];
      // find desired langauge and change the former language of the hidden selection-field
      if (option.value == language) {
         selectField.selectedIndex = i;
         // trigger change event afterwards to make google-lib translate this side
         selectField.dispatchEvent(new Event("change"));
         break;
      }
   }
}




// Returns a function, that, as long as it continues to be invoked, will not
// be triggered. The function will be called after it stops being called for
// N milliseconds. If `immediate` is passed, trigger the function on the
// leading edge, instead of the trailing.
function debounce(func, wait, immediate) {
   var timeout;

   // This is the function that is actually executed when
   // the DOM event is triggered.
   return function executedFunction() {
      // Store the context of this and any
      // parameters passed to executedFunction
      var context = this;
      var args = arguments;

      // The function to be called after 
      // the debounce time has elapsed
      var later = function () {
         // null timeout to indicate the debounce ended
         timeout = null;

         // Call function now if you did not on the leading end
         if (!immediate) func.apply(context, args);
      };

      // Determine if you should call the function
      // on the leading or trail end
      var callNow = immediate && !timeout;

      // This will reset the waiting every function execution.
      // This is the step that prevents the function from
      // being executed because it will never reach the 
      // inside of the previous setTimeout  
      clearTimeout(timeout);

      // Restart the debounce waiting period.
      // setTimeout returns a truthy value (it differs in web vs node)
      timeout = setTimeout(later, wait);

      // Call immediately if you're dong a leading
      // end execution
      if (callNow) func.apply(context, args);
   };
};


let newsletterForm = document.getElementsByClassName('newsletter_form')[0];
let newsletterButton = document.getElementsByClassName('newsletter_button')[0];

$('.newsletter_form').submit(function (event) {
   event.preventDefault();

   let l = Ladda.create(newsletterButton);
   l.start();

   let newsletterFormData = new FormData(newsletterForm);

   let dataToSubmit = {};
   for (let data of newsletterFormData.entries()) {
      dataToSubmit[data[0]] = data[1]
   }

   let newsletterUrl = `${URL_ROOT}/home/newsletter`;

   postData(newsletterUrl, dataToSubmit).then(response => {

      l.stop();
      switch (response) {
         case false:
            showToast('error', 'Failed to save email');
            break;

         case true:
            document.querySelector('.newsletter_form input').value = '';
            showToast('success', 'Thanks for subscribing to our platform');
            break;

         default:
            showToast('error', Object.values(response)[0]);
            break;
      }
   });




});

window.addEventListener('load', function () {

   if (location.pathname.includes('admin') || location.pathname.includes('login') || location.pathname.includes('confirm-otp')) {
      return;
   }

   let getLanguageUrl = `${URL_ROOT}/configuration/get-language`;
   getData(getLanguageUrl).then(response => {
      if ($('#language').val() !== response) {
         $('#language').val(response);
         changeLanguageByButtonClick();
      }
   });
})