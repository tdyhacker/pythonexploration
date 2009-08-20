<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Blog Index</title>
</%def>
<%def name="footer()"></%def>

${h.form("%saccount/login" % g.site_prefix, method="post")}
    Username<br />
    ${h.text(name="login_name", value="")}<br />
    Password<br />
    ${h.password(name="password", value="")}<br />
    ${h.submit("Login", "Login")}<br />
${h.end_form()}
<br />
${c.failed}

<br />
<br />