<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:fn="http://www.w3.org/2005/xpath-functions"
 xmlns:user="http://android.riteshsahu.com">

  <xsl:variable name="stats"><!--Read Received -->Sent</xsl:variable>
  <xsl:variable name="year">2013</xsl:variable>


  <xsl:output omit-xml-declaration="yes" indent="yes"/>

  <xsl:template match="message">
	<xsl:if test="contains($stats, stat) and substring(dateenc,1,4) = $year">
          <xsl:copy>
             <xsl:apply-templates select="node()|@*"/>
          </xsl:copy>
        </xsl:if>
  </xsl:template>

    <xsl:template match="node()|@*">
         <xsl:copy>
             <xsl:apply-templates select="node()|@*"/>
          </xsl:copy>
     </xsl:template>

</xsl:stylesheet>
