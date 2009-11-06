<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Blog Index</title>
</%def>
<%def name="footer()"></%def>

${h.form(h.url_for(action="change_password"), method="post")}
    Current Password<br />
    ${h.password(name="current_password", value="")}<br />
    New Password<br />
    ${h.password(name="password1", value="")}<br />
    Confirm New Password<br />
    ${h.password(name="password2", value="")}<br />
    ${h.submit("Change Password", "Change Password")}<br />
${h.end_form()}
<br />
${c.failed}

<br />
<br />