function someoneSays(name, content, end = "<br />") {
    $("div#dialogue").append(name)
    $("div#dialogue").append(content)
    $("div#dialogue").append(end)
}

function whatDidISay() {
    return $("#textinput").val().trim();
}

function grandMaSays(data) {
    someoneSays("[GrandMa] ", data.message);
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
