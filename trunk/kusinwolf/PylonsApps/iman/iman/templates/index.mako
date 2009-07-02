<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Blog Index</title>
</%def>

Add a question here<br />
${h.form("/blog/question_insert", method="post")}
    ${h.textarea(name="question", content="", cols=60, rows=1, wrap="hard")}<br />
    Quick Response<br />
    ${h.textarea(name="response", content="", cols=60, rows=25)}<br />
    ${h.submit("Add", "Add")}<br />
${h.end_form()}

${h.ul([h.link_to(question.question, h.url_for(controller="blog", action="question_show", id=question.id)) for question in c.all_questions])}

<br />
<br />