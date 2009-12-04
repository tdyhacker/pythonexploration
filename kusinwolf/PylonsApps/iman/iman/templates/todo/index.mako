<%inherit file="../base.mako"/>
<%def name="head_tags()">
    <title>Todo List</title>
</%def>

Add a task<br />
${h.form(h.url_for(action="task_create"), method="post")}
    ${h.textarea(name="task", rows=1, cols=80, content="")}
    <br />
    Priority ${h.select("priority", None, c.priorities)}
    &nbsp;&nbsp;&nbsp;&nbsp;
    Category ${h.select("category", None, c.categories)}
    &nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;&nbsp;
    &nbsp;&nbsp;&nbsp;&nbsp;
    ${h.submit("Add Task", "Add Task")}<br />
${h.end_form()}

<br />

${h.form(h.url_for(action="index"), method="post")}
    Sort Type ${h.select("sort_type", None, c.sort_type)}
    &nbsp;&nbsp;
    Direction ${h.select("sort_direction", None, c.direction)}
    &nbsp;&nbsp;
    History ${h.select("history_order", None, c.direction)}
    &nbsp;&nbsp;
    ${h.submit("Resort", "Resort")}<br />
    <br />
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
            ${h.form(h.url_for(action="task_delete"), method="post")}
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