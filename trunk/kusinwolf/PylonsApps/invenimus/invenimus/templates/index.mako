<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Overview</title>
</%def>
${c.pictures.sort()}

<center>
<h2>Currently in ${g.picture_path + c.path} and moving files to ${g.picture_path + c.move_to_path}</h2><br />
% if c.min < c.id - 1:
	${h.link_to("Previous Page #%d" % (c.id - 1), h.url_for(id=c.id-1))} -
% else:
	${h.link_to("Previous Page #%d" % (c.max), h.url_for(id=c.max))} -
% endif
	${h.link_to("Current Page #%d of %d" % (c.id, c.max), h.url_for(id=c.id))} -
% if c.max >= c.id + 1:
	${h.link_to("Next Page #%d" % (c.id + 1), h.url_for(id=c.id+1))}
% else:
	${h.link_to("Next Page #%d" % (1), h.url_for(id=1))}
% endif
</center>

<br />
<br />
<center>
<table border=0>
	<tr>
		<td>
			${h.form(h.url_for(action="index"), method="post")}
				Directory ${h.select("directories", None, c.directories)} ${h.submit("Change Directory", "Change Directory")}
			${h.end_form()}
		</td>
		<td width=150>
		</td>
		<td>
			${h.form(h.url_for(action="index"), method="post")}
				Send to Directory ${h.select("destination", None, c.directories)} ${h.submit("Change Directory", "Change Directory")}
			${h.end_form()}
		</td>
	</tr>
</table>
</center>

${h.form(h.url_for(action="move_images"), method="post")}
<table cellpadding='3' border=1>
    % for p in range(0, len(c.pictures), 3):
    <tr>
        % for q in range(0, 3):
        <td align = "center" width="33%" valign="top">
			% if p + q < len(c.pictures) and c.pictures[p+q].find(".") > -1:
				<a href="/${c.path + c.pictures[p + q]}" target="_blank"><img src="/${c.path + c.pictures[p + q]}" width="100%"></a><br />
				
				<center>
				Mark to Move? ${h.checkbox(name='Mark', value=(p + q + (49 * (c.id - 1)) + (c.id - 1)), checked='')}
				&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
				<a href="/${c.path + c.pictures[p + q]}" target="_blank">${c.pictures[p+q]}</a>
				</center>
			% elif p + q < len(c.pictures) and c.pictures[p+q].find(".") <= -1:
				Attempted to display folder "${c.pictures[p + q]}"
			% endif
        </td>
        % endfor
    </tr>
    % endfor
    </tr>
</table>
<br />
<center>
${h.submit("Move Images", "Move Images", confirm="Are you sure?")} to ${g.picture_path + c.move_to_path}?<br />
</center>
${h.end_form()}

<br />

<center>
% if c.min < c.id - 1:
	${h.link_to("Previous Page #%d" % (c.id - 1), h.url_for(id=c.id-1))} -
% else:
	${h.link_to("Previous Page #%d" % (c.max), h.url_for(id=c.max))} -
% endif
	${h.link_to("Current Page #%d of %d" % (c.id, c.max), h.url_for(id=c.id))} -
% if c.max >= c.id + 1:
	${h.link_to("Next Page #%d" % (c.id + 1), h.url_for(id=c.id+1))}
% else:
	${h.link_to("Next Page #%d" % (1), h.url_for(id=1))}
% endif
</center>

<br />
<br />