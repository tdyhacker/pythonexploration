<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Index</title>
</%def>

Paste your Espionage Report here<br />

${h.form("espionage_insert", controller="ogame", method="post")}
    ${h.textarea(name="report", content="", cols=60, rows=25)}<br />
    ${h.submit("Save", "Save")}<br />
${h.end_form()}

Search planet at
${h.form("planet_search", controller="ogame", method="post")}
    Galaxy ${h.text(name="galaxy", content="", size=2)}
    System ${h.text(name="system", content="", size=3)}
    Orbit ${h.text(name="orbit", content="", size=2)}
    ${h.submit("Search", "Search")}<br />
${h.end_form()}

% for espi in c.e_reports:
    ${h.link_to(espi, h.url_for(action='espionage_show', id=espi.id))}<br />
% endfor

<br />
<br />