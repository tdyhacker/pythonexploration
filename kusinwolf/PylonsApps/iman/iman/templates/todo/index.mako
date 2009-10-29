<%inherit file="../base.mako"/>
<%def name="head_tags()">
    <title>Blog Index</title>
</%def>

Add a task<br />
${h.form("%stodo/task_create" % g.site_prefix, method="post")}
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
        Priority - Category - Task<br />
        % for task in c.tasks:
            ${h.form("%stodo/task_delete" % g.site_prefix, method="post")}
                ${h.hidden(name="id", value=task.id, checked='checked')}
                ${h.submit("X", "X")}
                <font color=${task.priority[0].color}>${task.priority[0].name}</font> - <font color=${task.category[0].color}>${task.category[0].name}</font> - ${task.task}<br />
            ${h.end_form()}
        % endfor
        </td>
    </tr>
</table>
<br />
<br />