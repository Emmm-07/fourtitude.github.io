
function goToHome(){
    window.location.href="/home";
}

     //Get input price if ENTER is clicked
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
        url:"/test" ,
        type:"POST",
        contentType:"application/json",
        data: s,
        success: function(response){
            //window.location.href=response.redirect_url;
            if(response.change!="Insufficient amount "){
                $('#change').html("<p>CHANGE: Php "+response.change +"</p>");
            }else{
                $('#change').html("Insufficient amount ");
            }
            $('#total').html("<p>TOTAL: "+response.total +"</p>");
             document.getElementById("amt_paid").placeholder = "Enter_Amount";
            console.log("Successfullll");

        }
        });
                    //console.log("DONEEEE")
                    //window.location.href = '/toyota';
    }
//
//CHECKOUT----------------------------------------------------------------------------------------------------------------------------------------------------
var checkout = document.getElementById("checkout");
   		checkout.addEventListener("click",function(event){
        var img = document.getElementById("receipt_img");
            $.ajax({
                url: '/checkout',
                type: 'POST',
                data:{
                		origin:origin,
               			no_data:"no_data"
               			},
                success: function(response) {
                img.src="/static/"+response.img_file;
                console.log(response.img_file);
                     $('#result-container').html("<p> </p>");
                   $('#total').html("<p>TOTAL: 		</p>");
                   $('#change').html("<p>CHANGE:  </p>");
                   $('#amt_P').html("<p>AMOUNT PAID: <input type=\"text\" id=\"amt_paid\" placeholder={{placeholder}}></p>");
                    document.getElementById("amt_paid").placeholder = " ";
                    console.log("Successfully Checked out transaction")
                    console.log("Successful Checkout")
                }

            })
   	})

//----------------------------------------------------------------------------------------------------------------------------------------------------
function filterTransactions(){
        var date = document.getElementById('date-select').value;
        console.log(date)

         $.ajax({
                url: '/filter_history',
                type: 'POST',
                data:{
                		date:date
               			},
                success: function(response) {
                    if(response.exist){
                           window.location.href='/database';
                    }else{
                           alert("No transaction occured on this date " + date);
                    }

                }
            })

}





// //Databae Delete checked rows
//function deleteRows(){
//                var checkedData =[]
//                var checkRows=document.querySelectorAll('#transac-table .select-radio:checked');
//                checkRows.forEach(function(radio){
//                var row = radio.closest('tr');                       //to get the checked row
//                var cells = row.querySelectorAll('td');
//                var confirm = document.getElementById("delete_confirm");
//                var emp_idElement = document.getElementById("d_emp_id");
//
//                checkedData.push(cells[1].textContent.trim());
//                emp_idElement.textContent = "Employee ID: " + cells[1].textContent.trim();
//               // emp_idElement.innerHTML = "Employee ID: " + "HALLO"
//                console.log("HEllo")
//   		        confirm.addEventListener("click",function(event){
//   		        console.log(checkedData)
//
//                $.ajax({
//                url: '/delete_data',
//                type: 'POST',
//                data:{
//                		checkedList:checkedData
//               		 },
//                success: function(response) {
//
//                        console.log("success delete");
//                        window.location.href='/employees';
//
//                }
//
//
//                });
//   		        })
//                 });
//
//            };
//
////EDIT EMPLOYEE PASSWORD
//function editPass(){
//        var checkRows=document.querySelectorAll('#transac-table .select-radio:checked');
//                checkRows.forEach(function(radio){
//                var row = radio.closest('tr');                       //to get the checked row
//                var cells = row.querySelectorAll('td');
//                var confirm = document.getElementById("edit_confirm");
//                var emp_idElement = document.getElementById("d_emp_id");
//                var checkedData = cells[1].textContent.trim();
//                emp_idElement.textContent = "Employee ID: " + checkedData;
//
//                confirm.addEventListener("click",function(event){
//   		        console.log(checkedData)
//                var newPass = document.getElementById("newPass").value;
//                console.log(newPass)
//
//                $.ajax({
//                url: '/edit_data',
//                type: 'POST',
//                data:{
//                		checkedData:checkedData,
//                		newPass:newPass
//               		 },
//                success: function(response) {
//
//                        console.log("success edit");
//                        window.location.href='/employees';
//
//                }
//
//
//                });
//   		        });
//
//           });
//        }
//
//function addEmp(){
//        var confirm = document.getElementById("add_confirm");
//        confirm.addEventListener("click",function(event){
//                var emp_id = document.getElementById("emp_id").value;
//                var emp_name = document.getElementById("emp_name").value;
//                var emp_pass = document.getElementById("emp_pass").value;
//                var emp_add = document.getElementById("emp_add").value;
//                var emp_contact = document.getElementById("emp_contact").value;
//
//                $.ajax({
//                url: '/add_data',
//                type: 'POST',
//                data:{
//                		id:emp_id,
//                		name:emp_name,
//                		pass:emp_pass,
//                		add:emp_add,
//                		contact:emp_contact
//               		 },
//                success: function(response) {
//
//                        console.log("success add");
//                        window.location.href='/employees';
//
//                }
//
//
//              });
//          });
//}


