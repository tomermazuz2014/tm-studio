# TM Studio TLV

The portfolio site of Tomer Mazuz (TM Studio TLV): one static page, `index.html`, with its images, fonts and clips beside it.

- Live site: https://tomermazuz2014.github.io/tm-studio/
- Home page and a Services page (`#services`) live in the same file.
- `api/chat.js` is the server route for the site's assistant (a Vercel function). It needs `ANTHROPIC_API_KEY` set on the
  host; the key is never in the browser. On GitHub Pages there is no server, so the assistant shows a note with the
  Instagram link instead of answering.
- The Hebrew font (Ploni, by AlefAlefAlef) is licensed to the site owner and is not free to reuse.
