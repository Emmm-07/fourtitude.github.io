function submitV() {
    document.getElementById("submit_vios").click();
    }
function submitHc() {
    document.getElementById("submit_hiace").click();
    }
function submitHx() {
    document.getElementById("submit_hilux").click();
    }

//Get input price if ENTER is clicked ---------------------------------------------------------------------------------------
var amtElement = document.getElementById("amt_paid");
amtElement.addEventListener("keydown", function (e) {
if (e.code === "Enter") {  //checks whether the pressed key is "Enter"
	validate(e);
	}
	});

function validate(e) {
				//var text = e.target.value;
    amt_value = amtElement.value;
    console.log(amt_value)
                    //alert("some error occured in session agent")	       //to popup alert
                    //window.location.href = '/menu';						//to navigate to other page/python

    const s = JSON.stringify(amt_value)
    console.log("DONEEEE: ")
    console.log(s)
    $.ajax({												//Send data to python
    url:"/test",
    type:"POST",
    contentType:"application/json",
    data: s,
    success: function(response){
        window.location.href=response.redirect_url;
    }
    });
				//console.log("DONEEEE")
				//window.location.href = '/toyota';
}

//GET transaction code and SEND Transaction to HTML ---------------------------------------------------------------------------------------
        //Buy Vios
$('#viosForm').submit(function(event) {
    event.preventDefault();  // Prevent form submission
    // Get the HTML content of the result container
    var divElement = document.getElementById('result-container').outerHTML;
    $.ajax({
        url: '/transaction',
        type: 'POST',
        data: {
            formData: $('#viosForm').serialize(),
            divData: divElement
        },
        success: function(response) {
            // Append the response to the result container
            $('#result-container').html(response.result);     //.html to overwrite the <div id="result-container" //.append para di maoverwrite, para mag append lang
        },
        error: function(xhr, status, error) {
            console.error('Error performing operation:', error);
        }
    });
});

    //Buy Hiace
$('#hiaceForm').submit(function(event) {
    event.preventDefault();  // Prevent form submission
    // Get the HTML content of the result container
    var divElement = document.getElementById('result-container').outerHTML;
    $.ajax({
        url: '/transaction',
        type: 'POST',
        data: {
            formData: $('#hiaceForm').serialize(),
            divData: divElement
        },
        success: function(response) {
            // Append the response to the result container
            $('#result-container').html(response.result);     //.html to overwrite the <div id="result-container" //.append para di maoverwrite, para mag append lang
        },
        error: function(xhr, status, error) {
            console.error('Error performing operation:', error);
        }
    });
});

    //Buy Hilux
$('#hiluxForm').submit(function(event) {
    event.preventDefault();  // Prevent form submission
    // Get the HTML content of the result container
    var divElement = document.getElementById('result-container').outerHTML;
    $.ajax({
        url: '/transaction',
        type: 'POST',
        data: {
            formData: $('#hiluxForm').serialize(),
            divData: divElement
        },
        success: function(response) {
            // Append the response to the result container
            $('#result-container').html(response.result);     //.html to overwrite the <div id="result-container" //.append para di maoverwrite, para mag append lang
        },
        error: function(xhr, status, error) {
            console.error('Error performing operation:', error);
        }
    });
});