(function () {
  const input = document.getElementById('demo-input');
  const output = document.getElementById('demo-output');
  const statusEl = document.getElementById('demo-status');
  const downloadBtn = document.getElementById('demo-download');
  if (!input || !output || !statusEl || !downloadBtn) {
    return;
  }

  const FRBR_URI = '/akn/za/act/2026/1';
  let parserReadyPromise;
  let parseFn;
  let pyodideScriptPromise;
  let prettyPrintXml;

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
      const pyodide = await initParser();
      setStatus('Parsing…', 'info');
      const pyResult = parseFn(text, FRBR_URI);
      const result = pyResult.toJs({ create_proxies: false });
      pyResult.destroy();
      if (result.error) {
        setStatus('Parse error. See details below.', 'error');
        output.textContent = result.result;
        downloadBtn.disabled = true;
      } else {
        setStatus('Parsed successfully.', 'success');
        const formatted = prettyPrintXml
          ? prettyPrintXml(result.result)
          : result.result;
        output.textContent = formatted;
        downloadBtn.disabled = false;
        downloadBtn.dataset.xml = result.result;
      }
    } catch (err) {
      console.error(err);
      setStatus(`Failed to initialise parser: ${err.message}`, 'error');
      output.textContent = `<!-- Failed to parse: ${err.message} -->`;
    }
  }

  input.addEventListener('input', () => {
    void updateOutput();
  });

  void updateOutput();

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

  // Pretty printer setup (runs immediately)
  (function initPrettyPrinter() {
    const xsltSource = [
      '<?xml version="1.0"?>',
      '<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"',
      '  xmlns:a="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">',
      '  <xsl:output method="xml" indent="no" encoding="UTF-8"/>',
      '  <xsl:strip-space elements="*"/>',
      '  <xsl:preserve-space elements="a:a a:affectedDocument a:b a:block a:caption a:change a:concept a:courtType a:date a:def a:del a:docCommittee a:docDate a:docIntroducer a:docJurisdiction a:docNumber a:docProponent a:docPurpose a:docStage a:docStatus a:docTitle a:docType a:docketNumber a:entity a:event a:extractText a:fillIn a:from a:heading a:i a:inline a:ins a:judge a:lawyer a:legislature a:li a:listConclusion a:listIntroduction a:location a:mmod a:mod a:mref a:narrative a:neutralCitation a:num a:object a:omissis a:opinion a:organization a:outcome a:p a:party a:person a:placeholder a:process a:quantity a:quotedText a:recordedTime a:ref a:relatedDocument a:remark a:rmod a:role a:rref a:scene a:session a:shortTitle a:signature a:span a:sub a:subheading a:summary a:sup a:term a:tocItem a:u a:vote"/>',
      '  <xsl:template match="a:a|a:affectedDocument|a:b|a:block|a:caption|a:change|a:concept|a:courtType|a:date|a:def|a:del|a:docCommittee|a:docDate|a:docIntroducer|a:docJurisdiction|a:docNumber|a:docProponent|a:docPurpose|a:docStage|a:docStatus|a:docTitle|a:docType|a:docketNumber|a:entity|a:event|a:extractText|a:fillIn|a:from|a:heading|a:i|a:inline|a:ins|a:judge|a:lawyer|a:legislature|a:li|a:listConclusion|a:listIntroduction|a:location|a:mmod|a:mod|a:mref|a:narrative|a:neutralCitation|a:num|a:object|a:omissis|a:opinion|a:organization|a:outcome|a:p|a:party|a:person|a:placeholder|a:process|a:quantity|a:quotedText|a:recordedTime|a:ref|a:relatedDocument|a:remark|a:rmod|a:role|a:rref|a:scene|a:session|a:shortTitle|a:signature|a:span|a:sub|a:subheading|a:summary|a:sup|a:term|a:tocItem|a:u|a:vote">',
      '    <xsl:param name="depth">0</xsl:param>',
      '    <xsl:text>&#xA;</xsl:text>',
      '    <xsl:call-template name="indent">',
      '      <xsl:with-param name="depth" select="$depth"/>',
      '    </xsl:call-template>',
      '    <xsl:copy-of select="." />',
      '  </xsl:template>',
      '  <xsl:template match="*|comment()">',
      '    <xsl:param name="depth">0</xsl:param>',
      '    <xsl:if test="$depth &gt; 0">',
      '      <xsl:text>&#xA;</xsl:text>',
      '    </xsl:if>',
      '    <xsl:call-template name="indent">',
      '      <xsl:with-param name="depth" select="$depth"/>',
      '    </xsl:call-template>',
      '    <xsl:copy>',
      '      <xsl:if test="self::*">',
      '        <xsl:copy-of select="@*"/>',
      '        <xsl:apply-templates>',
      '          <xsl:with-param name="depth" select="$depth + 1"/>',
      '        </xsl:apply-templates>',
      '        <xsl:if test="count(*) &gt; 0">',
      '          <xsl:text>&#xA;</xsl:text>',
      '          <xsl:call-template name="indent">',
      '            <xsl:with-param name="depth" select="$depth"/>',
      '          </xsl:call-template>',
      '        </xsl:if>',
      '      </xsl:if>',
      '    </xsl:copy>',
      '    <xsl:variable name="isLastNode" select="count(../..) = 0 and position() = last()"/>',
      '    <xsl:if test="$isLastNode">',
      '      <xsl:text>&#xA;</xsl:text>',
      '    </xsl:if>',
      '  </xsl:template>',
      '  <xsl:template name="indent">',
      '    <xsl:param name="depth"/>',
      '    <xsl:if test="$depth &gt; 0">',
      '      <xsl:text>  </xsl:text>',
      '      <xsl:call-template name="indent">',
      '        <xsl:with-param name="depth" select="$depth - 1"/>',
      '      </xsl:call-template>',
      '    </xsl:if>',
      '  </xsl:template>',
      '</xsl:stylesheet>',
    ].join('');

    try {
      const parser = new DOMParser();
      const xsltDoc = parser.parseFromString(xsltSource, 'application/xml');
      const transform = new XSLTProcessor();
      transform.importStylesheet(xsltDoc);
      const serializer = new XMLSerializer();

      prettyPrintXml = function prettyPrintXml(xml) {
        const sourceDoc =
          typeof xml === 'string'
            ? parser.parseFromString(xml, 'application/xml')
            : xml;
        const resultDoc = transform.transformToDocument(sourceDoc);
        return serializer.serializeToString(resultDoc);
      };
    } catch (err) {
      console.warn('Failed to initialise pretty printer', err);
      prettyPrintXml = null;
    }
  })();
})();
