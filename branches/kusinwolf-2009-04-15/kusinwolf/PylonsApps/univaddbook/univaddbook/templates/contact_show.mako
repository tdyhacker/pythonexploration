<%inherit file="base.mako"/>
<%def name="head_tags()">
</%def>

<div class="head">

    <h1> Contact Info </h1>
    
</div>

<table>
    <tr>
        <td valign="center">
            <div class="contact_name">
                ${c.contact}
            </div>
        </td>
        <td>
            ${h.form(h.url_for(action='contact_edit', method='POST'))}
                ${h.hidden(name='id', value=c.contact.id, checked='checked')}
                ${h.submit("Edit", "Edit")}
            ${h.end_form()}
        </td>
    </tr>
</table>
<br />
${h.ul(["Group: %s" % c.contact.relationship, "NickName: %s" % c.contact.nick_name])}
<ul>
<div class="emails">
    % for group in c.emails:
        <li>
            ${group} Emails
        </li>
        ${h.ul(c.emails[group])}
    % endfor
</div>
${h.form(h.url_for(action='contact_addemail', method='POST'))}
    ${h.text(name="email", value="", id="email", size=20)}
    ${h.select("group", None, c.groups)}
    ${h.hidden(name='id', value=c.contact.id, checked='checked')}
    ${h.submit("Add Email", "Add Email")}
${h.end_form()}
</ul>