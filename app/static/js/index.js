function do_instant_search(method, search_string) {

  var xhttp = new XMLHttpRequest();
  
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var jsonObj = JSON.parse(this.responseText);
      console.log(jsonObj);

      if(method == "api")
        document.getElementById("display1").innerHTML = "";
      else if(method == "wc")
        document.getElementById("display2").innerHTML = "";

      for(var i=0; i<jsonObj.data.length; i++){
        var new_div = document.createElement('div');
        new_div.id = jsonObj.data[i].id;

        var new_a = document.createElement('a');
        new_a.href = '/movies/' + jsonObj.data[i].id

        if(method == "api")
          document.getElementById("display1").appendChild(new_div);
        else if(method == "wc") 
          document.getElementById("display2").appendChild(new_div);

        new_div.appendChild(new_a);

        // document.getElementById(jsonObj.data[i].id).innerHTML = jsonObj.data[i].l; 
        new_a.innerHTML = jsonObj.data[i].l; 
      }
    }
  };

  var url = '/api/search?search_string=' + search_string + '&method=' + method;
  console.log(url);
  xhttp.open("GET", url, true);
  xhttp.send();
}

function search_via_api(){
  var search_string = document.getElementById("api_search").value;

  do_instant_search('api', search_string);
}

function search_by_WC(){
  var search_string = document.getElementById("wc_search").value;

  do_instant_search('wc', search_string);

}
