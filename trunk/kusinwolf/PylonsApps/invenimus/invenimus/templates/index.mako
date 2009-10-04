<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Overview</title>
</%def>
${c.pictures.sort()}
<table cellpadding='3' border=1>
    % for p in range(0, len(c.pictures), 3):
    <tr>
        % for q in range(0, 3):
        <td align = "center" width="33%">
            <img src="/${c.pictures[p + q]}" width="100%">
        </td>
        % endfor
    </tr>
    % endfor
    </tr>
</table>

<br />
<br />