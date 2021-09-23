<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:a="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"
                exclude-result-prefixes="a">

  <xsl:output method="xml" encoding="utf8" />

  <!-- unwrap hcontainers -->
  <!-- TODO: do this only when the hcontainer is the only "content" in a hier elem -->
  <xsl:template match="a:part/a:hcontainer | a:section/a:hcontainer | a:article/a:hcontainer
                       | a:chapter/a:hocntainer | a:subsection/a:hcontainer">
    <xsl:apply-templates select="a:content" />
  </xsl:template>

  <!-- old-style fake crossheadings -->
  <xsl:template match="a:hcontainer[@name='crossheading']">
    <a:crossHeading>
      <xsl:apply-templates select="a:heading/* | a:heading/text()" />
    </a:crossHeading>
  </xsl:template>

  <xsl:template match="*">
    <xsl:copy>
      <xsl:copy-of select="@*" />
      <xsl:apply-templates />
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>
