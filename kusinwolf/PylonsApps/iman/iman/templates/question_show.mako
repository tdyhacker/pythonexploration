<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Question</title>
</%def>

<h3>Question - ${c.question.question}
% if c.question.user_id == c.user_id:
    % if c.question.public:
        ${h.form(h.url_for(action="question_private"), method="post")}
            ${h.hidden(name='id', value=c.question.id, checked='checked')}
            ${h.submit("Make Private", "Make Private", id=None)}
        ${h.end_form()}
    % else:
        ${h.form(h.url_for(action="question_public"), method="post")}
            ${h.hidden(name='id', value=c.question.id, checked='checked')}
            ${h.submit("Make Public", "Make Public", id=None)}
        ${h.end_form()}
    % endif
%endif
</h3>

<h5>Writen by <%context.write(c.question.user.username)%> on ${c.question.created} and modified on ${c.question.modified}</h5><br />

Add a response here<br />
${h.form(h.url_for(action="response_insert"), method="post")}
    ${h.hidden(name='id', value=c.question.id, checked='checked')}
    ${h.textarea(name="response", content="", cols=60, rows=25)}<br />
    ${h.submit("Add", "Add", id=None)}<br />
${h.end_form()}

<h4>Responses</h4>
% for response in c.question.responses:
    <%context.write(c.convert_text(response.response))%>
    <div class="post_info">
        posted by ${response.user.username} on ${response.created - g.central_time} and last modified ${response.modified - g.central_time}
    </div>
    % for comment in response.comments:
        <div class="comment">
            <%context.write(c.convert_text(comment.comment))%>
            <div class="post_info">
                posted by ${comment.user.username} on ${comment.created - g.central_time} and last modified ${comment.modified - g.central_time}
            </div>
        <br />
        </div>
    % endfor
    <br />
% endfor



<br />
<br />