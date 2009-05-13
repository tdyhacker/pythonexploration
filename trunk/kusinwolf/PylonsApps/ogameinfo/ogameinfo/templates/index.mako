<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Index</title>
</%def>

Paste your Espionage Report here<br />

${h.form("espionage_insert", controller="ogame", method="post")}
    ${h.textarea(name="report", content="", cols=60, rows=25)}<br />
    ${h.submit("Save", "Save")}<br />
${h.end_form()}

% for espi in c.e_reports:
    ${espi}<br />
% endfor

<br />
<br />