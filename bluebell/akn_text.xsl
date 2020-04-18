<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:a="http://www.akomantoso.org/2.0"
  exclude-result-prefixes="a">

  <xsl:output method="text" indent="no" omit-xml-declaration="yes" />

  <!-- strip whitespace from most elements, but preserve whitespace in inline elements that can contain text -->
  <xsl:strip-space elements="*"/>
  <xsl:preserve-space elements="a:a a:affectedDocument a:b a:block a:caption a:change a:concept a:courtType a:date a:def a:del a:docCommittee a:docDate a:docIntroducer a:docJurisdiction a:docNumber a:docProponent a:docPurpose a:docStage a:docStatus a:docTitle a:docType a:docketNumber a:entity a:event a:extractText a:fillIn a:from a:heading a:i a:inline a:ins a:judge a:lawyer a:legislature a:li a:listConclusion a:listIntroduction a:location a:mmod a:mod a:mref a:narrative a:neutralCitation a:num a:object a:omissis a:opinion a:organization a:outcome a:p a:party a:person a:placeholder a:process a:quantity a:quotedText a:recordedTime a:ref a:relatedDocument a:remark a:rmod a:role a:rref a:scene a:session a:shortTitle a:signature a:span a:sub a:subheading a:summary a:sup a:term a:tocItem a:u a:vote"/>

  <!-- adds a backslash to the start of the value param, if necessary -->
  <xsl:template name="escape">
    <xsl:param name="value"/>

    <xsl:variable name="prefix" select="translate(substring($value, 1, 13), 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')" />
    <!-- '(' is considered special, so translate numbers into '(' so we can find and escape them -->
    <xsl:variable name="numprefix" select="translate(substring($value, 1, 3), '1234567890', '((((((((((')" />

    <!-- p tags must escape initial content that looks like a block element marker -->
    <xsl:if test="$prefix = 'BODY' or
                  $prefix = 'PREAMBLE' or
                  $prefix = 'PREFACE' or
                  starts-with($prefix, 'CHAPTER ') or
                  starts-with($prefix, 'PART ') or
                  starts-with($prefix, 'SUBPART ') or
                  starts-with($prefix, 'PARA ') or
                  starts-with($prefix, 'ARTICLE ') or
                  starts-with($prefix, 'SCHEDULE ') or
                  starts-with($prefix, 'HEADING ') or
                  starts-with($prefix, 'SUBHEADING ') or
                  starts-with($prefix, 'LONGTITLE ') or
                  starts-with($prefix, 'CROSSHEADING ') or
                  starts-with($prefix, '{|') or
                  starts-with($numprefix, '(')">
      <xsl:text>\</xsl:text>
    </xsl:if>
    <xsl:value-of select="$value"/>
  </xsl:template>

  <!-- repeats a character a certain number of times -->
  <xsl:template name="repeat">
    <xsl:param name="str" />
    <xsl:param name="count" />

    <xsl:if test="$count &gt; 0">
      <xsl:value-of select="$str" />
      <xsl:call-template name="repeat">
        <xsl:with-param name="str" select="$str" />
        <xsl:with-param name="count" select="$count - 1" />
      </xsl:call-template>
    </xsl:if>
  </xsl:template>

  <!-- indent with spaces -->
  <xsl:template name="indent">
    <xsl:param name="level" />

    <xsl:call-template name="repeat">
      <xsl:with-param name="str" select="'    '" />
      <xsl:with-param name="count" select="$level" />
    </xsl:call-template>
  </xsl:template>


  <xsl:template match="a:act">
    <xsl:apply-templates select="a:coverPage" />
    <xsl:apply-templates select="a:preface" />
    <xsl:apply-templates select="a:preamble" />
    <xsl:apply-templates select="a:body" />
    <xsl:apply-templates select="a:conclusions" />
  </xsl:template>

  <xsl:template match="a:preface">
    <xsl:text>PREFACE</xsl:text>
    <xsl:text>&#10;&#10;</xsl:text>

    <xsl:apply-templates />
  </xsl:template>

  <xsl:template match="a:preamble">
    <xsl:text>PREAMBLE</xsl:text>
    <xsl:text>&#10;&#10;</xsl:text>

    <xsl:apply-templates />
  </xsl:template>

  <xsl:template match="a:body">
    <xsl:text>BODY</xsl:text>
    <xsl:text>&#10;&#10;</xsl:text>

    <xsl:apply-templates />
  </xsl:template>

  <xsl:template match="a:part">
    <xsl:text>Part </xsl:text>
    <xsl:value-of select="a:num" />
    <xsl:text> - </xsl:text>
    <xsl:apply-templates select="a:heading" />
    <xsl:text>&#10;&#10;</xsl:text>

    <xsl:apply-templates select="./*[not(self::a:num) and not(self::a:heading)]" />
  </xsl:template>

  <xsl:template match="a:subpart">
    <xsl:text>SUBPART </xsl:text>
    <xsl:value-of select="a:num" />
    <xsl:text> - </xsl:text>
    <xsl:apply-templates select="a:heading" />
    <xsl:text>&#10;&#10;</xsl:text>

    <xsl:apply-templates select="./*[not(self::a:num) and not(self::a:heading)]" />
  </xsl:template>

  <xsl:template match="a:chapter">
    <xsl:text>Chapter </xsl:text>
    <xsl:value-of select="a:num" />
    <xsl:text> - </xsl:text>
    <xsl:apply-templates select="a:heading" />
    <xsl:text>&#10;&#10;</xsl:text>

    <xsl:apply-templates select="./*[not(self::a:num) and not(self::a:heading)]" />
  </xsl:template>

  <xsl:template match="a:article">
    <xsl:text>Article </xsl:text>
    <xsl:value-of select="a:num" />
    <xsl:if test="a:heading">
      <xsl:text> - </xsl:text>
      <xsl:apply-templates select="a:heading" />
    </xsl:if>
    <xsl:text>&#10;&#10;</xsl:text>
    <xsl:apply-templates select="./*[not(self::a:num) and not(self::a:heading)]" />
  </xsl:template>

  <xsl:template match="a:paragraph">
    <xsl:if test="a:num != ''">
      <!-- paragraphs in articles that look like (a) don't need to be prefixed with PARA -->
      <xsl:if test="not(parent::a:article) or not(starts-with(a:num, '(')) or substring(a:num, string-length(a:num)) != ')'">
        <xsl:text>PARA </xsl:text>
      </xsl:if>
      <xsl:value-of select="a:num" />
      <xsl:text> </xsl:text>
    </xsl:if>

    <xsl:apply-templates select="./*[not(self::a:num)]" />
  </xsl:template>

  <xsl:template match="a:section">
    <xsl:value-of select="a:num" />
    <xsl:text> </xsl:text>
    <xsl:apply-templates select="a:heading" />
    <xsl:text>&#10;&#10;</xsl:text>

    <xsl:apply-templates select="./*[not(self::a:num) and not(self::a:heading)]" />
  </xsl:template>

  <xsl:template match="a:subsection">
    <xsl:if test="a:num != ''">
      <xsl:value-of select="a:num" />
      <xsl:text> </xsl:text>
    </xsl:if>

    <xsl:apply-templates select="./*[not(self::a:num) and not(self::a:heading)]" />
  </xsl:template>

  <!-- crossheadings -->
  <xsl:template match="a:hcontainer[@name='crossheading']">
    <xsl:text>CROSSHEADING </xsl:text>
    <xsl:apply-templates select="a:heading" />
    <xsl:text>&#10;&#10;</xsl:text>
  </xsl:template>

  <!-- longtitle -->
  <xsl:template match="a:longTitle">
    <xsl:text>LONGTITLE </xsl:text>
    <xsl:apply-templates />
    <xsl:text>&#10;&#10;</xsl:text>
  </xsl:template>

  <!-- p tags must end with a blank line -->
  <xsl:template match="a:p">
    <xsl:apply-templates/>
    <xsl:text>&#10;&#10;</xsl:text>
  </xsl:template>


  <!-- indented blocklists -->
  <xsl:template match="a:blockList">
    <xsl:param name="indent">1</xsl:param>

    <xsl:if test="not(a:listIntroduction)">
      <xsl:text>&#10;&#10;</xsl:text>
    </xsl:if>

    <xsl:apply-templates>
      <xsl:with-param name="indent" select="$indent" />
    </xsl:apply-templates>
  </xsl:template>

  <xsl:template match="a:item">
    <xsl:param name="indent">0</xsl:param>

    <xsl:call-template name="indent">
      <xsl:with-param name="level" select="$indent" />
    </xsl:call-template>

    <xsl:value-of select="a:num" />
    <xsl:text> </xsl:text>
    <xsl:apply-templates select="./*[not(self::a:num)]">
      <xsl:with-param name="indent" select="$indent+1" />
    </xsl:apply-templates>
  </xsl:template>

  <xsl:template match="a:listIntroduction">
    <xsl:param name="indent">0</xsl:param>

    <!--
      Only indent the listIntroduction text if:

      1. our parent blockList is NOT immediately preceded by a:num, AND
      2. our parent blockList is the first child AND its parent is immediately preceded by a:num

      In both cases, the list intro is preceded by a num and the text should appear on the same line.
    -->

    <xsl:variable name="parentpos" select="count(../preceding-sibling::*) + 1"/>
    <xsl:if test="not(../preceding-sibling::*[1][self::a:num]) and not($parentpos = 1 and ../../preceding-sibling::*[1][self::a:num])">
      <xsl:call-template name="indent">
        <xsl:with-param name="level" select="$indent" />
      </xsl:call-template>
    </xsl:if>

    <xsl:apply-templates>
      <xsl:with-param name="indent" select="$indent" />
    </xsl:apply-templates>

    <xsl:text>&#10;&#10;</xsl:text>
  </xsl:template>

  <xsl:template match="a:item/a:p | a:td/a:p | a:th/a:p">
    <xsl:param name="indent">0</xsl:param>

    <!-- don't indent the first p tag -->
    <xsl:if test="position() &gt; 1">
      <xsl:call-template name="indent">
        <xsl:with-param name="level" select="$indent" />
      </xsl:call-template>
    </xsl:if>

    <xsl:apply-templates>
      <xsl:with-param name="indent" select="$indent" />
    </xsl:apply-templates>

    <xsl:if test="not(parent::a:th) and not(parent::a:td)">
      <xsl:text>&#10;&#10;</xsl:text>
    </xsl:if>
  </xsl:template>

  <xsl:template match="a:list">
    <xsl:if test="a:intro != ''">
      <xsl:apply-templates select="a:intro" />
      <xsl:text>&#10;&#10;</xsl:text>
    </xsl:if>
    <xsl:apply-templates select="./*[not(self::a:intro)]" />
  </xsl:template>

  <!-- first text nodes of these elems must be escaped if they have special chars -->
  <xsl:template match="a:p[not(ancestor::a:table)]/text()[not(preceding-sibling::*)] | a:listIntroduction/text()[not(preceding-sibling::*)] | a:intro/text()[not(preceding-sibling::*)]">
    <xsl:call-template name="escape">
      <xsl:with-param name="value" select="." />
    </xsl:call-template>
  </xsl:template>


  <!-- components/schedules -->
  <!-- new-style schedules, "hcontainer" elements -->
  <xsl:template match="a:hcontainer[@name='schedule']">
    <xsl:text>SCHEDULE&#10;HEADING </xsl:text>
    <xsl:apply-templates select="a:heading" />
    <xsl:text>&#10;</xsl:text>

    <xsl:if test="a:subheading">
      <xsl:text>SUBHEADING </xsl:text>
      <xsl:apply-templates select="a:subheading" />
      <xsl:text>&#10;</xsl:text>
    </xsl:if>

    <xsl:text>&#10;&#10;</xsl:text>
    <xsl:apply-templates select="./*[not(self::a:heading) and not(self::a:subheading)]" />
  </xsl:template>


  <!-- old-style schedules, "article" elements -->
  <xsl:template match="a:doc/a:mainBody/a:article">
    <xsl:text>SCHEDULE&#10;HEADING </xsl:text>
    <xsl:value-of select="../../a:meta/a:identification/a:FRBRWork/a:FRBRalias/@value" />
    <xsl:text>&#10;</xsl:text>

    <xsl:if test="a:heading">
      <xsl:text>SUBHEADING </xsl:text>
      <xsl:apply-templates select="a:heading" />
      <xsl:text>&#10;</xsl:text>
    </xsl:if>

    <xsl:text>&#10;</xsl:text>
    <xsl:apply-templates select="./*[not(self::a:heading)]"/>
  </xsl:template>


  <!-- tables -->
  <xsl:template match="a:table">
    <xsl:param name="indent">0</xsl:param>

    <xsl:call-template name="indent">
      <xsl:with-param name="level" select="$indent" />
    </xsl:call-template>
    <xsl:text>{| </xsl:text>

    <!-- attributes -->
    <xsl:for-each select="@*[local-name()!='id']">
      <xsl:value-of select="local-name(.)" />
      <xsl:text>="</xsl:text>
      <xsl:value-of select="." />
      <xsl:text>" </xsl:text>
    </xsl:for-each>

    <xsl:text>&#10;</xsl:text>
    <xsl:call-template name="indent">
      <xsl:with-param name="level" select="$indent" />
    </xsl:call-template>
    <xsl:text>|-</xsl:text>

    <!-- table rows -->
    <xsl:apply-templates>
      <xsl:with-param name="indent" select="$indent" />
    </xsl:apply-templates>

    <xsl:text>&#10;</xsl:text>
    <xsl:call-template name="indent">
      <xsl:with-param name="level" select="$indent" />
    </xsl:call-template>
    <xsl:text>|}&#10;&#10;</xsl:text>
  </xsl:template>

  <xsl:template match="a:tr">
    <xsl:param name="indent">0</xsl:param>

    <xsl:apply-templates>
      <xsl:with-param name="indent" select="$indent" />
    </xsl:apply-templates>

    <xsl:text>&#10;</xsl:text>
    <xsl:call-template name="indent">
      <xsl:with-param name="level" select="$indent" />
    </xsl:call-template>
    <xsl:text>|-</xsl:text>
  </xsl:template>

  <xsl:template match="a:th|a:td">
    <xsl:param name="indent">0</xsl:param>

    <xsl:text>&#10;</xsl:text>
    <xsl:call-template name="indent">
      <xsl:with-param name="level" select="$indent" />
    </xsl:call-template>

    <xsl:choose>
      <xsl:when test="local-name(.) = 'th'">
        <xsl:text>! </xsl:text>
      </xsl:when>
      <xsl:when test="local-name(.) = 'td'">
        <xsl:text>| </xsl:text>
      </xsl:when>
    </xsl:choose>

    <!-- attributes -->
    <xsl:if test="@*">
      <xsl:for-each select="@*">
        <xsl:value-of select="local-name(.)" />
        <xsl:text>="</xsl:text>
        <xsl:value-of select="." />
        <xsl:text>" </xsl:text>
      </xsl:for-each>
      <xsl:text>| </xsl:text>
    </xsl:if>

    <xsl:apply-templates>
      <xsl:with-param name="indent" select="$indent" />
    </xsl:apply-templates>
  </xsl:template>

  <!-- END tables -->

  <xsl:template match="a:remark">
    <xsl:text>[</xsl:text>
    <xsl:apply-templates />
    <xsl:text>]</xsl:text>
  </xsl:template>

  <xsl:template match="a:ref">
    <xsl:text>[</xsl:text>
    <xsl:apply-templates />
    <xsl:text>](</xsl:text>
    <xsl:value-of select="@href" />
    <xsl:text>)</xsl:text>
  </xsl:template>

  <xsl:template match="a:img">
    <xsl:text>![</xsl:text>
    <xsl:value-of select="@alt" />
    <xsl:text>](</xsl:text>
    <xsl:value-of select="@src" />
    <xsl:text>)</xsl:text>
  </xsl:template>

  <xsl:template match="a:i">
    <xsl:text>//</xsl:text>
    <xsl:apply-templates />
    <xsl:text>//</xsl:text>
  </xsl:template>

  <xsl:template match="a:b">
    <xsl:text>**</xsl:text>
    <xsl:apply-templates />
    <xsl:text>**</xsl:text>
  </xsl:template>

  <xsl:template match="a:eol">
    <xsl:param name="indent">0</xsl:param>

    <xsl:text>&#10;</xsl:text>

    <xsl:call-template name="indent">
      <xsl:with-param name="level" select="$indent" />
    </xsl:call-template>
  </xsl:template>


  <!-- for most nodes, just dump their text content -->
  <xsl:template match="*">
    <xsl:apply-templates />
  </xsl:template>

</xsl:stylesheet>
