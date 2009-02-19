<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Add Event</title>
</%def>

<div id="addevent">
<FORM id="event" name="event">
    <TABLE width=100%>
        <TR>
            <TD width=70%>
                <div id="addevent-title">
                    <input type="text" name="event-title" value="Title" size=70%>
                </div>
            </TD>
            <TD width=30% valign=top>
                <div id="addevent-type">
                    <SELECT>
                    <OPTION value="yang">Yang (Good)</OPTION>
                    <OPTION value="neutral">Neutral</OPTION>
                    <OPTION value="yin">Yin (Bad)</OPTION>
                    </SELECT>
                </div>
            </TD>
        </TR>
    </TABLE>
    <div id="addevent-text">
        <BR />
        <CENTER>
            <textarea id="event-text" rows="8" cols="100">Event</textarea> <!-- Prevents extra newlines being placed in the field -->
        </CENTER>
        <BR />
    </div>
</FORM>
</div>

<%def name="footer()">
    <!-- no default site map for you! -->
</%def>