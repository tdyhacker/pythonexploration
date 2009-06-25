<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Blog Index</title>
</%def>

% for question in c.all_questions:
  ${h.ul(h.link_to(question.question, h.url_for(action="question_show", id = question.id)))}
% endfor

<br />
<br />