(function () {
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
    let parserReadyPromise;
    let parseFn;
    let pyodideScriptPromise;
    let prettyPrintTransformPromise;
    let htmlXsltPromise;
    let latestXmlRaw = '';
    let latestXmlPretty = '';
    let activeTab = 'xml';
    const domParser = new DOMParser();
    const xmlSerializer = new XMLSerializer();
    let lawWidgetsPromise;

    function setStatus(message, tone = 'info') {
      statusEl.textContent = message;
      statusEl.dataset.tone = tone;
    }

    function ensurePyodideScript() {
      if (window.loadPyodide) {
        return Promise.resolve();
      }
      if (!pyodideScriptPromise) {
        pyodideScriptPromise = new Promise((resolve, reject) => {
          const script = document.createElement('script');
          script.src = 'https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js';
          script.onload = () => resolve();
          script.onerror = () => reject(new Error('Failed to load Pyodide.'));
          document.head.appendChild(script);
        });
      }
      return pyodideScriptPromise;
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
          htmlContainer.textContent = 'No XML available yet.';
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
          htmlContainer.textContent = `Failed to render HTML: ${err.message}`;
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
        setStatus('Initializing parser (downloading Pyodide)…', 'info');
        await ensurePyodideScript();
        const pyodide = await loadPyodide();
        setStatus('Installing Bluebell dependencies…', 'info');
        await pyodide.loadPackage('micropip');
        const micropip = pyodide.pyimport('micropip');
        await micropip.install('cobalt');
        await micropip.install('bluebell-akn');
        micropip.destroy();

        const setupScript = `
from bluebell.parser import AkomaNtosoParser, ParseError
from cobalt import FrbrUri
from lxml import etree

def parse_bluebell_text(text, frbr_uri):
    frbr_uri = FrbrUri.parse(frbr_uri)
    frbr_uri.work_component = 'main'
    root = frbr_uri.doctype
    try:
        parser = AkomaNtosoParser(frbr_uri)
        xml = parser.parse_to_xml(text, root)
    except ParseError as e:
        return {"error": True, "result": str(e)}
    xml = etree.tostring(xml, encoding='unicode')
    return {"error": False, "result": xml}
`;
        await pyodide.runPythonAsync(setupScript);
        parseFn = pyodide.globals.get('parse_bluebell_text');
        setStatus('Parser ready. Edit the text to see updates.', 'success');
        return pyodide;
      })();

      return parserReadyPromise;
    }

    async function updateOutput() {
      const text = input.value;
      try {
        await initParser();
        setStatus('Parsing…', 'info');
        const pyResult = parseFn(text, FRBR_URI);
        const result = pyResult.toJs({ create_proxies: false });
        pyResult.destroy();
        if (result.error) {
          setStatus('Parse error. See details below.', 'error');
          clearOutput(result.result);
        } else {
          setStatus('Parsed successfully.', 'success');
          latestXmlRaw = result.result;
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
        }
      } catch (err) {
        console.error(err);
        setStatus(`Failed to initialise parser: ${err.message}`, 'error');
        clearOutput(`<!-- Failed to parse: ${err.message} -->`);
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
