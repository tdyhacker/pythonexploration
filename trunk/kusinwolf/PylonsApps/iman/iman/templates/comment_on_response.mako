<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Response</title>
</%def>
<%context.write(c.convert_text(c.response.response))%>
<h5>Writen by <%context.write(c.response.user.username)%> on ${c.response.created} and modified on ${c.response.modified}</h5><br />
<%context.write( h.link_to("Back to Question", h.url_for(action="question_show", id=c.response.question[0].id)) )%>
<br />
<br />
Add a comment here<br />
${h.form(h.url_for(action="comment_insert"), method="post")}
    ${h.hidden(name='id', value=c.response.id, checked='checked')}
    ${h.textarea(name="comment", content="", cols=60, rows=25)}<br />
    ${h.submit("Submit", "Add Comment", id=None)}<br />
${h.end_form()}

<h4>Comments</h4>
% for comment in c.response.comments:
    <div class="comment">
        <%context.write(c.convert_text(comment.comment))%>
        <div class="post_info">
            posted by ${comment.user.username} on ${comment.created - g.central_time} and last modified ${comment.modified - g.central_time}
        </div>
    <br />
    </div>
% endfor

<br />
<%context.write( h.link_to("Back to Question", h.url_for(action="question_show", id=c.response.question[0].id)) )%>
<br />
<br />
<br />