<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Index</title>
</%def>

At ${c.e_report.created}, Planet ${"%s at" % c.e_report.planet[0].name} ${h.link_to("%d:%03d:%02d" % (c.e_report.planet[0].galaxy, c.e_report.planet[0].system, c.e_report.planet[0].orbit),h.url_for(action='planet_show', id=int("%d%03d%02d" % (c.e_report.planet[0].galaxy, c.e_report.planet[0].system, c.e_report.planet[0].orbit))))} owned by ${h.link_to(c.e_report.owner[0], h.url_for(action='player_show', id=c.e_report.owner[0].id))} had<br />

${h.ul(c.e_report.resources)}
Total of <span class='number_highlight'>${c.samount}</span> resources,<br />
${h.ul(c.e_report.fleet)}
Stationed in orbit,<br />
${h.ul(c.e_report.defences)}
defences protecting the planet,<br />
${h.ul(c.e_report.buildings)}
structures,<br />
${h.ul(c.e_report.research)}
Researched<br /><br />
with a ${c.e_report.counter_espionage}% chance of losing espionage probe(s)<br />


<br />
<br />