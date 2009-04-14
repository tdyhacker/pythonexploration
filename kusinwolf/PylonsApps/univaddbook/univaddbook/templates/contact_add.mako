<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Add Contact</title>
</%def>

<br />
<br />
<br />
<form method="POST" action="insert">
    First Name: <input type="text", name='fname', id='lname', value='John/Jane'><br />
    Last Name: <input type="text", name='lname', id='lname', value='Doe'><br />
    Middle Name: <input type="text", name='mname', id='mname', value='M.'><br />
    Nick Name: <input type="text", name='nname', id='nname', value='Bobby'><br />
    Birthday:
        ${h.select("month", 1, range(1,13))}
        ${h.select("day", 1, range(1,32))}
        ${h.select("year", 2009, range(2015,1900, -1))}<br />
    Street: <input type="text" name='street', id='street', value='7653 Woodmill Rd.'><br />
    State:
        ${h.select("state", None, c.states)}<br />
    City: <input type="text" name='city', id='city', value='Paris'><br />
    Zipcode: <input type="text" name='zipcode', id='zipcode', value='74387'><br />
<input type='submit'>
</form>
<br />
<br />
<br />