<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Edit Comment</title>
</%def>

<h3>
    Edit Comment
</h3>

Edit Comment<br />
${h.form(h.url_for(action="comment_update"), method="post")}
    ${h.hidden(name='id', value=c.comment.id, checked='checked')}
    ${h.textarea(name="comment", content=c.comment.comment, cols=60, rows=25)}<br />
    ${h.submit("Submit", "Update Comment", id=None)}<br />
${h.end_form()}

<br />
<br />