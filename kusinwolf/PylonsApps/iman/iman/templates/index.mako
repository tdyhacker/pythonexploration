<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Blog Index</title>
</%def>

Add a question here<br />
${h.form("%sblog/question_insert" % g.site_prefix, method="post")}
    ${h.textarea(name="question", content="", cols=60, rows=1, wrap="hard")}<br />
    Quick Response<br />
    ${h.textarea(name="response", content="", cols=60, rows=25)}<br />
    ${h.submit("Add", "Add")}<br />
${h.end_form()}

<table cellpadding='3'>
    <tr>
        <td>
            <h5>Your personal Questions</h5>
        </td>
        <td bgcolor='#000000'>
        </td>
        <td>
            <h5>Everyone else's Questions</h5>
        </td>
    </tr>
    <tr>
        <td valign='top'>
            % for question in c.personal_questions:
                % if question.public:
                    % if c.lastlogin == None or (len(question.responses) > 1 and c.lastlogin < question.responses[-1].created):
                        <div class="new_post_on_public_question">
                    % else:
                        <div class="public_question">
                    % endif
                % endif
                ${h.link_to(question.question, h.url_for(controller="blog", action="question_show", id=question.id))} (${len(question.responses)})<br />
                % if question.public:
                    </div>
                % endif
            % endfor
            <!--${h.ul([h.link_to(question.question, h.url_for(controller="blog", action="question_show", id=question.id)) for question in c.personal_questions])}-->
        </td>
        <td bgcolor='#000000'>
        </td>
        <td valign='top'>
            % for question in c.not_personal_questions:
                % if c.lastlogin == None or (len(question.responses) > 1 and c.lastlogin < question.responses[-1].created):
                    <div class="new_post_on_public_question">
                % else:
                    <div class="public_question">
                % endif
                ${h.link_to(question.question, h.url_for(controller="blog", action="question_show", id=question.id))} (${len(question.responses)})<br /></div>
            % endfor
            <!--${h.ul([h.link_to(question.question, h.url_for(controller="blog", action="question_show", id=question.id)) for question in c.not_personal_questions])}-->
        </td>
    </tr>
</table>

<br />
<br />