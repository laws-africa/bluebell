<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:a="http://docs.oasis-open.org/legaldocml/ns/akn/3.0"
                exclude-result-prefixes="a">

  <xsl:output method="text" indent="no" omit-xml-declaration="yes" />
  <xsl:param name="indentStr" select="'  '"/>

  <!-- strip whitespace from most elements, but preserve whitespace in inline elements that can contain text -->
  <xsl:strip-space elements="*"/>
  <xsl:preserve-space elements="a:a a:affectedDocument a:b a:block a:caption a:change a:concept a:courtType a:date a:def
                                a:del a:docCommittee a:docDate a:docIntroducer a:docJurisdiction a:docNumber a:docProponent
                                a:docPurpose a:docStage a:docStatus a:docTitle a:docType a:docketNumber a:entity a:event
                                a:extractText a:fillIn a:from a:heading a:i a:inline a:ins a:judge a:lawyer a:legislature
                                a:listConclusion a:listIntroduction a:location a:mmod a:mod a:mref a:narrative
                                a:neutralCitation a:num a:object a:omissis a:opinion a:organization a:outcome a:p
                                a:party a:person a:placeholder a:process a:quantity a:quotedText a:recordedTime a:ref
                                a:relatedDocument a:remark a:rmod a:role a:rref a:scene a:session a:shortTitle a:signature
                                a:span a:sub a:subheading a:summary a:sup a:term a:tocItem a:u a:vote"/>

  <!-- ...............................................................................
       Functions / helper templates
       ............................................................................... -->

  <!-- trims whitespace from the left of a string -->
  <xsl:template name="string-ltrim">
    <xsl:param name="text" />
    <xsl:param name="trim" select="'&#09;&#10;&#13; '" />

    <xsl:if test="string-length($text) &gt; 0">
      <xsl:choose>
        <xsl:when test="contains($trim, substring($text, 1, 1))">
          <xsl:call-template name="string-ltrim">
            <xsl:with-param name="text" select="substring($text, 2)" />
            <xsl:with-param name="trim" select="$trim" />
          </xsl:call-template>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="$text" />
        </xsl:otherwise>
      </xsl:choose>
    </xsl:if>
  </xsl:template>

  <!-- replaces "value" in "text" with "replacement" -->
  <xsl:template name="string-replace-all">
    <xsl:param name="text" />
    <xsl:param name="value" />
    <xsl:param name="replacement" />

    <xsl:choose>
      <xsl:when test="$text = '' or $value = '' or not($value)">
        <xsl:value-of select="$text" />
      </xsl:when>
      <xsl:when test="contains($text, $value)">
        <xsl:value-of select="substring-before($text, $value)"/>
        <xsl:value-of select="$replacement" />
        <xsl:call-template name="string-replace-all">
          <xsl:with-param name="text" select="substring-after($text, $value)" />
          <xsl:with-param name="value" select="$value" />
          <xsl:with-param name="replacement" select="$replacement" />
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$text" />
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- the run of the same char at the start of the string -->
  <xsl:template name="prefix-run">
    <xsl:param name="text" />
    <xsl:param name="ch" select="substring($text, 1, 1)" />

    <xsl:if test="substring($text, 1, 1) = $ch">
      <xsl:value-of select="$ch" />
      <xsl:call-template name="prefix-run">
        <xsl:with-param name="text" select="substring($text, 2)" />
        <xsl:with-param name="ch" select="$ch" />
      </xsl:call-template>
    </xsl:if>
  </xsl:template>

  <!-- the run of chars at the end of the string -->
  <xsl:template name="suffix-run">
    <xsl:param name="text" />
    <xsl:param name="ch" select="substring($text, string-length($text))" />

    <xsl:if test="substring($text, string-length($text)) = $ch">
      <xsl:value-of select="$ch" />
      <xsl:call-template name="suffix-run">
        <xsl:with-param name="text" select="substring($text, 1, string-length($text) - 1)" />
        <xsl:with-param name="ch" select="$ch" />
      </xsl:call-template>
    </xsl:if>
  </xsl:template>

  <!-- Escape inline markers with a backslash -->
  <xsl:template name="escape-inlines">
    <xsl:param name="text" />

    <!-- This works from the inside out, first escaping backslash chars themselves, then escaping
         the different types of inline markers -->
    <xsl:call-template name="string-replace-all">
      <xsl:with-param name="text">
        <xsl:call-template name="string-replace-all">
          <xsl:with-param name="text">
            <xsl:call-template name="string-replace-all">
              <xsl:with-param name="text">
                <xsl:call-template name="string-replace-all">
                  <xsl:with-param name="text">
                    <xsl:call-template name="string-replace-all">
                      <xsl:with-param name="text">
                        <xsl:call-template name="string-replace-all">
                          <!-- replace newlines with spaces -->
                          <xsl:with-param name="text" select="translate($text, '&#13;&#10;', '  ')" />
                          <xsl:with-param name="value"><xsl:value-of select="'\'" /></xsl:with-param>
                          <xsl:with-param name="replacement"><xsl:value-of select="'\\'" /></xsl:with-param>
                        </xsl:call-template>
                      </xsl:with-param>
                      <xsl:with-param name="value"><xsl:value-of select="'**'" /></xsl:with-param>
                      <xsl:with-param name="replacement"><xsl:value-of select="'\*\*'" /></xsl:with-param>
                    </xsl:call-template>
                  </xsl:with-param>
                  <xsl:with-param name="value"><xsl:value-of select="'//'" /></xsl:with-param>
                  <xsl:with-param name="replacement"><xsl:value-of select="'\/\/'" /></xsl:with-param>
                </xsl:call-template>
              </xsl:with-param>
              <xsl:with-param name="value"><xsl:value-of select="'__'" /></xsl:with-param>
              <xsl:with-param name="replacement"><xsl:value-of select="'\_\_'" /></xsl:with-param>
            </xsl:call-template>
          </xsl:with-param>
          <xsl:with-param name="value"><xsl:value-of select="'{{'" /></xsl:with-param>
          <xsl:with-param name="replacement"><xsl:value-of select="'\{\{'" /></xsl:with-param>
        </xsl:call-template>
      </xsl:with-param>
      <xsl:with-param name="value"><xsl:value-of select="'}}'" /></xsl:with-param>
      <xsl:with-param name="replacement"><xsl:value-of select="'\}\}'" /></xsl:with-param>
    </xsl:call-template>
  </xsl:template>

  <!-- escape inlines, but also escape special chars when they are adjacent to the start or end of their inlines.
    - stars and b tags
    - slashes and i tags
    - undescores and u tags

    We need to determine whether we escape the run of special chars at the start (prefix) or end (suffix) of the
    given string. Either way, we only escape the last char of the run, and only if the run is an odd length. This is
    because the general inline-escaping code will escape the double chars, starting on the left of the string.

    Examples:

    <b>***     - escape prefix
    <b>***foo  - escape prefix
    </b>***    - escape prefix

    ***<b>     - escape suffix
    foo***</b> - escape suffix

    <b>***</b> - either (but not both)
    -->
  <xsl:template name="escape-inlines-start-end">
    <xsl:param name="text" />

    <!-- the run of the same char at the start of the string -->
    <xsl:variable name="prefix-run">
      <xsl:call-template name="prefix-run">
        <xsl:with-param name="text" select="$text" />
      </xsl:call-template>
    </xsl:variable>

    <!-- the run of the same char at the end of the string -->
    <xsl:variable name="suffix-run">
      <xsl:call-template name="suffix-run">
        <xsl:with-param name="text" select="$text" />
      </xsl:call-template>
    </xsl:variable>

    <xsl:variable name="odd-prefix" select="string-length($prefix-run) mod 2 = 1" />
    <xsl:variable name="odd-suffix" select="string-length($suffix-run) mod 2 = 1" />

    <xsl:variable name="escape-prefix" select="
      (starts-with($text, '*') and $odd-prefix and (
        (parent::a:b and not(preceding-sibling::*)) or preceding-sibling::*[1][self::a:b]
      )) or
      (starts-with($text, '/') and $odd-prefix and (
        (parent::a:i and not(preceding-sibling::*)) or preceding-sibling::*[1][self::a:i]
      )) or
      (starts-with($text, '_') and $odd-prefix and (
        (parent::a:u and not(preceding-sibling::*)) or preceding-sibling::*[1][self::a:u]
      ))
    " />
    <xsl:variable name="escape-suffix" select="
      (substring($text, string-length($text)) = '*' and $odd-suffix and (
        (parent::a:b and not(following-sibling::*)) or following-sibling::*[1][self::a:b]
      )) or
      (substring($text, string-length($text)) = '/' and $odd-suffix and (
        (parent::a:i and not(following-sibling::*)) or following-sibling::*[1][self::a:i]
      )) or
      (substring($text, string-length($text)) = '_' and $odd-suffix and (
        (parent::a:u and not(following-sibling::*)) or following-sibling::*[1][self::a:u]
      ))
    " />

    <xsl:choose>
      <xsl:when test="$escape-prefix and $escape-suffix">
        <xsl:text>\</xsl:text>
        <xsl:value-of select="substring($text, 1, 1)" />
        <xsl:if test="string-length($text) > 1">
          <xsl:call-template name="escape-inlines">
            <xsl:with-param name="text" select="substring($text, 2, string-length($text) - 2)" />
          </xsl:call-template>
          <xsl:text>\</xsl:text>
          <xsl:value-of select="substring($text, string-length($text))" />
        </xsl:if>
      </xsl:when>
      <xsl:when test="$escape-prefix and not($escape-suffix)">
        <xsl:text>\</xsl:text>
        <xsl:value-of select="substring($text, 1, 1)" />
        <xsl:call-template name="escape-inlines">
          <xsl:with-param name="text" select="substring($text, 2)" />
        </xsl:call-template>
      </xsl:when>
      <xsl:when test="$escape-suffix and not($escape-prefix)">
        <xsl:call-template name="escape-inlines">
          <xsl:with-param name="text" select="substring($text, 1, string-length($text) - 1)" />
        </xsl:call-template>
        <xsl:text>\</xsl:text>
        <xsl:value-of select="substring($text, string-length($text))" />
      </xsl:when>
      <xsl:otherwise>
        <xsl:call-template name="escape-inlines">
          <xsl:with-param name="text" select="$text" />
        </xsl:call-template>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- Escape prefixes with a backslash -->
  <xsl:template name="escape-prefixes">
    <xsl:param name="text" />

    <xsl:variable name="slash">
      <!-- p tags must escape initial content that looks like a block element marker -->
      <xsl:if test="$text = 'ARGUMENTS' or
                    $text = 'BACKGROUND' or
                    $text = 'BODY' or
                    $text = 'CONCLUSIONS' or
                    $text = 'DECISION' or
                    $text = 'INTRODUCTION' or
                    $text = 'MOTIVATION' or
                    $text = 'PREAMBLE' or
                    $text = 'PREFACE' or
                    $text = 'REMEDIES' or
                    starts-with($text, 'ADDRESS') or
                    starts-with($text, 'ADJOURNMENT') or
                    starts-with($text, 'ADMINISTRATIONOFOATH') or
                    starts-with($text, 'ALINEA') or
                    starts-with($text, 'ANNEXURE') or
                    starts-with($text, 'ANSWER') or
                    starts-with($text, 'APPENDIX') or
                    starts-with($text, 'ART') or
                    starts-with($text, 'ARTICLE') or
                    starts-with($text, 'ATTACHMENT') or
                    starts-with($text, 'BLOCKLIST') or
                    starts-with($text, 'BOOK') or
                    starts-with($text, 'BULLETS') or
                    starts-with($text, 'CHAP') or
                    starts-with($text, 'CHAPTER') or
                    starts-with($text, 'CLAUSE') or
                    starts-with($text, 'COMMUNICATION') or
                    starts-with($text, 'CROSSHEADING') or
                    starts-with($text, 'DEBATESECTION') or
                    starts-with($text, 'DECLARATIONOFVOTE') or
                    starts-with($text, 'DIVISION') or
                    starts-with($text, 'FOOTNOTE') or
                    starts-with($text, 'FROM') or
                    starts-with($text, 'HEADING') or
                    starts-with($text, 'INDENT') or
                    starts-with($text, 'ITEMS') or
                    starts-with($text, 'LEVEL') or
                    starts-with($text, 'LIST') or
                    starts-with($text, 'LONGTITLE') or
                    starts-with($text, 'MINISTERIALSTATEMENTS') or
                    starts-with($text, 'NARRATIVE') or
                    starts-with($text, 'NATIONALINTEREST') or
                    starts-with($text, 'NOTICESOFMOTION') or
                    starts-with($text, 'ORALSTATEMENTS') or
                    starts-with($text, 'P ') or
                    starts-with($text, 'P.') or
                    starts-with($text, 'PAPERS') or
                    starts-with($text, 'PARA') or
                    starts-with($text, 'PARAGRAPH') or
                    starts-with($text, 'PART') or
                    starts-with($text, 'PERSONALSTATEMENTS') or
                    starts-with($text, 'PETITIONS') or
                    starts-with($text, 'POINT') or
                    starts-with($text, 'POINTOFORDER') or
                    starts-with($text, 'PRAYERS') or
                    starts-with($text, 'PROCEDURALMOTIONS') or
                    starts-with($text, 'PROVISO') or
                    starts-with($text, 'P{') or
                    starts-with($text, 'QUESTION') or
                    starts-with($text, 'QUESTIONS') or
                    starts-with($text, 'QUOTE') or
                    starts-with($text, 'RESOLUTIONS') or
                    starts-with($text, 'ROLLCALL') or
                    starts-with($text, 'RULE') or
                    starts-with($text, 'SCENE') or
                    starts-with($text, 'SCHEDULE') or
                    starts-with($text, 'SEC') or
                    starts-with($text, 'SECTION') or
                    starts-with($text, 'SPEECH') or
                    starts-with($text, 'SPEECHGROUP') or
                    starts-with($text, 'SUBCHAP') or
                    starts-with($text, 'SUBCHAPTER') or
                    starts-with($text, 'SUBCLAUSE') or
                    starts-with($text, 'SUBDIVISION') or
                    starts-with($text, 'SUBHEADING') or
                    starts-with($text, 'SUBLIST') or
                    starts-with($text, 'SUBPARA') or
                    starts-with($text, 'SUBPARAGRAPH') or
                    starts-with($text, 'SUBPART') or
                    starts-with($text, 'SUBRULE') or
                    starts-with($text, 'SUBSEC') or
                    starts-with($text, 'SUBSECTION') or
                    starts-with($text, 'SUBTITLE') or
                    starts-with($text, 'SUMMARY') or
                    starts-with($text, 'TABLE') or
                    starts-with($text, 'TC') or
                    starts-with($text, 'TH') or
                    starts-with($text, 'TITLE') or
                    starts-with($text, 'TOME') or
                    starts-with($text, 'TR') or
                    starts-with($text, 'TRANSITIONAL') or
                    starts-with($text, 'WRITTENSTATEMENTS')">
        <xsl:value-of select="'\'" />
      </xsl:if>
    </xsl:variable>

    <xsl:value-of select="concat($slash, $text)" />
  </xsl:template>

  <xsl:template name="escape-hyphens">
    <xsl:param name="text"/>

    <xsl:call-template name="string-replace-all">
      <xsl:with-param name="text"><xsl:value-of select="$text" /></xsl:with-param>
      <xsl:with-param name="value"><xsl:value-of select="'-'" /></xsl:with-param>
      <xsl:with-param name="replacement"><xsl:value-of select="'\-'" /></xsl:with-param>
    </xsl:call-template>
  </xsl:template>

  <xsl:template name="escape-slashes">
    <xsl:param name="text"/>

    <xsl:call-template name="string-replace-all">
      <xsl:with-param name="text"><xsl:value-of select="$text" /></xsl:with-param>
      <xsl:with-param name="value"><xsl:value-of select="'\'" /></xsl:with-param>
      <xsl:with-param name="replacement"><xsl:value-of select="'\\'" /></xsl:with-param>
    </xsl:call-template>
  </xsl:template>

  <!-- convert a string to uppercase -->
  <xsl:variable name="lowercase" select="'abcdefghijklmnopqrstuvwxyz'" />
  <xsl:variable name="uppercase" select="'ABCDEFGHIJKLMNOPQRSTUVWXYZ'" />
  <xsl:template name="uppercase">
    <xsl:param name="s"/>
    <xsl:value-of select="translate($s, $lowercase, $uppercase)" />
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
      <xsl:with-param name="str" select="$indentStr" />
      <xsl:with-param name="count" select="$level" />
    </xsl:call-template>
  </xsl:template>

  <!-- ...............................................................................
       Main structures
       ............................................................................... -->

  <!-- ignore these elements -->
  <xsl:template match="a:meta | a:judgment/a:header" />

  <!-- ...............................................................................
       Containers and hierarchical elements
       ............................................................................... -->

  <!-- content containers -->
  <xsl:template match="a:arguments | a:background | a:conclusions | a:decision | a:introduction | a:motivation
                       | a:preamble | a:preface | a:remedies">
    <xsl:param name="indent">0</xsl:param>

    <xsl:call-template name="indent">
      <xsl:with-param name="level" select="$indent" />
    </xsl:call-template>
    <xsl:call-template name="uppercase">
      <xsl:with-param name="s" select="local-name()"/>
    </xsl:call-template>
    <xsl:text>&#10;&#10;</xsl:text>

    <xsl:apply-templates>
      <xsl:with-param name="indent" select="$indent + 1" />
    </xsl:apply-templates>
  </xsl:template>

  <!-- hier content containers -->
  <xsl:template match="a:body | a:mainBody | a:judgmentBody | a:debateBody">
    <xsl:param name="indent">0</xsl:param>

    <!-- only add the BODY marker if a preface or preamble comes before the body -->
    <xsl:if test="preceding-sibling::a:preface or preceding-sibling::a:preamble">
      <xsl:call-template name="indent">
        <xsl:with-param name="level" select="$indent" />
      </xsl:call-template>
      <xsl:text>BODY</xsl:text>
      <xsl:text>&#10;&#10;</xsl:text>
    </xsl:if>

    <xsl:apply-templates>
      <xsl:with-param name="indent" select="$indent" />
    </xsl:apply-templates>
  </xsl:template>

  <!-- Hierarchical, speech-hierarchical and speech container elements. These all have num, heading and subheading
       and behave very similarly.
   -->
  <xsl:template match="a:alinea | a:article | a:book | a:chapter | a:clause | a:division | a:indent | a:level | a:list
                       | a:paragraph | a:part | a:point | a:proviso | a:rule | a:section | a:subchapter | a:subclause
                       | a:subdivision | a:sublist | a:subparagraph | a:subpart | a:subrule | a:subsection | a:subtitle
                       | a:title | a:tome | a:transitional | a:item
                       | a:address | a:adjournment | a:administrationOfOath | a:communication | a:debateSection
                       | a:declarationOfVote | a:ministerialStatements | a:nationalInterest | a:noticesOfMotion
                       | a:oralStatements | a:papers | a:personalStatements | a:petitions | a:pointOfOrder | a:prayers
                       | a:proceduralMotions | a:questions | a:resolutions | a:rollCall | a:writtenStatements
                       | a:answer | a:other | a:question | a:speech | a:speechGroup">
    <xsl:param name="indent">0</xsl:param>

    <xsl:call-template name="indent">
      <xsl:with-param name="level" select="$indent" />
    </xsl:call-template>

    <xsl:choose>
      <!-- shorter synonyms for some common elements -->
      <xsl:when test="self::a:article"><xsl:text>ART</xsl:text></xsl:when>
      <xsl:when test="self::a:chapter"><xsl:text>CHAP</xsl:text></xsl:when>
      <xsl:when test="self::a:paragraph"><xsl:text>PARA</xsl:text></xsl:when>
      <xsl:when test="self::a:section"><xsl:text>SEC</xsl:text></xsl:when>
      <xsl:when test="self::a:subchapter"><xsl:text>SUBCHAP</xsl:text></xsl:when>
      <xsl:when test="self::a:subparagraph"><xsl:text>SUBPARA</xsl:text></xsl:when>
      <xsl:when test="self::a:subsection"><xsl:text>SUBSEC</xsl:text></xsl:when>
      <xsl:otherwise>
        <xsl:call-template name="uppercase">
          <xsl:with-param name="s" select="local-name()"/>
        </xsl:call-template>
      </xsl:otherwise>
    </xsl:choose>

    <xsl:call-template name="block-attrs" />

    <xsl:if test="a:num">
      <xsl:text> </xsl:text>
      <xsl:call-template name="escape-hyphens">
        <xsl:with-param name="text">
          <xsl:call-template name="escape-slashes">
            <xsl:with-param name="text" select="a:num" />
          </xsl:call-template>
        </xsl:with-param>
      </xsl:call-template>
    </xsl:if>

    <xsl:if test="a:heading">
      <xsl:text> - </xsl:text>
      <xsl:apply-templates select="a:heading" />
    </xsl:if>
    <xsl:if test="a:subheading">
      <xsl:text>&#10;</xsl:text>
      <xsl:apply-templates select="a:subheading">
        <xsl:with-param name="indent" select="$indent + 1" />
      </xsl:apply-templates>
    </xsl:if>
    <xsl:if test="a:from">
      <xsl:text>&#10;</xsl:text>
      <xsl:apply-templates select="a:from">
        <xsl:with-param name="indent" select="$indent + 1" />
      </xsl:apply-templates>
    </xsl:if>
    <!-- ITEM is the exception, it doesn't get a blank line -->
    <xsl:text>&#10;</xsl:text>
    <xsl:if test="not(self::a:item)">
      <xsl:text>&#10;</xsl:text>
    </xsl:if>

    <xsl:apply-templates select="a:heading//a:authorialNote | a:subheading//a:authorialNote" mode="content">
      <xsl:with-param name="indent" select="$indent + 1" />
    </xsl:apply-templates>

    <xsl:apply-templates select="./*[not(self::a:num) and not(self::a:heading) and not(self::a:subheading) and not(self::a:from)]">
      <xsl:with-param name="indent" select="$indent + 1" />
    </xsl:apply-templates>
  </xsl:template>

  <!-- ...............................................................................
       Block elements
       ............................................................................... -->

  <!-- indented blocklists -->
  <xsl:template match="a:blockList">
    <xsl:param name="indent">0</xsl:param>

    <xsl:call-template name="indent">
      <xsl:with-param name="level" select="$indent" />
    </xsl:call-template>
    <xsl:text>ITEMS</xsl:text>
    <xsl:call-template name="block-attrs" />
    <xsl:text>&#10;</xsl:text>

    <xsl:apply-templates>
      <xsl:with-param name="indent" select="$indent + 1" />
    </xsl:apply-templates>
  </xsl:template>

  <xsl:template match="a:listIntroduction | a:listWrapUp">
    <xsl:param name="indent">0</xsl:param>

    <xsl:call-template name="indent">
      <xsl:with-param name="level" select="$indent" />
    </xsl:call-template>
    <xsl:apply-templates>
      <xsl:with-param name="indent" select="$indent" />
    </xsl:apply-templates>

    <xsl:text>&#10;&#10;</xsl:text>

    <xsl:apply-templates select=".//a:authorialNote" mode="content">
      <xsl:with-param name="indent" select="$indent" />
    </xsl:apply-templates>
  </xsl:template>

  <xsl:template match="a:ul">
    <xsl:param name="indent">0</xsl:param>

    <xsl:call-template name="indent">
      <xsl:with-param name="level" select="$indent" />
    </xsl:call-template>
    <xsl:text>BULLETS</xsl:text>
    <xsl:call-template name="block-attrs" />
    <xsl:text>&#10;</xsl:text>

    <xsl:apply-templates>
      <xsl:with-param name="indent" select="$indent + 1" />
    </xsl:apply-templates>

    <!-- the p tags inside the ul's li elements only get one newline, so add a bonus one to create an empty line -->
    <xsl:text>&#10;</xsl:text>
  </xsl:template>

  <xsl:template match="a:li">
    <xsl:param name="indent">0</xsl:param>

    <xsl:call-template name="indent">
      <xsl:with-param name="level" select="$indent" />
    </xsl:call-template>
    <xsl:text>* </xsl:text>

    <xsl:apply-templates>
      <xsl:with-param name="indent" select="$indent + 1" />
    </xsl:apply-templates>
  </xsl:template>

  <!-- block quotes as embeddedStructure -->
  <xsl:template match="a:embeddedStructure">
    <xsl:param name="indent">0</xsl:param>

    <xsl:call-template name="indent">
      <xsl:with-param name="level" select="$indent" />
    </xsl:call-template>
    <xsl:text>QUOTE</xsl:text>
    <xsl:call-template name="block-attrs" />
    <xsl:text>&#10;</xsl:text>
    <xsl:apply-templates>
      <xsl:with-param name="indent" select="$indent + 1" />
    </xsl:apply-templates>
  </xsl:template>

  <!-- authorial notes are made up of two parts:
       1. a reference, inline where the note appears (the default)
       2. the content, as a block element (mode=content)
  -->
  <xsl:template match="a:authorialNote">
    <xsl:text>{{FOOTNOTE </xsl:text>
    <xsl:value-of select="@marker"/>
    <xsl:text>}}</xsl:text>
  </xsl:template>

  <xsl:template match="a:authorialNote" mode="content">
    <xsl:param name="indent">0</xsl:param>

    <xsl:call-template name="indent">
      <xsl:with-param name="level" select="$indent" />
    </xsl:call-template>
    <xsl:text>FOOTNOTE </xsl:text>
    <xsl:value-of select="@marker"/>
    <xsl:text>&#10;</xsl:text>

    <xsl:apply-templates>
      <xsl:with-param name="indent" select="$indent + 1" />
    </xsl:apply-templates>
  </xsl:template>

  <!-- ...............................................................................
       Tables
       ............................................................................... -->
  <xsl:template match="a:table">
    <xsl:param name="indent">0</xsl:param>

    <xsl:call-template name="indent">
      <xsl:with-param name="level" select="$indent" />
    </xsl:call-template>
    <xsl:text>TABLE</xsl:text>
    <xsl:call-template name="block-attrs" />
    <xsl:text>&#10;</xsl:text>

    <xsl:apply-templates>
      <xsl:with-param name="indent" select="$indent + 1" />
    </xsl:apply-templates>
  </xsl:template>


  <xsl:template match="a:tr">
    <xsl:param name="indent">0</xsl:param>

    <xsl:call-template name="indent">
      <xsl:with-param name="level" select="$indent" />
    </xsl:call-template>
    <xsl:text>TR&#10;</xsl:text>

    <xsl:apply-templates>
      <xsl:with-param name="indent" select="$indent + 1" />
    </xsl:apply-templates>
  </xsl:template>


  <xsl:template match="a:th|a:td">
    <xsl:param name="indent">0</xsl:param>

    <xsl:call-template name="indent">
      <xsl:with-param name="level" select="$indent" />
    </xsl:call-template>

    <xsl:choose>
      <xsl:when test="local-name(.) = 'th'">
        <xsl:text>TH</xsl:text>
      </xsl:when>
      <xsl:when test="local-name(.) = 'td'">
        <xsl:text>TC</xsl:text>
      </xsl:when>
    </xsl:choose>

    <xsl:call-template name="block-attrs" />
    <xsl:text>&#10;</xsl:text>

    <xsl:apply-templates>
      <xsl:with-param name="indent" select="$indent + 1" />
    </xsl:apply-templates>
  </xsl:template>

  <!-- ...............................................................................
       Attribute lists at the start of marked blocks
       ............................................................................... -->

  <xsl:template name="block-attrs">
    <xsl:if test="@class">
      <xsl:text>.</xsl:text>
      <xsl:value-of select="translate(@class, ' ', '.')" />
    </xsl:if>

    <!-- ignore:
       - @eId
       - @class
       - @by
       - @name for elements that match the element name
       - @name for <inline name="em">
       -->
    <xsl:if test="@*[local-name() != 'eId' and local-name() != 'class' and local-name() != 'by'
                  and (local-name() != 'name' or . != local-name(parent::a:*))
                  and not(parent::a:inline and local-name() = 'name' and . = 'em')]">
      <xsl:text>{</xsl:text>
      <xsl:for-each select="@*[local-name() != 'eId' and local-name() != 'class' and local-name() != 'by'
                  and (local-name() != 'name' or . != local-name(parent::a:*))
                  and not(parent::a:inline and local-name() = 'name' and . = 'em')]">
        <xsl:apply-templates select="." mode="generic">
          <xsl:with-param name="index" select="position()"/>
        </xsl:apply-templates>
      </xsl:for-each>
      <xsl:text>}</xsl:text>
    </xsl:if>
  </xsl:template>

  <xsl:template match="@*" mode="generic">
    <xsl:param name="index">0</xsl:param>

    <xsl:if test="$index > 1">
      <xsl:text>|</xsl:text>
    </xsl:if>
    <xsl:value-of select="local-name(.)" />
    <xsl:text> </xsl:text>
    <xsl:value-of select="." />
  </xsl:template>

  <!-- ...............................................................................
       Attachments
       ............................................................................... -->

  <xsl:template match="a:attachment">
    <xsl:param name="indent">0</xsl:param>

    <xsl:call-template name="indent">
      <xsl:with-param name="level" select="$indent" />
    </xsl:call-template>
    <xsl:call-template name="uppercase">
      <xsl:with-param name="s" select="a:doc/@name" />
    </xsl:call-template>

    <xsl:if test="a:heading">
      <xsl:text> </xsl:text>
      <xsl:apply-templates select="a:heading" />
    </xsl:if>

    <xsl:if test="a:subheading">
      <xsl:text>&#10;</xsl:text>
      <xsl:apply-templates select="a:subheading">
        <xsl:with-param name="indent" select="$indent + 1" />
      </xsl:apply-templates>
    </xsl:if>

    <xsl:text>&#10;&#10;</xsl:text>

    <xsl:apply-templates select="a:heading//a:authorialNote | a:subheading//a:authorialNote" mode="content">
      <xsl:with-param name="indent" select="$indent + 1" />
    </xsl:apply-templates>

    <xsl:apply-templates select="a:doc">
      <xsl:with-param name="indent" select="$indent + 1" />
    </xsl:apply-templates>
  </xsl:template>

  <!-- ...............................................................................
       Content elements
       ............................................................................... -->

  <!-- p tags must end with a blank line -->
  <xsl:template match="a:p">
    <xsl:param name="indent">0</xsl:param>

    <!-- first p tag in li doesn't get indented -->
    <xsl:if test="not(parent::a:li and count(preceding-sibling::a:p) = 0)">
      <xsl:call-template name="indent">
        <xsl:with-param name="level" select="$indent" />
      </xsl:call-template>
    </xsl:if>

    <!-- include explicit P marker if the element has attributes other than eId -->
    <xsl:if test="@*[not(local-name() = 'eId')]">
      <xsl:text>P</xsl:text>
      <xsl:call-template name="block-attrs" />
      <xsl:text> </xsl:text>
    </xsl:if>

    <xsl:apply-templates>
      <xsl:with-param name="indent" select="$indent" />
    </xsl:apply-templates>

    <xsl:text>&#10;</xsl:text>
    <!-- p tags in lists only end with one newline -->
    <xsl:if test="not(parent::a:li)">
      <xsl:text>&#10;</xsl:text>
    </xsl:if>

    <!-- we only want authorialNotes that don't have an intermediate element between this p
     and the note. -->
    <xsl:variable name="cnt" select="count(ancestor-or-self::a:p)" />
    <xsl:apply-templates select=".//a:authorialNote[count(ancestor::a:p) = $cnt]" mode="content">
      <xsl:with-param name="indent" select="$indent" />
    </xsl:apply-templates>
  </xsl:template>

  <xsl:template match="a:subheading">
    <xsl:param name="indent">0</xsl:param>

    <xsl:call-template name="indent">
      <xsl:with-param name="level" select="$indent" />
    </xsl:call-template>
    <xsl:text>SUBHEADING </xsl:text>
    <xsl:apply-templates>
      <xsl:with-param name="indent" select="$indent" />
    </xsl:apply-templates>
  </xsl:template>

  <xsl:template match="a:crossHeading">
    <xsl:param name="indent">0</xsl:param>

    <xsl:call-template name="indent">
      <xsl:with-param name="level" select="$indent" />
    </xsl:call-template>
    <xsl:text>CROSSHEADING </xsl:text>
    <xsl:apply-templates>
      <xsl:with-param name="indent" select="$indent" />
    </xsl:apply-templates>
    <xsl:text>&#10;&#10;</xsl:text>

    <xsl:apply-templates select=".//a:authorialNote" mode="content">
      <xsl:with-param name="indent" select="$indent" />
    </xsl:apply-templates>
  </xsl:template>

  <xsl:template match="a:from">
    <xsl:param name="indent">0</xsl:param>

    <xsl:call-template name="indent">
      <xsl:with-param name="level" select="$indent" />
    </xsl:call-template>
    <xsl:text>FROM </xsl:text>
    <xsl:apply-templates>
      <xsl:with-param name="indent" select="$indent" />
    </xsl:apply-templates>
  </xsl:template>

  <xsl:template match="a:scene | a:narrative | a:summary">
    <xsl:param name="indent">0</xsl:param>

    <xsl:call-template name="indent">
      <xsl:with-param name="level" select="$indent" />
    </xsl:call-template>
    <xsl:call-template name="uppercase">
      <xsl:with-param name="s" select="local-name()"/>
    </xsl:call-template>
    <xsl:call-template name="block-attrs" />
    <xsl:text> </xsl:text>
    <xsl:apply-templates>
      <xsl:with-param name="indent" select="$indent" />
    </xsl:apply-templates>
    <xsl:text>&#10;&#10;</xsl:text>

    <xsl:apply-templates select=".//a:authorialNote" mode="content">
      <xsl:with-param name="indent" select="$indent" />
    </xsl:apply-templates>
  </xsl:template>

  <!-- TODO: this is actually a block element, not a container -->
  <xsl:template match="a:longTitle">
    <xsl:param name="indent">0</xsl:param>

    <xsl:call-template name="indent">
      <xsl:with-param name="level" select="$indent" />
    </xsl:call-template>
    <xsl:text>LONGTITLE </xsl:text>
    <xsl:apply-templates/>
    <xsl:text>&#10;&#10;</xsl:text>
  </xsl:template>

  <!-- ...............................................................................
       Inline and marker elements
       ............................................................................... -->

  <xsl:template match="a:remark">
    <xsl:param name="indent">0</xsl:param>

    <xsl:text>{{*</xsl:text>
    <xsl:apply-templates>
      <xsl:with-param name="indent" select="$indent" />
    </xsl:apply-templates>
    <xsl:text>}}</xsl:text>
  </xsl:template>

  <xsl:template match="a:remark/a:br">
    <xsl:param name="indent">0</xsl:param>
    <xsl:text>&#10;</xsl:text>
    <xsl:call-template name="indent">
      <xsl:with-param name="level" select="$indent" />
    </xsl:call-template>
  </xsl:template>

  <!-- left trim the first text node just after a br in a remark to prevent interfering with indents -->
  <xsl:template match="a:remark/text()[preceding-sibling::a:*[1][self::a:br]]">
    <xsl:call-template name="escape-inlines">
      <xsl:with-param name="text">
        <xsl:call-template name="string-ltrim">
          <xsl:with-param name="text" select="." />
        </xsl:call-template>
      </xsl:with-param>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="a:ref">
    <xsl:param name="indent">0</xsl:param>

    <xsl:text>{{&gt;</xsl:text>
    <xsl:call-template name="string-replace-all">
      <xsl:with-param name="text" select="@href"></xsl:with-param>
      <xsl:with-param name="value" select="' '"></xsl:with-param>
      <xsl:with-param name="replacement" select="'%20'"></xsl:with-param>
    </xsl:call-template>
    <xsl:text> </xsl:text>
    <xsl:apply-templates>
      <xsl:with-param name="indent" select="$indent" />
    </xsl:apply-templates>
    <xsl:text>}}</xsl:text>
  </xsl:template>

  <xsl:template match="a:img">
    <xsl:text>{{IMG </xsl:text>
    <xsl:call-template name="string-replace-all">
      <xsl:with-param name="text" select="@src"></xsl:with-param>
      <xsl:with-param name="value" select="' '"></xsl:with-param>
      <xsl:with-param name="replacement" select="'%20'"></xsl:with-param>
    </xsl:call-template>
    <xsl:if test="@alt">
      <xsl:text> </xsl:text>
      <xsl:value-of select="@alt" />
    </xsl:if>
    <xsl:text>}}</xsl:text>
  </xsl:template>

  <xsl:template match="a:i">
    <xsl:param name="indent">0</xsl:param>

    <xsl:text>//</xsl:text>
    <xsl:apply-templates>
      <xsl:with-param name="indent" select="$indent" />
    </xsl:apply-templates>
    <xsl:text>//</xsl:text>
  </xsl:template>

  <xsl:template match="a:b">
    <xsl:param name="indent">0</xsl:param>

    <xsl:text>**</xsl:text>
    <xsl:apply-templates>
      <xsl:with-param name="indent" select="$indent" />
    </xsl:apply-templates>
    <xsl:text>**</xsl:text>
  </xsl:template>

  <xsl:template match="a:u">
    <xsl:param name="indent">0</xsl:param>

    <xsl:text>__</xsl:text>
    <xsl:apply-templates>
      <xsl:with-param name="indent" select="$indent" />
    </xsl:apply-templates>
    <xsl:text>__</xsl:text>
  </xsl:template>

  <xsl:template match="a:sup">
    <xsl:param name="indent">0</xsl:param>

    <xsl:text>{{^</xsl:text>
    <xsl:apply-templates>
      <xsl:with-param name="indent" select="$indent" />
    </xsl:apply-templates>
    <xsl:text>}}</xsl:text>
  </xsl:template>

  <xsl:template match="a:sub">
    <xsl:param name="indent">0</xsl:param>

    <xsl:text>{{_</xsl:text>
    <xsl:apply-templates>
      <xsl:with-param name="indent" select="$indent" />
    </xsl:apply-templates>
    <xsl:text>}}</xsl:text>
  </xsl:template>

  <!-- general inlines that follow a common pattern -->
  <xsl:template match="a:abbr | a:def | a:term | a:inline | a:ins | a:del">
    <xsl:param name="indent">0</xsl:param>

    <xsl:text>{{</xsl:text>
    <xsl:choose>
      <xsl:when test="self::a:inline and @name='em'">
        <xsl:text>em</xsl:text>
      </xsl:when>
      <xsl:when test="self::a:ins">
        <xsl:text>+</xsl:text>
      </xsl:when>
      <xsl:when test="self::a:del">
        <xsl:text>-</xsl:text>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="local-name(.)" />
      </xsl:otherwise>
    </xsl:choose>
    <xsl:call-template name="block-attrs" />
    <xsl:text> </xsl:text>
    <xsl:apply-templates>
      <xsl:with-param name="indent" select="$indent" />
    </xsl:apply-templates>
    <xsl:text>}}</xsl:text>
  </xsl:template>

  <xsl:template match="a:eol">
    <xsl:param name="indent">0</xsl:param>

    <xsl:text>&#10;</xsl:text>

    <xsl:call-template name="indent">
      <xsl:with-param name="level" select="$indent" />
    </xsl:call-template>
  </xsl:template>

  <!-- ...............................................................................
       Text
       ............................................................................... -->

  <!-- first text nodes of these elems must be left-trimmed and escaped if they have special chars -->
  <xsl:template match="a:*[self::a:p or self::a:listIntroduction or self::a:listWrapUp]
                       /text()[not(preceding-sibling::*)]">
    <xsl:call-template name="escape-prefixes">
      <xsl:with-param name="text">
        <xsl:call-template name="escape-inlines-start-end">
          <xsl:with-param name="text">
            <xsl:call-template name="string-ltrim">
              <xsl:with-param name="text" select="." />
            </xsl:call-template>
          </xsl:with-param>
        </xsl:call-template>
      </xsl:with-param>
    </xsl:call-template>
  </xsl:template>

  <!-- escape inlines in text nodes -->
  <xsl:template match="text()">
    <xsl:call-template name="escape-inlines-start-end">
      <xsl:with-param name="text" select="." />
    </xsl:call-template>
  </xsl:template>

  <!-- ...............................................................................
       Catch-all
       ............................................................................... -->

  <!-- for most nodes, just dump their text content and pass through the indentation level
       to children -->
  <xsl:template match="*">
    <xsl:param name="indent">0</xsl:param>

    <xsl:apply-templates>
      <xsl:with-param name="indent" select="$indent"/>
    </xsl:apply-templates>
  </xsl:template>

</xsl:stylesheet>
