<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Export Contacts</title>
</%def>


${h.form("csv_export", controller="uniaddbook", method="post")}
<table>
% for position in range(c.limit-1):
    <tr>
        <td>
            ${h.checkbox(name='export', value=c.contacts1[position].id, checked='')}
        </td>
        <td>
            ${c.contacts1[position]}
        </td>
        <td>
            ${h.checkbox(name='export', value=c.contacts2[position].id, checked='')}
        </td>
        <td>
            ${c.contacts2[position]}
        </td>
        <td>
            ${h.checkbox(name='export', value=c.contacts3[position].id, checked='')}
        </td>
        <td>
            ${c.contacts3[position]}
        </td>
    </tr>
% endfor
% if c.microoffset != 0:
    <tr>
        <td>
            ${h.checkbox(name='export', value=c.contacts1[position].id, checked='')}
        </td>
        <td>
            ${c.contacts1[position]}
        </td>
    % if c.limit % 3 == 2:
        <td>
            ${h.checkbox(name='export', value=c.contacts2[position].id, checked='')}
        </td>
        <td>
            ${c.contacts2[position]}
        </td>
    </tr>
    % endif
    </tr>
% endif
</table>
${h.submit("Export", "Export")}
${h.end_form()}