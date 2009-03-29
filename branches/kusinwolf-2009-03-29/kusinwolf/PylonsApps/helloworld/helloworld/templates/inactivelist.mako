<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Link Database</title>
</%def>

<div class="datalink">
${h.link_to("Main Menu", h.url(controller="hello", action="index"))}
</div>
<BR>

${h.form(h.url(controller='hello', action='caseDelete', method='post'))}
${h.hidden_field(name='Redirect', value='inactivelist', checked='checked')}
<TABLE border='3' width='100%'>
    <TR>
        <TD width='10%' colspan=2>
            <div class="tableheader">
                Options
            </div>
        </TD>
        <TD>
            <div class="tableheader">
                Link - Inactive Links
            </div>
        </TD>        
        <TD width='7%'>
            <div class="tableheader">
                Reactivate
            </div>
        </TD>
        <TD width='10%'>
            <div class="tableheader">
                Inactivated
            </div>
        </TD>
    </TR>
    <TR></<TR>
${h.form(h.url(id="ZOMG BORKED!"))}
${h.end_form()}
% for l in c.link_data:
    <TR>
        <TD align='center' width='5%'>
            ${h.check_box(name='Delete', value=l.getID(), checked='')}
        </TD>
        <TD align='center' width='5%'>            
            ${h.form(h.url(controller='hello', action='edit', method='post'))}
            ${h.hidden_field(name='id', value=l.getID(), checked='checked')}
            ${h.submit('Edit')}
            ${h.end_form()}
        </TD>
        <TD>
            ID:
            ${l.getID()}:
            ${h.link_to(l.getLink(), l.getLink())}
            ${"""<input type='hidden' name='remove' value='%s' checked='checked'>""" % l.getLink()}
            <div class="tab">
                <div class="namespace">
                    <span class="namespacetitles">
                        Notes:
                    </span>
                    ${l.getNotes()}
                    <BR>
                    <span class="namespacetitles">
                        Tags:
                    </span>
                    % for t in l.parseTags():
                        ${h.link_to(t, h.url(controller='hello', action='search', method='GET', tags=t))}
                    % endfor
                </div>
            </div>
        </TD>
        <TD align='center' width='7%'>
            ${h.check_box(name='Activate', value=l.getID(), checked='')}
            ${h.hidden_field(name='Redirect', value='inactivelist', checked='checked')}
        </TD>
        <TD align='center' width='10%'>
            <div class="datedisplay">
                ${l.getInaTime()}
            </div>
        </TD>
    </TR>
    <TR></<TR>
% endfor
    <TR>
        <TD align='center' width='5%'>
            ${h.submit('Delete', confirm="Permanitly Delete?")}
        </TD>
        <TD align='center' width='5%'>
        </TD>
        <TD>
        </TD>
        <TD align='center' width='10%'>
            ${h.submit('Activate', confirm="Activate?")}
            ${h.end_form()}
        </TD>
        <TD align='center' width='10%'>
        </TD>
    </TR>
</TABLE>

<BR>
<div class="datalink">
${h.link_to("Main Menu", h.url(controller="hello", action="index"))}
</div>