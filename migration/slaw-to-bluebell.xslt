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

  <!-- ensure FRBRalias has name="title" -->
  <xsl:template match="a:FRBRalias[not(@name)]">
    <xsl:copy>
      <xsl:attribute name="name">title</xsl:attribute>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <!-- change source="#slaw" to source="#cobalt" -->
  <xsl:template match="a:*/@source[. = '#slaw']">
    <xsl:attribute name="source">#cobalt</xsl:attribute>
  </xsl:template>

  <!-- ensure <references> has a cobalt entry -->
  <xsl:template match="a:references[not(./a:TLCOrganization[@eId='cobalt'])]">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
      <a:TLCOrganization href="https://github.com/laws-africa/cobalt" showAs="cobalt"/>
    </xsl:copy>
  </xsl:template>

  <!-- remove slaw -->
  <xsl:template match="a:TLCOrganization[@eId='slaw']" />

  <!-- clear out FRBRAuthor -->
  <xsl:template match="a:FRBRauthor/@href[. != '']">
    <xsl:attribute name="href"></xsl:attribute>
  </xsl:template>

  <!-- ensure act[@contains="singleVersion"] or act[@contains="originalVersion"] -->
  <xsl:template match="a:*[self::a:act or self::a:doc][not(@contains)]">
    <xsl:copy>
      <xsl:choose>
        <xsl:when test="a:meta/a:lifecycle/a:eventRef[@name='amendment']">
          <xsl:attribute name="contains">singleVersion</xsl:attribute>
        </xsl:when>
        <xsl:otherwise>
          <xsl:attribute name="contains">originalVersion</xsl:attribute>
        </xsl:otherwise>
      </xsl:choose>

      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>
