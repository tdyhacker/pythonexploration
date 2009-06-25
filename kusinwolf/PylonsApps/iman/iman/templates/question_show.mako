<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Question</title>
</%def>

<h3>Question - ${question.id}<h3><br />
<h5>Writen by ${question.user.username} on ${question.created} and modified on ${question.modified}</h5><br />

<h4>Responses</h4><br />
% for response in c.all_questions:
  <p>${response.body}<br /> posted by ${response.user.username} on ${response.created} and last modified ${response.modified}</p>
% endfor

<br />
<br />