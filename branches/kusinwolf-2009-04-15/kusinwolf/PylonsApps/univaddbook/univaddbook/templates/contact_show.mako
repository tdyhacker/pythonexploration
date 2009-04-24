<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>${c.contact}</title>
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
        <table>
        % for email in c.emails[group]:
            <tr>
                <td>
                    ${h.form(h.url_for(action='email_edit', method='POST'))}
                        ${h.hidden(name='contact_id', value=c.contact.id, checked='checked')}
                        ${h.hidden(name='email_id', value=email.id, checked='checked')}
                        ${h.text(name="email_edit", value=email.email, id="email_edit", size=30)}
                        ${h.submit("Edit", "Edit")}
                    ${h.end_form()}
                </td>
                <td>
                    ${h.form(h.url_for(action='email_delete', method='POST'))}
                        ${h.hidden(name='contact_id', value=c.contact.id, checked='checked')}
                        ${h.hidden(name='email_id', value=email.id, checked='checked')}
                        ${h.submit("Delete", "Delete", confirm="Are you sure?")}
                    ${h.end_form()}
                </td>
            </tr>
        % endfor
        </table>
    % endfor
</div>
${h.form(h.url_for(action='contact_addemail', method='POST'))}
    ${h.text(name="email", value="", id="email", size=30)}
    ${h.select("group", None, c.groups)}
    ${h.hidden(name='id', value=c.contact.id, checked='checked')}
    ${h.submit("Add Email", "Add Email")}
${h.end_form()}
</ul>