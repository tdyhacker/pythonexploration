<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Edit Response</title>
</%def>

<h3>
    Edit Response
</h3>

Edit Response<br />
${h.form(h.url_for(action="response_update"), method="post")}
    ${h.hidden(name='id', value=c.response.id, checked='checked')}
    ${h.textarea(name="response", content=c.response.response, cols=60, rows=25)}<br />
    ${h.submit("Submit", "Update Response", id=None)}<br />
${h.end_form()}

<br />
<br />