# Bluebell Live Demo

Experiment with Bluebell text by editing the box below. The XML and HTML is updated live as you type. This uses
 [Pyodide](https://pyodide.org/en/stable/) to run the Bluebell parser in the browser, and styling for the HTML is apply with the Laws.Africa
[Law Widgets](https://github.com/laws-africa/law-widgets) library.

<div class="demo-container">
  <textarea id="demo-input" class="demo-input mdc-text-field__input" rows="18">
CHAPTER 1 - Preliminary
  SEC 1. - Short title
    This is some example text in section 1. It includes **bold** text and //italic// text.

  SEC 2. - Second section
    SUBSEC (1)
      This is subsection (1) under section 2, with two sub-items.

      ITEMS
        ITEM (a)
          First item.

        ITEM (b)
          Second item.
  </textarea>

  <p id="demo-status" class="demo-status">Loading parser…</p>

  <div class="demo-tab-bar">
    <div class="demo-tab-buttons">
      <button type="button" class="md-button md-button--outlined demo-tab-button is-active" data-demo-tab="xml">XML</button>
      <button type="button" class="md-button md-button--outlined demo-tab-button" data-demo-tab="html">HTML</button>
    </div>
  </div>
  <div id="demo-tab-xml" class="demo-tab-panel is-active">
    <div class="demo-download-bar">
      <button id="demo-download" class="md-button md-button--primary demo-download" type="button" disabled>Download XML</button>
    </div>
    <pre id="demo-output" class="demo-output">&lt;!-- XML output will appear here --&gt;</pre>
  </div>
  <div id="demo-tab-html" class="demo-tab-panel" hidden>
    <div id="demo-html" class="demo-html">
      <la-akoma-ntoso frbr-expression-uri="/akn/za/act/2026/1/eng@"></la-akoma-ntoso>
    </div>
  </div>

</div>
