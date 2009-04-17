<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Index</title>
</%def>

% for contact in c.contacts:
    ${h.link_to(contact, h.url_for(action="contact_show", id=contact.id))}<br />
% endfor