<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:a="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"
                exclude-result-prefixes="a">

  <xsl:output method="xml" encoding="utf8" />

  <!-- unwrap hcontainers -->
  <xsl:template match="a:*[self::a:part or self::a:section or self::a:article or self::a:chapter or self::a:subsection
                           or self::a:subpart or self::a:division]/a:hcontainer[@name='hcontainer']">
    <xsl:choose>
      <!-- strip hcontainer completely when it's the only content element in a hier element -->
      <xsl:when test="preceding-sibling::*[1][self::a:num or self::a:heading or self::a:subheading] and not(following-sibling::*)">
        <xsl:apply-templates select="a:content" />
      </xsl:when>

      <!-- change hcontainer into intro when it's the first content element in a hier element -->
      <xsl:when test="preceding-sibling::*[1][self::a:num or self::a:heading or self::a:subheading] and following-sibling::*">
        <a:intro>
          <xsl:apply-templates select="a:content/*" />
        </a:intro>
      </xsl:when>

      <!-- change hcontainer into wrapUp when it's the last content element in a hier element -->
      <xsl:when test="not(preceding-sibling::*[1][self::a:num or self::a:heading or self::a:subheading]) and not(following-sibling::*)">
        <a:wrapUp>
          <xsl:apply-templates select="a:content/*" />
        </a:wrapUp>
      </xsl:when>

      <!-- keep it -->
      <xsl:otherwise>
        <xsl:apply-templates />
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>
