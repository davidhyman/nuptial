<form action="/reregister" method="post">
	<input id="email" name="email" type="email" placeholder="Email"/>
	<input id="password" name="password" type="password" placeholder="Password"/>
    % if not get('authenticated'):
    <input id="secret" name="secret" type="secret" placeholder="Secret"/>
    % end
	<input value="Change Password" type="submit"/>
</form>