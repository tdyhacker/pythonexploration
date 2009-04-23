<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Index</title>
</%def>

<center>
<table border=1>
% for position in range(c.limit-1):
    <tr>
        <td valign=middle>
            ${h.form("contact_show", controller="uniaddbook", method="post")}
                ${h.hidden(name='id', value=c.contacts1[position].id, checked='checked')}
                ${h.submit("show", c.contacts1[position])}
            ${h.end_form()}
        </td>
        <td>
            ${h.form("contact_delete", controller="uniaddbook", method="post")}
                ${h.hidden(name='id', value=c.contacts1[position].id, checked='checked')}
                ${h.submit("Delete", "Delete", confirm="Are you sure?")}<br />
            ${h.end_form()}
        </td>
        <td>
            <div class="spacer"></div>
        </td>
        <td>
            ${h.form("contact_show", controller="uniaddbook", method="post")}
                ${h.hidden(name='id', value=c.contacts2[position].id, checked='checked')}
                ${h.submit("show", c.contacts2[position])}
            ${h.end_form()}
        </td>
        <td>
            ${h.form("contact_delete", controller="uniaddbook", method="post")}
                ${h.hidden(name='id', value=c.contacts2[position].id, checked='checked')}
                ${h.submit("Delete", "Delete", confirm="Are you sure?")}<br />
            ${h.end_form()}
        </td>
        <td>
            <div class="spacer"></div>
        </td>
        <td>
            ${h.form("contact_show", controller="uniaddbook", method="post")}
                ${h.hidden(name='id', value=c.contacts3[position].id, checked='checked')}
                ${h.submit("show", c.contacts3[position])}
            ${h.end_form()}
        </td>
        <td>
            ${h.form("contact_delete", controller="uniaddbook", method="post")}
                ${h.hidden(name='id', value=c.contacts3[position].id, checked='checked')}
                ${h.submit("Delete", "Delete", confirm="Are you sure?")}<br />
            ${h.end_form()}
        </td>
    </tr>
% endfor
% if c.microoffset != 0:
    <tr>
        <td>
            ${h.form("contact_show", controller="uniaddbook", method="post")}
                ${h.hidden(name='id', value=c.contacts1[c.limit].id, checked='checked')}
                ${h.submit("show", c.contacts1[c.limit])}
            ${h.end_form()}
        </td>
        <td>
            ${h.form("contact_delete", controller="uniaddbook", method="post")}
                ${h.hidden(name='id', value=c.contacts1[c.limit].id, checked='checked')}
                ${h.submit("Delete", "Delete", confirm="Are you sure?")}<br />
            ${h.end_form()}
        </td>
    % if c.limit % 3 == 2:
        <td>
            ${h.form("contact_show", controller="uniaddbook", method="post")}
                ${h.hidden(name='id', value=c.contacts2[c.limit].id, checked='checked')}
                ${h.submit("show", c.contacts2[c.limit])}
            ${h.end_form()}
        </td>
        <td>
            ${h.form("contact_delete", controller="uniaddbook", method="post")}
                ${h.hidden(name='id', value=c.contacts2[c.limit].id, checked='checked')}
                ${h.submit("Delete", "Delete", confirm="Are you sure?")}<br />
            ${h.end_form()}
        </td>
    % endif
    </tr>
% endif
</table>
</center>