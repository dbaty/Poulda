function refresh_progress_bar() {
    var file_id = document.getElementById("file_id").value;
    $.getJSON("status?file_id=" + file_id,
              function(data) {
                  var progress = document.getElementById("progress_bar");
                  progress.innerHTML = data.percent.toString() + " %";
                  var width = data.percent * (391.5 / 100);
                  progress.style.width = width.toString() + "px";
                  var eta = document.getElementById("eta");
                  eta.innerHTML = "ETA: " + data.eta;
              });
}

function init_upload_form() {
    $("#upload_form").submit(function() {
        var container = document.getElementById("progress_bar_container");
        container.style.display = "block";
        setInterval(refresh_progress_bar, 1000);
    });
}