//----------------------------------------------------------------------------------------------------------------------------------------------------
//Clear Cart
var clear = document.getElementById("clear_cart");
   		clear.addEventListener("click",function(event){
   			var origin = window.location.href
   			console.log(origin)
            $.ajax({
                url: '/clear',
                type: 'POST',
                data:{
                		origin:origin,
               			no_data:"no_data"
               			},
                success: function(response) {
                    // Append the response to the result container
                   // window.location.href = origin;
                   $('#result-container').html("<p> </p>");
                   $('#total').html("<p>TOTAL: 		</p>");
                    document.getElementById("amt_paid").placeholder = " ";
                    console.log("Successfully cleared transaction")
                }

            })
   	})

    //To handle Custom Service
//    var customConfirmElement = document.getElementById("custom_confirm");
//    customConfirmElement.addEventListener("click",function(event){
//    var custom_service = document.getElementById("custom_service").value;
//    var custom_price = document.getElementById("custom_price").value;
//         $.ajax({
//                url: '/transaction',
//                type: 'POST',
//                data: {
//                    custom_service:custom_service,
//                    custom_price:custom_price,
//                    code:"CS"
//                },
//                success: function(response) {
//                    console.log(custom_service);
//                    console.log(custom_price);
//                     $('#result-container').html(response.result);     //.html to overwrite the <div id="result-container" //.append para di maoverwrite, para mag append lang
//                    $('#total').html("<p>TOTAL:" +response.total+		"</p>");
//                    document.getElementById("amt_paid").placeholder = response.enter_value;
//                    // Append the response to the result container
////                    $('#result-container').html(response.result);     //.html to overwrite the <div id="result-container" //.append para di maoverwrite, para mag append lang
////                    $('#total').html("<p>TOTAL:" +response.total+		"</p>");
////                    document.getElementById("amt_paid").placeholder = response.enter_value;
//                   //  $('#amt_P').html(response.enter_value);
////                    if(response.enter_value!=0){
////                        $('#amt_P').html("<p>AMOUNT PAID: <input placeholder=\"Enter Amount\"></p>");
////                    }
//                },
//                error: function(xhr, status, error) {
//                    console.error('Error performing operation:', error);
//                }
//            })
//
//    })

