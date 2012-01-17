===============
cmsplugin-shop
===============

A set of django CMS plugins to expose some of django SHOP's functionality to CMS pages.

This is a work in progress, so don't exxpect anything to work yet :)

Some code was roughly open-sourced, so while it should work, it is still very
ugly and will most likely be renamed.

What you should expect here
===========================

cmsplugin_topproducts
---------------------
A plugin to display the N top selling products.

* displays list of products ordered by highest aggregated count across all Order objects.
* ability to choose template for list container
* ability to choose template for list item container

cmsplugin_shopcart
---------------------
A plugin to display the contents of the shop's shopping cart.

cmsplugin_usersorders
---------------------
Displays list of orders for the current user.

* filter by order status (multiple choice)
* ability to choose template for list container
* ability to choose template for list item container

cmsplugin_featuredproducts
--------------------------
Displays list of selected products for selective display.

* ability to choose template for list container
* ability to choose template for list item container

