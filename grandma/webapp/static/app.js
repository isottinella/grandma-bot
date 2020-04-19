function someoneSays(name, content, end = "<br />") {
    $("div#dialogue").append(name)
    $("div#dialogue").append(content)
    $("div#dialogue").append(end)
}

function iSay() {
    var value = $("#textinput").val();
    someoneSays("[Moi] ", value);

    return value;
}

function grandMaSays(html) {
    someoneSays("[GrandMa] ", html);
}

$(function() {
    $("button#submit").bind('click', function() {
	var query = iSay();

	$.getJSON($API_ROOT,
		  {query: query},
		  function(data) {
		      grandMaSays(data.message);
		  });
    });
})
