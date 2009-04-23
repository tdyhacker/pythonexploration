<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Index</title>
</%def>

<table>
% for position in c.limit:
    <tr>
        <td>
            ${h.form("contact_show", controller="uniaddbook", method="post")}
                ${h.hidden(name='id', value=c.contacts1[postion].id, checked='checked')}
                ${h.submit("show", c.contacts1[position])}
            ${h.end_form()}
        </td>
        <td>
            ${h.form("contact_delete", controller="uniaddbook", method="post")}
                ${h.hidden(name='id', value=c.contacts1[postion].id, checked='checked')}
                ${h.submit("Delete", "Delete", confirm="Are you sure?")}<br />
            ${h.end_form()}
        </td>
        
         <td>
            ${h.form("contact_show", controller="uniaddbook", method="post")}
                ${h.hidden(name='id', value=c.contacts2[postion].id, checked='checked')}
                ${h.submit("show", c.contacts2[position])}
            ${h.end_form()}
        </td>
        <td>
            ${h.form("contact_delete", controller="uniaddbook", method="post")}
                ${h.hidden(name='id', value=c.contacts2[postion].id, checked='checked')}
                ${h.submit("Delete", "Delete", confirm="Are you sure?")}<br />
            ${h.end_form()}
        </td>
        <td>
            ${h.form("contact_show", controller="uniaddbook", method="post")}
                ${h.hidden(name='id', value=c.contacts3[postion].id, checked='checked')}
                ${h.submit("show", c.contacts3[position])}
            ${h.end_form()}
        </td>
        <td>
            ${h.form("contact_delete", controller="uniaddbook", method="post")}
                ${h.hidden(name='id', value=c.contacts3[postion].id, checked='checked')}
                ${h.submit("Delete", "Delete", confirm="Are you sure?")}<br />
            ${h.end_form()}
        </td>
        
    </tr>
% endfor
</table>