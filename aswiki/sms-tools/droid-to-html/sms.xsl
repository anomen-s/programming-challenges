<?xml version="1.0" encoding="ISO-8859-1"?>
<!--
  ~ Copyright (c) 2010 - 2016 Carbonite. All Rights Reserved.
  -->

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:msxsl="urn:schemas-microsoft-com:xslt"
                xmlns:user="http://android.riteshsahu.com">
<xsl:template match="/">

  <xsl:text disable-output-escaping='yes'>&lt;!DOCTYPE html></xsl:text>
  <html>
	  <head>
		  <style type="text/css">
		  body 
		  {
			font-family:arial,sans-serif;
			color:#000;
			font-size:13px;
			color:#333;
		  }
		  table 
		  {
			font-size:1em;
			margin:0 0 1em;
			border-collapse:collapse;
			border-width:0;
			empty-cells:show;
		  }
		  td,th 
		  {
			border:1px solid #ccc;
			padding:6px 12px;
			text-align:left;
			vertical-align:top;
			background-color:inherit;
		  }
		  th 
		  {
			background-color:#dee8f1;
		  }
		  </style>
	  </head>
	  <body>
	  <h2>Messages</h2>
	  <table>
	   <colgroup>
            <col style="width:80px"/>
            <col style="width:120px"/>
            <col style="width:120px"/>
            <col style="width:160px"/>
        </colgroup>
		<tr>
		  <th>Type</th>
		  <th>Number</th>
		  <th>Contact</th>
		  <th>Date</th>
		  <th>Message</th>
		</tr>
		<xsl:for-each select="smses/*">
		<tr>
			<xsl:choose>
			<xsl:when test="name() = 'sms'">
				<td>
					<xsl:if test="@type = 1">
					Received
					</xsl:if>
					<xsl:if test="@type = 2">
					Sent
					</xsl:if>
					<xsl:if test="@type = 3">
					Draft
					</xsl:if>
			  </td>
			</xsl:when>
			<xsl:otherwise>
				<td>
					<xsl:if test="@msg_box = 1">
					Received
					</xsl:if>
					<xsl:if test="@msg_box = 2">
					Sent
					</xsl:if>
					<xsl:if test="@msg_box = 3">
					Draft
					</xsl:if>
			  </td>
			</xsl:otherwise>
		  </xsl:choose>
		  <td><xsl:value-of select="@address"/></td>
		  <td><xsl:value-of select="@contact_name"/></td>
		  <td><xsl:value-of select="@readable_date"/></td>
		  <td>
			<xsl:choose>
			<xsl:when test="name() = 'sms'">
				<xsl:value-of select="@body"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:for-each select="parts/part">
					<xsl:choose>
					<xsl:when test="@ct = 'application/smil'">
					</xsl:when>
					<xsl:when test="@ct = 'text/plain'">
						<xsl:value-of select="@text"/><br/>
					</xsl:when>
					<xsl:when test="starts-with(@ct,'image/')" >
						<img height="300">
						  <xsl:attribute name="src">
							<xsl:value-of select="concat(concat('data:',@ct), concat(';base64,',@data))"/>
						  </xsl:attribute>
						</img><br/>
					</xsl:when>
					<xsl:otherwise>
						<i>Preview of <xsl:value-of select="@ct"/> not supported.</i><br/>
					</xsl:otherwise>
				  </xsl:choose>
				</xsl:for-each>
			</xsl:otherwise>
		  </xsl:choose>

		  </td>
		</tr>
		</xsl:for-each>
	  </table>
	  </body>
  </html>
</xsl:template>
</xsl:stylesheet>