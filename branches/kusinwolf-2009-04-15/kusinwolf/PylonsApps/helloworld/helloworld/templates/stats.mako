<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Link Database</title>
</%def>

<div id='statsbox'>
    % for s in c.stats:
        ${"<FONT style=\"font-size: %spt\">" % c.stats[s][1]}${h.link_to(s, h.url(controller='hello', action='search', method='GET', tags=s))}</FONT>
        -
    % endfor
</div>

<div id='statsright'>
    Amount - Tag
    % for s in c.sorted:
        <BR>${s[0][0]} - ${h.link_to(s[1], h.url(controller='hello', action='search', method='GET', tags=s[1]))}
    % endfor
</div>


