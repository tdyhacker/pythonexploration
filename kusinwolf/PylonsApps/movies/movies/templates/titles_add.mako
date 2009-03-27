<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Add Movie</title>
</%def>

<br />
<br />
<br />
<form method="POST" action="insert"}>
    Name: <input type="text", name='name', id='name', value='Some Name'><br />
    Released:
        ${h.select("month", None, range(1,13))}
        ${h.select("day", None, range(1,32))}
        ${h.select("year", 2009, range(2015,1900, -1))}<br />
    Duration: <input type="text" name='duration', id='duration', value='120'><br />
    Rating: <select name='rating', id='rating'>
                <option value="G">G</option>
                <option value="PG">PG</option>
                <option value="PG-13">PG-13</option>
                <option value="R">R</option>
            </select><br />
    Category: <input type="text", name='category', id='category', value='5'><br />
<input type='submit'>
</form>
<br />
<br />
<br />