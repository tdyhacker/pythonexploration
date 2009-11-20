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

<h5>
    Writen by <%context.write(c.question.user.username)%> on ${c.question.created} and modified on ${c.question.modified}
<%  if c.question.user.uid == c.user_id:
        context.write("<span class=\"post_info\">")
        context.write(h.link_to("Edit", h.url_for(action="question_edit", id=c.question.id)))
        #context.write("&nbsp;&nbsp;-&nbsp;&nbsp;")
        #context.write(h.link_to("Delete", h.url_for(action="question_delete", id=c.question.id)))
        context.write("</span>")%>
</h5>

<br />

Add a response here<br />
${h.form(h.url_for(action="response_insert"), method="post")}
    ${h.hidden(name='id', value=c.question.id, checked='checked')}
    ${h.textarea(name="response", content="", cols=60, rows=25)}<br />
    ${h.submit("Submit", "Add Response", id=None)}<br />
${h.end_form()}

<h4>Responses</h4>
% for response in c.question.responses:
    <%context.write(c.convert_text(response.response))%>
    <div class="post_info">
        posted by ${response.user.username} on ${response.created - g.central_time} and last modified ${response.modified - g.central_time}
        <%  if response.user.uid == c.user_id:
                context.write("<span class=\"post_info\">")
                context.write(h.link_to("Edit", h.url_for(action="response_edit", id=response.id)))
                #context.write("&nbsp;&nbsp;-&nbsp;&nbsp;")
                #context.write(h.link_to("Delete", h.url_for(action="response_delete", id=response.id)))
                context.write("</span>")%>
    </div>
    <%
        context.write("<div class=\"post_info\">")
        context.write(h.link_to("Add Comment", h.url_for(action="response_show", id=response.id)))
        context.write("</div>")
    %>
    % for comment in response.comments:
        <div class="comment">
            <%context.write(c.convert_text(comment.comment))%>
            <div class="post_info">
                posted by ${comment.user.username} on ${comment.created - g.central_time} and last modified ${comment.modified - g.central_time}
                <%  if comment.user.uid == c.user_id:
                        context.write("<span class=\"post_info\">")
                        context.write(h.link_to("Edit", h.url_for(action="comment_edit", id=comment.id)))
                        #context.write("&nbsp;&nbsp;-&nbsp;&nbsp;")
                        #context.write(h.link_to("Delete", h.url_for(action="comment_delete", id=comment.id)))
                        context.write("</span>")%>
            </div>
        </div>
    % endfor
    <%  if response.comments:
            context.write("<div class=\"post_info\">")
            context.write(h.link_to("Add Comment", h.url_for(action="response_show", id=response.id)))
            context.write("</div>")%>
    <div class="paragraph_buffer" />
% endfor



<br />
<br />