# n8n lead flow

What happens after someone submits the checklist or newsletter form: tag the source, send four emails over 14 days, stop when they reply or book, notify you, and log everything to your CRM.

## Inputs

Every lead form on the site posts these fields to Pageclip: `email`, `form` (newsletter, checklist or audit), `source` (the page it came from), `language` (en, fr or ar), and the honeypot `botcheck`. The audit form also sends `name`, `company` and `website`. The Pageclip form key is set in `data/site.json`.

## Workflow 1: capture and sequence

1. **Webhook** node, method POST, path `kortex-lead`. In Pageclip, open the form, then Integrations, and add a webhook that points to the n8n production URL. If your Pageclip plan does not offer webhooks, forward the Pageclip notification email to a Gmail address and use a **Gmail Trigger** node instead, then add a **Code** node to read the fields from the message body. Check your Pageclip plan before building.
2. **IF** node: stop if `botcheck` is set, or if `email` is empty.
3. **Edit Fields (Set)** node: build the record. Fields: `email`, `form`, `source`, `language`, `captured_at` (`{{ $now }}`), `utm_source` (the page `source`), and `stage` set to `new`.
4. **HTTP Request** node, enrichment: call your enrichment provider with the email domain to get company name, size and country. Set the node to continue on error, because a missing match must not stop the flow. Add the result to the record.
5. **Odoo** node, resource Lead, operation Create: write the lead with the tags `source:<page>`, `form:<name>` and `lang:<code>`. If you keep your CRM in Google Sheets, use a **Google Sheets** node, operation Append, instead.
6. **Switch** node on `form`:
   - `checklist` goes to the full four-email sequence below.
   - `newsletter` goes to a single confirmation email from the **Send Email** node, then ends. Newsletter issues are sent from your newsletter tool.
   - `audit` goes to workflow 3.
7. **Send Email** node, SMTP: email 1 from `content/emails/01-checklist.md` (day 0).
8. **Wait** node, resume after a time interval of 3 days.
9. **IF** node, check for a stop signal (see workflow 2). If stopped, end. Otherwise **Send Email** with email 2 (`02-teardown.md`).
10. **Wait** 4 days, same stop check, then email 3 (`03-not-a-fit.md`), day 7.
11. **Wait** 7 days, same stop check, then email 4 (`04-audit.md`), day 14.
12. **Odoo** node, operation Update: set the lead stage to `nurture complete`.

Use a language branch: after the **Switch**, add an **IF** on `language` so French leads get French versions. The emails in `content/emails/` are English only. Write French versions before turning the branch on.

## Workflow 2: stop on reply or booking

1. **Gmail Trigger** node on your inbox, polling every minute.
2. **IF** node: does the sender match an email in your lead table? Use an **Odoo** node (Get Many, filter by email) or a **Google Sheets** node (Lookup).
3. If yes, **Odoo** node Update: set `stage` to `replied`. This is the stop signal that the sequence checks before each send.
4. **Slack** node (or **Send Email** to yourself): notify "Reply from <email>, source <page>".

A second trigger covers bookings: a **Webhook** node receiving Cal.com webhooks for the `BOOKING_CREATED` event. In Cal.com, open Settings, Developer, Webhooks and add the n8n URL. Match the attendee email, set `stage` to `booked`, and notify yourself. The booking payload also carries any UTM values passed in the link, so record `utm_campaign` to see which button produced the call.

## Workflow 3: audit requests

1. Same **Webhook** and **Edit Fields** nodes as workflow 1, with `form = audit`.
2. **Odoo** node: create the lead with the tag `audit-request`, including `name`, `company` and `website`.
3. **Send Email** node to yourself: "Audit request: <company>, <website>" with the fit-check checklist.
4. **Send Email** node to the lead: a plain fit-check reply written by hand from a template, not automated copy. Payment comes after the fit check.
5. When you approve the fit, send the Stripe Payment Link. If you set `stripeAuditUrl` in `data/site.json`, the site shows the payment button directly and you can skip the fit-check step for leads you already know.

## Rules to keep the flow safe

- Never send email 2, 3 or 4 to someone whose stage is `replied`, `booked` or `unsubscribed`.
- Every email carries an unsubscribe link. Use your sending tool's link, or a **Webhook** node that sets `stage` to `unsubscribed`.
- Add an **Error Trigger** workflow that emails you when any node fails.
- Test with your own address in n8n's test mode before activating, and read the four emails once as the recipient.
