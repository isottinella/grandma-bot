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
    someoneSays("[GrandMa] ", data.address);

    if (data.errors.indexOf("no-static-map") == -1) {
	someoneSays("[GrandMa] ", ("<img src=\"" +
				   data.staticmap +
				   "\" />"));
    }

    if (data.errors.indexOf("no-wiki-text") == -1) {
	someoneSays("[GrandMa] ", data.funfact);
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
