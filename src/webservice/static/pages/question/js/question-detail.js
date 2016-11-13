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

  var markdown_preview = $('.question-description');
  for(var i = 0; i < markdown_preview.length; i++) {
    $(markdown_preview[i]).find('.question-description-html').html(marked($(markdown_preview[i]).find('.question-description-markdown').text()))
    MathJax.Hub.Typeset(markdown_preview[i]);
  }

  hljs.initHighlightingOnLoad();

  if($("#new-answer-editor").length > 0) {
    answerEditor = new SimpleMDE({
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
  }

  $(".comments").on("click", ".comment-button", function(event) {
    var target = $(event.target);
    var comment_form = $(target).parent().find('.comment-form');
    if(comment_form.is(':visible')) {
      comment_form.hide(300);
    } else {
      comment_form.show(300);
    }
  });

  function disable_vote_button(vote_area) {
    var up_button = $($(vote_area).find('.vote-up-button')[0]);
    var down_button = $($(vote_area).find('.vote-down-button')[0]);
    $(up_button).before(up_button.html());
    $(down_button).before(down_button.html());
    up_button.remove();
    down_button.remove();
  }

  $(".question-vote").on("click", ".vote-up-button", function(event) {
    var target = $(event.target);
    var vote_area = $(target).parents('.question-vote').find(".question-votes");
    disable_vote_button($(target).parents('.question-vote'));
    $.post(
      "/api/1.0/question/vote",
      {
        value : 1,
        type : target.data("type"),
        qaid : target.data("qaid")
      }, function(data) {
        console.log(data);
        if(data.result) {
          vote_area.text(parseInt(vote_area.text())+1);
        } else {
          alert(data.msg);
        }
      }
    )
  });

  $(".question-vote").on("click", ".vote-down-button", function(event) {
    var target = $(event.target);
    var vote_area = $(target).parents('.question-vote').find(".question-votes");
    disable_vote_button($(target).parents('.question-vote'));
    $.post(
      "/api/1.0/question/vote",
      {
        value : 0,
        type : target.data("type"),
        qaid : target.data("qaid")
      },function(data) {
        console.log(data);
        if(data.result) {
          vote_area.text(parseInt(vote_area.text())-1);
        } else {
          alert(data.msg);
        }
      }
    )
  });

  $("#answer-it-button").click(function() {
    $("#new-answer-editor").focus();
  });

  $(".comment-save-button").click(function(event) {
    var target = $(event.target);

    var comment_input = $($($(target).parents('.row')[0]).find('input'));
    var comment_cotent = comment_input.val();

    if(comment_cotent.length == 0) {
      alert("请输入评论内容");
      return false;
    }

    if(comment_cotent.length > 400) {
      alert("评论内容不得超过400字符");
      return false;
    }

    comment_input.val("");

    // close comment form
    var comment_form = $(target).parents('.comment-form');

    $(comment_form).hide(300);

    // post to server
    $.post(
      '/api/1.0/question/comment',
      {
        method : 'create',
        comment : comment_cotent,
        type : target.data('type'),
        qaid : target.data('qaid')
      },
      function(data) {
        console.log(data);
        if(data.result) {
          // add comment element
          var new_comment = $('.template-comment').clone(false);

          $($(new_comment).find('.content')[0]).text(comment_cotent);
          $($(new_comment).find('.one-comment')).attr('data-cid', data.data.cid);
          var comment_wrapper = $($(target).parents(".comments")).find('.comment-main')[0];
          console.log(new_comment);
          $(new_comment).hide();

          $(comment_wrapper).append(new_comment.html());

          $(new_comment).show(300);
        }
      }
    )

  });

  $(".comments").on('click', '.comment-remove-button', function(event) {
    var comment_item = $(event.target).parents('.one-comment');
    var delimeter = $(comment_item).next();
    var comment_id = $(comment_item).data('cid');
    console.log(comment_id);
    $.post(
      "/api/1.0/question/comment",
      {
        method : 'delete',
        cid : comment_id
      },
      function(data) {
        console.log(data);
        if(data.result) {
          $(comment_item).hide(300);
          $(delimeter).hide(300);
          $(comment_item).remove();
          $(delimeter).remove();
        } else {
          alert(data.msg);
        }
      }
    )
  });

  $("#new-answer-submit-button").click(function(event) {
    var editor = $("#new-answer-editor");

    var content = answerEditor.value();
    var question = $(event.target).data('question');

    if(content.length == 0) {
      alert("answer内容不能为空!");
      return false;
    }

    if(content.length > 3000) {
      alert("answer内容不能大于3000字符!");
      return false;
    }

    // post the content to server
    $.post(
      '/api/1.0/question/answer',
      {
        method : 'create',
        answer : content,
        question : question
      },
      function(data) {
        if(data.result) {
          window.location.reload();
        }
      }
    )
  });

  $(".question-remove-button").click(function(event) {
    if(!confirm("确定删除该问题？")) {
      return false;
    }
    var qid = $(event.target).parents(".question-detial").data('qid');
    $.post(
      '/api/1.0/question/question',
      {
        method : "delete",
        qid : qid
      },
      function(data) {
        if(data.result) {
          alert("删除成功");
          window.location.href = "/question";
        } else {
          alert(data.msg)
        }
      }
    )
  });

  $(".answer-remove-button").click(function(event) {
    if(!confirm("确定删除该回答？")) {
      return false;
    }
    var aid = $(event.target).parents(".one-answer").data("aid");
    $.post(
      '/api/1.0/question/answer',
      {
        method : 'delete',
        aid : aid
      },
      function(data) {
        if(data.result) {
          alert("删除成功");
          window.location.reload();
        } else {
          alert(data.msg);
        }
      }
    )
  });

  $(".answer-edit-button").click(function(event) {
    var aid = $(event.target).parents(".one-answer").data("aid");
    window.location.replace("/question/answer/edit/"+aid)
  });

  inlineAttachment.editors.codemirror4.attach(answerEditor.codemirror, {
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
