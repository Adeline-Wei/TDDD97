displayWelcomeView = function(){
	var wv = document.getElementById("welcomeview");
    document.body.innerHTML = wv.text;
};


displayProfileView = function(){
    var pv = document.getElementById("profileview");
    document.body.innerHTML = pv.text;
	
	// Show the default tab
	document.getElementById('Home').style.display = "block";
	getUserData('Home');
	getUserMessages('Home');
};

window.onload = function(){
	if (localStorage.getItem("token") == null) {
		displayWelcomeView();	
	}
    else {
        displayProfileView();
    }
};

//========================== WELCOME VIEW ==========================//
//Sign In
sendSignInInformation = function(){
    var email = document.getElementsByName("emailsignin")[0].value;
    var password = document.getElementsByName("pwsignin")[0].value;
    var sendBackMessage = serverstub.signIn(email, password);
    if (sendBackMessage.success == true){
		localStorage.setItem('token', sendBackMessage.data);		// UPDATE: store token in the localstorage without the help from serverstub.js
        displayProfileView();
    }
	else {
		document.getElementById("signInAlert").innerHTML = sendBackMessage.message;
	}
};

signInValidation = function() {
    var password = document.getElementsByName("pwsignin")[0].value;
    if (password.length < 5){
        document.getElementById("signInAlert").innerHTML = "The length of password should be more than 5.";
        return false;
    }
    sendSignInInformation();
};



// Sign Up
sendSignUpInformation = function(){
    var email = document.getElementsByName("email")[0].value;
    var password = document.getElementsByName("pwsignup")[0].value;
    var firstname = document.getElementsByName("firstname")[0].value;
    var familyname = document.getElementsByName("familyname")[0].value;
    var gender = document.getElementsByName("gender")[0].value;
    var city = document.getElementsByName("city")[0].value;
    var country = document.getElementsByName("country")[0].value;

    var infoObj = JSON.stringify({
        'email':email,
        'password':password,
        'firstname':firstname,
        'familyname':familyname,
        'gender':gender,
        'city':city,
        'country':country
    });
    var con = new XMLHttpRequest();

    con.onreadystatechange = function () {
        if (con.readyState == 4 && con.status == 200) {
            var response = JSON.parse(con.responseText);
            console.log(response['status']);
            displayProfileView();
        }
        else {
        }
    };
    con.open("POST", '/sign_up', true);
    con.setRequestHeader("Content-Type", "application/json");
    console.log(infoObj);
    con.send(infoObj);
};

signUpValidation = function() {
	document.getElementById("signUpAlert").innerHTML = "";	// Empty any alert in the SIGN_UP function
    var password1 = document.getElementsByName("pwsignup")[0].value;
    var password2 = document.getElementsByName("repeatpsw")[0].value;
    if (password1.length < 5){
        document.getElementById("signUpAlert").innerHTML = "The length of password should be more than 5.";
        return false;
    }
    if (password1 != password2){
        document.getElementById("signUpAlert").innerHTML = "Password is incorrect.";
        return false;
    }
    sendSignUpInformation();
};

//========================== PROFILE VIEW ==========================//
openTab = function(evt, tabName) {
     // Get all elements with class="tabcontent" and hide them
     var i, tabcontent, tablinks;

     tabcontent = document.getElementsByClassName("tabcontent");
     for (i = 0; i < tabcontent.length; i ++){
        tabcontent[i].style.display = "none";
     }

     // Get all elements with class="tablinks" and remove the class "active"
     tablinks = document.getElementsByClassName("tablinks");
     for (i = 0; i < tablinks.length; i ++){
        tablinks[i].className = tablinks[i].className.replace("active", "");
     }

	// Show the current tab, and add an "active" class to the link that opened the tab
	document.getElementById(tabName).style.display = "block";
	evt.currentTarget.className += "active";
	 
	if (tabName == "Home") {
		getUserData(tabName);
		getUserMessages(tabName);
	}
	// Decide to show the rest of elements except email search bar.
	else if (tabName == "Browse") {
		document.getElementById("ifUserFounded").style.display = 'none';
	}
};

