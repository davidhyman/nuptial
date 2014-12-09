% rebase('base.tpl', title='Welcome', current='welcome')
Welcome!

This page is our most basic introduction

% if get('authenticated'):
% include('registered.tpl')
% else:
% include('register.tpl')
% end