<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Link Database</title>
</%def>

<div class="datalink">
${h.link_to("Main Menu", h.url(controller="hello", action="index"))}
</div>
<BR>

${h.form(h.url(controller='hello', action='allLinks'), method='GET')}

<span class='controls-top'>
# Per Page
</span
<select name='limit'>
% for length in c.pagelimits:
    %if c.pagesize == length:
        <option value=${length} selected='selected'>${length}</option>
    %else:
        <option value=${length}>${length}</option>
    % endif
% endfor
</select>

<span class='controls-top'>
Page #
</span>
<select name='offset'>
    % for length in range(1, c.pageoffset + 1):
        % if c.pagenumber == length:
            <option value=${length} selected='selected'>${length}</option>
        % else:
            <option value=${length}>${length}</option>
        % endif
    % endfor
</select>

${h.submit('Go')}
${h.end_form()}

<span class="controls-bottom">
    % if c.pagenumber <= 1:
        [ Previous ] -
    % else:
        [ ${h.link_to("Previous", h.url(controller='hello', action='allLinks', limit=c.pagesize, offset=c.pagenumber-1), method='GET')} ] -
    % endif
    
    % if c.pagenumber >= c.pageoffset:
        [ Next ]
    % else:
        [ ${h.link_to("Next",h.url(controller='hello', action='allLinks', limit=c.pagesize, offset=c.pagenumber+1), method='GET')} ]
    % endif
</span>

<BR><BR>

${h.form(h.url(controller='hello', action='inactivateObject'), method='post')}
${h.hidden_field(name='Redirect', value='alllinks', checked='checked')}
<TABLE border='3' width='100%'>
    <TR>
        <TD width='10%' colspan=2>
            <div class="tableheader">
                Options
            </div>
        </TD>
        <TD>
            <div class="tableheader">
                Link
            </div>
        </TD>
        <TD width='7%'>
            <div class="tableheader">
                Added
            </div>
        </TD>
        <TD width='10%'>
            <div class="tableheader">
                Modified
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
            ${h.form(h.url(controller='hello', action='edit', method='POST'))}
            ${h.hidden_field(name='id', value=l.getID(), checked='checked')}
            ${h.submit('Edit')}
            ${h.end_form()}
        </TD>
        <TD>
            ID:
            ${l.getID()}:
            ${h.link_to(l.getLink(), l.getLink())}
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
        <TD align='center' width='10%'>
            <div class="datedisplay">
                ${l.getAddTime()}
            </div>
        </TD>
        <TD align='center' width='10%'>
            <div class="datedisplay">
                ${l.getModTime()}
            </div>
        </TD>
    </TR>
    <TR></<TR>
% endfor
    <TR>
        <TD align='center' width='5%'>
            ${h.submit('Delete', confirm="Delete?")}
            ${h.end_form()}
        </TD>
        <TD align='center' width='5%'>
        </TD>
        <TD>
        </TD>
        <TD align='center' width='10%'>
        </TD>
        <TD align='center' width='10%'>
        </TD>
    </TR>
</TABLE>

<BR>
<div class="datalink">
${h.link_to("Main Menu", h.url(controller="hello", action="index"))}
</div>

