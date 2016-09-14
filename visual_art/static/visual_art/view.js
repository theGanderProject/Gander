$(document).ready(function(){
  var img = $("#zoomable_img");
  
  var navbar_offset = $("#navbar-offset").height();

  var placeholder = $("#placeholder");

  function fit_img_to_screen(){
    var available_height = window.innerHeight - navbar_offset;
    var available_width  = window.innerWidth;

    img.css("height", "auto");
    img.css("width", "auto");

    if (available_height < img.height()){
      img.height(available_height);
    }
    if (available_width < img.width()){
      img.width(available_width);
      img.css("height", "auto");
    }

    placeholder.height(img.height());
    placeholder.width(img.width());
  }

  // when page loads, fit image to screen
  fit_img_to_screen(img);

  // these functions correspond to html in visual_art/view.html
  // which makes the page load blank, with the footer pushed down
  // instead of loading and showing an image and then resizing it
  // these can be removed (along with the corresponding html)
  function load_page(){
    $("#slow_load").css("display", "initial").css("opacity", 1);
    $("#spacer").css("display", "none");
  }

  if (placeholder.complete){
    load_page();
  } else {
    placeholder.one("load", load_page());
  }

  var zoomed_in = false;
  img.css('cursor', 'zoom-in');

  $(window).resize(function(){
    if ( ! zoomed_in){
      fit_img_to_screen(img);
    }
  });

  //zoom in or out
  img.click(function(){
    if ( ! zoomed_in){
      img.css('height', 'auto');
      img.css('width', 'auto');

      zoomed_in = true;
      img.css('cursor', 'zoom-out');

    } else {
      fit_img_to_screen(img);

      zoomed_in = false;
      img.css('cursor', 'zoom-in');
    }
  });

  function fade_into_image(){
    placeholder.css("position", "absolute");
    img.css("position", "initial");
    img.css("opacity", 1);
    placeholder.fadeOut(50);
  }
  
  if (img.complete){
    fade_into_image();
  } else {
    img.one("load",fade_into_image());
  }

  $("time.timeago").timeago();

});