$(document).ready(function() {

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

  var markdown_preview = $('.snippet-code');
  for(var i = 0; i < markdown_preview.length; i++) {
    $(markdown_preview[i]).find('.snippet-code-html').html(marked($(markdown_preview[i]).find('.snippet-code-markdown').text()))
    // MathJax.Hub.Typeset(markdown_preview[i]);
  }

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

  $('#snippet-comment-post-button').click(function() {
    var content = $("#new-snippet-comment-editor").val();
    var sid = $(event.target).data('sid');
    
    if(!check_snippet_param(content)) {
      return false;
    }

    $.post(
      "/api/1.0/snippet/comment",
      {
        method : 'create',
        content : content,
        sid: sid
      },
      function(data) {
        if(data.result) {
          window.location = "/snippet/comment/"+sid
        } else {
          alert(data.msg);
        }
      }
    )
  });

  $("#new-snippet-comment-editor").keyup(function() {
    var content = $("#new-snippet-comment-editor").val();
    var len = content.length;
    
    $(".words-num")[0].innerHTML = 148-len;
  });

  $(".praise-button").click(function() {
    var sid = $(this).attr('data-sid');
    var that = $(this);
    $.post(
      "/api/1.0/snippet/praise",
      {
        method : 'create',
        sid : sid
      },
      function(data) {
        if(data.result) {
          // window.location = "/snippet/comment/"+sid;
          var temp = that.parent().siblings('.praise-count');
          temp.text(parseInt(temp.text())+1);
          that.addClass('praised');
        } else {
          alert(data.msg);
        }
      }
    )
  });

});
