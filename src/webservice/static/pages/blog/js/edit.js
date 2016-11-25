$(document).ready(function() {

  function check_blog_param(content, title, tags) {
    if (title == "") {
      alert("请输入标题")
      return false;
    }

    if (title.length > 50) {
      alert("标题长度不能大于 50")
      return false;
    }

    if (content == "") {
      alert("请输入内容");
      return false;
    }

    if(content.length > 10000) {
      alert("内容不能超过10000")
      return false;
    }

    if(tags.length > 5) {
      alert("tag数不能超过5")
    }

    for(var i = 0; i < tags.length; i++) {
      if(tags[i].length > 10) {
        alert(tags[i] + ' 的长度不能超过10')
        return false;
      }
    }

    return true;
  }

  $("#blog-submit-button").click(function() {
    var content = blogEditor.value();
    var title = $("#new-blog-title").val();
    var tags = $("#tag-input").val();
    if (tags == "") {
      tags = [];
    }

    if(!check_blog_param(content, title, tags)) {
      return false;
    }

    // console.log(JSON.stringify(tags));

    $.post(
      "/api/1.0/blog/blog",
      {
        method : 'create',
        content : content,
        title : title,
        tags : JSON.stringify(tags)
      },
      function(data) {
        if(data.result) {
          window.location = "/blog/detail/"+data.data.bid;
        } else {
          alert(data.msg);
        }
      }
    )
  });

  // $("#question-modify-submit-button").click(function(event) {
  //   var description = questionEditor.value();
  //   var title = $("#new-question-title").val();
  //   var tags = $("#tag-input").val();
  //   var qid = $(event.target).data('qid');

  //   if(!check_question_param(description, title, tags)) {
  //     return false;
  //   }

  //   $.post(
  //     "/api/1.0/question/question",
  //     {
  //       method : 'update',
  //       qid : qid,
  //       description : description,
  //       title : title,
  //       tags : JSON.stringify(tags)
  //     },
  //     function(data) {
  //       if(data.result) {
  //         window.location.href = "/question/detail/"+data.data.qid;
  //       } else {
  //         alert(data.msg);
  //       }
  //     }
  //   )
  // })

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

  hljs.initHighlightingOnLoad();

  var blogEditor = new SimpleMDE({
    element: $("#new-blog-editor")[0],
    previewRender: function(plainText, preview) {
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

  // inlineAttachment.editors.codemirror4.attach(questionEditor.codemirror, {
  //     uploadUrl : '/api/1.0/base/filesystem/picture/',
  //     uploadMethod : 'POST',
  //     onFileUploadResponse: function(xhr) {
  //         var result = JSON.parse(xhr.responseText),
  //         filename = result[this.settings.jsonFieldName];

  //         if (result && filename) {
  //             var newValue;
  //             if (typeof this.settings.urlText === 'function') {
  //                 newValue = this.settings.urlText.call(this, filename, result);
  //             } else {
  //                 newValue = this.settings.urlText.replace(this.filenameTag, filename);
  //             }
  //             var text = this.editor.getValue().replace(this.lastValue, newValue);
  //             this.editor.setValue(text);
  //             this.settings.onFileUploaded.call(this, filename);
  //         }
  //         return false;
  //     }
  // });

});