//---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    //GET transaction code and SEND Transaction to HTML
    document.querySelectorAll(".b-button").forEach(function(link){                      //To iterate iterate all href class=b-button , and check which is clicked
        link.addEventListener("click",function(event){
            console.log("Query Selector")
                var code = this.getAttribute("data-id");

                if(code=="SM_06"){
                var customConfirmElement = document.getElementById("custom_confirm");

                customConfirmElement.addEventListener("click",function(event){
                var custom_service = document.getElementById("custom_service").value;
                var custom_price = document.getElementById("custom_price").value;
                var data ={
                    custom_service:custom_service,
                    custom_price:custom_price,
                    code:code
                }

                $.ajax({
                url: '/transaction',
                type: 'POST',
                data:data,
                success: function(response) {
                    // Append the response to the result container
                    $('#result-container').html(response.result);                               //.html to overwrite the <div id="result-container" //.append para di maoverwrite, para mag append lang
                    $('#total').html("<p>TOTAL:" +response.total+		"</p>");
                    document.getElementById("amt_paid").placeholder = response.enter_value;
                },
                error: function(xhr, status, error) {
                    console.error('Error performing operation:', error);
                }
            })


            })

            } else{
                 event.preventDefault();
                 var data={
                    code:code
                 }

            console.log("Submit " + code + " link clicked!");

            $.ajax({
                url: '/transaction',
                type: 'POST',
                data:data,
                success: function(response) {
                    // Append the response to the result container
                    $('#result-container').html(response.result);     //.html to overwrite the <div id="result-container" //.append para di maoverwrite, para mag append lang
                    $('#total').html("<p>TOTAL:" +response.total+		"</p>");
                    document.getElementById("amt_paid").placeholder = response.enter_value;
                   //  $('#amt_P').html(response.enter_value);
//                    if(response.enter_value!=0){
//                        $('#amt_P').html("<p>AMOUNT PAID: <input placeholder=\"Enter Amount\"></p>");
//                    }
                },
                error: function(xhr, status, error) {
                    console.error('Error performing operation:', error);
                }
            })
            }
        })

    })

    //
    //        //Buy Vios
    //$('#viosForm').submit(function(event) {
    //    event.preventDefault();  // Prevent form submission
    //    // Get the HTML content of the result container
    //    var divElement = document.getElementById('result-container').outerHTML;
    //    $.ajax({
    //        url: '/transaction',
    //        type: 'POST',
    //        data: {
    //            formData: $('#viosForm').serialize(),
    //            divData: divElement
    //        },
    //        success: function(response) {
    //            // Append the response to the result container
    //            $('#result-container').html(response.result);     //.html to overwrite the <div id="result-container" //.append para di maoverwrite, para mag append lang
    //        },
    //        error: function(xhr, status, error) {
    //            console.error('Error performing operation:', error);
    //        }
    //    });
    //});
    //
    //    //Buy Hiace
    //$('#hiaceForm').submit(function(event) {
    //    event.preventDefault();  // Prevent form submission
    //    // Get the HTML content of the result container
    //    var divElement = document.getElementById('result-container').outerHTML;
    //    $.ajax({
    //        url: '/transaction',
    //        type: 'POST',
    //        data: {
    //            formData: $('#hiaceForm').serialize(),
    //            divData: divElement
    //        },
    //        success: function(response) {
    //            // Append the response to the result container
    //            $('#result-container').html(response.result);     //.html to overwrite the <div id="result-container" //.append para di maoverwrite, para mag append lang
    //        },
    //        error: function(xhr, status, error) {
    //            console.error('Error performing operation:', error);
    //        }
    //    });
    //});
    //
    //    //Buy Hilux
    //$('#hiluxForm').submit(function(event) {
    //    event.preventDefault();  // Prevent form submission
    //    // Get the HTML content of the result container
    //    var divElement = document.getElementById('result-container').outerHTML;
    //    $.ajax({
    //        url: '/transaction',
    //        type: 'POST',
    //        data: {
    //            formData: $('#hiluxForm').serialize(),
    //            divData: divElement
    //        },
    //        success: function(response) {
    //            // Append the response to the result container
    //            $('#result-container').html(response.result);     //.html to overwrite the <div id="result-container" //.append para di maoverwrite, para mag append lang
    //        },
    //        error: function(xhr, status, error) {
    //            console.error('Error performing operation:', error);
    //        }
    //    });
    //});