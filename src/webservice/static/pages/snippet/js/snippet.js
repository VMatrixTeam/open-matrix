$(document).ready(function() {

  function registerEvents() {
    $(".preview-picture").click(function(event) {
      $("#ImagePreviewer").modal("show");
      $("#big-image").attr('src', $(event.target).attr('src'))
    });
  }

  function renderMarkdown() {
    var markdown_preview = $('.snippet-code');
    for(var i = 0; i < markdown_preview.length; i++) {
      $(markdown_preview[i]).find('.snippet-code-html').html(marked($(markdown_preview[i]).find('.snippet-code-markdown').text()))
      // MathJax.Hub.Typeset(markdown_preview[i]);
    }
  }

  marked.setOptions({
      renderer: new marked.Renderer(),
      gfm: true,
      tables: true,
      breaks: true,
      pedantic: false,
      sanitize: false,
      smartLists: false,
      smartypants: false,
      highlight: function (code) {
        return hljs.highlightAuto(code).value;
      }
    });

  var codeEditor = CodeMirror($('#code-editor')[0], {

    lineNumbers: true,
    lineWrapping: true,
    // readOnly: 'false',
    // theme: 'twilight',
    indentWithTabs: 'false',
    tabSize: 4,
    extraKeys: {
      "Tab": function(cm){
        cm.replaceSelection("    " , "end");
      }
    },
    // mode: 'text/x-c++src'

  });
  // codeEditor.setValue('int main() {}');

  $('.code-editor-wrapper').hide();

  registerEvents();
  renderMarkdown();

  function check_snippet_param(content) {
    if (content == "") {
      alert("请输入内容")
      return false;
    }
    if (content.length > 148) {
      alert("内容长度不能大于 148")
      return false;
    }

    return true;
  }

  function check_snippet_code_param(content) {
    if (content.length > 2000) {
      alert("代码长度不能大于 2000")
      return false;
    }

    return true;
  }

  $("#snippet-post-button").click(function() {
    var content = $("#new-snippet-editor").val();
    // var code = $("#code-editor").val();
    var code = codeEditor.getValue();
    
    if(!check_snippet_param(content)) {
      // console.log(content)
      return false;
    }
    if(!check_snippet_code_param(code)) {
      return false;
    }

    $("#code-area").val(code);

    // $('#snippet-form').submit();

    var formData = new FormData($("#snippet-form")[0]);

    $.ajax({
      type: "POST",
      url: "/api/1.0/snippet/snippet",
      enctype: 'multipart/form-data',
      data: formData,
      processData: false,
      contentType: false
    })
    .done(function(res) {
      alert(res.msg);
      if (res.result) {
        window.location = "/snippet";
      }
    })
    .fail(function(res) {

    });

    // $.post(
    //   "/api/1.0/snippet/snippet",
    //   formData,
    //   function(data) {
    //     if(data.result) {
    //       window.location = "/snippet"
    //     } else {
    //       alert(data.msg);
    //     }
    //   }
    // )
  });

  $("#new-snippet-editor").keyup(function() {
    var content = $("#new-snippet-editor").val();
    var len = content.length;
    
    $(".words-num")[0].innerHTML = 148-len;
  });

  $('#read-more').click(function() {
    var page = parseInt($(this).attr('data-page'));
    $.get(
      "/api/1.0/snippet/snippet",
      {
        page: page
      },
      function(data) {
        if (data == '') {
          $('#read-more').html('no more');
        } else {
          $('#read-more').attr('data-page', page+1);
          $('#snippets-container').append(data);
          registerEvents();
          renderMarkdown();
        }
        
      }
    )
  });

});

function previewFile(dom){
    var files    = $('#image')[0].files;
    var previews = []
    var reader = []

    $('#upload-image-list').html('');
    for (var i = 0; i < files.length; i++) {
        if (!check_file_type(files[i].type)) {
          $('#upload-image-list').html('');
          dom.value = '';
          return;
        }

        previews[i] = $('<img/>');
        $('#upload-image-list').append(previews[i]); //append the query named img
        
        reader[i]  = new FileReader();
        reader[i].onloadend = (function (ii) {
            return function() {
                previews[ii][0].src = reader[ii].result;
            }
        })(i);

        if (files[i]) {
            reader[i].readAsDataURL(files[i]); //reads the data as a URL
        } else {
            previews[i][0].src = "";
        }


        previews[i].click(function(event) {
          $("#ImagePreviewer").modal("show");
          $("#big-image").attr('src', $(event.target).attr('src'))
        });
    }

}

function postPraise(dom) {
  var sid = $(dom).attr('data-sid');
  var that = $(dom);
  $.post(
    "/api/1.0/snippet/praise",
    {
      method : 'create',
      sid : sid
    },
    function(data) {
      if(data.result) {
        // window.location = "/snippet"
        var temp = that.parent().siblings('.praise-count');
        temp.text(parseInt(temp.text())+1);
        that.addClass('praised');
      } else {
        alert(data.msg);
      }
    }
  )
}

function check_file_type(type) {
  if (!/^image\//i.test(type)) {
    alert('图片格式错误');
    return false;
  }

  return true;
}