<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Edit Link</title>
</%def>

<BR>
    ${h.form(h.url(controller='hello', action='edit', method='post'))}
<div class='editpage'>
    Link:
        % if c.link_data.getLink():
            ${h.text_field(name='link', value=c.link_data.getLink(), size='128')}
        % else:
            ${h.text_field(name='link', value='', size='128')}
        % endif
    <BR>
    Notes:
    <div class='editpagefields'>
        % if c.link_data.getNotes():
            ${h.text_field(name='notes', value=c.link_data.getNotes(), size='128')}
        % else:
            ${h.text_field(name='notes', value='', size='128')}
        % endif
    </div>
    <BR>

    Tags:
    <div class='editpagefields'>
        % if c.link_data.getTags():
            ${h.text_field(name='tags', value=c.link_data.getTags(), size='128')}
        % else:
            ${h.text_field(name='tags', value='', size='128')}
        % endif
    </div>
    <BR>

    Activity:
        <select name='active'>
        % if c.link_data.getActivity():
            <option value="True" selected='selected'>Active</option>
            <option value="False">Inactive</option>
        % else:
            <option value="True">Active</option>
            <option value="False" selected='selected'>Inactive</option>
        % endif
        </select>

    <BR>
    <BR>
    ${h.hidden_field(name='id', value=c.link_data.getID(), checked='checked', method='GET')}
    ${h.submit('Edit', confirm="Is this correct?")}
</div>
    ${h.end_form()}

<BR><BR>
    
<div class='editpage'>
    % if c.success:
        ${c.success}
    % endif
</div>

<div class="datalink">
${h.link_to("Main Menu", h.url(controller="hello", action="index"))}
</div>
<BR>
