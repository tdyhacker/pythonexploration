<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Edit Question</title>
</%def>

<h3>
    Edit Question
</h3>

Edit Question<br />
${h.form(h.url_for(action="question_update"), method="post")}
    ${h.hidden(name='id', value=c.question.id, checked='checked')}
    ${h.textarea(name="question", content=c.question.question, cols=60, rows=25)}<br />
    ${h.submit("Submit", "Update Question", id=None)}<br />
${h.end_form()}

<br />
<br />