<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Full List</title>
</%def>

    <h1>Our Movies!</h1>
    <ul>
        % for title in c.titles:
            <li>${h.link_to(title.name, h.url_for(controller='titles', action='show', id=title.id))}</li>
        % endfor
    </ul>
