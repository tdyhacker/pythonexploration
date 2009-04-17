<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Index</title>
</%def>

${c.contact}
<br />
${h.ul(["Group: %s" % c.contact.relationship, "NickName: %s" % c.contact.nick_name])}
<ul>
% for group in c.emails:
    <li>
        ${group} Emails
    </li>
    ${h.ul(c.emails[group])}
% endfor
${h.form(h.url_for(action='contact_edit', method='POST'))}
${h.hidden_field(name='id', value=c.contact.id, checked='checked')}
${
</ul>