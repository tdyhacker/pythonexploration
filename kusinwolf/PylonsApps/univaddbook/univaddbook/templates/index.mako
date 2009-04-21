<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Index</title>
</%def>

% for contact in c.contacts:
    ${h.form(action="contact_delete", method="post")}
    ${h.hidden_field(name='id', value=c.contact.id, checked='checked')}
    ${h.link_to(contact, h.url_for(action="contact_show", id=c.contact.id))} - ${h.submit("Delete", confirm="Are you sure?")}<br />
    ${h.end_form()}
% endfor
