% rebase('base.tpl', title='Details', current='rsvp')

We can't wait for you to join us!

Please fill in your RSVP below. You can come back and update it later if needed. We'll have to lock it down as we get closer to the day.

<form action="/rsvp/submit" method="post">
    <fieldset>
    <input id="first" name="first" type="text" placeholder="First Name" value="{{get('first',[''])[0]}}"/>
    <input id="last" name="last" type="text" placeholder="Last Name" value="{{get('last',[''])[0]}}"/>
    </fieldset>
    <fieldset>
        Any dietary requirements:
        <select name="dietary" multiple="multiple">
            <option value="vegetarian">Vegetarian</option>
            <option value="vegan">Vegan</option>
            <option value="nuts">Nut Allergy</option>
            <option value="lactose">Lactose-Free</option>
            <option value="gluten">Gluten-Free</option>
        </select>
        Any guests:
        <select name="plusone">
            <option value="0">No</option>
            <option value="1">Yes</option>
        </select>
        And their requirements:
        <select name="dietary2" multiple="multiple">
            <option value="vegetarian">Vegetarian</option>
            <option value="vegan">Vegan</option>
            <option value="nuts">Nut Allergy</option>
            <option value="lactose">Lactose-Free</option>
            <option value="gluten">Gluten-Free</option>
        </select>
        Will you be staying all day?
        <select name="staying">
            <option value="2">All of it!</option>
            <option value="0">Just the morning (The important bit!)</option>
            <option value="1">Just the afternoon (The tasty bit!)</option>
        </select>
    </fieldset>
    <input value="Send" type="submit" />
</form>

