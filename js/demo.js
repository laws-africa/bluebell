// Live demo powered by @lawsafrica/bluebell-wasm (the Rust Bluebell parser
// compiled to WebAssembly), loaded from jsDelivr and pinned to a major
// version (see WASM_MODULE_CDN_URL below).
//
// Testing locally, before the npm package is published or to try local
// changes: build a `--target web` package and copy it into
// docs/js/bluebell-wasm/ (git-ignored), then load the demo page with a
// `?local-wasm` query parameter to use that copy instead of the CDN.
//
//   poe build-wasm   # builds --target web into crates/bluebell-wasm/pkg
//   cp -r crates/bluebell-wasm/pkg docs/js/bluebell-wasm
//   mkdocs serve     # then open http://127.0.0.1:8000/bluebell/demo/?local-wasm
//
(function () {
  // Pinned to the major version so the demo doesn't break on a breaking
  // change to the package, but still picks up fixes/features.
  const WASM_MODULE_CDN_URL = 'https://cdn.jsdelivr.net/npm/@lawsafrica/bluebell-wasm@4/bluebell_wasm.js';

  function init() {
    const input = document.getElementById('demo-input');
    const output = document.getElementById('demo-output');
    const statusEl = document.getElementById('demo-status');
    const downloadBtn = document.getElementById('demo-download');
    const htmlContainer = document.getElementById('demo-html');
    const htmlViewer = htmlContainer.querySelector('la-akoma-ntoso');
    const xmlPanel = document.getElementById('demo-tab-xml');
    const htmlPanel = document.getElementById('demo-tab-html');
    const tabButtons = Array.from(document.querySelectorAll('.demo-tab-button'));
    if (!input || !output || !statusEl || !downloadBtn || !htmlContainer || !xmlPanel || !htmlPanel || tabButtons.length === 0) {
      return;
    }

    const FRBR_URI = '/akn/za/act/2026/1';
    const PARSE_ROOT = 'act';
    let parserReadyPromise;
    let parseFn;
    let prettyPrintTransformPromise;
    let htmlXsltPromise;
    let latestXmlRaw = '';
    let latestXmlPretty = '';
    let activeTab = 'html';
    const domParser = new DOMParser();
    const xmlSerializer = new XMLSerializer();
    let lawWidgetsPromise;

    function setStatus(message, tone = 'info') {
      statusEl.textContent = message;
      statusEl.dataset.tone = tone;
    }

    function wasmModuleUrl() {
      const params = new URLSearchParams(window.location.search);
      if (params.has('local-wasm')) {
        return new URL('../js/bluebell-wasm/bluebell_wasm.js', document.baseURI).toString();
      }
      return WASM_MODULE_CDN_URL;
    }

    function setActiveTab(tab) {
      if (tab === activeTab) {
        return;
      }
      activeTab = tab;
      tabButtons.forEach((btn) => {
        const isActive = btn.dataset.demoTab === tab;
        btn.classList.toggle('is-active', isActive);
        btn.setAttribute('aria-pressed', String(isActive));
      });
      void renderActiveOutput();
    }

    async function ensureHtmlTransformer() {
      if (!htmlXsltPromise) {
        const xsltUrl = new URL('../js/html_akn.xsl', document.baseURI).toString();
        htmlXsltPromise = fetch(xsltUrl)
          .then((resp) => {
            if (!resp.ok) {
              throw new Error('Failed to load HTML renderer.');
            }
            return resp.text();
          })
          .then((xsltText) => {
            const xsltDoc = domParser.parseFromString(xsltText, 'application/xml');
            const processor = new XSLTProcessor();
            processor.importStylesheet(xsltDoc);
            return processor;
          });
      }
      return htmlXsltPromise;
    }

    async function getPrettyPrinter() {
      if (!prettyPrintTransformPromise) {
        const xsltUrl = new URL('../js/pretty_print.xsl', document.baseURI).toString();
        prettyPrintTransformPromise = fetch(xsltUrl)
          .then((resp) => {
            if (!resp.ok) {
              throw new Error('Failed to load pretty-print stylesheet.');
            }
            return resp.text();
          })
          .then((xsltText) => {
            const xsltDoc = domParser.parseFromString(xsltText, 'application/xml');
            const transform = new XSLTProcessor();
            transform.importStylesheet(xsltDoc);
            return transform;
          });
      }
      return prettyPrintTransformPromise;
    }

    async function ensureLawWidgets() {
      if (window.customElements && window.customElements.get('la-akoma-ntoso')) {
        return;
      }
      if (!lawWidgetsPromise) {
        lawWidgetsPromise = new Promise((resolve, reject) => {
          const script = document.createElement('script');
          script.type = 'module';
          script.src = 'https://cdn.jsdelivr.net/npm/@lawsafrica/law-widgets@latest/dist/lawwidgets/lawwidgets.esm.js';
          script.onload = () => resolve();
          script.onerror = () => reject(new Error('Failed to load law-widgets.'));
          document.head.appendChild(script);
        });
      }
      return lawWidgetsPromise;
    }

    async function renderActiveOutput() {
      const hasXml = Boolean(latestXmlRaw);
      downloadBtn.style.display = activeTab === 'xml' ? '' : 'none';
      if (activeTab === 'xml') {
        xmlPanel.classList.add('is-active');
        htmlPanel.classList.remove('is-active');
        output.textContent = hasXml ? latestXmlPretty : '<!-- XML output will appear here -->';
      } else {
        xmlPanel.classList.remove('is-active');
        htmlPanel.classList.add('is-active');
        if (!hasXml) {
          // Write to the viewer, not the container: setting textContent on
          // htmlContainer would remove the <la-akoma-ntoso> element that
          // htmlViewer references, detaching it so later renders go nowhere.
          if (htmlViewer) {
            htmlViewer.textContent = 'No XML available yet.';
          } else {
            htmlContainer.textContent = 'No XML available yet.';
          }
          return;
        }
        await ensureLawWidgets();
        try {
          const processor = await ensureHtmlTransformer();
          const xmlDoc = domParser.parseFromString(latestXmlRaw, 'application/xml');
          const fragment = processor.transformToFragment(xmlDoc, document);
          if (htmlViewer) {
            htmlViewer.innerHTML = '';
            htmlViewer.appendChild(fragment);
          } else {
            htmlContainer.innerHTML = '';
            htmlContainer.appendChild(fragment);
          }
        } catch (err) {
          const message = `Failed to render HTML: ${err.message}`;
          if (htmlViewer) {
            htmlViewer.textContent = message;
          } else {
            htmlContainer.textContent = message;
          }
        }
      }
    }

    function clearOutput(message) {
      latestXmlRaw = '';
      latestXmlPretty = '';
      downloadBtn.disabled = true;
      downloadBtn.dataset.xml = '';
      if (activeTab === 'xml') {
        xmlPanel.classList.add('is-active');
        htmlPanel.classList.remove('is-active');
        output.textContent = message;
      } else {
        xmlPanel.classList.remove('is-active');
        htmlPanel.classList.add('is-active');
        if (htmlViewer) {
          htmlViewer.textContent = message;
        } else {
          htmlContainer.textContent = message;
        }
      }
    }

    async function initParser() {
      if (parserReadyPromise) {
        return parserReadyPromise;
      }

      parserReadyPromise = (async () => {
        setStatus('Initializing parser (downloading WebAssembly module)…', 'info');
        const moduleUrl = wasmModuleUrl();
        const wasmModule = await import(/* webpackIgnore: true */ moduleUrl);
        await wasmModule.default();
        parseFn = wasmModule.parseToXml;
        setStatus('Parser ready. Edit the text to see updates.', 'success');
        return wasmModule;
      })();

      return parserReadyPromise;
    }

    async function updateOutput() {
      const text = input.value;
      try {
        await initParser();
      } catch (err) {
        console.error(err);
        setStatus(`Failed to initialise parser: ${err.message}`, 'error');
        clearOutput(`<!-- Failed to initialise parser: ${err.message} -->`);
        return;
      }

      setStatus('Parsing…', 'info');
      try {
        const xml = parseFn(text, PARSE_ROOT, FRBR_URI);
        setStatus('Parsed successfully.', 'success');
        latestXmlRaw = xml;
        try {
          const printer = await getPrettyPrinter();
          const sourceDoc = domParser.parseFromString(latestXmlRaw, 'application/xml');
          const prettyDoc = printer.transformToDocument(sourceDoc);
          latestXmlPretty = xmlSerializer.serializeToString(prettyDoc);
        } catch (printerError) {
          console.warn('Pretty-print failed', printerError);
          latestXmlPretty = latestXmlRaw;
        }
        downloadBtn.disabled = false;
        downloadBtn.dataset.xml = latestXmlRaw;
        void renderActiveOutput();
      } catch (err) {
        setStatus('Parse error. See details below.', 'error');
        clearOutput(err.message);
      }
    }

    input.addEventListener('input', () => {
      void updateOutput();
    });

    tabButtons.forEach((btn) => {
      const tab = btn.dataset.demoTab;
      btn.setAttribute('aria-pressed', String(tab === activeTab));
      btn.addEventListener('click', () => {
        if (tab) {
          setActiveTab(tab);
        }
      });
    });

    downloadBtn.addEventListener('click', () => {
      const xml = downloadBtn.dataset.xml;
      if (!xml) {
        return;
      }
      const blob = new Blob([xml], { type: 'application/xml' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'bluebell-demo.xml';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    });

    void renderActiveOutput();
    void updateOutput();

  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
