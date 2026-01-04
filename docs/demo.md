# Bluebell Live Demo

Experiment with Bluebell text by editing the textarea below. The XML output updates automatically in your browser using
Pyodide to run the real Bluebell parser.

<div class="demo-container">
  <label for="demo-input" class="md-typeset__label">Bluebell text</label>
  <textarea id="demo-input" class="demo-input mdc-text-field__input" rows="18">
PREFACE
  Demo preface text.

BODY

CHAPTER 1 - Preliminary
  SECTION 1 - Short title
    Short title text.

  SECTION 2
    ITEMS
      ITEM (a)
        First item.

      ITEM (b)
        Second item.
  </textarea>

  <p id="demo-status" class="demo-status">Loading parser…</p>

  <label for="demo-output" class="md-typeset__label">Generated XML</label>
  <button id="demo-download" class="md-button md-button--primary demo-download" type="button" disabled>Download XML</button>
  <pre id="demo-output" class="demo-output">&lt;!-- XML output will appear here --&gt;</pre>

</div>
