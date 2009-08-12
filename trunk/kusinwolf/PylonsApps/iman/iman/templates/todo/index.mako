<%inherit file="../base.mako"/>
<%def name="head_tags()">
    <title>Blog Index</title>
</%def>

Add a task<br />
${h.form("/todo/task_create", method="post")}
    ${h.textarea(name="task", rows=1, cols=80, content="")}
    <br />
    Priority ${h.select("priority", None, c.priorities)}
    <br />
    Category ${h.select("category", None, c.categories)}
    <br />
    ${h.submit("Add", "Add")}<br />
${h.end_form()}

<table cellpadding='3'>
    <tr>
        <td>
            <h5>Your Tasks</h5>
        </td>
    </tr>
    <tr>
        <td valign='top'>
        % for task in c.tasks:
            ${h.form("/todo/task_delete", id=task.id), method="post")}
                ${h.submit("X", "X")}
                ${task.task}
            ${h.end_form()}
            <br />
        % endfor
        </td>
    </tr>
</table>
<br />
<br />