<%inherit file="base.mako"/>
<%def name="head_tags()">
    <title>Index</title>
</%def>

<%def name="footer()">
    New User? Well, I don't care, come back later when I do
</%def>

<center>
    ${h.form("auth", controller="ogame", method="post")}
        Username ${h.text(name="lgoin", content="")}<br />
        Password ${h.text(name="password", content="")}<br />
        ${h.submit("Sign In", "Sign In")}<br />
    ${h.end_form()}
    ${c.fail}
</center>

<br />
<br />