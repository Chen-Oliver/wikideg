  $(function(){
      $('[data-toggle="popover"]').popover();
  });
  function filterlinks(){
    var sval = document.getElementById("search").value.toString();
    var links =  document.getElementsByClassName("btn btn-link");
    var regex = new RegExp(sval,"i");
    var i;
      for (i = 0; i < links.length; i++) {
        links[i].style.display="inline-block";
         var n = (links[i].value).search(regex);
         //console.log(n);
         if(n==-1) links[i].style.display="none";
       }
  }
  //edited snippet of https://stackoverflow.com/questions/42193700/detect-when-inspect-element-is-open
    var element = new Image;
    var devtoolsOpen = false;
    element.__defineGetter__("id", function() {
      devtoolsOpen = true; // This only executes when devtools is open.
      window.location.assign("https://github.com/Chen-Oliver/wikideg");
      });
    setInterval(function() {
      devtoolsOpen = false;
      console.log(element)
    }, 1000);
