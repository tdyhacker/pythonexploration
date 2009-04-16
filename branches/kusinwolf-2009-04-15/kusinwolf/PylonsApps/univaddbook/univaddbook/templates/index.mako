<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Index</title>
</%def>

% for contact in c.contacts:
    ${contact}<br />
% endfor