<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Link Saver</title>
</%def>

<div id='processbox'>
    <div class='innerprocessbox'>
        <!--Ex: "http://Gibberish.com/here.html?originallink=http://What_we_are_looking_for.com/the_name.mp3"<BR>-->
        Ex: "http://www.google.com/"
    </div>
    ${h.form(h.url(controller='hello', action='', method='post'))}
    Link - 
    ${h.text_field(name='link', id='link', value='', size='128')}
    <BR>
    <BR>
    <div class='innerprocessbox'>
        Ex: "This information is useful!"
    </div>
    Notes - 
    ${h.text_field(name='notes', id='notes', value='', size='128')}
    <BR>
    <BR>
    <div class='innerprocessbox'>
        Ex: "searchengine google homepage"
        <BR>
        Info: Tags are broken apart by spaces and non-alphabet characters
    </div>
    Tags - 
    ${h.text_field(name='tags', id='tags', value='', size='128')}
    <BR>
    <BR>
    <div class='innerprocessbox'>
    ${h.submit('Process')}
    </div>
    ${h.end_form()}
</div>

<div class='editpage'>
    % if c.success:
        ${c.success}
    % endif
</div>

<div class="datalink">
    ${h.link_to("Whole List", h.url(controller="hello", action="allLinks"))}
</div>

<BR>
${h.form(h.url(controller='hello', action='inactivateObject', method='post'))}
${h.hidden_field(name='Redirect', value='serverinfo', checked='checked')}
<center>
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
            ${h.form(h.url(controller='hello', action='edit'), method='GET')}
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
                        ${h.link_to(t, h.url(controller='hello', action='search', tags=t), method='GET')}
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
</center>

<BR>

<div class="datalink">
    ${h.link_to("Whole List", h.url(controller="hello", action="allLinks"))}
</div>


<%def name="column_one()">
    Hello World!
</%def>

<%def name="column_two()">
    Nubbles
</%def>