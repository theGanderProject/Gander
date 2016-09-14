editor = new Quill('.advanced-wrapper .editor-container', {
  modules: {
    'toolbar': {
      container: '.advanced-wrapper .toolbar-container'
    },
    'link-tooltip': true,
    'image-tooltip': true,
  },
  styles: false,
  theme: 'snow'
});

var csrftoken = Cookies.get('csrftoken');

function uploadStory(){

  $.ajax({
          type:"POST",
          beforeSend: function (request)
          {
              request.setRequestHeader("X-CSRFToken", csrftoken);
          },
          url: "/writing/submit/",
          data: { upload : editor.getHTML()},
          error: function(msg) {
              $("body").html(msg);
          },
          success: function(msg) {
            console.log("uploaded the text");
            console.log(msg);
            saved = true;
          }
  });

}

var time_since_last_unsaved_edit;
var saved = true;

window.onbeforeunload = function() {
  uploadStory();
  if ( ! saved ){
    return "Your changes haven't been saved yet. Are you sure you want to leave?";
  }
}

$('#editor').on('input propertychange change', function() {
    console.log('Textarea Change');
    saved = false;

    clearTimeout(time_since_last_unsaved_edit);
    time_since_last_unsaved_edit = setTimeout(function() {
        // Runs 1 second (1000 ms) after the last change    
        uploadStory();
    }, 4000);
});