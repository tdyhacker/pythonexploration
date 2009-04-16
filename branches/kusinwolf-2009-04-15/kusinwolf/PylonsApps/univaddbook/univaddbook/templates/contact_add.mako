<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Add Contact</title>
</%def>

<br />
<br />
<br />
<form method="POST" action="contact_insert">
    <table>
        <tr>
            <td>
                First Name:
            </td>
            <td>
                <input type="text", name='fname', id='lname', value='John/Jane'>
            </td>
        </tr>
        <tr>
            <td>
                Last Name:
            </td>
            <td>
                <input type="text", name='lname', id='lname', value='Doe'>
            </td>
        </tr>
        <tr>
            <td>
                Middle Name:
            </td>
            <td>
                <input type="text", name='mname', id='mname', value='M.'>
            </td>
        </tr>
        <tr>
            <td>
                Nick Name:
            </td>
            <td>
                <input type="text", name='nname', id='nname', value='Bobby'>
            </td>
        </tr>
        <tr>
            <td>
                Relationship:
            </td>
            <td>
                ${h.select("relationship", None, c.relationships)}
            </td>
        </tr>
        <tr>
            <td>
                Birthday:
            </td>
            <td>
                ${h.select("month", 1, range(1,13))}
                ${h.select("day", 1, range(1,32))}
                ${h.select("year", 2009, range(2015,1900, -1))}
            </td>
        </tr>
        <tr>
            <td>
                Street:
            </td>
            <td>
                <input type="text" name='street', id='street', value='7653 Woodmill Rd.'>
            </td>
        </tr>
        <tr>
            <td>
                State:
            </td>
            <td>
                ${h.select("state", None, c.states)}
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
                City:
            </td>
            <td>
                <input type="text" name='city', id='city', value='Paris'>
            </td>
        </tr>
        <tr>
            <td>
                Zipcode:
            </td>
            <td>
                <input type="text" name='zipcode', id='zipcode', value='74387'>
            </td>
        </tr>
        <tr>
            <td colspan=2>
                <input type='submit'>
            </td>
        </tr>
    </table>
</form>
<br />
<br />
<br />