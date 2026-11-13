Subject: A mistake we made on our own site
Preview: Three of our most important pages told Google not to index them. Here is how we found it.
Send: day 3

Hi {{first_name}},

One teardown, as promised. This one is about us.

For a while, five addresses on kortexlab.me, including our pricing, blog and contact pages, sent search engines a confusing signal. If you typed the address without the trailing slash, the server returned a nearly empty page marked noindex, and some of those pages named a French version as the canonical. The address with the slash, the one every menu link used, served the full page. Google could reach both, so it saw a conflict.

How we found it: we requested every address on the site in both forms, with and without the slash, and wrote down the status code, the robots tag and the canonical for each. Five addresses were wrong, and the pattern was obvious once it was on one page: the cause was a set of old redirect files that the host served before it served the real page.

The fix was to delete those files, so the host now answers with a plain 301 redirect to the full page. We then checked all 147 addresses again, and the live site.

Three things to take from it.

First, check both forms of every important address. Most audits only test the one in the menu.

Second, look at the raw response, not the page in your browser. A browser follows redirects and runs scripts, which hides this kind of fault.

Third, write the result down with a date. We keep our own checks in a public log: https://www.kortexlab.me/proof/

The access checks in the checklist would have caught this on day one. If you have not run them yet, start there.

Hamza
