<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Add Contact</title>
</%def>

<br />
<br />
<br />
<form method="POST" controller="uniaddbook", action="contact_insert">
    <table>
        <tr>
            <td>
                First Name:
            </td>
            <td>
                % if session.has_key('edit') and session['edit']:
                    ${h.text(name='fname', value=session['fname'])}
                % else:
                    <input type="text", name='fname', id='lname', value='John/Jane'>
                % endif
            </td>
        </tr>
        <tr>
            <td>
                Last Name:
            </td>
            <td>
                % if session.has_key('edit') and session['edit']:
                    ${h.text(name='lname', value=session['lname'])}
                % else:
                    <input type="text", name='lname', id='lname', value='Doe'>
                % endif
            </td>
        </tr>
        <tr>
            <td>
                Middle Name:
            </td>
            <td>
                % if session.has_key('edit') and session['edit']:
                    ${h.text(name='mname', value=session['mname'])}
                % else:
                    <input type="text", name='mname', id='mname', value='M.'>
                % endif
            </td>
        </tr>
        <tr>
            <td>
                Nick Name:
            </td>
            <td>
                % if session.has_key('edit') and session['edit']:
                    ${h.text(name='nname', value=session['nname'])}
                % else:
                    <input type="text", name='nname', id='nname', value='Bobby'>
                % endif
            </td>
        </tr>
        <tr>
            <td>
                Birthday:
            </td>
            <td>
                % if session.has_key('edit') and session['edit']:
                    Month: ${h.select("month", session['month'], range(1,13))}
                    Day: ${h.select("day", session['day'], range(1,32))}
                    Year: ${h.select("year", session['year'], range(2015,1900, -1))}
                % else:
                    Month: ${h.select("month", 1, range(1,13))}
                    Day: ${h.select("day", 1, range(1,32))}
                    Year: ${h.select("year", 2009, range(2015,1900, -1))}
                % endif
            </td>
        </tr>
        <tr>
            <td>
                Relationship:
            </td>
            <td>
                % if session.has_key('edit') and session['edit']:
                    ${h.select('relationship', session['relationship'], c.relationships)}
                % else:
                    ${h.select("relationship", None, c.relationships)}
                % endif
            </td>
        </tr>
        <tr>
            <td>
                Country:
            </td>
            <td>
                ${h.select("country", None, ["USA",])}
            </td>
        </tr>
        <tr>
            <td>
                State:
            </td>
            <td>
                % if session.has_key('edit') and session['edit']:
                    ${h.select('State', session['State'], c.states)}
                % else:
                    ${h.select("State", None, c.states)}
                % endif
            </td>
        </tr>
        <tr>
            <td>
                City:
            </td>
            <td>
                % if session.has_key('edit') and session['edit']:
                    ${h.text(name='city', value=session['city'])}
                % else:
                    <input type="text" name='city', id='city', value='Paris'>
                % endif
            </td>
        </tr>
        <tr>
            <td>
                Zipcode:
            </td>
            <td>
                % if session.has_key('edit') and session['edit']:
                    ${h.text(name='zipcode', value=session['zipcode'])}
                % else:
                    <input type="text" name='zipcode', id='zipcode', value='74387'>
                % endif
            </td>
        </tr>
        <tr>
            <td>
                Street:
            </td>
            <td>
                % if session.has_key('edit') and session['edit']:
                    ${h.text(name='street', value=session['street'])}
                % else:
                    <input type="text" name='street', id='street', value='7653 Woodmill Rd.'>
                % endif
            </td>
        </tr>
        <tr>
            <td colspan=2>
                <input type='submit', value="Save">
            </td>
        </tr>
    </table>
</form>
<br />
<br />
<br />