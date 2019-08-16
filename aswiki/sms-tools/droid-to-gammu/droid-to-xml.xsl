<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:date="http://exslt.org/dates-and-times" xmlns:xs="http://www.w3.org/2001/XMLSchema" version="1.0">
	<!--
		xsl for converting SMS export from Android app "SMS Backup & Restore" to format used by GAMMU.
		
		Input might have ns "http://android.riteshsahu.com".
	-->
	<xsl:output method="xml" indent="yes" encoding="utf-8"/>
	<xsl:param name="TYPE"/>
	<xsl:param name="YEAR"/>
	<xsl:param name="MONTH"/>
	<xsl:template name="break">
		<xsl:param name="text" select="string(.)"/>
		<xsl:choose>
			<xsl:when test="contains($text, '&#10;')">
				<xsl:value-of select="substring-before($text, '&#10;')"/>
				<br/>
				<xsl:call-template name="break">
					<xsl:with-param name="text" select="substring-after($text, '&#10;')"/>
				</xsl:call-template>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="$text"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template match="/">
		<messages>
			<xsl:for-each select="smses/sms">
				<xsl:sort select="@date"/>
				<xsl:if test="@type = $TYPE">
					<xsl:variable name="d" select="date:add('1970-01-01T01:00:00Z', date:duration(@date div 1000))"/>
					<xsl:if test="starts-with(concat(substring($d,1,4),substring($d,6,2)), concat($YEAR,$MONTH))">
						<message>
							<date>
								<xsl:value-of select="@readable_date"/>
							</date>
							<dateenc>
								<xsl:value-of select="substring($d,1,4)"/>
								<xsl:value-of select="substring($d,6,2)"/>
								<xsl:value-of select="substring($d,9,2)"/>
								<xsl:value-of select="substring($d,12,2)"/>
								<xsl:value-of select="substring($d,15,2)"/>
								<xsl:value-of select="substring($d,18,2)"/>
							</dateenc>
							<text>
								<xsl:call-template name="break">
									<xsl:with-param name="text" select="@body"/>
								</xsl:call-template>
							</text>
							<telephone>
								<xsl:value-of select="@address"/>
							</telephone>
							<contact>
								<xsl:if test="@contact_name != '(Unknown)'">
									<xsl:value-of select="@contact_name"/>
								</xsl:if>
								<xsl:if test="@contact_name = '(Unknown)'">
									<xsl:value-of select="@address"/>
								</xsl:if>
							</contact>
							<stat>
								<xsl:if test="@type = 1">Received</xsl:if>
								<xsl:if test="@type = 2">Sent</xsl:if>
							</stat>
						</message>
					</xsl:if>
				</xsl:if>
			</xsl:for-each>
		</messages>
	</xsl:template>
</xsl:stylesheet>
