function someoneSays(name, content, end = "<br />") {
    var new_message = $("<div></div>").addClass("message");
    
    new_message.append(name);
    new_message.append(content);
    new_message.append(end);
    
    $("div#dialogue").append(new_message);
    scrollDown();
}

function scrollDown() {
    var elmnt = $("div#dialogue");
    elmnt.scrollTop(elmnt.prop("scrollHeight"));
}

function whatDidISay() {
    return $("#textinput").val().trim();
}

function grandMaSays(data) {
    // First we print the error message if there is one.
    if (data.errors.indexOf("error-message") >= 0) {
	someoneSays("[GrandMa] ", data.error_message);
    }
    
    // Then the address message, if there is one
    if (data.errors.indexOf("no-address") == -1) {
	someoneSays("[GrandMa] ", data.messages.address);
    }

    // Then the static map,
    if (data.errors.indexOf("no-static-map") == -1) {
	someoneSays("[GrandMa] ", ("<img src=\"" +
				   data.staticmap +
				   "\" />"));
    }

    // Then the funfact.
    if (data.errors.indexOf("no-wiki-text") == -1) {
	someoneSays("[GrandMa] ", data.messages.funfact);
    }
}

function emptyInput() {
    $("#textinput").val("");
}

// Bind Enter key to submit button
$(document).keypress(function(e){
    if (e.which == 13){
        $("button#submit").click();
    }
});

$(function() {
    $("button#submit").click(function() {
	var query = whatDidISay();

	if (query != "") {
	    emptyInput();
	    someoneSays("[Moi] ", query);
	    $.getJSON($API_ROOT,
		      {query: query},
		      grandMaSays);
	}
    });
})
