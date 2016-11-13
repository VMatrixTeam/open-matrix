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

    hljs.initHighlightingOnLoad();

    var AnswerEditor = new SimpleMDE({
      element: $("#new-answer-editor")[0],
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

    $("#answer-submit-button").click(function(event) {
      var qid = $(event.target).data("qid");
      var content = AnswerEditor.value();

      if(content.length == 0) {
        alert("answer内容不能为空!");
        return false;
      }

      if(content.length > 3000) {
        alert("answer内容不能大于3000字符!");
        return false;
      }

      $.post(
        '/api/1.0/question/answer',
        {
          method : 'create',
          answer: content,
          question: qid
        },
        function(data) {
          console.log(data);
        }
      )
    });

    $("#answer-update-button").click(function(event) {
      var aid = $(event.target).data('aid');
      var qid = $(event.target).data('qid');

      var content = AnswerEditor.value();

      if(content.length == 0) {
        alert("answer内容不能为空!");
        return false;
      }

      if(content.length > 3000) {
        alert("answer内容不能大于3000字符!");
        return false;
      }

      $.post(
        '/api/1.0/question/answer',
        {
          method : 'update',
          content : content,
          aid: aid
        },
        function(data) {
          console.log(data);
          if(data.result) {
            alert('更新成功');
            window.location.href = '/question/detail/' + qid;
          } else {
            alert(data.msg);
          }
        }
      )
    });

  inlineAttachment.editors.codemirror4.attach(AnswerEditor.codemirror, {
      uploadUrl : '/api/1.0/base/filesystem/picture/',
      uploadMethod : 'POST',
      onFileUploadResponse: function(xhr) {
          var result = JSON.parse(xhr.responseText),
          filename = result[this.settings.jsonFieldName];

          if (result && filename) {
              var newValue;
              if (typeof this.settings.urlText === 'function') {
                  newValue = this.settings.urlText.call(this, filename, result);
              } else {
                  newValue = this.settings.urlText.replace(this.filenameTag, filename);
              }
              var text = this.editor.getValue().replace(this.lastValue, newValue);
              this.editor.setValue(text);
              this.settings.onFileUploaded.call(this, filename);
          }
          return false;
      }
  });
});
