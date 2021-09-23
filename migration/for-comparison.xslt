<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:a="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"
                exclude-result-prefixes="a">

  <xsl:output method="xml" encoding="utf8" />

  <xsl:template match="*">
    <xsl:copy>
      <!-- skip eIds -->
      <xsl:copy-of select="@*[not(local-name(.) = 'eId')]" />

      <xsl:apply-templates />
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>
