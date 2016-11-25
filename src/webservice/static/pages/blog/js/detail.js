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
    highlight: function (plainText, preview) {
      return hljs.highlightAuto(code).value;
    }
  });

  var markdown_preview = $('.comment-body');
  for(var i = 0; i < markdown_preview.length; i++) {
    $(markdown_preview[i]).find('.commentc-content-html').html(marked($(markdown_preview[i]).find('.commentc-content-markdown').text()))
    MathJax.Hub.Typeset(markdown_preview[i]);
  }

  var simplemde = new SimpleMDE({
    element: $("#comment-editor")[0],
    previewRender: function(plainText, preview) { // Async method
      $(preview).addClass('markdown-body');
      $(preview).html(marked(plainText));
      MathJax.Hub.Typeset(preview);
      return $(preview).html();
    },
    toolbar: [
      {
        name: "bold",
        action: SimpleMDE.toggleBold,
        className: "fa fa-bold",
        title: "Bold",
      },
      {
        name: "italic",
        action: SimpleMDE.toggleItalic,
        className: "fa fa-italic",
        title: "Italic",
      },
      {
        name: "heading-1",
        action: SimpleMDE.toggleHeading1,
        className: "fa fa fa-header fa-header-x fa-header-1",
        title: "Heading-1",
      },
      {
        name: "heading-2",
        action: SimpleMDE.toggleHeading2,
        className: "fa fa-header fa-header-x fa-header-2",
        title: "Heading-2",
      },
      {
        name: "heading-3",
        action: SimpleMDE.toggleHeading3,
        className: "fa fa-header fa-header-x fa-header-3",
        title: "Heading-3",
      },
      {
        name: "code",
        action: SimpleMDE.toggleCodeBlock,
        className: "fa fa-code",
        title: "Code",
      },
      {
        name: "unordered-list",
        action: SimpleMDE.toggleUnorderedList,
        className: "fa fa-list-ul",
        title: "Unordered List",
      },
      {
        name: "ordered-list",
        action: SimpleMDE.toggleOrderedList,
        className: "fa fa-list-ol",
        title: "Ordered List",
      },
      {
        name: "link",
        action: SimpleMDE.drawLink,
        className: "fa fa-link",
        title: "Link",
      },
      {
        name: "preview",
        action: SimpleMDE.togglePreview,
        className: "fa fa-eye no-disable",
        title: "Preview"
      },
      {
        name: "fullscreen",
        action: SimpleMDE.toggleFullScreen,
        className: "fa fa-arrows-alt no-disable no-mobile",
        title: "Fullscreen"
      },
      {
        name: "side-by-side",
        action: SimpleMDE.toggleSideBySide,
        className: "fa fa-columns no-disable no-mobile",
        title: "Side by Side"
      },
      {
        name: "guide",
        action: function(editor) {
          return false;
        },
        className: "fa fa-question-circle",
        tittle: "Markdown Guide"
      }
    ],
  });

  $("#btn-praise").on("click", function() {
    var bid = $(event.target).data('bid');

    $.post(
      "/api/1.0/blog/praise",
      {
        method : 'create',
        bid : bid
      },
      function(data) {
        if(data.result) {
          alert(data.msg);
        } else {
          alert(data.msg);
        }
      }
    )
  });

  $("#comment-submit-button").on("click", function(event) {
    var content = simplemde.value();
    var bid = $(event.target).data('bid');

    if(content.length == 0) {
      alert("comment内容不能为空!");
      return false;
    }

    if(content.length > 3000) {
      alert("comment内容不能大于3000字符!");
      return false;
    }

    // post the content to server
    $.post(
      '/api/1.0/blog/comment',
      {
        method : 'create',
        content : content,
        bid : bid
      },
      function(data) {
        if(data.result) {
          window.location.reload();
        } else {
          alert(data.msg);
        }
      }
    )
  });

});
