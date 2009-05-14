<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Index</title>
</%def>

${c.player} owns<br /><br />

% for pl in c.player.planets:
    ${h.link_to(pl, h.url_for(action='planet_show', id=int("%d%03d%02d" % (pl.galaxy, pl.system, pl.orbit))))}<br />
% endfor

<br />
<br />