$(document).ready(function() {
    var emailPattern = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}\b/;
    $('#submit').click(function(event) {
        event.preventDefault();
        var name = $('#name').val();
        var phone = $('#mobile').val();
        var email = $('#email').val();
        var message = $('#message').val();
        var fields = [name, phone, email, message];
        var isValid = true;
        // console.log(message);
        for (i = 0; i < fields.length; i++) {
            if (fields[i].value == '') {
                isValid = false;
                alert('All fields are required');
            } else {

            }
        }
        if (!emailPattern.test(email)) {
            isValid = false;
            alert('Enter a valid email address');
        } else {
            //email.next().text("");
        }
        fields[i].val(fields[i].value);

        if (isNaN(phone.val().trim()) || phone.val() === ''){
            isValid = false;
            phone.next().text('It should be a number.');
        } else{
            phone.next().text('');
        }

        if (isValid == false) {
            event.preventDefault();
        }
    });
});
