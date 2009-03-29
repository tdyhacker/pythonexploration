<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Testing</title>
</%def>

${h.form(h.url(controller='hello', action='test', method='post'))}
${h.select("Locations", c.drops)}
${h.submit("Press")}
${h.end_form()}

% try:
    ${request.params["Locations"]}
% except:
    ${"Ooops"}
% endtry

<!--
% for a in range(50):
    ${"<font style=\"font-size: %spt\">Testing</font>" % a}
    <BR>
% endfor
-->
