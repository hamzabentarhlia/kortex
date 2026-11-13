# GA4 setup and measurement

## What fires

The site only sends events after a visitor accepts analytics in the cookie banner. Before that, no GA4 request is made. Every event carries `page` (the path). Events are sent by one small delegated listener in `src/scripts/site.js`.

| Event | When | Parameters |
|---|---|---|
| `book_call_click` | Any click on a Cal.com booking link or button | `cta`, `page` |
| `outbound_calcom` | Same click, as an outbound link marker | `cta`, `page` |
| `audit_cta_click` | Any click on a link to the audit page, or the Stripe payment button | `cta`, `page` |
| `cta_click` | Any click on an element with a `data-cta` or `data-track` id | `cta`, `page` |
| `generate_lead` | A lead form posts successfully (contact, audit, newsletter, checklist) | `form_name`, `page` |
| `newsletter_signup` | The newsletter form posts successfully | `form_name`, `page` |
| `checklist_download` | The checklist form posts successfully, or the PDF link is clicked | `form_name`, `page` |
| `pricing_plan_view` | A plan card is 60 percent visible on the pricing page, once per plan | `plan`, `page` |
| `theme_toggle` | The theme button is used | `theme` |
| `language_switch` | A language is chosen in the switcher | `to`, `page` |

## Mark key events

In GA4: Admin, Data display, Events. Switch on "Mark as key event" for:

1. `generate_lead`
2. `book_call_click`
3. `newsletter_signup`
4. `checklist_download`
5. `audit_cta_click`

Events appear in that list only after they have fired once. Trigger each one yourself first, then mark it. Use DebugView (Admin, Data display, DebugView) while testing.

## Conversion pages

Clean destination URLs for ads and funnel reports, all noindex:

- `/thanks/` and `/fr/thanks/`: contact form, checklist form
- `/thanks-audit/` and `/fr/thanks-audit/`: audit request

In GA4 you can create a key event from a page view of these paths: Admin, Data display, Events, Create event, matching `page_location` contains `/thanks`.

## Link Search Console

Admin, Product links, Search Console links, Link. Choose the `https://www.kortexlab.me/` property you verified with the HTML file. Then use Reports, Acquisition, Search Console to see queries next to conversions.

## CTA ids

Every button and booking link has a `data-cta` id, either hand-written (for example `pricing-swarm`) or generated from the page (for example `pricing-cta3`). The id becomes `utm_campaign` on booking links, so the same name shows up in GA4 and in Cal.com.

## UTM convention

Booking links carry three parameters, added by the build:

- `utm_source=site`
- `utm_medium=<page id>` such as `pricing`, `home`, `blog-measure-ai-citations`
- `utm_campaign=<cta id>`

The plan chooser adds `utm_content=plan_<plan>` and a note with the plan name. Links in emails use `utm_source=email`, `utm_medium=nurture` and `utm_campaign=<email name>`. Links you post on LinkedIn should use `utm_source=linkedin`, `utm_medium=social` and a campaign name of your choice. Keep values lowercase, with hyphens.

Cal.com receives these parameters on the booking page. Check in Cal.com that your booking page and webhook payload keep them; if they do not, read the source from the `utm_medium` and `utm_campaign` in GA4 instead.

## Weekly metric

See the final report for the one number to watch each week.
