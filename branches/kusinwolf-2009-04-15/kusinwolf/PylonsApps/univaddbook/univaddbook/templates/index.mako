<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Index</title>
</%def>

<table>
% for contact in c.contacts:
    <tr>
        <td>
            ${h.form("contact_show", controller="uniaddbook", method="post")}
                ${h.hidden(name='id', value=contact.id, checked='checked')}
                ${h.submit("show", contact)}
            ${h.end_form()}
        </td>
        <td>
            ${h.form("contact_delete", controller="uniaddbook", method="post")}
                ${h.hidden(name='id', value=contact.id, checked='checked')}
                ${h.submit("Delete", "Delete", confirm="Are you sure?")}<br />
            ${h.end_form()}
        </td>
    </tr
% endfor
</table>