// Home & Browse
getUserData = function(tabName) {
	var token = localStorage.getItem("token");    
	var sendBackMessage = "";
    var email = "";
	var data = "";
    if (tabName == "Home") {
        sendBackMessage = serverstub.getUserDataByToken(token);
		// ******** Collect all data of the user, and append those info as a string. Then, innerHTML
		data = "Email: " + sendBackMessage.data.email + "<br>" + "Firstname: " + sendBackMessage.data.firstname + "<br>" + "Familyname: " + sendBackMessage.data.familyname + "<br>" + "Gender: " + sendBackMessage.data.gender + "<br>" + "City: " + sendBackMessage.data.city + "<br>" + "Country: " + sendBackMessage.data.country + "<br>";
    document.getElementById("userData"+tabName).innerHTML = data;
    }
    else {
        email = document.getElementById("userEmail").value;
        sendBackMessage = serverstub.getUserDataByEmail(token, email);
		if (sendBackMessage.success == false) {
			document.getElementById("browseAlert").innerHTML = sendBackMessage.message;
			document.getElementById("ifUserFounded").style.display = 'none';
			document.getElementById("userEmail").value = "";
		}
		else {
			document.getElementById("browseAlert").innerHTML = "";
			document.getElementById("ifUserFounded").style.display = 'block';
			data = "Email: " + sendBackMessage.data.email + "<br>" + "Firstname: " + sendBackMessage.data.firstname + "<br>" + "Familyname: " + sendBackMessage.data.familyname + "<br>" + "Gender: " + sendBackMessage.data.gender + "<br>" + "City: " + sendBackMessage.data.city + "<br>" + "Country: " + sendBackMessage.data.country + "<br>";
    document.getElementById("userData"+tabName).innerHTML = data;
		}
    }
};

getUserTextarea = function(tabName) {

	var token = localStorage.getItem("token");    
	var data = serverstub.getUserDataByToken(token);
	var text = document.getElementById("userTextarea"+tabName).value;
	if (text != "") {
		var email = "";
		if (tabName == "Home") {
			   email = data.data.email;
		}
		else {
			   email = document.getElementById("userEmail").value;
		}

		var sendBackMessage = serverstub.postMessage(token, text, email);
		document.getElementById("userTextarea"+tabName).value = "";
    }
};

getUserMessages = function(tabName) {
	var token = localStorage.getItem("token");	
	var sendBackMessage = "";
	if (tabName == "Home"){
		sendBackMessage = serverstub.getUserMessagesByToken(token);
	}
	else {
		var email = document.getElementById("userEmail").value;
		sendBackMessage = serverstub.getUserMessagesByEmail(token, email);
		if (sendBackMessage.message == false) return false;
	}
	objs = sendBackMessage.data;
	var messages = "";
	for (var i in objs) {
		messages = messages + (objs[i].writer + " said: " + objs[i].content + "<br>");
	}
	document.getElementById("userMessages"+tabName).innerHTML = messages;
};



// Account
changePassword = function() {
    var oldPassword = document.getElementsByName("oldpw")[0].value;
    var newPassword = document.getElementsByName("newpw")[0].value;
	if (newPassword.length < 5){
        document.getElementById("accountAlert").innerHTML = "The length of password should be more than 5.";
        return false;
    }
	var token = localStorage.getItem("token");
    var sendBackMessage = serverstub.changePassword(token, oldPassword, newPassword);
    document.getElementById("accountAlert").innerHTML = sendBackMessage.message;
};


signOut = function() {
	var token = localStorage.getItem('token');
    var sendBackMessage = serverstub.signOut(token);
    if (sendBackMessage.success == true) {
		localStorage.removeItem("token");
        displayWelcomeView();
    }
};
