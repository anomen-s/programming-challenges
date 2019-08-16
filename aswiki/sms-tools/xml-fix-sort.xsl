<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<!--
		xsl for sorting messages by date
	-->
	<xsl:output method="xml" indent="yes" encoding="utf-8"/>

	<xsl:variable name="nl" select="'&#10;&#09;    '"/>

	<xsl:template match="/messages">
		<messages>
			<xsl:for-each select="message">
				<xsl:sort select="dateenc"/>

				<xsl:copy>
					<xsl:if test="string-length(dateenc) != 14 or (string-length(translate(dateenc, '0123456789', '')) != 0)">
					     <xsl:comment> 
					        <xsl:value-of select="$nl"/>
					        <xsl:text>INVALID date: "</xsl:text>
					        <xsl:value-of select="dateenc"/>
					        <xsl:text>"</xsl:text>
					        <xsl:value-of select="$nl"/>
					     </xsl:comment>
					</xsl:if>
					<xsl:apply-templates select="node()|@*"/>
				</xsl:copy>
			</xsl:for-each>
		</messages>
	</xsl:template>
	<xsl:template match="node()|@*">
		<xsl:copy>
			<xsl:apply-templates select="node()|@*"/>
		</xsl:copy>
	</xsl:template>
</xsl:stylesheet>
