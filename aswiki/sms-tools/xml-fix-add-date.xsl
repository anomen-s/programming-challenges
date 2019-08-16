<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<!--
		xsl for adding dateenc to messages
	-->
	<xsl:output method="xml" indent="yes" encoding="utf-8"/>
	<xsl:template match="node()">
		<xsl:copy>
			<xsl:apply-templates select="node()"/>
		</xsl:copy>
	</xsl:template>

	<xsl:template name="remove-spaces">
		<xsl:param name="text"/>
		<xsl:choose>
			<xsl:when test="contains($text, '. ')">
				<xsl:value-of select="substring-before($text, '. ')"/>
				<xsl:text>.</xsl:text>
				<xsl:call-template name="remove-spaces">
					<xsl:with-param name="text" select="substring-after($text, '. ')"/>
				</xsl:call-template>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="$text"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>

	<xsl:template name="lpad">
		<xsl:param name="text" />
		<xsl:param name="length" />
		<xsl:variable name="padded" select="concat('000000', translate(string($text), ' ', ''))"/>
		<xsl:variable name="final" select="substring($padded, string-length($padded) - $length + 1, $length)"/>
		<xsl:value-of select="$final"/>
	</xsl:template>

	<xsl:template match="message">
		<xsl:variable name="dateenc" select="dateenc"/>
		<xsl:variable name="datetrim">
			<xsl:call-template name="remove-spaces">
			    <xsl:with-param name="text" select="date"/>
			</xsl:call-template>
		</xsl:variable>
		<xsl:variable name="date_d" select="substring-before($datetrim,'.')"/>
		<xsl:variable name="date_dr" select="substring-after($datetrim,'.')"/>
		<xsl:variable name="date_m" select="substring-before($date_dr,'.')"/>
		<xsl:variable name="date_mr" select="substring-after($date_dr,'.')"/>
		<xsl:variable name="date_y" select="substring-before($date_mr,' ')"/>
		<xsl:variable name="date_yr" select="substring-after($date_mr,' ')"/>
		<xsl:variable name="date_hrs" select="substring-before($date_yr,':')"/>
		<xsl:variable name="date_hrsr" select="substring-after($date_yr,':')"/>
		<xsl:variable name="date_min" select="substring-before(concat($date_hrsr, ':'),':')"/>
		<xsl:variable name="date_minr" select="substring-after(concat($date_hrsr, ':00'),':')"/>
		<xsl:variable name="date_sec" select="substring-before(concat($date_minr, ':00'), ':')"/>

		<xsl:if test="string-length($dateenc) &lt;= 10">
			<message>
				<dateenc>
					<xsl:call-template name="lpad">
					    <xsl:with-param name="text" select="$date_y"/>
					    <xsl:with-param name="length" select="4"/>
					</xsl:call-template>
					<xsl:call-template name="lpad">
					    <xsl:with-param name="text" select="$date_m"/>
					    <xsl:with-param name="length" select="2"/>
					</xsl:call-template>
					<xsl:call-template name="lpad">
					    <xsl:with-param name="text" select="$date_d"/>
					    <xsl:with-param name="length" select="2"/>
					</xsl:call-template>
					<xsl:call-template name="lpad">
					    <xsl:with-param name="text" select="$date_hrs"/>
					    <xsl:with-param name="length" select="2"/>
					</xsl:call-template>
					<xsl:call-template name="lpad">
					    <xsl:with-param name="text" select="$date_min"/>
					    <xsl:with-param name="length" select="2"/>
					</xsl:call-template>
					<xsl:call-template name="lpad">
					    <xsl:with-param name="text" select="$date_sec"/>
					    <xsl:with-param name="length" select="2"/>
					</xsl:call-template>
				</dateenc>
				<xsl:apply-templates select="*[local-name() != 'dateenc']|text()|@*"/>
			</message>
		</xsl:if>
		<xsl:if test="string-length($dateenc) &gt; 10">
			<xsl:copy-of select="."/>
		</xsl:if>
	</xsl:template>
</xsl:stylesheet>
