<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:a="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"
                exclude-result-prefixes="a">

  <xsl:output method="xml" encoding="utf8" />

  <!-- unwrap hcontainers, but only when it is the only "content" in a hier elem -->
  <xsl:template match="a:*[self::a:part or self::a:section or self::a:article or self::a:chapter or self::a:subsection
                           or self::a:subpart or self::a:division]
                           /a:hcontainer[
                             @name='hcontainer'
                             and preceding-sibling::*[1][self::a:num or self::a:heading or self::a:subheading]
                             and not(following-sibling::*)
                           ]">
    <xsl:apply-templates select="a:content" />
  </xsl:template>

  <xsl:template match="*">
    <xsl:copy>
      <xsl:copy-of select="@*" />
      <xsl:apply-templates />
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>
