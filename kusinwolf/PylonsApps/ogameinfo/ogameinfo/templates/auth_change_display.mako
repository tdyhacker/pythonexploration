<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Index</title>
</%def>

<center>
    ${h.form("auth_change_password", controller="ogame", method="post")}
        New Password ${h.text(name="password_1", content="")}<br />
        Retype New Password ${h.text(name="password_2", content="")}<br />
        ${h.submit("Change Password", "Change Password")}<br />
    ${h.end_form()}
    ${c.fail}
</center>

<br />
<br />