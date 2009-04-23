<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Download Export</title>
</%def>

Right click the ${h.link_to("download", h.url_for(controller=c.filename, action=""))} link and save as...

