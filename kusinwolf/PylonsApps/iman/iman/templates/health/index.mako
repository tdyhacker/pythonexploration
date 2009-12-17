<%inherit file="../base.mako"/>
<%def name="head_tags()">
    <title>Health Index</title>
</%def>

Add new weight marker<br />
${h.form(h.url_for(action="weight_add"), method="post")}
    ${h.textarea(name="weight", rows=1, cols=10, content="")}
    &nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;&nbsp;
    Unit Type ${h.select("unit", None, c.units)}
    &nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;&nbsp;
    ${h.submit("Submit", "Add Weight")}<br />
${h.end_form()}

<br />
% if c.last_weight:
    <h2>Your Last Weight was ${c.last_weight.weight} ${c.last_weight.unit.digest}</h2>
% endif
<br />

<table cellpadding='3' border = 3>
    <tr>
        <td align="center">
            <font size='2'>Oops?</font>
        </td>
        <td align="center">
            <h4>Your Weight</h4>
        </td>
        <td align="center">
            <h4>On</h4>
        </td>
        <td rowspan='${len(c.weight) + 1}' valign="top" align="center">
            <h3>Progression Graph</h3>
            <img src=${c.plot_file} />
        </td>
    </tr>
% for group in c.weight:
    <tr>
        ${h.form(h.url_for(action="weight_delete"), method="post")}
        <td valign='top'>
            ${h.submit("X", "X")}
        </td>
        <td valign='top'>
            ${h.hidden(name="id", value=group.id, checked='checked')}
            <% context.write("%s %s" % (group.weight, group.unit.digest) )%>
        </td>
        <td valign='top'>
            ${group.created}
        </td>
        ${h.end_form()}
    </tr>
% endfor
</table>
<br />
<br />