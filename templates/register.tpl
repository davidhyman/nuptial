<form action="/register" method="post">
	<input id="email" name="email" type="email" placeholder="Email" />
	<input id="password" name="password" type="password" placeholder="Password"/>
	<input value="Register" type="submit" />
</form>

<form action="/authenticate" method="post">
	<input id="email" name="email" type="email" placeholder="Email" />
	<input id="password" name="password" type="password" placeholder="Password"/>
	<input value="Login" type="submit"/>
    <button type="submit" formaction="/password_reset"/>Forgot</button>
</form>