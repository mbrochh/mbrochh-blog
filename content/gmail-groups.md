Date: 2012-06-11
Title: Follow mailing lists using GMail
Slug: gmail-groups
Category: Blog
Tags: google, gmail, lifehacking, productivity

Here is a small trick to manage your mailing list subscriptions with your GMail
account without cluttering your inbox.

# Step 1: Setup multiple inboxes

* Open GMail and go to _Settings_
* Go to _Labs_
* Search for _Multiple Inboxes_ and enable it
* Save your changes
* Go to _Settings_ again
* Go to _Multiple Inboxes_
* Replace the search query for _Pane 0_ with this: ``-label:muted
  label:]-groups is:unread``
* Delete the search query for _Pane 1_
* Set _Extra panel positioning_ to _Below the inbox_
* Go to _Settings_
* Got to _Labels_
* Create a new label _] Groups_

What have we done so far? We have told GMail that we want a second inbox below
our main inbox that

* does not display muted posts. This is a nice hack, it turns out that _muted_
  is a hidden label in Gmail, so you can filter for muted conversations
* does display anything that has the label _] Groups_ (filtering for labels
  seems to be case insensitive)
* does only display conversations that are unread

# Step 2: Create filters for your mailing lists

If you are subscribed to _N_ mailing lists you need to create _N+1_ filters
now.

First create one big filter for all your mailing lists. Set it up like so:

* _Has the words_: ``list1@example.com OR list2@example.com ... OR listN@example.com``
* _Skip inbox_
* _Apply label_: _] Groups_

At this point you would be able to see how many unread mailing list posts there
are because the _] Groups_ label would become bold and display a number
behind itself. However, it would be nice if you could see exactly how many
unread items _each_ of your subscriptions has. For this you simply need to add
one more filter for each subscription:

* _Has the words_: ``listX@example.com``
* _Skip inbox_
* _Apply label_: _] Groups/listX_

So if you are following the Python users mailing list, you would for example
create a new sub label called _python-users_ under the label _] Groups_.

# Step 3: Profit

This setup allowed me to follow 16 mailing lists during the last 2 years
without drowning in content overflow. If a thread on the list is very active
but you already know that you are not interested in following the discussion,
just mute the conversation and it will no longer pop up in your second inbox.

Because the new filters make sure that those messages skip the main inbox, you
will not get notifications on your Android phone for all these messages, which
is another huge plus.

From now on it is just scanning through the headlines in your inbox and marking
them all as read. Another good thing about this is that you will be able to
perform searches in GMail to find old discussions.

Your new inbox should look like this:

<img src="./images/mailinglists.png" width="100%" alt="Gmail with multiple inboxes" />
