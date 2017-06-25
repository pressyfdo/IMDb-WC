function do_instant_search() {
  var search_string = document.getElementById("search").value;

  var xhttp = new XMLHttpRequest();
  
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var jsonObj = JSON.parse(this.responseText);
      console.log(jsonObj);

      document.getElementById("display").innerHTML = "";
      for(var i=0; i<jsonObj.data.length; i++){
        var new_div = document.createElement('div');
        new_div.id = jsonObj.data[i].id;

        var new_a = document.createElement('a');
        new_a.href = '/movies/' + jsonObj.data[i].id

        document.getElementById("display").appendChild(new_div);
        new_div.appendChild(new_a);

        // document.getElementById(jsonObj.data[i].id).innerHTML = jsonObj.data[i].l; 
        new_a.innerHTML = jsonObj.data[i].l; 
      }
    }
  };

  var url = '/api/search?search_string=' + search_string;
  console.log(url);
  xhttp.open("GET", url, true);
  xhttp.send();
}
