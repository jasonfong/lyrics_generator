$( document ).ready(function() {

  function getData(id, status) {
    var data = {"line_id":id, "status":status};

    $.ajax( "/admin/moderate_action",
      {
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(data),
        type: "post",
        success: function(data) {
          var element = document.getElementById(data["id"]);

          element.parentNode.removeChild(element);
        },
        failure: function(errMsg) {
          alert(errMsg);
        }
      });
  }

  $( ".acceptedButton" ).click(function(){
    getData(this.dataset.id, "accepted");
  });

  $( ".rejectedButton" ).click(function(){
    getData(this.dataset.id, "rejected");
  });
});