<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Index</title>
</%def>

${c.planet} owned by ${h.link_to(c.planet.owner[0], h.url_for(action='player_show', id=c.planet.owner[0].id))}<br /><br />

% for espi in c.planet.espionage_reports:
    ${h.link_to(espi, h.url_for(action='espionage_show', id=espi.id))}<br />
% endfor

<br />
<br />