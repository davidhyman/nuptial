<html>
<head>
    <link rel="stylesheet" href="static/styles.css">
    <script src="static/jquery-2.1.1.min.js"></script>
    <script src="static/underscore-min.js"></script>
    <title>{{title or 'No title'}}</title>
</head>
<header>
    <div id="menu">
        % for link, name in menu_links.items():
        % classes = 'current' if current == link else ''
<a href="/{{link}}" class="{{classes}}">{{name}}</a>\\
        % end
    </div>
</header>
<body>
    <div id="content">
        {{!base}}
    </div>
</body>
</html>